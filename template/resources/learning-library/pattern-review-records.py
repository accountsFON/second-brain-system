#!/usr/bin/env python3
"""Create or verify deterministic Pattern Review schema version 2 envelopes."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from pattern_review_core import (
    ContractError,
    build_decision,
    build_execution,
    build_proposal,
    build_validation,
    parse_json_payload,
    verify_envelope,
)


def load_json_file(path: Path) -> dict[str, Any]:
    try:
        return parse_json_payload(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ContractError(f"cannot read {path}: {exc}") from exc


def render_envelope(envelope: dict[str, Any]) -> str:
    return json.dumps(envelope, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def atomic_write(path: Path, content: str) -> None:
    if not path.parent.is_dir():
        raise ContractError(f"output parent directory does not exist: {path.parent}")
    temporary_name: str | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
        )
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary_name, 0o644)
        try:
            os.link(temporary_name, path)
        except FileExistsError as exc:
            raise ContractError(f"refusing to overwrite existing output: {path}") from exc
        except OSError as exc:
            raise ContractError(f"cannot atomically create output {path}: {exc}") from exc
    except OSError as exc:
        raise ContractError(f"cannot stage atomic output {path}: {exc}") from exc
    finally:
        if temporary_name is not None:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass


def emit(envelope: dict[str, Any], output: Path | None) -> None:
    content = render_envelope(envelope)
    if output is None:
        sys.stdout.write(content)
        return
    atomic_write(output, content)
    print(f"Created {output}")
    print(f"Record ID: {envelope['record_id']}")
    print(f"Record digest: {envelope['record_digest']}")


def create_proposal(args: argparse.Namespace) -> None:
    emit(build_proposal(load_json_file(args.payload), args.created_date), args.output)


def create_decision(args: argparse.Namespace) -> None:
    emit(build_decision(load_json_file(args.payload), args.nonce), args.output)


def create_execution(args: argparse.Namespace) -> None:
    emit(build_execution(load_json_file(args.payload), args.attempt), args.output)


def create_validation(args: argparse.Namespace) -> None:
    emit(
        build_validation(
            load_json_file(args.payload), args.execution_receipt_digest, args.sequence
        ),
        args.output,
    )


def verify_record(args: argparse.Namespace) -> None:
    verify_envelope(load_json_file(args.record))
    print(f"Verified {args.record}")


def add_common_create(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--payload", required=True, type=Path, help="Canonical JSON payload")
    parser.add_argument(
        "--output",
        type=Path,
        help="Atomically create this envelope file. Existing files are never overwritten.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("create", help="Create a deterministic record envelope")
    kinds = create.add_subparsers(dest="kind", required=True)

    proposal = kinds.add_parser("proposal")
    add_common_create(proposal)
    proposal.add_argument("--created-date", required=True)
    proposal.set_defaults(handler=create_proposal)

    decision = kinds.add_parser("decision")
    add_common_create(decision)
    decision.add_argument(
        "--nonce",
        required=True,
        help="Exactly eight lowercase hexadecimal characters. No random default is used.",
    )
    decision.set_defaults(handler=create_decision)

    execution = kinds.add_parser("execution")
    add_common_create(execution)
    execution.add_argument("--attempt", required=True, type=int)
    execution.set_defaults(handler=create_execution)

    validation = kinds.add_parser("validation")
    add_common_create(validation)
    validation.add_argument("--execution-receipt-digest", required=True)
    validation.add_argument("--sequence", required=True, type=int)
    validation.set_defaults(handler=create_validation)

    verify = commands.add_parser("verify", help="Verify a previously created envelope")
    verify.add_argument("--record", required=True, type=Path)
    verify.set_defaults(handler=verify_record)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        handler: Callable[[argparse.Namespace], None] = args.handler
        handler(args)
    except ContractError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
