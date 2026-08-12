from __future__ import annotations

import json
import os
import re
import stat
from pathlib import Path

import pytest

from productquant import cli, uci
from productquant.errors import IntegrityError, NetworkError, StateError

from conftest import SyntheticSource


def _one_json_line(text: str) -> dict[str, object]:
    lines = text.splitlines()
    assert len(lines) == 1
    value = json.loads(lines[0])
    assert isinstance(value, dict)
    return value


@pytest.mark.parametrize(
    "arguments",
    [
        ["--help"],
        ["uci", "--help"],
        ["uci", "fetch", "--help"],
        ["uci", "normalize", "--help"],
        ["uci", "verify", "--help"],
        ["uci", "prepare", "--help"],
    ],
)
def test_help_is_text_on_stdout_and_creates_no_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    arguments: list[str],
) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = cli.main(arguments)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "usage:" in captured.out
    assert captured.err == ""
    assert not (tmp_path / "data").exists()


@pytest.mark.parametrize(
    "arguments",
    [[], ["unknown"], ["uci"], ["uci", "unknown"]],
)
def test_usage_error_before_valid_command_is_single_json_without_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    arguments: list[str],
) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = cli.main(arguments)

    captured = capsys.readouterr()
    error = _one_json_line(captured.err)
    assert exit_code == 2
    assert captured.out == ""
    assert error == {
        "command": None,
        "status": "error",
        "error": {
            "code": "usage_error",
            "message": error["error"]["message"],
        },
        "receipt_path": None,
    }
    assert isinstance(error["error"]["message"], str)
    assert not (tmp_path / "data").exists()


def test_usage_error_after_valid_command_writes_failure_receipt(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    data_root = tmp_path / "data"

    exit_code = cli.main(
        ["uci", "fetch", "--data-root", str(data_root), "--unexpected"]
    )

    captured = capsys.readouterr()
    error = _one_json_line(captured.err)
    assert exit_code == 2
    assert captured.out == ""
    assert error["command"] == "uci.fetch"
    assert error["status"] == "error"
    assert error["error"]["code"] == "usage_error"
    receipt_path = Path(error["receipt_path"])
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["schema_version"] == "productquant.command-receipt.v1"
    assert receipt["command"] == "uci.fetch"
    assert receipt["status"] == "failure"
    assert receipt["error"]["code"] == "usage_error"
    assert receipt["statistics"] == {}
    if os.name == "posix":
        assert stat.S_IMODE(receipt_path.stat().st_mode) == 0o600


def test_prepare_success_emits_one_json_object_and_one_row_free_receipt(
    tmp_path: Path,
    synthetic_source: SyntheticSource,
    mocked_download: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    data_root = tmp_path / "data"

    exit_code = cli.main(["uci", "prepare", "--data-root", str(data_root)])

    captured = capsys.readouterr()
    output = _one_json_line(captured.out)
    assert exit_code == 0
    assert captured.err == ""
    assert output["command"] == "uci.prepare"
    assert output["status"] == "created"
    assert output["data_root"] == str(data_root.resolve())
    assert output["artifacts"]["raw"]["action"] == "created"
    assert output["artifacts"]["normalized"]["action"] == "created"
    assert output["statistics"] == synthetic_source.expected_profile
    assert mocked_download == [uci.SOURCE_URL]
    receipt_path = Path(output["receipt_path"])
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["command"] == "uci.prepare"
    assert receipt["status"] == "success"
    assert receipt["error"] is None
    assert receipt["artifacts"] == output["artifacts"]
    assert receipt["statistics"] == output["statistics"]
    assert re.fullmatch(r"\d{8}T\d{12}Z-[0-9a-f]{8}", receipt["run_id"])
    assert receipt["started_at_utc"].endswith("Z")
    assert receipt["finished_at_utc"].endswith("Z")
    serialized = captured.out + receipt_path.read_text(encoding="utf-8")
    assert "INV-PRIVATE-ROW-99381" not in serialized
    assert "SKU-WHITESPACE" not in serialized
    assert '"400"' not in serialized


def test_offline_prepare_missing_cache_returns_state_error_without_network(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def forbidden_network(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("offline prepare attempted network")

    monkeypatch.setattr(uci.urllib.request, "urlopen", forbidden_network)
    data_root = tmp_path / "data"

    exit_code = cli.main(
        ["uci", "prepare", "--data-root", str(data_root), "--offline"]
    )

    captured = capsys.readouterr()
    error = _one_json_line(captured.err)
    assert exit_code == 5
    assert captured.out == ""
    assert error["command"] == "uci.prepare"
    assert error["status"] == "error"
    assert error["error"] == {
        "code": "state_error",
        "message": "offline mode requires a complete valid raw bundle",
    }
    receipt = json.loads(Path(error["receipt_path"]).read_text(encoding="utf-8"))
    assert receipt["status"] == "failure"
    assert receipt["error"] == error["error"]


def test_offline_prepare_verifies_complete_cache_without_network(
    normalized_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def forbidden_network(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("offline prepare attempted network")

    monkeypatch.setattr(uci.urllib.request, "urlopen", forbidden_network)

    exit_code = cli.main(
        ["uci", "prepare", "--data-root", str(normalized_root), "--offline"]
    )

    captured = capsys.readouterr()
    output = _one_json_line(captured.out)
    assert exit_code == 0
    assert captured.err == ""
    assert output["status"] == "verified"
    assert output["artifacts"]["raw"]["action"] == "verified"
    assert output["artifacts"]["normalized"]["action"] == "verified"


def test_cli_maps_network_integrity_state_and_internal_failures_to_stable_codes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
    capsys: pytest.CaptureFixture[str],
) -> None:
    scenarios = [
        (NetworkError("download failed"), 3, "network_error"),
        (IntegrityError("source schema differs"), 4, "integrity_error"),
        (StateError("state conflict"), 5, "state_error"),
        (RuntimeError("PRIVATE-CUSTOMER-ROW-400"), 1, "internal_error"),
    ]
    for index, (failure, expected_exit, expected_code) in enumerate(scenarios):
        monkeypatch.setattr(uci, "normalize", lambda *_args, _failure=failure: (_ for _ in ()).throw(_failure))
        data_root = tmp_path / f"case-{index}"

        exit_code = cli.main(
            ["uci", "normalize", "--data-root", str(data_root)]
        )
        captured = capsys.readouterr()
        error = _one_json_line(captured.err)
        assert exit_code == expected_exit
        assert captured.out == ""
        assert error["error"]["code"] == expected_code
        assert "PRIVATE-CUSTOMER-ROW-400" not in captured.err
        receipt = Path(error["receipt_path"]).read_text(encoding="utf-8")
        assert "PRIVATE-CUSTOMER-ROW-400" not in receipt


def test_prepare_failure_receipt_preserves_completed_raw_artifact(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
    mocked_download: list[str],
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(
        uci,
        "normalize",
        lambda *_args: (_ for _ in ()).throw(
            IntegrityError("injected normalization failure")
        ),
    )
    data_root = tmp_path / "data"

    exit_code = cli.main(["uci", "prepare", "--data-root", str(data_root)])

    error = _one_json_line(capsys.readouterr().err)
    receipt = json.loads(Path(error["receipt_path"]).read_text(encoding="utf-8"))
    assert exit_code == 4
    assert mocked_download == [uci.SOURCE_URL]
    assert receipt["status"] == "failure"
    assert receipt["artifacts"]["raw"]["artifact_id"] == uci.RAW_ARTIFACT_ID
    assert receipt["artifacts"]["raw"]["action"] == "created"
    assert receipt["artifacts"]["normalized"] is None
    assert receipt["statistics"] == {}


def test_unwritable_data_root_does_not_mask_primary_state_failure(
    tmp_path: Path,
    synthetic_source: SyntheticSource,
    capsys: pytest.CaptureFixture[str],
) -> None:
    data_root = tmp_path / "not-a-directory"
    data_root.write_text("file", encoding="utf-8")

    exit_code = cli.main(["uci", "fetch", "--data-root", str(data_root)])

    captured = capsys.readouterr()
    error = _one_json_line(captured.err)
    assert exit_code == 5
    assert captured.out == ""
    assert error["command"] == "uci.fetch"
    assert error["error"]["code"] == "state_error"
    assert error["receipt_path"] is None


def test_receipts_are_immutable_unique_records_for_idempotent_commands(
    normalized_root: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    arguments = ["uci", "verify", "--data-root", str(normalized_root)]

    first_exit = cli.main(arguments)
    first = _one_json_line(capsys.readouterr().out)
    second_exit = cli.main(arguments)
    second = _one_json_line(capsys.readouterr().out)

    assert first_exit == second_exit == 0
    assert first["status"] == second["status"] == "verified"
    assert first["receipt_path"] != second["receipt_path"]
    assert Path(first["receipt_path"]).is_file()
    assert Path(second["receipt_path"]).is_file()


def test_write_receipt_collision_fails_without_overwrite_or_partial(
    tmp_path: Path,
) -> None:
    receipt = {
        "run_id": "20260812T000000000000Z-deadbeef",
        "row_free": True,
    }
    first = uci.write_receipt(tmp_path, receipt)
    before = first.read_bytes()

    with pytest.raises(StateError, match="appeared during publication"):
        uci.write_receipt(tmp_path, receipt)

    assert first.read_bytes() == before
    assert not list(first.parent.glob("*.part"))


def test_receipt_atomic_publication_failure_removes_temporary_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    receipt = {
        "run_id": "20260812T000000000000Z-acde1234",
        "row_free": True,
    }
    monkeypatch.setattr(
        uci,
        "_rename_noreplace",
        lambda *_args: (_ for _ in ()).throw(
            StateError("injected receipt publication failure")
        ),
    )

    with pytest.raises(StateError, match="injected receipt publication failure"):
        uci.write_receipt(tmp_path, receipt)

    directory = uci.receipts_directory(tmp_path.resolve())
    assert not (directory / f"{receipt['run_id']}.json").exists()
    assert not list(directory.glob("*.part"))


def test_receipt_target_appearing_at_commit_is_not_overwritten(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    receipt = {
        "run_id": "20260812T000000000000Z-1234abcd",
        "row_free": True,
    }
    final = uci.receipts_directory(tmp_path.resolve()) / f"{receipt['run_id']}.json"
    original = uci._rename_noreplace

    def appear_then_publish(source: Path, destination: Path) -> None:
        destination.write_text("competitor", encoding="utf-8")
        original(source, destination)

    monkeypatch.setattr(uci, "_rename_noreplace", appear_then_publish)

    with pytest.raises(StateError, match="appeared during publication"):
        uci.write_receipt(tmp_path, receipt)

    assert final.read_text(encoding="utf-8") == "competitor"
    assert not list(final.parent.glob("*.part"))


def test_receipt_postcommit_sync_failure_leaves_complete_real_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    receipt = {
        "run_id": "20260812T000000000000Z-fedcba98",
        "row_free": True,
    }
    final = uci.receipts_directory(tmp_path.resolve()) / f"{receipt['run_id']}.json"
    monkeypatch.setattr(
        uci,
        "fsync_directory",
        lambda *_args: (_ for _ in ()).throw(OSError("injected receipt sync failure")),
    )

    with pytest.raises(StateError, match="directory sync failed"):
        uci.write_receipt(tmp_path, receipt)

    assert final.is_file() and not final.is_symlink()
    assert json.loads(final.read_text(encoding="utf-8")) == receipt
    assert not list(final.parent.glob("*.part"))
