#!/usr/bin/env python3
"""Validate the portable Pattern Review schema version 2 contract.

This script uses only the Python standard library. It can validate the public
template surfaces or the concrete records in a generated vault.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


MODULE_DIR = Path(__file__).resolve().parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

from pattern_review_core import (  # noqa: E402
    ContractError,
    DECISION_ID_RE,
    DIGEST_RE,
    EXECUTION_ID_RE,
    PROPOSAL_ID_RE,
    VALIDATION_ID_RE,
    authorization_digest,
    canonical_json_bytes,
    digest_hex,
    digest_payload,
    digest_text,
    parse_json_payload,
)


CANDIDATE_ID_RE = re.compile(r"^PR-\d{4}-\d{2}-\d{2}-\d{2,}$")
VALIDATOR_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._:-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ALLOWED_DISPOSITIONS = {
    "hold",
    "reject",
    "narrow",
    "request-details",
    "approve-exact",
    "revoke",
}
ALLOWED_EXECUTION_RESULTS = {"blocked", "executed", "partial", "rolled-back"}
ROOT_DISPOSITIONS = {
    "hold",
    "reject",
    "narrow",
    "request-details",
    "approve-exact",
}
ALLOWED_TRANSITIONS = {
    "hold": ROOT_DISPOSITIONS,
    "approve-exact": {"revoke"},
    "revoke": set(),
    "reject": set(),
    "narrow": set(),
    "request-details": set(),
}
RECORD_DIRS = {
    "proposal": "proposals",
    "decision": "decisions",
    "execution": "executions",
    "validation": "validations",
}


@dataclass
class Record:
    kind: str
    path: Path
    frontmatter: dict[str, str]
    payload: dict[str, Any]

    @property
    def record_id(self) -> str:
        field = {
            "proposal": "proposal-id",
            "decision": "decision-id",
            "execution": "execution-id",
            "validation": "validation-id",
        }[self.kind]
        return self.frontmatter.get(field, "")


@dataclass(frozen=True)
class CandidateRecord:
    candidate_id: str
    report_path: Path
    fingerprint: str


@dataclass(frozen=True)
class ValidatedPathState:
    path: str
    before_sha256: str
    after_sha256: str
    completed_at: datetime
    execution: Record
    validation: Record


@dataclass
class ValidationReport:
    errors: list[str]
    warnings: list[str]
    record_count: int = 0

    def error(self, path: Path | str, message: str) -> None:
        self.errors.append(f"{path}: {message}")

    def warn(self, path: Path | str, message: str) -> None:
        self.warnings.append(f"{path}: {message}")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ContractError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ContractError("unterminated YAML frontmatter")
    block = text[4:end]
    body = text[end + 5 :]
    values: dict[str, str] = {}
    for line_number, line in enumerate(block.splitlines(), start=2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            raise ContractError(
                f"frontmatter line {line_number} must be a flat key and scalar value"
            )
        key, raw_value = line.split(":", 1)
        key = key.strip()
        value = raw_value.strip()
        if not key or key in values:
            raise ContractError(f"invalid or duplicate frontmatter key on line {line_number}")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        values[key] = value
    return values, body


def extract_json_block(body: str) -> str:
    match = re.search(r"```json\s*\n(.*?)\n```", body, flags=re.DOTALL)
    if not match:
        raise ContractError("missing canonical JSON code block")
    return match.group(1)


def load_record(kind: str, path: Path) -> Record:
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        raise ContractError("record is not valid UTF 8") from exc
    frontmatter, body = parse_frontmatter(text)
    payload = parse_json_payload(extract_json_block(body))
    return Record(kind=kind, path=path, frontmatter=frontmatter, payload=payload)


def parse_iso_date(value: str, field: str) -> date:
    if not isinstance(value, str) or DATE_RE.fullmatch(value) is None:
        raise ContractError(f"{field} must be YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ContractError(f"{field} must be YYYY-MM-DD") from exc


def parse_utc(value: str, field: str) -> datetime:
    if not isinstance(value, str) or UTC_RE.fullmatch(value) is None:
        raise ContractError(f"{field} must be UTC YYYY-MM-DDTHH:MM:SSZ")
    try:
        parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ContractError(f"{field} must be UTC YYYY-MM-DDTHH:MM:SSZ") from exc
    return parsed.replace(tzinfo=timezone.utc)


def payload_string(payload: dict[str, Any], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ContractError(f"payload field {key} must be a nonempty string")
    return value


def payload_list(payload: dict[str, Any], key: str) -> list[Any]:
    value = payload.get(key)
    if not isinstance(value, list):
        raise ContractError(f"payload field {key} must be an array")
    return value


def require_frontmatter(record: Record, expected: dict[str, str]) -> None:
    for key, value in expected.items():
        actual = record.frontmatter.get(key)
        if actual != value:
            raise ContractError(f"frontmatter {key} must be {value!r}, found {actual!r}")


def require_parent_month(record: Record, compact_date: str) -> None:
    expected = f"{compact_date[:4]}-{compact_date[4:6]}"
    expected_kind = RECORD_DIRS[record.kind]
    if (
        record.path.parent.name != expected
        or record.path.parent.parent.name != expected_kind
    ):
        raise ContractError(
            f"record path must be {expected_kind}/{expected}/<record ID>.md"
        )


def is_safe_relative_path(value: str) -> bool:
    if not value or "\\" in value or value.startswith(("/", "~")):
        return False
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and "." != value


def is_contained_by_root(root: Path, value: str) -> bool:
    """Resolve existing symlinks and require the target to remain under root."""
    if not is_safe_relative_path(value):
        return False
    try:
        resolved_root = root.resolve(strict=True)
        target = (root / Path(*PurePosixPath(value).parts)).resolve(strict=False)
        target.relative_to(resolved_root)
    except (OSError, RuntimeError, ValueError):
        return False
    return True


def infer_vault_root(path: Path) -> Path | None:
    absolute = path.absolute()
    for ancestor in absolute.parents:
        if ancestor.name == "learning-library" and ancestor.parent.name == "resources":
            return ancestor.parent.parent
    return None


def first_symlink_component(path: Path, vault_root: Path) -> Path | None:
    absolute = path.absolute()
    absolute_root = vault_root.absolute()
    try:
        relative = absolute.relative_to(absolute_root)
    except ValueError:
        return absolute
    current = absolute_root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            return current
    return None


def require_record_storage_path(path: Path, vault_root: Path | None = None) -> None:
    effective_root = vault_root or infer_vault_root(path)
    if effective_root is None:
        raise ContractError("record path is not under resources/learning-library")
    symlink = first_symlink_component(path, effective_root)
    if symlink is not None:
        raise ContractError(f"record path contains a symlink component: {symlink}")
    try:
        absolute_root = effective_root.absolute()
        absolute_path = path.absolute()
        absolute_path.relative_to(absolute_root)
        resolved_root = effective_root.resolve(strict=True)
        resolved_path = path.resolve(strict=True)
        resolved_path.relative_to(resolved_root)
    except (OSError, RuntimeError, ValueError) as exc:
        raise ContractError("record path escapes the vault root") from exc


def digest_live_target(root: Path, value: str) -> str:
    if not is_contained_by_root(root, value):
        raise ContractError(f"live target escapes vault through a symlink: {value}")
    target = (root / Path(*PurePosixPath(value).parts)).resolve(strict=False)
    if not target.is_file():
        raise ContractError(f"live target is not a readable file: {value}")
    digest = hashlib.sha256()
    try:
        with target.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as exc:
        raise ContractError(f"cannot hash live target {value}: {exc}") from exc
    return "sha256:" + digest.hexdigest()


def validate_hash(value: Any, *, allow_absent: bool = False) -> bool:
    return isinstance(value, str) and (
        (allow_absent and value == "absent") or DIGEST_RE.fullmatch(value) is not None
    )


def validate_proposal(record: Record) -> None:
    require_record_storage_path(record.path)
    require_frontmatter(
        record,
        {
            "type": "learning-proposal",
            "schema-version": "2",
            "status": "proposed",
            "authority": "none",
        },
    )
    proposal_id = record.frontmatter.get("proposal-id", "")
    match = PROPOSAL_ID_RE.fullmatch(proposal_id)
    if not match:
        raise ContractError("proposal-id must match FPRP-YYYYMMDD-<12 lowercase hex>")
    require_parent_month(record, match.group(1))
    created_date = parse_iso_date(record.frontmatter.get("created-date", ""), "created-date")
    if match.group(1) != created_date.strftime("%Y%m%d"):
        raise ContractError("proposal ID date must match created-date")
    stored_digest = record.frontmatter.get("proposal-digest", "")
    full_hex = digest_hex(stored_digest)
    if full_hex is None:
        raise ContractError("proposal-digest must contain a full SHA 256 digest")
    computed = digest_payload(record.payload)
    if stored_digest != computed:
        raise ContractError("proposal-digest does not match canonical JSON payload")
    if match.group(2) != full_hex[:12]:
        raise ContractError("proposal ID suffix does not match proposal digest prefix")
    if record.path.stem != proposal_id:
        raise ContractError("proposal filename must equal proposal-id")
    if record.payload.get("schema_version") != 2:
        raise ContractError("proposal payload schema_version must be 2")

    revision = payload_string(record.payload, "revision_of")
    if revision != "none" and not PROPOSAL_ID_RE.fullmatch(revision):
        raise ContractError("revision_of must be none or an FPRP ID")

    candidates = payload_list(record.payload, "source_candidates")
    if not candidates:
        raise ContractError("source_candidates must not be empty")
    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            raise ContractError(f"source_candidates[{index}] must be an object")
        candidate_id = candidate.get("id")
        if not isinstance(candidate_id, str) or not CANDIDATE_ID_RE.fullmatch(candidate_id):
            raise ContractError(f"source_candidates[{index}].id is not a candidate ID")
        for key in ("path", "fingerprint"):
            if not isinstance(candidate.get(key), str) or not candidate[key]:
                raise ContractError(f"source_candidates[{index}].{key} is required")

    payload_string(record.payload, "scope")
    operations = payload_list(record.payload, "operations")
    if not operations:
        raise ContractError("operations must not be empty")
    seen_paths: set[str] = set()
    for index, operation in enumerate(operations):
        if not isinstance(operation, dict):
            raise ContractError(f"operations[{index}] must be an object")
        for key in ("action", "path", "change_format", "exact_change"):
            if not isinstance(operation.get(key), str) or not operation[key]:
                raise ContractError(f"operations[{index}].{key} is required")
        path = operation["path"]
        if not is_safe_relative_path(path):
            raise ContractError(f"operations[{index}].path must be vault relative")
        if path in seen_paths:
            raise ContractError(f"duplicate operation path: {path}")
        seen_paths.add(path)
        action = operation["action"]
        before = operation.get("before_sha256")
        if action not in {"create", "replace"}:
            raise ContractError(f"operations[{index}].action must be create or replace")
        if action == "create" and before != "absent":
            raise ContractError(
                f"operations[{index}] create requires before_sha256 absent"
            )
        if action == "replace" and not validate_hash(before):
            raise ContractError(
                f"operations[{index}] replace requires a full before_sha256 digest"
            )
        if not validate_hash(operation.get("after_sha256")):
            raise ContractError(f"operations[{index}].after_sha256 is invalid")
        if operation["change_format"] != "full-content":
            raise ContractError("schema version 2 permits full-content changes only")
        if operation["after_sha256"] != digest_text(operation["exact_change"]):
            raise ContractError(
                f"operations[{index}].after_sha256 does not hash exact_change"
            )

    prohibited = payload_list(record.payload, "prohibited_expansion")
    if not prohibited or not all(isinstance(item, str) and item for item in prohibited):
        raise ContractError("prohibited_expansion must contain at least one statement")
    validators = payload_list(record.payload, "validation")
    if not validators or len(set(validators)) != len(validators):
        raise ContractError("validation must contain unique trusted validator IDs")
    for validator in validators:
        if not isinstance(validator, str) or not VALIDATOR_ID_RE.fullmatch(validator):
            raise ContractError(f"unsafe trusted validator ID: {validator!r}")
    payload_string(record.payload, "failure_behavior")


def validate_decision_shape(record: Record) -> None:
    require_record_storage_path(record.path)
    require_frontmatter(
        record,
        {
            "type": "learning-decision",
            "schema-version": "2",
            "status": "recorded",
            "authority": "human-decision",
        },
    )
    decision_id = record.frontmatter.get("decision-id", "")
    match = DECISION_ID_RE.fullmatch(decision_id)
    if not match:
        raise ContractError("decision-id must match FPRD-YYYYMMDDTHHMMSSZ-<8 nonce hex>")
    require_parent_month(record, match.group(1)[:8])
    if record.path.stem != decision_id:
        raise ContractError("decision filename must equal decision-id")
    if record.payload.get("schema_version") != 2:
        raise ContractError("decision payload schema_version must be 2")
    if payload_string(record.payload, "decision_id") != decision_id:
        raise ContractError("decision payload ID does not match frontmatter")
    decided_at = parse_utc(payload_string(record.payload, "decided_at"), "decided_at")
    if match.group(1) != decided_at.strftime("%Y%m%dT%H%M%SZ"):
        raise ContractError("decision ID timestamp must match decided_at")
    decided_date = parse_iso_date(record.frontmatter.get("decided-date", ""), "decided-date")
    if decided_date != decided_at.date():
        raise ContractError("decided-date must match decided_at")
    stored_digest = record.frontmatter.get("decision-digest", "")
    if digest_hex(stored_digest) is None or stored_digest != digest_payload(record.payload):
        raise ContractError("decision-digest does not match canonical JSON payload")

    proposal_id = payload_string(record.payload, "proposal_id")
    proposal_digest = payload_string(record.payload, "proposal_digest")
    if not PROPOSAL_ID_RE.fullmatch(proposal_id):
        raise ContractError("decision proposal_id must be an FPRP ID, not a candidate ID")
    if digest_hex(proposal_digest) is None:
        raise ContractError("decision proposal_digest must be a full SHA 256 digest")
    proposal_match = PROPOSAL_ID_RE.fullmatch(proposal_id)
    if proposal_match is not None and proposal_match.group(2) != proposal_digest[7:19]:
        raise ContractError("decision proposal ID suffix does not match proposal digest")
    if record.frontmatter.get("proposal-id") != proposal_id:
        raise ContractError("decision proposal ID does not match frontmatter")
    if record.frontmatter.get("proposal-digest") != proposal_digest:
        raise ContractError("decision proposal digest does not match frontmatter")

    previous = payload_string(record.payload, "previous_event_id")
    if previous != "none" and not DECISION_ID_RE.fullmatch(previous):
        raise ContractError("previous_event_id must be none or an FPRD ID")
    if record.frontmatter.get("previous-event-id") != previous:
        raise ContractError("previous event ID does not match frontmatter")
    disposition = payload_string(record.payload, "disposition")
    if disposition not in ALLOWED_DISPOSITIONS:
        raise ContractError(f"unsupported disposition: {disposition}")
    if record.frontmatter.get("disposition") != disposition:
        raise ContractError("decision disposition does not match frontmatter")
    payload_string(record.payload, "scope_lock")
    for key in ("constraints", "prohibited_expansion"):
        values = payload_list(record.payload, key)
        if not all(isinstance(item, str) and item for item in values):
            raise ContractError(f"{key} must contain nonempty strings")
    payload_string(record.payload, "decided_by")
    payload_string(record.payload, "approval_source")
    expires = parse_iso_date(payload_string(record.payload, "expires_date"), "expires_date")
    replacement = payload_string(record.payload, "replacement_proposal")
    if disposition in {"narrow", "request-details"}:
        if replacement != "pending" and not (
            PROPOSAL_ID_RE.fullmatch(replacement) and replacement != proposal_id
        ):
            raise ContractError(
                f"{disposition} requires replacement_proposal pending or a distinct FPRP ID"
            )
    elif replacement != "none":
        raise ContractError(f"{disposition} requires replacement_proposal none")
    if disposition == "revoke" and previous == "none":
        raise ContractError("revoke cannot be a root decision event")

    execution_authority = record.frontmatter.get("execution-authority")
    stored_authorization = record.frontmatter.get("authorization-digest")
    if disposition == "approve-exact":
        if expires < decided_at.date():
            raise ContractError("approve-exact expiry cannot precede decided_at")
        if execution_authority != "exact":
            raise ContractError("approve-exact requires execution-authority: exact")
        expected = authorization_digest(proposal_digest, stored_digest)
        if stored_authorization != expected:
            raise ContractError("authorization-digest is invalid")
    else:
        if execution_authority != "none" or stored_authorization != "none":
            raise ContractError("nonauthorizing disposition must have no execution authority")


def validate_execution_shape(record: Record) -> None:
    require_record_storage_path(record.path)
    require_frontmatter(
        record,
        {"type": "learning-execution", "schema-version": "2", "authority": "none"},
    )
    execution_id = record.frontmatter.get("execution-id", "")
    match = EXECUTION_ID_RE.fullmatch(execution_id)
    if not match:
        raise ContractError("execution-id must match FPRE-YYYYMMDD-<12 auth hex>-NN")
    require_parent_month(record, match.group(1))
    if record.path.stem != execution_id:
        raise ContractError("execution filename must equal execution-id")
    if record.payload.get("schema_version") != 2:
        raise ContractError("execution payload schema_version must be 2")
    if payload_string(record.payload, "execution_id") != execution_id:
        raise ContractError("execution payload ID does not match frontmatter")
    started_at = parse_utc(payload_string(record.payload, "started_at"), "started_at")
    completed_at = parse_utc(payload_string(record.payload, "completed_at"), "completed_at")
    if completed_at < started_at:
        raise ContractError("completed_at cannot precede started_at")
    executed_date = parse_iso_date(record.frontmatter.get("executed-date", ""), "executed-date")
    if match.group(1) != completed_at.strftime("%Y%m%d") or executed_date != completed_at.date():
        raise ContractError("execution ID date and executed-date must match completed_at")

    auth_digest = payload_string(record.payload, "authorization_digest")
    auth_hex = digest_hex(auth_digest)
    if auth_hex is None:
        raise ContractError("execution authorization_digest must be a full digest")
    if match.group(2) != auth_hex[:12]:
        raise ContractError("execution ID prefix must match authorization digest")
    proposal_digest = payload_string(record.payload, "proposal_digest")
    decision_digest = payload_string(record.payload, "decision_digest")
    if auth_digest != authorization_digest(proposal_digest, decision_digest):
        raise ContractError("execution authorization digest does not bind payload digests")
    for front_key, payload_key in (
        ("proposal-id", "proposal_id"),
        ("proposal-digest", "proposal_digest"),
        ("decision-id", "decision_id"),
        ("decision-digest", "decision_digest"),
        ("authorization-digest", "authorization_digest"),
    ):
        if record.frontmatter.get(front_key) != payload_string(record.payload, payload_key):
            raise ContractError(f"execution {payload_key} does not match frontmatter")

    stored_receipt = record.frontmatter.get("receipt-digest", "")
    if digest_hex(stored_receipt) is None or stored_receipt != digest_payload(record.payload):
        raise ContractError("receipt-digest does not match canonical JSON payload")
    result = payload_string(record.payload, "result")
    if result not in ALLOWED_EXECUTION_RESULTS:
        raise ContractError(f"unsupported execution result: {result}")
    if record.frontmatter.get("status") != result:
        raise ContractError("execution result does not match frontmatter status")
    consumed = record.payload.get("approval_consumed")
    if not isinstance(consumed, bool):
        raise ContractError("approval_consumed must be a boolean")
    changed_paths = payload_list(record.payload, "changed_paths")
    if result == "blocked":
        if consumed or changed_paths:
            raise ContractError("blocked execution must not consume approval or change paths")
    elif not consumed:
        raise ContractError(f"{result} execution must consume approval")
    if result != "blocked" and not changed_paths:
        raise ContractError(f"{result} execution must identify affected paths")
    seen_paths: set[str] = set()
    for index, changed in enumerate(changed_paths):
        if not isinstance(changed, dict):
            raise ContractError(f"changed_paths[{index}] must be an object")
        path = changed.get("path")
        if not isinstance(path, str) or not is_safe_relative_path(path):
            raise ContractError(f"changed_paths[{index}].path must be vault relative")
        if path in seen_paths:
            raise ContractError(f"duplicate changed path: {path}")
        seen_paths.add(path)
        if not validate_hash(changed.get("before_sha256"), allow_absent=True):
            raise ContractError(f"changed_paths[{index}].before_sha256 is invalid")
        if not validate_hash(changed.get("expected_after_sha256")):
            raise ContractError(f"changed_paths[{index}].expected_after_sha256 is invalid")
        observed = changed.get("observed_after_sha256")
        observed_valid = validate_hash(observed, allow_absent=result != "executed")
        if result == "partial" and observed == "unknown":
            observed_valid = True
        if not observed_valid:
            raise ContractError(f"changed_paths[{index}].observed_after_sha256 is invalid")
        if result == "executed" and observed != changed.get("expected_after_sha256"):
            raise ContractError(
                f"changed_paths[{index}] executed observed hash must equal expected hash"
            )
        if result == "rolled-back" and observed != changed.get("before_sha256"):
            raise ContractError(
                f"changed_paths[{index}] rolled-back observed state must equal before state"
            )
    task_receipt = record.payload.get("task_receipt")
    if not isinstance(task_receipt, dict):
        raise ContractError("task_receipt must be an object")
    for key in ("system", "task_id"):
        if not isinstance(task_receipt.get(key), str) or not task_receipt[key]:
            raise ContractError(f"task_receipt.{key} is required")
    run_ids = task_receipt.get("run_ids")
    if not isinstance(run_ids, list) or any(
        not isinstance(run_id, str) or not run_id for run_id in run_ids
    ):
        raise ContractError("task_receipt.run_ids must contain nonempty strings")


def validate_validation_shape(record: Record) -> None:
    require_record_storage_path(record.path)
    require_frontmatter(
        record,
        {"type": "learning-validation", "schema-version": "2", "authority": "none"},
    )
    validation_id = record.frontmatter.get("validation-id", "")
    match = VALIDATION_ID_RE.fullmatch(validation_id)
    if not match:
        raise ContractError("validation-id must match FPRV-YYYYMMDD-<12 receipt hex>-NN")
    require_parent_month(record, match.group(1))
    if record.path.stem != validation_id:
        raise ContractError("validation filename must equal validation-id")
    if record.payload.get("schema_version") != 2:
        raise ContractError("validation payload schema_version must be 2")
    if payload_string(record.payload, "validation_id") != validation_id:
        raise ContractError("validation payload ID does not match frontmatter")
    execution_id = payload_string(record.payload, "execution_id")
    if record.frontmatter.get("execution-id") != execution_id:
        raise ContractError("validation execution ID does not match frontmatter")
    validated_at = parse_utc(payload_string(record.payload, "validated_at"), "validated_at")
    validation_date = parse_iso_date(
        record.frontmatter.get("validation-date", ""), "validation-date"
    )
    if match.group(1) != validated_at.strftime("%Y%m%d") or validation_date != validated_at.date():
        raise ContractError("validation ID date and validation-date must match validated_at")
    stored_digest = record.frontmatter.get("validation-digest", "")
    if digest_hex(stored_digest) is None or stored_digest != digest_payload(record.payload):
        raise ContractError("validation-digest does not match canonical JSON payload")
    result = payload_string(record.payload, "result")
    if result not in {"passed", "failed"} or record.frontmatter.get("status") != result:
        raise ContractError("validation result must be passed or failed and match status")
    validator_results = payload_list(record.payload, "validator_results")
    seen: set[str] = set()
    for index, item in enumerate(validator_results):
        if not isinstance(item, dict):
            raise ContractError(f"validator_results[{index}] must be an object")
        validator_id = item.get("id")
        if not isinstance(validator_id, str) or not VALIDATOR_ID_RE.fullmatch(validator_id):
            raise ContractError(f"validator_results[{index}].id is invalid")
        if validator_id in seen:
            raise ContractError(f"duplicate validator result: {validator_id}")
        seen.add(validator_id)
        if item.get("result") not in {"passed", "failed"}:
            raise ContractError(f"validator_results[{index}].result is invalid")
        if not isinstance(item.get("evidence"), str) or not item["evidence"]:
            raise ContractError(f"validator_results[{index}].evidence is required")
    live_hashes = payload_list(record.payload, "live_hashes")
    seen_paths: set[str] = set()
    for index, item in enumerate(live_hashes):
        if not isinstance(item, dict):
            raise ContractError(f"live_hashes[{index}] must be an object")
        path = item.get("path")
        if not isinstance(path, str) or not is_safe_relative_path(path):
            raise ContractError(f"live_hashes[{index}].path must be vault relative")
        if path in seen_paths:
            raise ContractError(f"duplicate live hash path: {path}")
        seen_paths.add(path)
        if not validate_hash(item.get("sha256")):
            raise ContractError(f"live_hashes[{index}].sha256 is invalid")


def validate_template_surfaces(repo_root: Path) -> ValidationReport:
    report = ValidationReport(errors=[], warnings=[])
    base = repo_root / "template" / "resources" / "learning-library"
    required = {
        base / "README.md": ("approve-exact", "candidates", "executions"),
        base / "approval-contract.md": (
            "FPRP-YYYYMMDD-<first 12 proposal digest hex>",
            "FPRD-YYYYMMDDTHHMMSSZ-<8 lowercase nonce hex>",
            "FPRE-YYYYMMDD-<first 12 authorization digest hex>-NN",
            "FPRV-YYYYMMDD-<first 12 execution receipt digest hex>-NN",
            "pattern-review-approval-v1",
            "Historical `FPRV` records remain immutable structural evidence",
            "Governance record files must be regular files reached without any symlink component",
        ),
        base / "candidate-report-template.md": (
            "canonical: false",
            "authority: none",
            "Candidate like malformed headings are invalid and must be reported",
        ),
        base / "exemplar-template.md": (
            "immutable `FPRP` proposal",
            "one use `FPRE` execution",
            "passing `FPRV` validation",
        ),
        base / "rubric-template.md": (
            "immutable `FPRP` proposal",
            "one use `FPRE` execution",
            "passing `FPRV` validation",
        ),
        base / "proposal-template.md": (
            "type: learning-proposal",
            '"operations"',
            '"prohibited_expansion"',
        ),
        base / "decision-template.md": (
            "type: learning-decision",
            "decision-digest:",
            "authorization-digest:",
            "approve-exact",
        ),
        base / "execution-receipt-template.md": (
            "type: learning-execution",
            '"approval_consumed"',
            '"changed_paths"',
        ),
        base / "validation-receipt-template.md": (
            "type: learning-validation",
            '"validator_results"',
            '"live_hashes"',
        ),
        base / "validate-pattern-review.py": (
            "def validate_vault",
            "def _collect_candidate_records",
            "def digest_live_target",
            "def require_record_storage_path",
            "class ValidatedPathState",
            "malformed candidate heading",
            "validated path history is discontinuous",
            "validation cannot precede execution completion",
            "execution proposal ID does not exactly match decision proposal ID",
        ),
        base / "pattern_review_core.py": (
            "def canonical_json_bytes",
            "def build_proposal",
            "def build_decision",
            "def build_execution",
            "def build_validation",
            "must be a JSON integer",
        ),
        base / "pattern-review-records.py": (
            'commands.add_parser("create"',
            "def atomic_write",
            "os.link",
        ),
        repo_root / "template" / "skills" / "pattern-review.md": (
            "candidate can never be approved directly",
            "approve-exact",
        ),
        repo_root / "template" / "skills" / "intake-processor.md": (
            "complete schema version 2",
            "passing live validation",
        ),
        repo_root / "template" / "context" / "learned-rules.md": (
            "immutable exact proposal",
            "one use execution",
            "passing validation receipt",
        ),
        repo_root / "template" / "resources" / "agent-platform" / "README.md": (
            "exact `FPRP`",
            "consumed `FPRE`",
            "passing `FPRV`",
        ),
        repo_root / "second-brain-operator.md": (
            "immutable exact proposal",
            "one use execution",
            "final passing validation",
        ),
        repo_root / "second-brain-initiate.md": ("learning-proposal", "learning-validation"),
        repo_root / "README.md": ("immutable `FPRP`", "passing `FPRV`"),
    }
    for path, markers in required.items():
        if not path.is_file():
            report.error(path, "required public contract surface is missing")
            continue
        text = path.read_text(encoding="utf-8")
        for marker in markers:
            if marker not in text:
                report.error(path, f"missing required contract marker: {marker}")

    report.record_count = len([path for path in required if path.is_file()])
    return report


def _collect_candidate_records(
    vault_root: Path, report: ValidationReport
) -> dict[str, CandidateRecord]:
    directory = vault_root / "resources" / "learning-library" / "candidates"
    candidates: dict[str, CandidateRecord] = {}
    if not directory.exists():
        return candidates
    heading_pattern = re.compile(
        r"^## Candidate (PR-\d{4}-\d{2}-\d{2}-\d{2,}):\s+\S.*$",
        flags=re.MULTILINE,
    )
    candidate_like_pattern = re.compile(
        r"^[ \t]{0,3}#{1,6}[ \t]*Candidate(?:[ \t]|:|PR-|$)",
        flags=re.IGNORECASE,
    )
    fingerprint_pattern = re.compile(
        r"^\*\*Fingerprint:\*\*\s*`([^`\n]+)`\s*$", flags=re.MULTILINE
    )
    for path in sorted(directory.rglob("*.md")):
        if path.name == "README.md":
            continue
        try:
            relative_report = path.relative_to(vault_root).as_posix()
            if not is_contained_by_root(vault_root, relative_report):
                raise ContractError("candidate report escapes vault through a symlink")
            text = path.read_text(encoding="utf-8")
            frontmatter, body = parse_frontmatter(text)
            for key, expected in {
                "type": "learning-candidate-report",
                "schema-version": "2",
                "status": "candidate",
                "canonical": "false",
                "authority": "none",
            }.items():
                if frontmatter.get(key) != expected:
                    raise ContractError(
                        f"candidate report frontmatter {key} must be {expected!r}"
                    )
            body_lines = body.splitlines()
            for line_number, line in enumerate(body_lines, 1):
                if candidate_like_pattern.match(line) and heading_pattern.fullmatch(line) is None:
                    raise ContractError(
                        f"malformed candidate heading on body line {line_number}: {line}"
                    )
            headings = list(heading_pattern.finditer(body))
            for index, heading in enumerate(headings):
                candidate_id = heading.group(1)
                section_end = (
                    headings[index + 1].start() if index + 1 < len(headings) else len(body)
                )
                section = body[heading.end() : section_end]
                fingerprint_match = fingerprint_pattern.search(section)
                if fingerprint_match is None:
                    raise ContractError(
                        f"candidate {candidate_id} is missing a Fingerprint field"
                    )
                candidate = CandidateRecord(
                    candidate_id=candidate_id,
                    report_path=path,
                    fingerprint=fingerprint_match.group(1),
                )
                previous = candidates.get(candidate_id)
                if previous is not None:
                    report.error(
                        path,
                        f"duplicate candidate ID also used by {previous.report_path}: {candidate_id}",
                    )
                else:
                    candidates[candidate_id] = candidate
        except (ContractError, OSError, UnicodeDecodeError) as exc:
            report.error(path, str(exc))
    return candidates


def _collect_records(vault_root: Path, report: ValidationReport) -> dict[str, list[Record]]:
    base = vault_root / "resources" / "learning-library"
    records: dict[str, list[Record]] = {kind: [] for kind in RECORD_DIRS}
    if not base.is_dir():
        report.error(base, "learning library does not exist")
        return records
    for kind, folder in RECORD_DIRS.items():
        directory = base / folder
        if directory.is_symlink():
            report.error(directory, f"record path contains a symlink component: {directory}")
            continue
        if not directory.exists():
            continue
        try:
            require_record_storage_path(directory, vault_root)
        except ContractError as exc:
            report.error(directory, str(exc))
            continue
        symlink_entries = {
            path for path in directory.rglob("*") if path.is_symlink()
        }
        for path in sorted(symlink_entries):
            report.error(path, f"record path contains a symlink component: {path}")
        for path in sorted(directory.rglob("*.md")):
            if path.name == "README.md":
                continue
            if path in symlink_entries or first_symlink_component(path, vault_root) is not None:
                if path not in symlink_entries:
                    report.error(path, "record path contains a symlink component")
                continue
            try:
                require_record_storage_path(path, vault_root)
                record = load_record(kind, path)
                {
                    "proposal": validate_proposal,
                    "decision": validate_decision_shape,
                    "execution": validate_execution_shape,
                    "validation": validate_validation_shape,
                }[kind](record)
                records[kind].append(record)
            except (ContractError, OSError) as exc:
                report.error(path, str(exc))
    return records


def _unique_map(records: Iterable[Record], report: ValidationReport) -> dict[str, Record]:
    result: dict[str, Record] = {}
    for record in records:
        if record.record_id in result:
            report.error(record.path, f"duplicate record ID also used by {result[record.record_id].path}")
        else:
            result[record.record_id] = record
    return result


def validate_vault(vault_root: Path) -> ValidationReport:
    report = ValidationReport(errors=[], warnings=[])
    candidates = _collect_candidate_records(vault_root, report)
    records = _collect_records(vault_root, report)
    report.record_count = len(candidates) + sum(len(items) for items in records.values())
    proposals = _unique_map(records["proposal"], report)
    decisions = _unique_map(records["decision"], report)
    executions = _unique_map(records["execution"], report)
    validations = _unique_map(records["validation"], report)

    revision_parents: dict[str, str] = {}
    for proposal_id, proposal in proposals.items():
        revision = proposal.payload.get("revision_of")
        if isinstance(revision, str) and revision != "none":
            if revision not in proposals:
                report.error(
                    proposal.path,
                    f"revision_of proposal does not exist: {revision}",
                )
            else:
                revision_parents[proposal_id] = revision
        for source in proposal.payload.get("source_candidates", []):
            if not isinstance(source, dict):
                continue
            candidate_id = source.get("id")
            candidate = candidates.get(candidate_id)
            if candidate is None:
                report.error(
                    proposal.path,
                    f"source candidate does not resolve to a candidate report record: {candidate_id}",
                )
                continue
            reference = source.get("path")
            if not isinstance(reference, str):
                continue
            report_reference, separator, fragment = reference.partition("#")
            if (
                not separator
                or fragment != candidate_id
                or not is_safe_relative_path(report_reference)
            ):
                report.error(
                    proposal.path,
                    f"source candidate path must be a vault relative report path with #{candidate_id}",
                )
            else:
                actual_report = candidate.report_path.relative_to(vault_root).as_posix()
                if report_reference != actual_report:
                    report.error(
                        proposal.path,
                        f"source candidate path does not match its report record: {candidate_id}",
                    )
            if source.get("fingerprint") != candidate.fingerprint:
                report.error(
                    proposal.path,
                    f"source candidate fingerprint does not match its report record: {candidate_id}",
                )
        for operation in proposal.payload.get("operations", []):
            if not isinstance(operation, dict):
                continue
            target = operation.get("path")
            if isinstance(target, str) and not is_contained_by_root(vault_root, target):
                report.error(
                    proposal.path,
                    f"proposal target escapes vault through a symlink: {target}",
                )

    for proposal_id in revision_parents:
        seen: set[str] = set()
        current = proposal_id
        while current in revision_parents:
            if current in seen:
                report.error(
                    proposals[proposal_id].path,
                    "proposal revision chain contains a cycle",
                )
                break
            seen.add(current)
            current = revision_parents[current]

    children: dict[str, list[str]] = {}
    proposal_roots: dict[str, list[str]] = {}
    for decision_id, decision in decisions.items():
        payload = decision.payload
        proposal_id = payload.get("proposal_id")
        proposal = proposals.get(proposal_id)
        if proposal is None:
            report.error(decision.path, f"referenced proposal does not exist: {proposal_id}")
        elif decision.frontmatter.get("proposal-digest") != proposal.frontmatter.get("proposal-digest"):
            report.error(decision.path, "decision proposal digest does not match proposal record")
        previous = payload.get("previous_event_id")
        if previous == "none":
            proposal_roots.setdefault(str(proposal_id), []).append(decision_id)
            if payload.get("disposition") not in ROOT_DISPOSITIONS:
                report.error(decision.path, "disposition is not allowed as a root decision")
        elif isinstance(previous, str):
            children.setdefault(previous, []).append(decision_id)
            previous_record = decisions.get(previous)
            if previous_record is None:
                report.error(decision.path, f"previous decision event does not exist: {previous}")
            else:
                if previous_record.payload.get("proposal_id") != proposal_id:
                    report.error(decision.path, "decision chain crosses proposal IDs")
                prior_disposition = previous_record.payload.get("disposition")
                current_disposition = payload.get("disposition")
                if current_disposition not in ALLOWED_TRANSITIONS.get(
                    str(prior_disposition), set()
                ):
                    report.error(
                        decision.path,
                        f"invalid decision transition: {prior_disposition} to {current_disposition}",
                    )
                try:
                    prior_time = parse_utc(
                        payload_string(previous_record.payload, "decided_at"), "decided_at"
                    )
                    current_time = parse_utc(payload_string(payload, "decided_at"), "decided_at")
                    if current_time <= prior_time:
                        report.error(decision.path, "decision event time must follow previous event")
                except ContractError as exc:
                    report.error(decision.path, str(exc))
        replacement = payload.get("replacement_proposal")
        if isinstance(replacement, str) and PROPOSAL_ID_RE.fullmatch(replacement):
            replacement_record = proposals.get(replacement)
            if replacement_record is None:
                report.error(
                    decision.path,
                    f"replacement proposal does not exist: {replacement}",
                )
            elif replacement_record.payload.get("revision_of") != proposal_id:
                report.error(
                    decision.path,
                    "replacement proposal revision_of must name the source proposal",
                )
    for proposal_id, roots in proposal_roots.items():
        if len(roots) > 1:
            report.error(proposal_id, f"decision chain has multiple roots: {', '.join(roots)}")
    for previous, next_ids in children.items():
        if len(next_ids) > 1:
            report.error(previous, f"decision chain branches to: {', '.join(next_ids)}")

    executions_by_auth: dict[str, list[Record]] = {}
    for execution in executions.values():
        payload = execution.payload
        proposal_id = payload.get("proposal_id")
        decision_id = payload.get("decision_id")
        auth = payload.get("authorization_digest")
        proposal = proposals.get(proposal_id)
        decision = decisions.get(decision_id)
        for changed in payload.get("changed_paths", []):
            if not isinstance(changed, dict):
                continue
            target = changed.get("path")
            if isinstance(target, str) and not is_contained_by_root(vault_root, target):
                report.error(
                    execution.path,
                    f"execution target escapes vault through a symlink: {target}",
                )
        if proposal is None:
            report.error(execution.path, f"referenced proposal does not exist: {proposal_id}")
        elif payload.get("proposal_digest") != proposal.frontmatter.get("proposal-digest"):
            report.error(execution.path, "execution proposal digest does not match proposal")
        if decision is None:
            report.error(execution.path, f"referenced decision does not exist: {decision_id}")
        else:
            if proposal_id != decision.payload.get("proposal_id"):
                report.error(
                    execution.path,
                    "execution proposal ID does not exactly match decision proposal ID",
                )
            if payload.get("decision_digest") != decision.frontmatter.get("decision-digest"):
                report.error(execution.path, "execution decision digest does not match decision")
            if auth != decision.frontmatter.get("authorization-digest"):
                report.error(execution.path, "execution authorization digest does not match decision")
            if decision.payload.get("disposition") != "approve-exact":
                report.error(execution.path, "execution decision is not approve-exact")
            if decision.frontmatter.get("execution-authority") != "exact":
                report.error(execution.path, "execution decision has no exact authority")
            try:
                started = parse_utc(payload_string(payload, "started_at"), "started_at")
                approved_at = parse_utc(
                    payload_string(decision.payload, "decided_at"), "decided_at"
                )
                if started < approved_at:
                    report.error(execution.path, "execution started before approve-exact decision")
                expires = parse_iso_date(
                    payload_string(decision.payload, "expires_date"), "expires_date"
                )
                if started.date() > expires:
                    report.error(execution.path, "authorization expired before execution attempt")
                applicable = [
                    item
                    for item in decisions.values()
                    if item.payload.get("proposal_id") == proposal_id
                    and parse_utc(payload_string(item.payload, "decided_at"), "decided_at") <= started
                ]
                if applicable:
                    latest = max(
                        applicable,
                        key=lambda item: (
                            parse_utc(payload_string(item.payload, "decided_at"), "decided_at"),
                            item.record_id,
                        ),
                    )
                    if latest.record_id != decision_id:
                        report.error(
                            execution.path,
                            f"execution decision is not latest applicable event; latest is {latest.record_id}",
                        )
            except ContractError as exc:
                report.error(execution.path, str(exc))
        if isinstance(auth, str):
            executions_by_auth.setdefault(auth, []).append(execution)
        if proposal is not None and payload.get("result") in {
            "executed",
            "partial",
            "rolled-back",
        }:
            expected = {
                item["path"]: (item["before_sha256"], item["after_sha256"])
                for item in proposal.payload.get("operations", [])
                if isinstance(item, dict) and "path" in item
            }
            observed = {
                item["path"]: (
                    item["before_sha256"],
                    item["expected_after_sha256"],
                    item["observed_after_sha256"],
                )
                for item in payload.get("changed_paths", [])
                if isinstance(item, dict) and "path" in item
            }
            result = payload.get("result")
            if result == "executed":
                required = {
                    path: (before, after, after)
                    for path, (before, after) in expected.items()
                }
                if observed != required:
                    report.error(
                        execution.path,
                        "executed changed_paths do not match every proposal path and observed hash",
                    )
            else:
                if not observed:
                    report.error(execution.path, f"{result} execution has no affected paths")
                for path, (before, expected_after, observed_after) in observed.items():
                    approved = expected.get(path)
                    if approved is None:
                        report.error(execution.path, f"{result} path is not approved: {path}")
                        continue
                    if (before, expected_after) != approved:
                        report.error(
                            execution.path,
                            f"{result} path hashes do not match proposal: {path}",
                        )
                    if result == "rolled-back" and observed_after != approved[0]:
                        report.error(
                            execution.path,
                            f"rolled-back path did not restore before hash: {path}",
                        )

    for auth, attempts in executions_by_auth.items():
        consumed = [item for item in attempts if item.payload.get("approval_consumed") is True]
        if len(consumed) > 1:
            report.error(auth, "authorization digest has more than one consumed execution")
        numbered: list[tuple[int, Record]] = []
        for item in attempts:
            match = EXECUTION_ID_RE.fullmatch(item.record_id)
            if match:
                numbered.append((int(match.group(3)), item))
        numbers = sorted(number for number, _ in numbered)
        if numbers != list(range(1, len(numbers) + 1)):
            report.error(auth, f"execution attempt sequence must be contiguous from 01, found {numbers}")
        ordered = sorted(numbered, key=lambda item: item[0])
        previous_started: datetime | None = None
        previous_completed: datetime | None = None
        for _, item in ordered:
            try:
                started = parse_utc(payload_string(item.payload, "started_at"), "started_at")
                completed = parse_utc(
                    payload_string(item.payload, "completed_at"), "completed_at"
                )
            except ContractError as exc:
                report.error(item.path, str(exc))
                continue
            if previous_started is not None and started < previous_started:
                report.error(item.path, "execution attempt start times must be nondecreasing")
            if previous_completed is not None and completed < previous_completed:
                report.error(item.path, "execution attempt completion times must be nondecreasing")
            if previous_completed is not None and started < previous_completed:
                report.error(item.path, "execution attempts must not overlap or move backward")
            previous_started = started
            previous_completed = completed
        if consumed:
            consumed_number = next(number for number, item in numbered if item is consumed[0])
            later = [item.record_id for number, item in numbered if number > consumed_number]
            if later:
                report.error(auth, f"attempts exist after authorization consumption: {', '.join(later)}")

    for decision in decisions.values():
        if decision.payload.get("disposition") != "revoke":
            continue
        previous_id = decision.payload.get("previous_event_id")
        previous = decisions.get(previous_id)
        if previous is None:
            continue
        consumed_before_revoke: list[str] = []
        for execution in executions.values():
            if (
                execution.payload.get("decision_id") != previous_id
                or execution.payload.get("approval_consumed") is not True
            ):
                continue
            consumed_before_revoke.append(execution.record_id)
        if consumed_before_revoke:
            report.error(
                decision.path,
                "cannot revoke an authorization already consumed by: "
                + ", ".join(sorted(consumed_before_revoke)),
            )

    validations_by_execution: dict[str, list[Record]] = {}
    locally_successful_validations: set[str] = set()
    for validation in validations.values():
        execution_id = validation.payload.get("execution_id")
        execution = executions.get(execution_id)
        if execution is None:
            report.error(validation.path, f"referenced execution does not exist: {execution_id}")
            continue
        receipt_hex = digest_hex(execution.frontmatter.get("receipt-digest", ""))
        match = VALIDATION_ID_RE.fullmatch(validation.record_id)
        binding_valid = receipt_hex is not None and match is not None
        if receipt_hex is not None and match and match.group(2) != receipt_hex[:12]:
            report.error(validation.path, "validation ID prefix does not match execution receipt digest")
            binding_valid = False
        validations_by_execution.setdefault(str(execution_id), []).append(validation)

        temporal_valid = True
        try:
            validated_at = parse_utc(
                payload_string(validation.payload, "validated_at"), "validated_at"
            )
            completed_at = parse_utc(
                payload_string(execution.payload, "completed_at"), "completed_at"
            )
            if validated_at < completed_at:
                report.error(
                    validation.path,
                    "validation cannot precede execution completion",
                )
                temporal_valid = False
        except ContractError as exc:
            report.error(validation.path, str(exc))
            temporal_valid = False

        if validation.payload.get("result") == "passed":
            locally_valid = binding_valid and temporal_valid
            if execution.payload.get("result") != "executed" or not execution.payload.get(
                "approval_consumed"
            ):
                report.error(validation.path, "passing validation requires a consumed executed receipt")
                continue
            proposal = proposals.get(execution.payload.get("proposal_id"))
            if proposal is None:
                continue
            required_validators = set(proposal.payload.get("validation", []))
            results = validation.payload.get("validator_results", [])
            observed_validators = {
                item.get("id") for item in results if isinstance(item, dict)
            }
            if observed_validators != required_validators:
                report.error(validation.path, "passing validation does not exactly cover proposal validators")
                locally_valid = False
            if any(item.get("result") != "passed" for item in results if isinstance(item, dict)):
                report.error(validation.path, "passing validation contains a failed validator result")
                locally_valid = False
            expected_hashes = {
                item.get("path"): item.get("after_sha256")
                for item in proposal.payload.get("operations", [])
                if isinstance(item, dict)
            }
            observed_hashes = {
                item.get("path"): item.get("sha256")
                for item in validation.payload.get("live_hashes", [])
                if isinstance(item, dict)
            }
            if observed_hashes != expected_hashes:
                report.error(validation.path, "passing validation live hashes do not match proposal")
                locally_valid = False
            if locally_valid:
                locally_successful_validations.add(validation.record_id)

    path_histories: dict[str, list[ValidatedPathState]] = {}
    for execution_id, items in validations_by_execution.items():
        numbered_validations = sorted(
            (
                int(match.group(3)),
                item,
            )
            for item in items
            if (match := VALIDATION_ID_RE.fullmatch(item.record_id))
        )
        numbers = [number for number, _ in numbered_validations]
        sequence_valid = True
        if numbers != list(range(1, len(numbers) + 1)):
            report.error(execution_id, f"validation sequence must be contiguous from 01, found {numbers}")
            sequence_valid = False
        previous_time: datetime | None = None
        for _, item in numbered_validations:
            try:
                current_time = parse_utc(
                    payload_string(item.payload, "validated_at"), "validated_at"
                )
            except ContractError as exc:
                report.error(item.path, str(exc))
                continue
            if previous_time is not None and current_time < previous_time:
                report.error(item.path, "validation attempt times must be nondecreasing")
                sequence_valid = False
            previous_time = current_time
        passed_numbers = [
            number
            for number, item in numbered_validations
            if item.payload.get("result") == "passed"
        ]
        if len(passed_numbers) > 1:
            report.error(execution_id, "an execution may have at most one passing validation")
            sequence_valid = False
        if passed_numbers and passed_numbers[0] != numbers[-1]:
            report.error(execution_id, "passing validation must be the final validation attempt")
            sequence_valid = False
        if len(passed_numbers) == 1 and sequence_valid:
            passing_validation = next(
                item
                for _, item in numbered_validations
                if item.payload.get("result") == "passed"
            )
            if passing_validation.record_id in locally_successful_validations:
                execution = executions.get(execution_id)
                proposal = (
                    proposals.get(execution.payload.get("proposal_id"))
                    if execution is not None
                    else None
                )
                if execution is not None and proposal is not None:
                    completed_at = parse_utc(
                        payload_string(execution.payload, "completed_at"), "completed_at"
                    )
                    for operation in proposal.payload.get("operations", []):
                        if not isinstance(operation, dict):
                            continue
                        path = operation.get("path")
                        before = operation.get("before_sha256")
                        after = operation.get("after_sha256")
                        if not all(isinstance(value, str) for value in (path, before, after)):
                            continue
                        path_histories.setdefault(path, []).append(
                            ValidatedPathState(
                                path=path,
                                before_sha256=before,
                                after_sha256=after,
                                completed_at=completed_at,
                                execution=execution,
                                validation=passing_validation,
                            )
                        )

    for path, states in path_histories.items():
        ordered_states = sorted(
            states,
            key=lambda state: (
                state.completed_at,
                state.execution.record_id,
                state.validation.record_id,
            ),
        )
        for previous, current in zip(ordered_states, ordered_states[1:]):
            if current.completed_at == previous.completed_at:
                report.error(
                    current.validation.path,
                    f"validated path history has ambiguous completion times: {path}",
                )
            if current.before_sha256 != previous.after_sha256:
                report.error(
                    current.validation.path,
                    f"validated path history is discontinuous for {path}",
                )
        latest = ordered_states[-1]
        try:
            current_digest = digest_live_target(vault_root, path)
        except ContractError as exc:
            report.error(latest.validation.path, str(exc))
            continue
        if current_digest != latest.after_sha256:
            report.error(
                latest.validation.path,
                f"current live vault target bytes do not match latest successful validation: {path}",
            )

    for execution in executions.values():
        items = validations_by_execution.get(execution.record_id, [])
        if execution.payload.get("result") == "executed":
            if not any(item.payload.get("result") == "passed" for item in items):
                report.error(
                    execution.path,
                    "executed receipt requires a passing validation receipt",
                )
        elif (
            execution.payload.get("approval_consumed")
            and execution.record_id not in validations_by_execution
        ):
            report.warn(
                execution.path,
                "consumed nonexecuted receipt has no validation receipt and is not complete",
            )

    return report


def print_report(report: ValidationReport) -> int:
    for warning in report.warnings:
        print(f"WARNING {warning}")
    for error in report.errors:
        print(f"ERROR {error}")
    if report.errors:
        print(
            f"Pattern Review validation failed: {len(report.errors)} error(s), "
            f"{len(report.warnings)} warning(s), {report.record_count} record(s)."
        )
        return 1
    print(
        f"Pattern Review validation passed: {report.record_count} record(s), "
        f"{len(report.warnings)} warning(s)."
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--templates", type=Path, metavar="REPO_ROOT")
    mode.add_argument("--vault", type=Path, metavar="VAULT_ROOT")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.templates is not None:
        report = validate_template_surfaces(args.templates.resolve())
    else:
        report = validate_vault(args.vault.resolve())
    return print_report(report)


if __name__ == "__main__":
    sys.exit(main())
