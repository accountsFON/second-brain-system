"""Shared canonical JSON and identifier functions for Pattern Review records."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from datetime import date, datetime
from pathlib import PurePosixPath
from typing import Any


DIGEST_RE = re.compile(r"^sha256:([0-9a-f]{64})$")
PROPOSAL_ID_RE = re.compile(r"^FPRP-(\d{8})-([0-9a-f]{12})$")
DECISION_ID_RE = re.compile(r"^FPRD-(\d{8}T\d{6}Z)-([0-9a-f]{8})$")
EXECUTION_ID_RE = re.compile(r"^FPRE-(\d{8})-([0-9a-f]{12})-(\d{2})$")
VALIDATION_ID_RE = re.compile(r"^FPRV-(\d{8})-([0-9a-f]{12})-(\d{2})$")
NONCE_RE = re.compile(r"^[0-9a-f]{8}$")
CANDIDATE_ID_RE = re.compile(r"^PR-\d{4}-\d{2}-\d{2}-\d{2,}$")
VALIDATOR_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._:-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
AUTHORIZATION_DOMAIN = "pattern-review-approval-v1"
ALLOWED_DISPOSITIONS = {
    "hold",
    "reject",
    "narrow",
    "request-details",
    "approve-exact",
    "revoke",
}
ALLOWED_EXECUTION_RESULTS = {"blocked", "executed", "partial", "rolled-back"}


class ContractError(ValueError):
    """Raised when canonical input violates the portable record contract."""


def _reject_float(_: str) -> None:
    raise ContractError("floating point values are not allowed in canonical JSON")


def _reject_constant(value: str) -> None:
    raise ContractError(f"nonfinite JSON value is not allowed: {value}")


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def parse_json_payload(raw: str) -> dict[str, Any]:
    try:
        value = json.loads(
            raw,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
            object_pairs_hook=_unique_object,
        )
    except (json.JSONDecodeError, ContractError) as exc:
        raise ContractError(f"invalid canonical JSON payload: {exc}") from exc
    if not isinstance(value, dict):
        raise ContractError("canonical JSON payload must be an object")
    return value


def canonical_json_bytes(payload: dict[str, Any]) -> bytes:
    def reject_floats(value: Any) -> None:
        if isinstance(value, float):
            raise ContractError("floating point values are not allowed in canonical JSON")
        if isinstance(value, dict):
            for key, item in value.items():
                if not isinstance(key, str):
                    raise ContractError("canonical JSON object keys must be strings")
                reject_floats(item)
        elif isinstance(value, list):
            for item in value:
                reject_floats(item)

    reject_floats(payload)
    try:
        return json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ContractError(f"payload cannot be serialized canonically: {exc}") from exc


def digest_payload(payload: dict[str, Any]) -> str:
    return "sha256:" + hashlib.sha256(canonical_json_bytes(payload)).hexdigest()


def digest_text(value: str) -> str:
    if not isinstance(value, str):
        raise ContractError("exact content must be a string")
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def authorization_digest(proposal_digest: str, decision_digest: str) -> str:
    require_digest(proposal_digest, "proposal_digest")
    require_digest(decision_digest, "decision_digest")
    material = (
        AUTHORIZATION_DOMAIN + "\n" + proposal_digest + "\n" + decision_digest
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(material).hexdigest()


def digest_hex(value: str) -> str | None:
    match = DIGEST_RE.fullmatch(value)
    return match.group(1) if match else None


def require_digest(value: Any, field: str) -> str:
    if not isinstance(value, str) or DIGEST_RE.fullmatch(value) is None:
        raise ContractError(f"{field} must be sha256: followed by 64 lowercase hex characters")
    return value


def _is_safe_relative_path(value: Any) -> bool:
    if not isinstance(value, str) or not value or "\\" in value:
        return False
    if value.startswith(("/", "~")) or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", value):
        return False
    path = PurePosixPath(value)
    return not path.is_absolute() and ".." not in path.parts and value != "."


def _is_digest_or(value: Any, *sentinels: str) -> bool:
    return isinstance(value, str) and (
        DIGEST_RE.fullmatch(value) is not None or value in sentinels
    )


def parse_date(value: str, field: str) -> date:
    if not isinstance(value, str) or DATE_RE.fullmatch(value) is None:
        raise ContractError(f"{field} must be YYYY-MM-DD")
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError) as exc:
        raise ContractError(f"{field} must be YYYY-MM-DD") from exc


def parse_utc(value: str, field: str) -> datetime:
    if not isinstance(value, str) or UTC_RE.fullmatch(value) is None:
        raise ContractError(f"{field} must be UTC YYYY-MM-DDTHH:MM:SSZ")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError) as exc:
        raise ContractError(f"{field} must be UTC YYYY-MM-DDTHH:MM:SSZ") from exc


def _require_schema(payload: dict[str, Any]) -> None:
    if payload.get("schema_version") != 2:
        raise ContractError("payload schema_version must be 2")


def _replace_pending(payload: dict[str, Any], field: str, value: str) -> dict[str, Any]:
    result = deepcopy(payload)
    current = result.get(field)
    if current not in {None, "PENDING"}:
        raise ContractError(f"create input {field} must be absent or PENDING")
    result[field] = value
    return result


def _require_nonempty_string(payload: dict[str, Any], field: str) -> str:
    value = payload.get(field)
    if not isinstance(value, str) or not value:
        raise ContractError(f"{field} must be a nonempty string")
    return value


def _require_string_list(
    payload: dict[str, Any], field: str, *, nonempty: bool = False
) -> list[str]:
    value = payload.get(field)
    if not isinstance(value, list) or (nonempty and not value):
        suffix = " and not empty" if nonempty else ""
        raise ContractError(f"{field} must be an array{suffix}")
    if not all(isinstance(item, str) and item for item in value):
        raise ContractError(f"{field} must contain nonempty strings")
    return value


def build_proposal(payload: dict[str, Any], created_date: str) -> dict[str, Any]:
    _require_schema(payload)
    parsed_date = parse_date(created_date, "created_date")
    if not isinstance(payload.get("source_candidates"), list) or not payload[
        "source_candidates"
    ]:
        raise ContractError("proposal payload requires source_candidates")
    revision = _require_nonempty_string(payload, "revision_of")
    if revision != "none" and PROPOSAL_ID_RE.fullmatch(revision) is None:
        raise ContractError("revision_of must be none or an FPRP ID")
    for index, candidate in enumerate(payload["source_candidates"]):
        if not isinstance(candidate, dict):
            raise ContractError(f"source_candidates[{index}] must be an object")
        candidate_id = candidate.get("id")
        if not isinstance(candidate_id, str) or CANDIDATE_ID_RE.fullmatch(candidate_id) is None:
            raise ContractError(f"source_candidates[{index}].id is invalid")
        for field in ("path", "fingerprint"):
            if not isinstance(candidate.get(field), str) or not candidate[field]:
                raise ContractError(f"source_candidates[{index}].{field} is required")
    _require_nonempty_string(payload, "scope")
    if not isinstance(payload.get("operations"), list) or not payload["operations"]:
        raise ContractError("proposal payload requires operations")
    seen_paths: set[str] = set()
    for index, operation in enumerate(payload["operations"]):
        if not isinstance(operation, dict):
            raise ContractError(f"proposal operation {index} must be an object")
        action = operation.get("action")
        if action not in {"create", "replace"}:
            raise ContractError(
                f"proposal operation {index} action must be create or replace"
            )
        path = operation.get("path")
        if not _is_safe_relative_path(path):
            raise ContractError(f"proposal operation {index} path must be vault relative")
        if path in seen_paths:
            raise ContractError(f"duplicate proposal operation path: {path}")
        seen_paths.add(path)
        before = operation.get("before_sha256")
        if action == "create" and before != "absent":
            raise ContractError(
                f"proposal operation {index} create requires before_sha256 absent"
            )
        if action == "replace" and not _is_digest_or(before):
            raise ContractError(
                f"proposal operation {index} replace requires a full before_sha256 digest"
            )
        if operation.get("change_format") != "full-content":
            raise ContractError("schema version 2 permits full-content changes only")
        exact_change = operation.get("exact_change")
        if not isinstance(exact_change, str):
            raise ContractError(f"proposal operation {index} requires exact_change")
        if operation.get("after_sha256") != digest_text(exact_change):
            raise ContractError(
                f"proposal operation {index} after_sha256 does not hash exact_change"
            )
    prohibited = _require_string_list(payload, "prohibited_expansion", nonempty=True)
    if not prohibited:
        raise ContractError("proposal payload requires prohibited expansion")
    validators = _require_string_list(payload, "validation", nonempty=True)
    if len(set(validators)) != len(validators):
        raise ContractError("validation identifiers must be unique")
    for validator in validators:
        if VALIDATOR_ID_RE.fullmatch(validator) is None:
            raise ContractError(f"unsafe trusted validator ID: {validator!r}")
    _require_nonempty_string(payload, "failure_behavior")
    finalized = deepcopy(payload)
    digest = digest_payload(finalized)
    identifier = f"FPRP-{parsed_date.strftime('%Y%m%d')}-{digest[7:19]}"
    return {
        "record_kind": "proposal",
        "record_id": identifier,
        "record_digest": digest,
        "created_date": created_date,
        "payload": finalized,
    }


def build_decision(payload: dict[str, Any], nonce: str) -> dict[str, Any]:
    _require_schema(payload)
    if NONCE_RE.fullmatch(nonce) is None:
        raise ContractError("nonce must contain exactly eight lowercase hexadecimal characters")
    decided_at = payload.get("decided_at")
    if not isinstance(decided_at, str):
        raise ContractError("decision payload requires decided_at")
    timestamp = parse_utc(decided_at, "decided_at")
    identifier = f"FPRD-{timestamp.strftime('%Y%m%dT%H%M%SZ')}-{nonce}"
    finalized = _replace_pending(payload, "decision_id", identifier)
    proposal_id = finalized.get("proposal_id")
    proposal_match = (
        PROPOSAL_ID_RE.fullmatch(proposal_id) if isinstance(proposal_id, str) else None
    )
    if proposal_match is None:
        raise ContractError("decision payload proposal_id must be an FPRP ID")
    proposal_digest = require_digest(finalized.get("proposal_digest"), "proposal_digest")
    if proposal_match.group(2) != proposal_digest[7:19]:
        raise ContractError("decision proposal_id suffix must match proposal_digest")
    decision_digest = digest_payload(finalized)
    disposition = finalized.get("disposition")
    if disposition not in ALLOWED_DISPOSITIONS:
        raise ContractError(f"unsupported decision disposition: {disposition!r}")
    expires_date = finalized.get("expires_date")
    if not isinstance(expires_date, str):
        raise ContractError("decision payload requires expires_date")
    expires = parse_date(expires_date, "expires_date")
    replacement = finalized.get("replacement_proposal")
    if disposition in {"narrow", "request-details"}:
        if replacement != "pending" and not (
            isinstance(replacement, str)
            and PROPOSAL_ID_RE.fullmatch(replacement) is not None
            and replacement != proposal_id
        ):
            raise ContractError(
                f"{disposition} requires replacement_proposal pending or a distinct FPRP ID"
            )
    elif replacement != "none":
        raise ContractError(f"{disposition} requires replacement_proposal none")
    previous = finalized.get("previous_event_id")
    if previous != "none" and not (
        isinstance(previous, str) and DECISION_ID_RE.fullmatch(previous) is not None
    ):
        raise ContractError("previous_event_id must be none or an FPRD ID")
    if disposition == "revoke" and previous == "none":
        raise ContractError("revoke cannot be a root decision event")
    _require_nonempty_string(finalized, "scope_lock")
    _require_string_list(finalized, "constraints")
    _require_string_list(finalized, "prohibited_expansion")
    _require_nonempty_string(finalized, "decided_by")
    _require_nonempty_string(finalized, "approval_source")
    if disposition == "approve-exact":
        if expires < timestamp.date():
            raise ContractError("approve-exact expiry cannot precede decided_at")
        execution_authority = "exact"
        auth_digest = authorization_digest(proposal_digest, decision_digest)
    else:
        execution_authority = "none"
        auth_digest = "none"
    return {
        "record_kind": "decision",
        "record_id": identifier,
        "record_digest": decision_digest,
        "authorization_digest": auth_digest,
        "execution_authority": execution_authority,
        "payload": finalized,
    }


def _require_sequence(value: int, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 99:
        raise ContractError(f"{field} must be an integer from 1 through 99")
    return value


def build_execution(payload: dict[str, Any], attempt: int) -> dict[str, Any]:
    _require_schema(payload)
    attempt = _require_sequence(attempt, "attempt")
    auth_digest = require_digest(payload.get("authorization_digest"), "authorization_digest")
    started_at = payload.get("started_at")
    if not isinstance(started_at, str):
        raise ContractError("execution payload requires started_at")
    started_timestamp = parse_utc(started_at, "started_at")
    proposal_id = payload.get("proposal_id")
    decision_id = payload.get("decision_id")
    if not isinstance(proposal_id, str) or PROPOSAL_ID_RE.fullmatch(proposal_id) is None:
        raise ContractError("execution payload proposal_id must be an FPRP ID")
    if not isinstance(decision_id, str) or DECISION_ID_RE.fullmatch(decision_id) is None:
        raise ContractError("execution payload decision_id must be an FPRD ID")
    proposal_digest = require_digest(payload.get("proposal_digest"), "proposal_digest")
    decision_digest = require_digest(payload.get("decision_digest"), "decision_digest")
    if auth_digest != authorization_digest(proposal_digest, decision_digest):
        raise ContractError("execution authorization_digest does not bind payload digests")
    completed_at = payload.get("completed_at")
    if not isinstance(completed_at, str):
        raise ContractError("execution payload requires completed_at")
    completed_timestamp = parse_utc(completed_at, "completed_at")
    if completed_timestamp < started_timestamp:
        raise ContractError("completed_at cannot precede started_at")
    identifier = (
        f"FPRE-{completed_timestamp.strftime('%Y%m%d')}-{auth_digest[7:19]}-{attempt:02d}"
    )
    finalized = _replace_pending(payload, "execution_id", identifier)
    result = finalized.get("result")
    if result not in ALLOWED_EXECUTION_RESULTS:
        raise ContractError(f"unsupported execution result: {result!r}")
    consumed = finalized.get("approval_consumed")
    changed_paths = finalized.get("changed_paths")
    if not isinstance(consumed, bool) or not isinstance(changed_paths, list):
        raise ContractError("execution payload requires boolean approval_consumed and changed_paths")
    if result == "blocked" and (consumed or changed_paths):
        raise ContractError("blocked execution cannot consume approval or contain changed paths")
    if result != "blocked" and not consumed:
        raise ContractError(f"{result} execution must consume approval")
    if result != "blocked" and not changed_paths:
        raise ContractError(f"{result} execution must identify affected paths")
    seen_paths: set[str] = set()
    for index, changed in enumerate(changed_paths):
        if not isinstance(changed, dict):
            raise ContractError(f"changed_paths[{index}] must be an object")
        path = changed.get("path")
        if not _is_safe_relative_path(path):
            raise ContractError(f"changed_paths[{index}].path must be vault relative")
        if path in seen_paths:
            raise ContractError(f"duplicate changed path: {path}")
        seen_paths.add(path)
        if not _is_digest_or(changed.get("before_sha256"), "absent"):
            raise ContractError(f"changed_paths[{index}].before_sha256 is invalid")
        if not _is_digest_or(changed.get("expected_after_sha256")):
            raise ContractError(
                f"changed_paths[{index}].expected_after_sha256 is invalid"
            )
        observed = changed.get("observed_after_sha256")
        allowed_sentinels = (
            ("absent", "unknown")
            if result == "partial"
            else (("absent",) if result == "rolled-back" else ())
        )
        if not _is_digest_or(observed, *allowed_sentinels):
            raise ContractError(
                f"changed_paths[{index}].observed_after_sha256 is invalid for {result}"
            )
        if result == "executed" and observed != changed.get("expected_after_sha256"):
            raise ContractError(
                f"changed_paths[{index}] executed observed hash must equal expected hash"
            )
        if result == "rolled-back" and observed != changed.get("before_sha256"):
            raise ContractError(
                f"changed_paths[{index}] rolled-back observed state must equal before state"
            )
    task_receipt = finalized.get("task_receipt")
    if not isinstance(task_receipt, dict):
        raise ContractError("execution payload requires task_receipt")
    _require_nonempty_string(task_receipt, "system")
    _require_nonempty_string(task_receipt, "task_id")
    _require_string_list(task_receipt, "run_ids")
    receipt_digest = digest_payload(finalized)
    return {
        "record_kind": "execution",
        "record_id": identifier,
        "record_digest": receipt_digest,
        "attempt": attempt,
        "payload": finalized,
    }


def build_validation(
    payload: dict[str, Any], execution_receipt_digest: str, sequence: int
) -> dict[str, Any]:
    _require_schema(payload)
    sequence = _require_sequence(sequence, "sequence")
    receipt_digest = require_digest(execution_receipt_digest, "execution_receipt_digest")
    validated_at = payload.get("validated_at")
    if not isinstance(validated_at, str):
        raise ContractError("validation payload requires validated_at")
    timestamp = parse_utc(validated_at, "validated_at")
    identifier = (
        f"FPRV-{timestamp.strftime('%Y%m%d')}-{receipt_digest[7:19]}-{sequence:02d}"
    )
    finalized = _replace_pending(payload, "validation_id", identifier)
    execution_id = finalized.get("execution_id")
    if not isinstance(execution_id, str) or EXECUTION_ID_RE.fullmatch(execution_id) is None:
        raise ContractError("validation payload execution_id must be an FPRE ID")
    if finalized.get("result") not in {"passed", "failed"}:
        raise ContractError("validation payload result must be passed or failed")
    validator_results = finalized.get("validator_results")
    if not isinstance(validator_results, list):
        raise ContractError("validation payload requires validator_results")
    seen_validators: set[str] = set()
    for index, item in enumerate(validator_results):
        if not isinstance(item, dict):
            raise ContractError(f"validator_results[{index}] must be an object")
        validator_id = item.get("id")
        if not isinstance(validator_id, str) or VALIDATOR_ID_RE.fullmatch(validator_id) is None:
            raise ContractError(f"validator_results[{index}].id is invalid")
        if validator_id in seen_validators:
            raise ContractError(f"duplicate validator result: {validator_id}")
        seen_validators.add(validator_id)
        if item.get("result") not in {"passed", "failed"}:
            raise ContractError(f"validator_results[{index}].result is invalid")
        if not isinstance(item.get("evidence"), str) or not item["evidence"]:
            raise ContractError(f"validator_results[{index}].evidence is required")
    live_hashes = finalized.get("live_hashes")
    if not isinstance(live_hashes, list):
        raise ContractError("validation payload requires live_hashes")
    seen_paths: set[str] = set()
    for index, item in enumerate(live_hashes):
        if not isinstance(item, dict):
            raise ContractError(f"live_hashes[{index}] must be an object")
        path = item.get("path")
        if not _is_safe_relative_path(path):
            raise ContractError(f"live_hashes[{index}].path must be vault relative")
        if path in seen_paths:
            raise ContractError(f"duplicate live hash path: {path}")
        seen_paths.add(path)
        if not _is_digest_or(item.get("sha256")):
            raise ContractError(f"live_hashes[{index}].sha256 is invalid")
    validation_digest = digest_payload(finalized)
    return {
        "record_kind": "validation",
        "record_id": identifier,
        "record_digest": validation_digest,
        "execution_receipt_digest": receipt_digest,
        "sequence": sequence,
        "payload": finalized,
    }


def verify_envelope(envelope: dict[str, Any]) -> None:
    kind = envelope.get("record_kind")
    payload = envelope.get("payload")
    if not isinstance(payload, dict):
        raise ContractError("record envelope payload must be an object")
    if kind == "proposal":
        rebuilt = build_proposal(payload, str(envelope.get("created_date", "")))
    elif kind == "decision":
        match = DECISION_ID_RE.fullmatch(str(envelope.get("record_id", "")))
        if match is None:
            raise ContractError("decision envelope record_id is invalid")
        draft = deepcopy(payload)
        draft["decision_id"] = "PENDING"
        rebuilt = build_decision(draft, match.group(2))
    elif kind == "execution":
        match = EXECUTION_ID_RE.fullmatch(str(envelope.get("record_id", "")))
        if match is None:
            raise ContractError("execution envelope record_id is invalid")
        attempt = envelope.get("attempt")
        if isinstance(attempt, bool) or not isinstance(attempt, int):
            raise ContractError("execution envelope attempt must be a JSON integer")
        draft = deepcopy(payload)
        draft["execution_id"] = "PENDING"
        rebuilt = build_execution(draft, attempt)
    elif kind == "validation":
        sequence = envelope.get("sequence")
        if isinstance(sequence, bool) or not isinstance(sequence, int):
            raise ContractError("validation envelope sequence must be a JSON integer")
        draft = deepcopy(payload)
        draft["validation_id"] = "PENDING"
        rebuilt = build_validation(
            draft,
            str(envelope.get("execution_receipt_digest", "")),
            sequence,
        )
    else:
        raise ContractError(f"unsupported record_kind: {kind!r}")
    for key, expected in rebuilt.items():
        if envelope.get(key) != expected:
            raise ContractError(f"record envelope field {key} does not verify")
