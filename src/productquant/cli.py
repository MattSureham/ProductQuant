"""Supported ProductQuant Phase 1 command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any, NoReturn

from productquant import uci
from productquant.errors import ProductQuantError


def _emit(stream: Any, value: dict[str, Any]) -> None:
    stream.write(json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")


class UsageError(Exception):
    pass


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> NoReturn:
        raise UsageError(message)


def _parser() -> JsonArgumentParser:
    parser = JsonArgumentParser(prog="productquant")
    areas = parser.add_subparsers(dest="area", required=True)
    uci_parser = areas.add_parser(
        "uci", help="manage the pinned UCI Online Retail II foundation"
    )
    commands = uci_parser.add_subparsers(dest="operation", required=True)
    for name in ("fetch", "normalize", "verify", "prepare"):
        command = commands.add_parser(name)
        command.add_argument(
            "--data-root",
            type=Path,
            default=Path("data"),
            help="local ignored data root (default: ./data)",
        )
        if name in {"fetch", "prepare"}:
            command.add_argument(
                "--offline",
                action="store_true",
                help="never access the network; require a valid cached raw bundle",
            )
    return parser


def _command_name(namespace: argparse.Namespace) -> str:
    return f"{namespace.area}.{namespace.operation}"


def _empty_artifacts() -> dict[str, Any]:
    return {"raw": None, "normalized": None}


def _execute(
    namespace: argparse.Namespace,
    artifacts: dict[str, Any],
    statistics: dict[str, Any],
) -> None:
    data_root = namespace.data_root.resolve()
    if namespace.operation == "fetch":
        artifacts["raw"] = uci.fetch(data_root, offline=namespace.offline)
    elif namespace.operation == "normalize":
        artifacts["normalized"] = uci.normalize(data_root)
    elif namespace.operation == "verify":
        result = uci.verify(data_root)
        artifacts["raw"] = result["raw"]
        artifacts["normalized"] = result["normalized"]
        statistics.update(result["statistics"])
    elif namespace.operation == "prepare":
        artifacts["raw"] = uci.fetch(data_root, offline=namespace.offline)
        artifacts["normalized"] = uci.normalize(data_root)
        result = uci.verify(data_root)
        artifacts["raw"] = result["raw"] | {
            "action": artifacts["raw"]["action"]
        }
        artifacts["normalized"] = result["normalized"] | {
            "action": artifacts["normalized"]["action"]
        }
        statistics.update(result["statistics"])
    else:  # pragma: no cover - argparse owns this invariant
        raise RuntimeError("unrecognized operation")


def _receipt_base(
    run_id: str, command: str, data_root: Path, started: str
) -> dict[str, Any]:
    revision, dirty = uci._git_state()
    return {
        "schema_version": uci.RECEIPT_SCHEMA,
        "run_id": run_id,
        "command": command,
        "started_at_utc": started,
        "finished_at_utc": None,
        "status": None,
        "data_root": str(data_root),
        "git_revision": revision,
        "git_dirty": dirty,
        "artifacts": _empty_artifacts(),
        "statistics": {},
        "error": None,
    }


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(argv) if argv is not None else sys.argv[1:]
    try:
        namespace = _parser().parse_args(arguments)
    except UsageError as exc:
        command = None
        receipt_path: str | None = None
        if len(arguments) >= 2 and arguments[0] == "uci" and arguments[1] in {
            "fetch",
            "normalize",
            "verify",
            "prepare",
        }:
            command = f"uci.{arguments[1]}"
            data_root = Path("data").resolve()
            if "--data-root" in arguments:
                index = arguments.index("--data-root")
                if index + 1 < len(arguments) and not arguments[index + 1].startswith("-"):
                    data_root = Path(arguments[index + 1]).resolve()
            run_id = uci.make_run_id()
            started = uci.utc_now()
            receipt = _receipt_base(run_id, command, data_root, started)
            receipt.update(
                {
                    "finished_at_utc": uci.utc_now(),
                    "status": "failure",
                    "error": {"code": "usage_error", "message": str(exc)},
                }
            )
            try:
                receipt_path = str(uci.write_receipt(data_root, receipt).resolve())
            except Exception:
                receipt_path = None
        _emit(
            sys.stderr,
            {
                "command": command,
                "status": "error",
                "error": {"code": "usage_error", "message": str(exc)},
                "receipt_path": receipt_path,
            },
        )
        return 2
    except SystemExit as exc:
        if exc.code == 0:
            return 0
        raise
    command = _command_name(namespace)
    data_root = namespace.data_root.resolve()
    run_id = uci.make_run_id()
    started = uci.utc_now()
    receipt = _receipt_base(run_id, command, data_root, started)
    artifacts = _empty_artifacts()
    statistics: dict[str, Any] = {}
    try:
        uci._assert_data_root_policy(data_root)
        _execute(namespace, artifacts, statistics)
        receipt.update(
            {
                "finished_at_utc": uci.utc_now(),
                "status": "success",
                "artifacts": artifacts,
                "statistics": statistics,
            }
        )
        receipt_path = uci.write_receipt(data_root, receipt)
        status = "created" if any(
            artifact is not None and artifact["action"] == "created"
            for artifact in artifacts.values()
        ) else "verified"
        _emit(
            sys.stdout,
            {
                "command": command,
                "status": status,
                "data_root": str(data_root),
                "artifacts": artifacts,
                "statistics": statistics,
                "receipt_path": str(receipt_path.resolve()),
            },
        )
        return 0
    except Exception as exc:
        if isinstance(exc, ProductQuantError):
            error_code = exc.error_code
            exit_code = exc.exit_code
            message = str(exc)
        elif isinstance(exc, OSError):
            error_code = "state_error"
            exit_code = 5
            message = f"local I/O failure: {type(exc).__name__}"
        else:
            error_code = "internal_error"
            exit_code = 1
            message = f"unexpected internal failure: {type(exc).__name__}"
        receipt.update(
            {
                "finished_at_utc": uci.utc_now(),
                "status": "failure",
                "artifacts": artifacts,
                "statistics": statistics,
                "error": {"code": error_code, "message": message},
            }
        )
        receipt_path: str | None = None
        try:
            receipt_path = str(uci.write_receipt(data_root, receipt).resolve())
        except Exception:
            receipt_path = None
        _emit(
            sys.stderr,
            {
                "command": command,
                "status": "error",
                "error": {"code": error_code, "message": message},
                "receipt_path": receipt_path,
            },
        )
        return exit_code
