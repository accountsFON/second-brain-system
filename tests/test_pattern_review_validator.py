from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = (
    REPO_ROOT
    / "template"
    / "resources"
    / "learning-library"
    / "validate-pattern-review.py"
)
CORE_PATH = VALIDATOR_PATH.with_name("pattern_review_core.py")
RECORD_CLI_PATH = VALIDATOR_PATH.with_name("pattern-review-records.py")
SPEC = importlib.util.spec_from_file_location("pattern_review_validator", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
VALIDATOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = VALIDATOR
SPEC.loader.exec_module(VALIDATOR)
CORE_SPEC = importlib.util.spec_from_file_location("pattern_review_core_test", CORE_PATH)
assert CORE_SPEC is not None and CORE_SPEC.loader is not None
CORE = importlib.util.module_from_spec(CORE_SPEC)
sys.modules[CORE_SPEC.name] = CORE
CORE_SPEC.loader.exec_module(CORE)


def write_record(
    path: Path, frontmatter: dict[str, str], payload: dict[str, Any], title: str
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    yaml = "\n".join(f"{key}: {value}" for key, value in frontmatter.items())
    body = json.dumps(payload, indent=2, ensure_ascii=False)
    path.write_text(
        f"---\n{yaml}\n---\n\n# {title}\n\n```json\n{body}\n```\n",
        encoding="utf-8",
    )


def build_valid_vault(root: Path, *, blocked_first: bool = False) -> dict[str, Any]:
    library = root / "resources" / "learning-library"
    exact_change = "Complete new content."
    after_hash = VALIDATOR.digest_text(exact_change)
    candidate_id = "PR-2026-01-15-01"
    candidate_fingerprint = "example::scope::mechanism::outcome"
    candidate_path = library / "candidates" / "2026-01-15-pattern-review.md"
    candidate_path.parent.mkdir(parents=True, exist_ok=True)
    candidate_path.write_text(
        "---\n"
        "name: pattern-review-2026-01-15\n"
        "description: Test candidate report.\n"
        "type: learning-candidate-report\n"
        "schema-version: 2\n"
        "updated: 2026-01-15\n"
        "status: candidate\n"
        "canonical: false\n"
        "authority: none\n"
        "---\n\n"
        f"## Candidate {candidate_id}: Example candidate\n\n"
        f"**Fingerprint:** `{candidate_fingerprint}`\n",
        encoding="utf-8",
    )
    proposal_payload = {
        "schema_version": 2,
        "revision_of": "none",
        "source_candidates": [
            {
                "id": candidate_id,
                "path": f"resources/learning-library/candidates/2026-01-15-pattern-review.md#{candidate_id}",
                "fingerprint": candidate_fingerprint,
            }
        ],
        "scope": "One bounded example scope.",
        "operations": [
            {
                "action": "create",
                "path": "skills/example.md",
                "before_sha256": "absent",
                "after_sha256": after_hash,
                "change_format": "full-content",
                "exact_change": exact_change,
            }
        ],
        "prohibited_expansion": ["Do not edit any other file."],
        "validation": ["schema-check", "target-hash-readback"],
        "failure_behavior": "Block before a write when a precondition fails.",
    }
    proposal_digest = VALIDATOR.digest_payload(proposal_payload)
    proposal_id = f"FPRP-20260115-{proposal_digest[7:19]}"
    proposal_path = library / "proposals" / "2026-01" / f"{proposal_id}.md"
    write_record(
        proposal_path,
        {
            "name": "2026-01-15-learning-proposal",
            "description": "Test proposal.",
            "type": "learning-proposal",
            "schema-version": "2",
            "status": "proposed",
            "authority": "none",
            "proposal-id": proposal_id,
            "proposal-digest": proposal_digest,
            "created-by": "Test Reviewer",
            "created-date": "2026-01-15",
            "updated": "2026-01-15",
        },
        proposal_payload,
        "Exact Learning Proposal",
    )

    decision_id = "FPRD-20260116T120000Z-1234abcd"
    decision_payload = {
        "schema_version": 2,
        "decision_id": decision_id,
        "proposal_id": proposal_id,
        "proposal_digest": proposal_digest,
        "previous_event_id": "none",
        "disposition": "approve-exact",
        "scope_lock": "One bounded example scope.",
        "constraints": ["Apply only the enumerated operation."],
        "prohibited_expansion": ["Do not edit any other file."],
        "decided_by": "Test Reviewer",
        "decided_at": "2026-01-16T12:00:00Z",
        "approval_source": "Test approval receipt.",
        "expires_date": "2026-02-15",
        "replacement_proposal": "none",
    }
    decision_digest = VALIDATOR.digest_payload(decision_payload)
    auth_digest = VALIDATOR.authorization_digest(proposal_digest, decision_digest)
    decision_path = library / "decisions" / "2026-01" / f"{decision_id}.md"
    decision_frontmatter = {
        "name": "2026-01-16-learning-decision",
        "description": "Test decision.",
        "type": "learning-decision",
        "schema-version": "2",
        "status": "recorded",
        "authority": "human-decision",
        "execution-authority": "exact",
        "decision-id": decision_id,
        "decision-digest": decision_digest,
        "authorization-digest": auth_digest,
        "proposal-id": proposal_id,
        "proposal-digest": proposal_digest,
        "previous-event-id": "none",
        "disposition": "approve-exact",
        "decided-by": "Test Reviewer",
        "decided-date": "2026-01-16",
        "approval-source": "Test approval receipt.",
        "updated": "2026-01-16",
    }
    write_record(
        decision_path,
        decision_frontmatter,
        decision_payload,
        "Learning Decision",
    )

    attempt = 1
    if blocked_first:
        blocked_id = f"FPRE-20260116-{auth_digest[7:19]}-01"
        blocked_payload = {
            "schema_version": 2,
            "execution_id": blocked_id,
            "proposal_id": proposal_id,
            "proposal_digest": proposal_digest,
            "decision_id": decision_id,
            "decision_digest": decision_digest,
            "authorization_digest": auth_digest,
            "result": "blocked",
            "approval_consumed": False,
            "started_at": "2026-01-16T12:02:00Z",
            "completed_at": "2026-01-16T12:02:01Z",
            "task_receipt": {
                "system": "test coordinator",
                "task_id": "test-blocked-1",
                "run_ids": [],
            },
            "changed_paths": [],
        }
        blocked_digest = VALIDATOR.digest_payload(blocked_payload)
        write_record(
            library / "executions" / "2026-01" / f"{blocked_id}.md",
            {
                "name": "2026-01-16-learning-execution",
                "description": "Blocked test execution.",
                "type": "learning-execution",
                "schema-version": "2",
                "status": "blocked",
                "authority": "none",
                "execution-id": blocked_id,
                "proposal-id": proposal_id,
                "proposal-digest": proposal_digest,
                "decision-id": decision_id,
                "decision-digest": decision_digest,
                "authorization-digest": auth_digest,
                "receipt-digest": blocked_digest,
                "executed-date": "2026-01-16",
                "updated": "2026-01-16",
            },
            blocked_payload,
            "Learning Execution Receipt",
        )
        attempt = 2

    execution_id = f"FPRE-20260116-{auth_digest[7:19]}-{attempt:02d}"
    execution_payload = {
        "schema_version": 2,
        "execution_id": execution_id,
        "proposal_id": proposal_id,
        "proposal_digest": proposal_digest,
        "decision_id": decision_id,
        "decision_digest": decision_digest,
        "authorization_digest": auth_digest,
        "result": "executed",
        "approval_consumed": True,
        "started_at": "2026-01-16T12:05:00Z",
        "completed_at": "2026-01-16T12:05:30Z",
        "task_receipt": {
            "system": "test coordinator",
            "task_id": "test-execution-1",
            "run_ids": ["run-1"],
        },
        "changed_paths": [
            {
                "path": "skills/example.md",
                "before_sha256": "absent",
                "expected_after_sha256": after_hash,
                "observed_after_sha256": after_hash,
            }
        ],
    }
    receipt_digest = VALIDATOR.digest_payload(execution_payload)
    execution_path = library / "executions" / "2026-01" / f"{execution_id}.md"
    write_record(
        execution_path,
        {
            "name": "2026-01-16-learning-execution",
            "description": "Test execution.",
            "type": "learning-execution",
            "schema-version": "2",
            "status": "executed",
            "authority": "none",
            "execution-id": execution_id,
            "proposal-id": proposal_id,
            "proposal-digest": proposal_digest,
            "decision-id": decision_id,
            "decision-digest": decision_digest,
            "authorization-digest": auth_digest,
            "receipt-digest": receipt_digest,
            "executed-date": "2026-01-16",
            "updated": "2026-01-16",
        },
        execution_payload,
        "Learning Execution Receipt",
    )

    validation_id = f"FPRV-20260116-{receipt_digest[7:19]}-01"
    validation_payload = {
        "schema_version": 2,
        "validation_id": validation_id,
        "execution_id": execution_id,
        "result": "passed",
        "validated_at": "2026-01-16T12:06:00Z",
        "validator_results": [
            {"id": "schema-check", "result": "passed", "evidence": "Schema passed."},
            {
                "id": "target-hash-readback",
                "result": "passed",
                "evidence": "Target hash matched.",
            },
        ],
        "live_hashes": [{"path": "skills/example.md", "sha256": after_hash}],
    }
    validation_digest = VALIDATOR.digest_payload(validation_payload)
    validation_path = library / "validations" / "2026-01" / f"{validation_id}.md"
    write_record(
        validation_path,
        {
            "name": "2026-01-16-learning-validation",
            "description": "Test validation.",
            "type": "learning-validation",
            "schema-version": "2",
            "status": "passed",
            "authority": "none",
            "validation-id": validation_id,
            "execution-id": execution_id,
            "validation-digest": validation_digest,
            "validated-by": "Test Validator",
            "validation-date": "2026-01-16",
            "updated": "2026-01-16",
        },
        validation_payload,
        "Learning Validation Receipt",
    )
    live_target = root / "skills" / "example.md"
    live_target.parent.mkdir(parents=True, exist_ok=True)
    live_target.write_bytes(exact_change.encode("utf-8"))
    return {
        "library": library,
        "candidate_id": candidate_id,
        "candidate_path": candidate_path,
        "candidate_fingerprint": candidate_fingerprint,
        "proposal_id": proposal_id,
        "proposal_digest": proposal_digest,
        "proposal_payload": proposal_payload,
        "proposal_path": proposal_path,
        "decision_id": decision_id,
        "decision_digest": decision_digest,
        "decision_payload": decision_payload,
        "decision_frontmatter": decision_frontmatter,
        "decision_path": decision_path,
        "authorization_digest": auth_digest,
        "execution_id": execution_id,
        "execution_payload": execution_payload,
        "execution_path": execution_path,
        "receipt_digest": receipt_digest,
        "validation_id": validation_id,
        "validation_payload": validation_payload,
        "validation_path": validation_path,
        "after_hash": after_hash,
        "live_target": live_target,
    }


def rewrite_execution(
    context: dict[str, Any], payload: dict[str, Any]
) -> Path:
    old_path = context["execution_path"]
    record = VALIDATOR.load_record("execution", old_path)
    attempt = int(context["execution_id"].rsplit("-", 1)[1])
    completed_date = payload["completed_at"][:10]
    compact_date = completed_date.replace("-", "")
    execution_id = (
        f"FPRE-{compact_date}-{context['authorization_digest'][7:19]}-{attempt:02d}"
    )
    payload = dict(payload)
    payload["execution_id"] = execution_id
    receipt_digest = VALIDATOR.digest_payload(payload)
    frontmatter = dict(record.frontmatter)
    frontmatter["execution-id"] = execution_id
    frontmatter["status"] = payload["result"]
    frontmatter["receipt-digest"] = receipt_digest
    frontmatter["executed-date"] = completed_date
    for front_key, payload_key in (
        ("proposal-id", "proposal_id"),
        ("proposal-digest", "proposal_digest"),
        ("decision-id", "decision_id"),
        ("decision-digest", "decision_digest"),
        ("authorization-digest", "authorization_digest"),
    ):
        frontmatter[front_key] = payload[payload_key]
    new_path = old_path.parent.parent / completed_date[:7] / f"{execution_id}.md"
    old_path.unlink()
    write_record(
        new_path,
        frontmatter,
        payload,
        "Learning Execution Receipt",
    )
    validation_path = context.get("validation_path")
    if isinstance(validation_path, Path) and validation_path.exists():
        validation_path.unlink()
    context["execution_path"] = new_path
    context["execution_id"] = execution_id
    context["execution_payload"] = payload
    context["receipt_digest"] = receipt_digest
    return new_path


def write_decision_event(
    context: dict[str, Any],
    *,
    decision_id: str,
    previous_event_id: str,
    disposition: str,
    replacement_proposal: str = "none",
    expires_date: str = "2026-02-15",
) -> Path:
    timestamp = decision_id[len("FPRD-") : len("FPRD-") + 16]
    decided_at = (
        f"{timestamp[0:4]}-{timestamp[4:6]}-{timestamp[6:8]}T"
        f"{timestamp[9:11]}:{timestamp[11:13]}:{timestamp[13:15]}Z"
    )
    payload = {
        "schema_version": 2,
        "decision_id": decision_id,
        "proposal_id": context["proposal_id"],
        "proposal_digest": context["proposal_digest"],
        "previous_event_id": previous_event_id,
        "disposition": disposition,
        "scope_lock": "One bounded example scope.",
        "constraints": ["Apply only the enumerated operation."],
        "prohibited_expansion": ["Do not edit any other file."],
        "decided_by": "Test Reviewer",
        "decided_at": decided_at,
        "approval_source": "Test approval receipt.",
        "expires_date": expires_date,
        "replacement_proposal": replacement_proposal,
    }
    decision_digest = VALIDATOR.digest_payload(payload)
    if disposition == "approve-exact":
        authority = "exact"
        auth_digest = VALIDATOR.authorization_digest(
            context["proposal_digest"], decision_digest
        )
    else:
        authority = "none"
        auth_digest = "none"
    date_value = decided_at[:10]
    path = (
        context["library"]
        / "decisions"
        / date_value[:7]
        / f"{decision_id}.md"
    )
    write_record(
        path,
        {
            "name": f"{date_value}-learning-decision",
            "description": "Test decision event.",
            "type": "learning-decision",
            "schema-version": "2",
            "status": "recorded",
            "authority": "human-decision",
            "execution-authority": authority,
            "decision-id": decision_id,
            "decision-digest": decision_digest,
            "authorization-digest": auth_digest,
            "proposal-id": context["proposal_id"],
            "proposal-digest": context["proposal_digest"],
            "previous-event-id": previous_event_id,
            "disposition": disposition,
            "decided-by": "Test Reviewer",
            "decided-date": date_value,
            "approval-source": "Test approval receipt.",
            "updated": date_value,
        },
        payload,
        "Learning Decision",
    )
    return path


def replace_proposal(
    context: dict[str, Any], payload: dict[str, Any], *, created_date: str = "2026-01-15"
) -> Path:
    old_path = context["proposal_path"]
    old_record = VALIDATOR.load_record("proposal", old_path)
    envelope = CORE.build_proposal(payload, created_date)
    frontmatter = dict(old_record.frontmatter)
    frontmatter["proposal-id"] = envelope["record_id"]
    frontmatter["proposal-digest"] = envelope["record_digest"]
    frontmatter["created-date"] = created_date
    old_path.unlink()
    new_path = (
        context["library"]
        / "proposals"
        / created_date[:7]
        / f"{envelope['record_id']}.md"
    )
    write_record(new_path, frontmatter, payload, "Exact Learning Proposal")
    context["proposal_path"] = new_path
    context["proposal_id"] = envelope["record_id"]
    context["proposal_digest"] = envelope["record_digest"]
    return new_path


def append_validated_revision(
    context: dict[str, Any],
    *,
    exact_change: str = "Second validated content.",
    before_sha256: str | None = None,
) -> dict[str, Any]:
    after_sha256 = VALIDATOR.digest_text(exact_change)
    proposal_payload = json.loads(json.dumps(context["proposal_payload"]))
    proposal_payload["revision_of"] = context["proposal_id"]
    proposal_payload["operations"] = [
        {
            "action": "replace",
            "path": "skills/example.md",
            "before_sha256": before_sha256 or context["after_hash"],
            "after_sha256": after_sha256,
            "change_format": "full-content",
            "exact_change": exact_change,
        }
    ]
    proposal = CORE.build_proposal(proposal_payload, "2026-01-17")
    proposal_path = (
        context["library"]
        / "proposals"
        / "2026-01"
        / f"{proposal['record_id']}.md"
    )
    write_record(
        proposal_path,
        {
            "name": "2026-01-17-learning-proposal",
            "description": "Second validated proposal.",
            "type": "learning-proposal",
            "schema-version": "2",
            "status": "proposed",
            "authority": "none",
            "proposal-id": proposal["record_id"],
            "proposal-digest": proposal["record_digest"],
            "created-by": "Test Reviewer",
            "created-date": "2026-01-17",
            "updated": "2026-01-17",
        },
        proposal_payload,
        "Exact Learning Proposal",
    )

    decision_payload = {
        "schema_version": 2,
        "decision_id": "PENDING",
        "proposal_id": proposal["record_id"],
        "proposal_digest": proposal["record_digest"],
        "previous_event_id": "none",
        "disposition": "approve-exact",
        "scope_lock": "Second bounded example scope.",
        "constraints": ["Apply only the second enumerated operation."],
        "prohibited_expansion": ["Do not edit any other file."],
        "decided_by": "Test Reviewer",
        "decided_at": "2026-01-17T12:00:00Z",
        "approval_source": "Second test approval receipt.",
        "expires_date": "2026-02-17",
        "replacement_proposal": "none",
    }
    decision = CORE.build_decision(decision_payload, "5678abcd")
    decision_path = (
        context["library"]
        / "decisions"
        / "2026-01"
        / f"{decision['record_id']}.md"
    )
    write_record(
        decision_path,
        {
            "name": "2026-01-17-learning-decision",
            "description": "Second test decision.",
            "type": "learning-decision",
            "schema-version": "2",
            "status": "recorded",
            "authority": "human-decision",
            "execution-authority": "exact",
            "decision-id": decision["record_id"],
            "decision-digest": decision["record_digest"],
            "authorization-digest": decision["authorization_digest"],
            "proposal-id": proposal["record_id"],
            "proposal-digest": proposal["record_digest"],
            "previous-event-id": "none",
            "disposition": "approve-exact",
            "decided-by": "Test Reviewer",
            "decided-date": "2026-01-17",
            "approval-source": "Second test approval receipt.",
            "updated": "2026-01-17",
        },
        decision["payload"],
        "Learning Decision",
    )

    execution_payload = {
        "schema_version": 2,
        "execution_id": "PENDING",
        "proposal_id": proposal["record_id"],
        "proposal_digest": proposal["record_digest"],
        "decision_id": decision["record_id"],
        "decision_digest": decision["record_digest"],
        "authorization_digest": decision["authorization_digest"],
        "result": "executed",
        "approval_consumed": True,
        "started_at": "2026-01-17T12:05:00Z",
        "completed_at": "2026-01-17T12:05:30Z",
        "task_receipt": {
            "system": "test coordinator",
            "task_id": "test-execution-2",
            "run_ids": ["run-2"],
        },
        "changed_paths": [
            {
                "path": "skills/example.md",
                "before_sha256": proposal_payload["operations"][0]["before_sha256"],
                "expected_after_sha256": after_sha256,
                "observed_after_sha256": after_sha256,
            }
        ],
    }
    execution = CORE.build_execution(execution_payload, 1)
    execution_path = (
        context["library"]
        / "executions"
        / "2026-01"
        / f"{execution['record_id']}.md"
    )
    write_record(
        execution_path,
        {
            "name": "2026-01-17-learning-execution",
            "description": "Second test execution.",
            "type": "learning-execution",
            "schema-version": "2",
            "status": "executed",
            "authority": "none",
            "execution-id": execution["record_id"],
            "proposal-id": proposal["record_id"],
            "proposal-digest": proposal["record_digest"],
            "decision-id": decision["record_id"],
            "decision-digest": decision["record_digest"],
            "authorization-digest": decision["authorization_digest"],
            "receipt-digest": execution["record_digest"],
            "executed-date": "2026-01-17",
            "updated": "2026-01-17",
        },
        execution["payload"],
        "Learning Execution Receipt",
    )

    validation_payload = {
        "schema_version": 2,
        "validation_id": "PENDING",
        "execution_id": execution["record_id"],
        "result": "passed",
        "validated_at": "2026-01-17T12:06:00Z",
        "validator_results": [
            {"id": "schema-check", "result": "passed", "evidence": "Schema passed."},
            {
                "id": "target-hash-readback",
                "result": "passed",
                "evidence": "Target hash matched.",
            },
        ],
        "live_hashes": [{"path": "skills/example.md", "sha256": after_sha256}],
    }
    validation = CORE.build_validation(
        validation_payload, execution["record_digest"], 1
    )
    validation_path = (
        context["library"]
        / "validations"
        / "2026-01"
        / f"{validation['record_id']}.md"
    )
    write_record(
        validation_path,
        {
            "name": "2026-01-17-learning-validation",
            "description": "Second test validation.",
            "type": "learning-validation",
            "schema-version": "2",
            "status": "passed",
            "authority": "none",
            "validation-id": validation["record_id"],
            "execution-id": execution["record_id"],
            "validation-digest": validation["record_digest"],
            "validated-by": "Test Validator",
            "validation-date": "2026-01-17",
            "updated": "2026-01-17",
        },
        validation["payload"],
        "Learning Validation Receipt",
    )
    context["live_target"].write_bytes(exact_change.encode("utf-8"))
    return {
        "proposal": proposal,
        "proposal_path": proposal_path,
        "decision": decision,
        "decision_path": decision_path,
        "execution": execution,
        "execution_path": execution_path,
        "validation": validation,
        "validation_path": validation_path,
        "after_hash": after_sha256,
    }


class PatternReviewValidatorTests(unittest.TestCase):
    def test_public_template_contract_is_complete(self) -> None:
        report = VALIDATOR.validate_template_surfaces(REPO_ROOT)
        self.assertEqual([], report.errors)

    def test_complete_record_chain_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build_valid_vault(root)
            report = VALIDATOR.validate_vault(root)
            self.assertEqual([], report.errors)
            self.assertEqual([], report.warnings)

    def test_executed_receipt_requires_passing_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            context["validation_path"].unlink()
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any(
                    "executed receipt requires a passing validation receipt" in error
                    for error in report.errors
                )
            )

    def test_execution_run_ids_require_nonempty_strings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            record = VALIDATOR.load_record("execution", context["execution_path"])
            payload = json.loads(json.dumps(context["execution_payload"]))
            payload["task_receipt"]["run_ids"] = [1]
            frontmatter = dict(record.frontmatter)
            frontmatter["receipt-digest"] = VALIDATOR.digest_payload(payload)
            write_record(
                context["execution_path"],
                frontmatter,
                payload,
                "Learning Execution Receipt",
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any(
                    "run_ids must contain nonempty strings" in error
                    for error in report.errors
                )
            )

    def test_revision_of_must_resolve_to_an_existing_proposal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            payload = json.loads(json.dumps(context["proposal_payload"]))
            payload["revision_of"] = "FPRP-20260101-000000000000"
            payload["operations"][0]["exact_change"] = "Unlinked revision content."
            payload["operations"][0]["after_sha256"] = VALIDATOR.digest_text(
                "Unlinked revision content."
            )
            proposal = CORE.build_proposal(payload, "2026-01-17")
            proposal_path = (
                context["library"]
                / "proposals"
                / "2026-01"
                / f"{proposal['record_id']}.md"
            )
            write_record(
                proposal_path,
                {
                    "name": "2026-01-17-learning-proposal",
                    "description": "Unlinked revision proposal.",
                    "type": "learning-proposal",
                    "schema-version": "2",
                    "status": "proposed",
                    "authority": "none",
                    "proposal-id": proposal["record_id"],
                    "proposal-digest": proposal["record_digest"],
                    "created-by": "Test Reviewer",
                    "created-date": "2026-01-17",
                    "updated": "2026-01-17",
                },
                proposal["payload"],
                "Exact Learning Proposal",
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any(
                    "revision_of proposal does not exist" in error
                    for error in report.errors
                )
            )

    def test_proposal_source_candidate_must_resolve_to_report_record(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            context["candidate_path"].unlink()
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("source candidate does not resolve" in error for error in report.errors)
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            text = context["candidate_path"].read_text(encoding="utf-8")
            context["candidate_path"].write_text(
                text.replace(
                    context["candidate_fingerprint"],
                    "different::candidate::fingerprint",
                ),
                encoding="utf-8",
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("fingerprint does not match" in error for error in report.errors)
            )

    def test_validation_cannot_precede_execution_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            record = VALIDATOR.load_record("validation", context["validation_path"])
            payload = json.loads(json.dumps(context["validation_payload"]))
            payload["validated_at"] = "2026-01-16T12:05:00Z"
            digest = VALIDATOR.digest_payload(payload)
            frontmatter = dict(record.frontmatter)
            frontmatter["validation-digest"] = digest
            write_record(
                context["validation_path"],
                frontmatter,
                payload,
                "Learning Validation Receipt",
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("validation cannot precede execution completion" in error for error in report.errors)
            )

    def test_passing_validation_hashes_actual_live_target_bytes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            context["live_target"].write_bytes(b"Receipt says valid, live bytes differ.")
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("current live vault target bytes" in error for error in report.errors)
            )

    def test_live_hash_check_uses_latest_successful_path_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            append_validated_revision(context)
            report = VALIDATOR.validate_vault(root)
            self.assertEqual([], report.errors)
            self.assertEqual([], report.warnings)

    def test_validated_path_history_must_be_continuous(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            append_validated_revision(
                context,
                before_sha256=VALIDATOR.digest_text("Unrelated prior state."),
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("validated path history is discontinuous" in error for error in report.errors)
            )

    def test_record_files_reject_symlink_components_directly_and_in_collection(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            original = context["proposal_path"]
            real_record = original.with_name("real-proposal-record.md")
            original.rename(real_record)
            original.symlink_to(real_record.name)
            record = VALIDATOR.load_record("proposal", original)
            with self.assertRaisesRegex(VALIDATOR.ContractError, "symlink component"):
                VALIDATOR.validate_proposal(record)
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("record path contains a symlink component" in error for error in report.errors)
            )

        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "vault"
            context = build_valid_vault(root)
            outside = base / context["proposal_path"].name
            outside.write_bytes(context["proposal_path"].read_bytes())
            context["proposal_path"].unlink()
            context["proposal_path"].symlink_to(outside)
            record = VALIDATOR.load_record("proposal", context["proposal_path"])
            with self.assertRaisesRegex(VALIDATOR.ContractError, "symlink component"):
                VALIDATOR.validate_proposal(record)
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("record path contains a symlink component" in error for error in report.errors)
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            month = context["proposal_path"].parent
            real_month = month.with_name("real-2026-01")
            month.rename(real_month)
            month.symlink_to(real_month.name, target_is_directory=True)
            logical_record = month / context["proposal_path"].name
            record = VALIDATOR.load_record("proposal", logical_record)
            with self.assertRaisesRegex(VALIDATOR.ContractError, "symlink component"):
                VALIDATOR.validate_proposal(record)
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("record path contains a symlink component" in error for error in report.errors)
            )

    def test_candidate_like_malformed_heading_is_reported(self) -> None:
        malformed_headings = (
            "## Candidate {candidate_id} Example candidate",
            "### Candidate {candidate_id}: Example candidate",
            " ## Candidate {candidate_id}: Example candidate",
            "##Candidate {candidate_id}: Example candidate",
        )
        for malformed_heading in malformed_headings:
            with self.subTest(heading=malformed_heading):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    context = build_valid_vault(root)
                    text = context["candidate_path"].read_text(encoding="utf-8")
                    context["candidate_path"].write_text(
                        text.replace(
                            f"## Candidate {context['candidate_id']}: Example candidate",
                            malformed_heading.format(candidate_id=context["candidate_id"]),
                        ),
                        encoding="utf-8",
                    )
                    report = VALIDATOR.validate_vault(root)
                    self.assertTrue(
                        any("malformed candidate heading" in error for error in report.errors)
                    )

    def test_execution_proposal_id_must_match_decision_even_with_same_digest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            alternate = CORE.build_proposal(context["proposal_payload"], "2026-01-14")
            original = VALIDATOR.load_record("proposal", context["proposal_path"])
            alternate_path = (
                context["library"]
                / "proposals"
                / "2026-01"
                / f"{alternate['record_id']}.md"
            )
            alternate_frontmatter = dict(original.frontmatter)
            alternate_frontmatter["proposal-id"] = alternate["record_id"]
            alternate_frontmatter["proposal-digest"] = alternate["record_digest"]
            alternate_frontmatter["created-date"] = "2026-01-14"
            write_record(
                alternate_path,
                alternate_frontmatter,
                context["proposal_payload"],
                "Exact Learning Proposal",
            )
            payload = json.loads(json.dumps(context["execution_payload"]))
            payload["proposal_id"] = alternate["record_id"]
            rewrite_execution(context, payload)
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any(
                    "execution proposal ID does not exactly match decision proposal ID" in error
                    for error in report.errors
                )
            )

    def test_blocked_attempt_can_precede_one_consumed_attempt(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            build_valid_vault(root, blocked_first=True)
            report = VALIDATOR.validate_vault(root)
            self.assertEqual([], report.errors)
            self.assertEqual([], report.warnings)

    def test_tampered_proposal_digest_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            path = context["proposal_path"]
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "Complete new content.", "Tampered content."
                ),
                encoding="utf-8",
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("proposal-digest does not match" in error for error in report.errors)
            )

    def test_candidate_id_cannot_be_approved(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            payload = dict(context["decision_payload"])
            payload["proposal_id"] = "PR-2026-01-15-01"
            decision_digest = VALIDATOR.digest_payload(payload)
            frontmatter = dict(context["decision_frontmatter"])
            frontmatter["proposal-id"] = "PR-2026-01-15-01"
            frontmatter["decision-digest"] = decision_digest
            frontmatter["authorization-digest"] = VALIDATOR.authorization_digest(
                context["proposal_digest"], decision_digest
            )
            write_record(
                context["decision_path"],
                frontmatter,
                payload,
                "Learning Decision",
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("must be an FPRP ID, not a candidate ID" in error for error in report.errors)
            )

    def test_second_consumed_execution_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            payload = dict(context["execution_payload"])
            execution_id = (
                f"FPRE-20260116-{context['authorization_digest'][7:19]}-02"
            )
            payload["execution_id"] = execution_id
            payload["started_at"] = "2026-01-16T12:07:00Z"
            payload["completed_at"] = "2026-01-16T12:07:30Z"
            payload["task_receipt"] = {
                "system": "test coordinator",
                "task_id": "test-execution-2",
                "run_ids": ["run-2"],
            }
            receipt_digest = VALIDATOR.digest_payload(payload)
            write_record(
                context["library"]
                / "executions"
                / "2026-01"
                / f"{execution_id}.md",
                {
                    "name": "2026-01-16-learning-execution",
                    "description": "Second consumed execution.",
                    "type": "learning-execution",
                    "schema-version": "2",
                    "status": "executed",
                    "authority": "none",
                    "execution-id": execution_id,
                    "proposal-id": context["proposal_id"],
                    "proposal-digest": context["proposal_digest"],
                    "decision-id": context["decision_id"],
                    "decision-digest": context["decision_digest"],
                    "authorization-digest": context["authorization_digest"],
                    "receipt-digest": receipt_digest,
                    "executed-date": "2026-01-16",
                    "updated": "2026-01-16",
                },
                payload,
                "Learning Execution Receipt",
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("more than one consumed execution" in error for error in report.errors)
            )

    def test_validation_id_must_bind_execution_receipt_digest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            context["validation_path"].unlink()
            invalid_id = "FPRV-20260116-deadbeefcafe-01"
            payload = dict(context["validation_payload"])
            payload["validation_id"] = invalid_id
            digest = VALIDATOR.digest_payload(payload)
            write_record(
                context["library"]
                / "validations"
                / "2026-01"
                / f"{invalid_id}.md",
                {
                    "name": "2026-01-16-learning-validation",
                    "description": "Invalid validation binding.",
                    "type": "learning-validation",
                    "schema-version": "2",
                    "status": "passed",
                    "authority": "none",
                    "validation-id": invalid_id,
                    "execution-id": context["execution_id"],
                    "validation-digest": digest,
                    "validated-by": "Test Validator",
                    "validation-date": "2026-01-16",
                    "updated": "2026-01-16",
                },
                payload,
                "Learning Validation Receipt",
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("does not match execution receipt digest" in error for error in report.errors)
            )

    def test_proposal_builder_enforces_exact_full_content_hash(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = build_valid_vault(Path(directory))
            bad_hash = json.loads(json.dumps(context["proposal_payload"]))
            bad_hash["operations"][0]["exact_change"] = "Different exact bytes."
            with self.assertRaisesRegex(CORE.ContractError, "does not hash exact_change"):
                CORE.build_proposal(bad_hash, "2026-01-15")

            patch_change = json.loads(json.dumps(context["proposal_payload"]))
            patch_change["operations"][0]["change_format"] = "unified-diff"
            with self.assertRaisesRegex(CORE.ContractError, "full-content"):
                CORE.build_proposal(patch_change, "2026-01-15")

    def test_proposal_action_controls_before_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = build_valid_vault(Path(directory))
            create_with_digest = json.loads(json.dumps(context["proposal_payload"]))
            create_with_digest["operations"][0]["before_sha256"] = context["after_hash"]
            with self.assertRaisesRegex(CORE.ContractError, "create requires"):
                CORE.build_proposal(create_with_digest, "2026-01-15")

            replace_absent = json.loads(json.dumps(context["proposal_payload"]))
            replace_absent["operations"][0]["action"] = "replace"
            with self.assertRaisesRegex(CORE.ContractError, "replace requires"):
                CORE.build_proposal(replace_absent, "2026-01-15")

            invalid_action = json.loads(json.dumps(context["proposal_payload"]))
            invalid_action["operations"][0]["action"] = "delete"
            with self.assertRaisesRegex(CORE.ContractError, "create or replace"):
                CORE.build_proposal(invalid_action, "2026-01-15")

    def test_execution_id_date_comes_from_completion(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = build_valid_vault(Path(directory))
            payload = json.loads(json.dumps(context["execution_payload"]))
            payload["execution_id"] = "PENDING"
            payload["started_at"] = "2026-01-16T23:59:59Z"
            payload["completed_at"] = "2026-01-17T00:00:01Z"
            envelope = CORE.build_execution(payload, 1)
            self.assertTrue(envelope["record_id"].startswith("FPRE-20260117-"))

    def test_execution_builder_requires_complete_unique_changed_path_fields(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = build_valid_vault(Path(directory))
            missing = json.loads(json.dumps(context["execution_payload"]))
            missing["execution_id"] = "PENDING"
            del missing["changed_paths"][0]["expected_after_sha256"]
            with self.assertRaisesRegex(CORE.ContractError, "expected_after_sha256"):
                CORE.build_execution(missing, 1)

            duplicate = json.loads(json.dumps(context["execution_payload"]))
            duplicate["execution_id"] = "PENDING"
            duplicate["changed_paths"].append(dict(duplicate["changed_paths"][0]))
            with self.assertRaisesRegex(CORE.ContractError, "duplicate changed path"):
                CORE.build_execution(duplicate, 1)

    def test_partial_receipt_requires_paths_and_allows_unknown_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            payload = json.loads(json.dumps(context["execution_payload"]))
            payload["result"] = "partial"
            payload["changed_paths"][0]["observed_after_sha256"] = "unknown"
            rewrite_execution(context, payload)
            report = VALIDATOR.validate_vault(root)
            self.assertEqual([], report.errors)

            payload["execution_id"] = "PENDING"
            payload["changed_paths"] = []
            with self.assertRaisesRegex(CORE.ContractError, "identify affected paths"):
                CORE.build_execution(payload, 1)

    def test_executed_and_rolled_back_hash_semantics_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            payload = json.loads(json.dumps(context["execution_payload"]))
            payload["changed_paths"][0]["observed_after_sha256"] = VALIDATOR.digest_text(
                "Wrong live bytes."
            )
            rewrite_execution(context, payload)
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("executed observed hash" in error for error in report.errors)
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            payload = json.loads(json.dumps(context["execution_payload"]))
            payload["result"] = "rolled-back"
            payload["changed_paths"][0]["observed_after_sha256"] = context["after_hash"]
            rewrite_execution(context, payload)
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("rolled-back observed state" in error for error in report.errors)
            )

    def test_attempt_sequence_and_timing_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root, blocked_first=True)
            payload = json.loads(json.dumps(context["execution_payload"]))
            payload["started_at"] = "2026-01-16T12:02:00Z"
            rewrite_execution(context, payload)
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("must not overlap" in error for error in report.errors)
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root, blocked_first=True)
            blocked = next(
                path
                for path in (context["library"] / "executions" / "2026-01").glob("*.md")
                if path.stem.endswith("-01")
            )
            blocked.unlink()
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("sequence must be contiguous" in error for error in report.errors)
            )

    def test_execution_cannot_start_before_approval(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            payload = json.loads(json.dumps(context["execution_payload"]))
            payload["started_at"] = "2026-01-16T11:59:00Z"
            rewrite_execution(context, payload)
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("started before approve-exact" in error for error in report.errors)
            )

    def test_validation_times_and_final_pass_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            validation_id = f"FPRV-20260116-{context['receipt_digest'][7:19]}-02"
            payload = {
                "schema_version": 2,
                "validation_id": validation_id,
                "execution_id": context["execution_id"],
                "result": "failed",
                "validated_at": "2026-01-16T12:05:45Z",
                "validator_results": [
                    {
                        "id": "schema-check",
                        "result": "failed",
                        "evidence": "Regression fixture.",
                    }
                ],
                "live_hashes": [],
            }
            digest = VALIDATOR.digest_payload(payload)
            write_record(
                context["library"]
                / "validations"
                / "2026-01"
                / f"{validation_id}.md",
                {
                    "name": "2026-01-16-learning-validation",
                    "description": "Failed follow up validation.",
                    "type": "learning-validation",
                    "schema-version": "2",
                    "status": "failed",
                    "authority": "none",
                    "validation-id": validation_id,
                    "execution-id": context["execution_id"],
                    "validation-digest": digest,
                    "validated-by": "Test Validator",
                    "validation-date": "2026-01-16",
                    "updated": "2026-01-16",
                },
                payload,
                "Learning Validation Receipt",
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("times must be nondecreasing" in error for error in report.errors)
            )
            self.assertTrue(
                any("passing validation must be the final" in error for error in report.errors)
            )

    def test_record_path_must_have_exact_kind_and_month_shape(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            wrong_parent = (
                context["library"]
                / "validations"
                / "nested"
                / "2026-01"
                / context["validation_path"].name
            )
            wrong_parent.parent.mkdir(parents=True)
            context["validation_path"].rename(wrong_parent)
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("record path must be validations/2026-01" in error for error in report.errors)
            )

    def test_decision_expiry_root_and_transition_rules_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            draft = json.loads(json.dumps(context["decision_payload"]))
            draft["decision_id"] = "PENDING"
            draft["expires_date"] = "2026-01-15"
            with self.assertRaisesRegex(CORE.ContractError, "expiry cannot precede"):
                CORE.build_decision(draft, "abcdef12")

            revoke = json.loads(json.dumps(context["decision_payload"]))
            revoke["decision_id"] = "PENDING"
            revoke["disposition"] = "revoke"
            with self.assertRaisesRegex(CORE.ContractError, "cannot be a root"):
                CORE.build_decision(revoke, "abcdef12")

            write_decision_event(
                context,
                decision_id="FPRD-20260116T120700Z-deadbeef",
                previous_event_id=context["decision_id"],
                disposition="hold",
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("invalid decision transition: approve-exact to hold" in error for error in report.errors)
            )

    def test_replacement_proposal_semantics_are_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            draft = json.loads(json.dumps(context["decision_payload"]))
            draft["decision_id"] = "PENDING"
            draft["disposition"] = "narrow"
            draft["replacement_proposal"] = "none"
            with self.assertRaisesRegex(CORE.ContractError, "requires replacement_proposal"):
                CORE.build_decision(draft, "abcdef12")

            write_decision_event(
                context,
                decision_id=context["decision_id"],
                previous_event_id="none",
                disposition="narrow",
                replacement_proposal="FPRP-20260117-abcdef123456",
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("replacement proposal does not exist" in error for error in report.errors)
            )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            replacement_payload = json.loads(json.dumps(context["proposal_payload"]))
            replacement_payload["revision_of"] = "none"
            replacement_payload["operations"][0]["exact_change"] = "Revised content."
            replacement_payload["operations"][0]["after_sha256"] = VALIDATOR.digest_text(
                "Revised content."
            )
            replacement = CORE.build_proposal(replacement_payload, "2026-01-17")
            replacement_path = (
                context["library"]
                / "proposals"
                / "2026-01"
                / f"{replacement['record_id']}.md"
            )
            write_record(
                replacement_path,
                {
                    "name": "2026-01-17-learning-proposal",
                    "description": "Invalidly linked replacement proposal.",
                    "type": "learning-proposal",
                    "schema-version": "2",
                    "status": "proposed",
                    "authority": "none",
                    "proposal-id": replacement["record_id"],
                    "proposal-digest": replacement["record_digest"],
                    "created-by": "Test Reviewer",
                    "created-date": "2026-01-17",
                    "updated": "2026-01-17",
                },
                replacement_payload,
                "Exact Learning Proposal",
            )
            write_decision_event(
                context,
                decision_id=context["decision_id"],
                previous_event_id="none",
                disposition="narrow",
                replacement_proposal=replacement["record_id"],
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("revision_of must name the source" in error for error in report.errors)
            )

    def test_revoke_cannot_follow_consumed_authority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root)
            write_decision_event(
                context,
                decision_id="FPRD-20260116T120700Z-cafebabe",
                previous_event_id=context["decision_id"],
                disposition="revoke",
            )
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("cannot revoke an authorization already consumed" in error for error in report.errors)
            )

    def test_proposal_and_execution_paths_cannot_escape_through_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / "vault"
            outside = base / "outside"
            outside.mkdir()
            context = build_valid_vault(root)
            context["live_target"].unlink()
            (root / "skills").rmdir()
            (root / "skills").symlink_to(outside, target_is_directory=True)
            report = VALIDATOR.validate_vault(root)
            self.assertTrue(
                any("proposal target escapes vault through a symlink" in error for error in report.errors)
            )
            self.assertTrue(
                any("execution target escapes vault through a symlink" in error for error in report.errors)
            )

    def test_deterministic_builder_creates_and_verifies_every_record_kind(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            context = build_valid_vault(Path(directory))

            proposal = CORE.build_proposal(context["proposal_payload"], "2026-01-15")
            self.assertEqual(context["proposal_id"], proposal["record_id"])
            self.assertEqual(context["proposal_digest"], proposal["record_digest"])
            CORE.verify_envelope(proposal)

            decision_payload = dict(context["decision_payload"])
            decision_payload["decision_id"] = "PENDING"
            decision = CORE.build_decision(decision_payload, "1234abcd")
            self.assertEqual(context["decision_id"], decision["record_id"])
            self.assertEqual(context["decision_digest"], decision["record_digest"])
            self.assertEqual(context["authorization_digest"], decision["authorization_digest"])
            CORE.verify_envelope(decision)

            execution_payload = dict(context["execution_payload"])
            execution_payload["execution_id"] = "PENDING"
            execution = CORE.build_execution(execution_payload, 1)
            self.assertEqual(context["execution_id"], execution["record_id"])
            self.assertEqual(context["receipt_digest"], execution["record_digest"])
            CORE.verify_envelope(execution)

            validation_payload = dict(context["validation_payload"])
            validation_payload["validation_id"] = "PENDING"
            validation = CORE.build_validation(
                validation_payload, context["receipt_digest"], 1
            )
            self.assertEqual(context["validation_id"], validation["record_id"])
            CORE.verify_envelope(validation)

    def test_envelope_sequence_requires_json_integer_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root / "vault")
            validation_payload = dict(context["validation_payload"])
            validation_payload["validation_id"] = "PENDING"
            envelope = CORE.build_validation(
                validation_payload, context["receipt_digest"], 1
            )
            invalid_sequence_values = (True, 1.0, "1", None, [], {})
            for invalid in invalid_sequence_values:
                with self.subTest(invalid=invalid):
                    malformed = dict(envelope)
                    malformed["sequence"] = invalid
                    with self.assertRaisesRegex(CORE.ContractError, "JSON integer"):
                        CORE.verify_envelope(malformed)

            malformed_path = root / "malformed-validation-envelope.json"
            malformed = dict(envelope)
            malformed["sequence"] = "not-an-integer"
            malformed_path.write_text(
                json.dumps(malformed, indent=2) + "\n", encoding="utf-8"
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(RECORD_CLI_PATH),
                    "verify",
                    "--record",
                    str(malformed_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("must be a JSON integer", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

            execution_payload = dict(context["execution_payload"])
            execution_payload["execution_id"] = "PENDING"
            execution = CORE.build_execution(execution_payload, 1)
            for invalid in invalid_sequence_values:
                with self.subTest(invalid_attempt=invalid):
                    malformed_execution = dict(execution)
                    malformed_execution["attempt"] = invalid
                    with self.assertRaisesRegex(CORE.ContractError, "JSON integer"):
                        CORE.verify_envelope(malformed_execution)

    def test_record_cli_writes_atomically_and_refuses_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root / "vault")
            payload_path = root / "proposal.json"
            payload_path.write_text(
                json.dumps(context["proposal_payload"], indent=2) + "\n",
                encoding="utf-8",
            )
            output_path = root / "proposal-envelope.json"
            command = [
                sys.executable,
                str(RECORD_CLI_PATH),
                "create",
                "proposal",
                "--payload",
                str(payload_path),
                "--created-date",
                "2026-01-15",
                "--output",
                str(output_path),
            ]
            first = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(0, first.returncode, first.stderr)
            original = output_path.read_bytes()
            second = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(1, second.returncode)
            self.assertIn("refusing to overwrite", second.stderr)
            self.assertEqual(original, output_path.read_bytes())
            verified = subprocess.run(
                [
                    sys.executable,
                    str(RECORD_CLI_PATH),
                    "verify",
                    "--record",
                    str(output_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, verified.returncode, verified.stderr)
            tampered = json.loads(output_path.read_text(encoding="utf-8"))
            tampered["payload"]["scope"] = "Tampered scope."
            tampered_path = root / "tampered-envelope.json"
            tampered_path.write_text(
                json.dumps(tampered, indent=2) + "\n", encoding="utf-8"
            )
            rejected = subprocess.run(
                [
                    sys.executable,
                    str(RECORD_CLI_PATH),
                    "verify",
                    "--record",
                    str(tampered_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(1, rejected.returncode)
            self.assertIn("does not verify", rejected.stderr)

    def test_record_cli_creates_all_four_record_kinds(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            context = build_valid_vault(root / "vault")
            payloads = {
                "proposal": dict(context["proposal_payload"]),
                "decision": {**context["decision_payload"], "decision_id": "PENDING"},
                "execution": {**context["execution_payload"], "execution_id": "PENDING"},
                "validation": {
                    **context["validation_payload"],
                    "validation_id": "PENDING",
                },
            }
            commands = {
                "proposal": ["--created-date", "2026-01-15"],
                "decision": ["--nonce", "1234abcd"],
                "execution": ["--attempt", "1"],
                "validation": [
                    "--execution-receipt-digest",
                    context["receipt_digest"],
                    "--sequence",
                    "1",
                ],
            }
            expected_ids = {
                "proposal": context["proposal_id"],
                "decision": context["decision_id"],
                "execution": context["execution_id"],
                "validation": context["validation_id"],
            }
            for kind, payload in payloads.items():
                with self.subTest(kind=kind):
                    payload_path = root / f"{kind}.json"
                    payload_path.write_text(
                        json.dumps(payload, indent=2) + "\n", encoding="utf-8"
                    )
                    result = subprocess.run(
                        [
                            sys.executable,
                            str(RECORD_CLI_PATH),
                            "create",
                            kind,
                            "--payload",
                            str(payload_path),
                            *commands[kind],
                        ],
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(0, result.returncode, result.stderr)
                    envelope = json.loads(result.stdout)
                    self.assertEqual(expected_ids[kind], envelope["record_id"])
                    CORE.verify_envelope(envelope)


if __name__ == "__main__":
    unittest.main()
