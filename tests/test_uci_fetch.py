from __future__ import annotations

import hashlib
import json
import os
import stat
import urllib.error
from pathlib import Path

import pytest

from productquant import uci
from productquant.errors import IntegrityError, NetworkError, StateError

from conftest import FakeResponse, SyntheticSource, make_archive


def test_fetch_persists_exact_archive_allowlisted_provenance_and_private_modes(
    tmp_path: Path,
    synthetic_source: SyntheticSource,
    mocked_download: list[str],
) -> None:
    data_root = tmp_path / "data"

    result = uci.fetch(data_root)

    raw_dir = uci.raw_directory(data_root.resolve())
    archive_path = raw_dir / uci.ARCHIVE_NAME
    manifest_path = raw_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert mocked_download == [uci.SOURCE_URL]
    assert result == {
        "artifact_id": synthetic_source.raw_artifact_id,
        "manifest_path": str(manifest_path.resolve()),
        "data_path": str(archive_path.resolve()),
        "action": "created",
    }
    assert archive_path.read_bytes() == synthetic_source.archive_bytes
    assert manifest["archive"] == {
        "path": uci.ARCHIVE_NAME,
        "bytes": len(synthetic_source.archive_bytes),
        "sha256": synthetic_source.archive_sha256,
    }
    assert manifest["member"] == {
        "name": uci.MEMBER_NAME,
        "bytes": len(synthetic_source.workbook_bytes),
        "sha256": synthetic_source.workbook_sha256,
    }
    assert manifest["raw_response_reference"] == uci.ARCHIVE_NAME
    assert manifest["capabilities"] == uci.CAPABILITIES
    assert manifest["retrieval"] == {
        "retrieved_at_utc": manifest["retrieval"]["retrieved_at_utc"],
        "mode": "download",
        "http_status": 200,
        "etag": '"synthetic-etag"',
        "last_modified": "Wed, 12 Aug 2026 00:00:00 GMT",
        "content_type": "application/zip",
        "content_length": str(len(synthetic_source.archive_bytes)),
        "rate_limit_state": "unknown",
        "query_parameters": {},
    }
    serialized = manifest_path.read_text(encoding="utf-8")
    assert "X-Private-Header" not in serialized
    assert "must-not-be-persisted" not in serialized
    assert {path.name for path in raw_dir.iterdir()} == {
        archive_path.name,
        manifest_path.name,
    }
    if os.name == "posix":
        assert stat.S_IMODE(raw_dir.stat().st_mode) == 0o700
        assert stat.S_IMODE(archive_path.stat().st_mode) == 0o600
        assert stat.S_IMODE(manifest_path.stat().st_mode) == 0o600


def test_fetch_is_verified_noop_without_network(
    fetched_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    archive_path = uci.raw_directory(fetched_root) / uci.ARCHIVE_NAME
    before = (archive_path.stat().st_mtime_ns, uci.sha256_file(archive_path))

    def forbidden_network(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("idempotent fetch attempted the network")

    monkeypatch.setattr(uci.urllib.request, "urlopen", forbidden_network)
    result = uci.fetch(fetched_root, offline=True)

    assert result["action"] == "verified"
    assert (archive_path.stat().st_mtime_ns, uci.sha256_file(archive_path)) == before


def test_offline_fetch_never_opens_network_and_requires_complete_bundle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> None:
    def forbidden_network(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("offline fetch attempted the network")

    monkeypatch.setattr(uci.urllib.request, "urlopen", forbidden_network)

    with pytest.raises(StateError, match="complete valid raw bundle"):
        uci.fetch(tmp_path / "missing", offline=True)


def test_fetch_maps_network_failure_without_publishing_partial_state(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> None:
    def fail_network(*_args: object, **_kwargs: object) -> None:
        raise urllib.error.URLError("PRIVATE-NETWORK-DETAIL")

    monkeypatch.setattr(uci.urllib.request, "urlopen", fail_network)
    data_root = tmp_path / "data"

    with pytest.raises(NetworkError) as captured:
        uci.fetch(data_root)

    assert "PRIVATE-NETWORK-DETAIL" not in str(captured.value)
    assert not uci.raw_directory(data_root).exists()
    parent = uci.raw_directory(data_root).parent
    assert not parent.exists() or not list(parent.glob("*.part-*"))


def test_fetch_maps_streaming_read_failure_and_never_publishes_partial_bundle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> None:
    class InterruptedResponse(FakeResponse):
        def __init__(self, body: bytes) -> None:
            super().__init__(body)
            self.read_count = 0

        def read(self, size: int = -1) -> bytes:
            self.read_count += 1
            if self.read_count == 1:
                return super().read(min(size, 128))
            raise urllib.error.URLError("PRIVATE-MIDSTREAM-DETAIL")

    monkeypatch.setattr(
        uci.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: InterruptedResponse(
            synthetic_source.archive_bytes
        ),
    )
    data_root = tmp_path / "data"

    with pytest.raises(NetworkError) as captured:
        uci.fetch(data_root)

    assert "interrupted" in str(captured.value)
    assert "PRIVATE-MIDSTREAM-DETAIL" not in str(captured.value)
    assert not uci.raw_directory(data_root).exists()
    parent = uci.raw_directory(data_root).parent
    assert not parent.exists() or not list(parent.glob("*.part-*"))


def test_initial_download_stops_at_expected_size_plus_one(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> None:
    consumed = 0

    class OversizedResponse(FakeResponse):
        def read(self, size: int = -1) -> bytes:
            nonlocal consumed
            chunk = super().read(size)
            consumed += len(chunk)
            return chunk

    monkeypatch.setattr(
        uci.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: OversizedResponse(
            synthetic_source.archive_bytes + b"unbounded-extra-content"
        ),
    )
    data_root = tmp_path / "data"

    with pytest.raises(IntegrityError, match="exceeds pinned byte count"):
        uci.fetch(data_root)

    assert consumed == len(synthetic_source.archive_bytes) + 1
    assert not uci.raw_directory(data_root).exists()
    assert not list(uci.raw_directory(data_root).parent.glob("*.part-*"))


def test_raw_archive_write_failure_never_publishes_bundle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> None:
    original_open = Path.open

    class FailingArchiveWriter:
        def __init__(self, handle: object) -> None:
            self.handle = handle

        def __enter__(self) -> "FailingArchiveWriter":
            return self

        def __exit__(self, *_args: object) -> None:
            self.handle.close()

        def __getattr__(self, name: str) -> object:
            return getattr(self.handle, name)

        def write(self, value: bytes) -> int:
            self.handle.write(value[:17])
            raise OSError("injected raw write failure")

    def failing_open(self: Path, mode: str = "r", *args: object, **kwargs: object):
        handle = original_open(self, mode, *args, **kwargs)
        if self.name == uci.ARCHIVE_NAME and mode == "xb":
            return FailingArchiveWriter(handle)
        return handle

    monkeypatch.setattr(Path, "open", failing_open)
    monkeypatch.setattr(
        uci.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: FakeResponse(synthetic_source.archive_bytes),
    )
    data_root = tmp_path / "data"

    with pytest.raises(OSError, match="injected raw write failure"):
        uci.fetch(data_root)

    assert not uci.raw_directory(data_root).exists()
    assert not list(uci.raw_directory(data_root).parent.glob("*.part-*"))


def test_fetch_resumes_clean_short_response_with_exact_sequential_ranges(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> None:
    initial_bytes = 113
    range_chunk_bytes = 512
    observed_ranges: list[tuple[str, str]] = []
    calls = 0

    monkeypatch.setattr(uci, "RANGE_CHUNK_BYTES", range_chunk_bytes)
    monkeypatch.setattr(uci, "MAX_RANGE_REQUESTS", 64)

    def ranged_response(request: object, *, timeout: int) -> FakeResponse:
        nonlocal calls
        calls += 1
        assert timeout == 60
        requested_range = request.get_header("Range")
        if calls == 1:
            assert requested_range is None
            return FakeResponse(synthetic_source.archive_bytes[:initial_bytes])

        assert requested_range is not None
        prefix, bounds = requested_range.split("=", 1)
        start_text, end_text = bounds.split("-", 1)
        assert prefix == "bytes"
        start, end = int(start_text), int(end_text)
        expected_end = min(
            start + range_chunk_bytes,
            len(synthetic_source.archive_bytes),
        ) - 1
        assert end == expected_end
        content_range = (
            f"bytes {start}-{end}/{len(synthetic_source.archive_bytes)}"
        )
        observed_ranges.append((requested_range, content_range))
        return FakeResponse(
            synthetic_source.archive_bytes[start : end + 1],
            status=206,
            headers={
                "Content-Range": content_range,
                "Content-Length": str(end - start + 1),
                "Content-Type": "application/zip",
            },
        )

    monkeypatch.setattr(uci.urllib.request, "urlopen", ranged_response)
    data_root = tmp_path / "data"

    result = uci.fetch(data_root)

    assert result["action"] == "created"
    assert len(observed_ranges) >= 2
    assert observed_ranges[0] == (
        f"bytes={initial_bytes}-{initial_bytes + range_chunk_bytes - 1}",
        (
            f"bytes {initial_bytes}-{initial_bytes + range_chunk_bytes - 1}/"
            f"{len(synthetic_source.archive_bytes)}"
        ),
    )
    for previous, current in zip(observed_ranges, observed_ranges[1:]):
        previous_end = int(previous[0].split("-")[1])
        current_start = int(current[0].split("=")[1].split("-")[0])
        assert current_start == previous_end + 1
    archive_path = uci.raw_directory(data_root) / uci.ARCHIVE_NAME
    assert archive_path.read_bytes() == synthetic_source.archive_bytes
    assert uci.verify_raw_bundle(data_root)["archive"]["sha256"] == (
        synthetic_source.archive_sha256
    )


@pytest.mark.parametrize(
    ("status", "content_range_mode", "body_mode", "error_type", "message"),
    [
        (200, "correct", "correct", IntegrityError, "metadata differs"),
        (206, "wrong", "correct", IntegrityError, "metadata differs"),
        (206, "correct", "empty", NetworkError, "returned no bytes"),
    ],
)
def test_fetch_range_resume_fails_closed_on_invalid_or_empty_response(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
    status: int,
    content_range_mode: str,
    body_mode: str,
    error_type: type[Exception],
    message: str,
) -> None:
    initial_bytes = 101
    monkeypatch.setattr(uci, "RANGE_CHUNK_BYTES", 512)
    calls = 0

    def invalid_range_response(request: object, *, timeout: int) -> FakeResponse:
        nonlocal calls
        calls += 1
        assert timeout == 60
        requested_range = request.get_header("Range")
        if calls == 1:
            assert requested_range is None
            return FakeResponse(synthetic_source.archive_bytes[:initial_bytes])

        assert requested_range is not None
        start_text, end_text = requested_range.removeprefix("bytes=").split("-")
        start, end = int(start_text), int(end_text)
        correct_content_range = (
            f"bytes {start}-{end}/{len(synthetic_source.archive_bytes)}"
        )
        content_range = (
            correct_content_range
            if content_range_mode == "correct"
            else f"bytes {start + 1}-{end}/{len(synthetic_source.archive_bytes)}"
        )
        body = (
            synthetic_source.archive_bytes[start : end + 1]
            if body_mode == "correct"
            else b""
        )
        return FakeResponse(
            body,
            status=status,
            headers={"Content-Range": content_range},
        )

    monkeypatch.setattr(uci.urllib.request, "urlopen", invalid_range_response)
    data_root = tmp_path / "data"

    with pytest.raises(error_type, match=message):
        uci.fetch(data_root)

    assert calls == 2
    assert not uci.raw_directory(data_root).exists()
    parent = uci.raw_directory(data_root).parent
    assert not parent.exists() or not list(parent.glob("*.part-*"))


def test_fetch_rejects_archive_digest_drift_and_removes_stage(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> None:
    corrupted = bytearray(synthetic_source.archive_bytes)
    corrupted[-1] ^= 0x01
    monkeypatch.setattr(
        uci.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: FakeResponse(bytes(corrupted)),
    )
    data_root = tmp_path / "data"

    with pytest.raises(IntegrityError, match="downloaded archive differs"):
        uci.fetch(data_root)

    assert not uci.raw_directory(data_root).exists()
    parent = uci.raw_directory(data_root).parent
    assert not parent.exists() or not list(parent.glob("*.part-*"))


@pytest.mark.parametrize(
    ("final_url", "status", "headers", "message"),
    [
        (
            "http://fixtures.invalid/online-retail-ii.zip",
            200,
            None,
            "raw final URL differs",
        ),
        (
            "https://fixtures.invalid/online-retail-ii.zip",
            404,
            None,
            "raw retrieval mode/status differs",
        ),
        (
            "https://fixtures.invalid/online-retail-ii.zip",
            200,
            {"Content-Length": 123},
            "raw retrieval header type differs",
        ),
    ],
)
def test_fetch_validates_generated_manifest_before_publication(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
    final_url: str,
    status: int,
    headers: dict[str, object] | None,
    message: str,
) -> None:
    monkeypatch.setattr(
        uci.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: FakeResponse(
            synthetic_source.archive_bytes,
            final_url=final_url,
            status=status,
            headers=headers,
        ),
    )
    data_root = tmp_path / "data"

    with pytest.raises(IntegrityError, match=message):
        uci.fetch(data_root)

    assert not uci.raw_directory(data_root).exists()
    assert not list(uci.raw_directory(data_root).parent.glob("*.part-*"))


def test_fetch_publication_failure_removes_stage_without_final_bundle(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> None:
    monkeypatch.setattr(
        uci.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: FakeResponse(synthetic_source.archive_bytes),
    )
    monkeypatch.setattr(
        uci,
        "atomic_publish_directory",
        lambda *_args: (_ for _ in ()).throw(
            StateError("injected raw publication failure")
        ),
    )
    data_root = tmp_path / "data"

    with pytest.raises(StateError, match="injected raw publication failure"):
        uci.fetch(data_root)

    assert not uci.raw_directory(data_root).exists()
    assert not list(uci.raw_directory(data_root).parent.glob("*.part-*"))


def test_archive_validation_rejects_member_set_drift(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> None:
    archive = make_archive(
        synthetic_source.workbook_bytes,
        member_name="renamed_or_extra_source.xlsx",
    )
    path = tmp_path / "member-drift.zip"
    path.write_bytes(archive)
    monkeypatch.setattr(uci, "ARCHIVE_BYTES", len(archive))
    monkeypatch.setattr(uci, "ARCHIVE_SHA256", hashlib.sha256(archive).hexdigest())

    with pytest.raises(IntegrityError, match="member set differs"):
        uci._verify_archive(path)


def test_archive_validation_rejects_archive_byte_count_drift_before_hash(
    tmp_path: Path,
    synthetic_source: SyntheticSource,
) -> None:
    path = tmp_path / "archive-size-drift.zip"
    path.write_bytes(synthetic_source.archive_bytes + b"x")

    with pytest.raises(IntegrityError, match="archive byte count differs"):
        uci._verify_archive(path)


def test_archive_validation_rejects_member_byte_count_drift_before_hash(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> None:
    archive = make_archive(synthetic_source.workbook_bytes + b"x")
    path = tmp_path / "member-size-drift.zip"
    path.write_bytes(archive)
    monkeypatch.setattr(uci, "ARCHIVE_BYTES", len(archive))
    monkeypatch.setattr(uci, "ARCHIVE_SHA256", hashlib.sha256(archive).hexdigest())

    with pytest.raises(IntegrityError, match="workbook byte count differs"):
        uci._verify_archive(path)


def test_archive_validation_rejects_inner_workbook_digest_drift(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> None:
    changed_workbook = bytearray(synthetic_source.workbook_bytes)
    changed_workbook[-1] ^= 0x01
    archive = make_archive(bytes(changed_workbook))
    path = tmp_path / "member-digest-drift.zip"
    path.write_bytes(archive)
    monkeypatch.setattr(uci, "ARCHIVE_BYTES", len(archive))
    monkeypatch.setattr(uci, "ARCHIVE_SHA256", hashlib.sha256(archive).hexdigest())

    with pytest.raises(IntegrityError, match="workbook SHA-256 differs"):
        uci._verify_archive(path)


@pytest.mark.parametrize("extra_name", [None, "unexpected.txt"])
def test_existing_incomplete_or_extra_raw_bundle_fails_closed_without_network(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
    extra_name: str | None,
) -> None:
    destination = uci.raw_directory(tmp_path)
    destination.mkdir(parents=True)
    (destination / uci.ARCHIVE_NAME).write_bytes(synthetic_source.archive_bytes)
    if extra_name is not None:
        (destination / extra_name).write_text("unexpected", encoding="utf-8")

    def forbidden_network(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("invalid existing target attempted network recovery")

    monkeypatch.setattr(uci.urllib.request, "urlopen", forbidden_network)

    with pytest.raises(IntegrityError, match="bundle contents differ"):
        uci.fetch(tmp_path)


def test_fetch_rejects_corrupt_existing_manifest_without_overwriting(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> None:
    destination = uci.raw_directory(tmp_path)
    destination.mkdir(parents=True)
    archive_path = destination / uci.ARCHIVE_NAME
    manifest_path = destination / "manifest.json"
    archive_path.write_bytes(synthetic_source.archive_bytes)
    manifest_path.write_text("not-json", encoding="utf-8")
    if os.name == "posix":
        destination.chmod(0o700)
        archive_path.chmod(0o600)
        manifest_path.chmod(0o600)
    original = archive_path.read_bytes(), manifest_path.read_bytes()

    monkeypatch.setattr(
        uci.urllib.request,
        "urlopen",
        lambda *_args, **_kwargs: pytest.fail("invalid bundle attempted network"),
    )
    with pytest.raises(IntegrityError, match="invalid JSON"):
        uci.fetch(tmp_path)

    assert (archive_path.read_bytes(), manifest_path.read_bytes()) == original


def test_raw_manifest_tampering_fails_closed(
    fetched_root: Path,
) -> None:
    manifest_path = uci.raw_directory(fetched_root) / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["archive"]["sha256"] = "0" * 64
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(IntegrityError, match="raw manifest field differs: archive"):
        uci.verify_raw_bundle(fetched_root)


def test_raw_capability_tampering_fails_closed(fetched_root: Path) -> None:
    manifest_path = uci.raw_directory(fetched_root) / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["capabilities"]["marketplace_listing_state"] = "supported"
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(IntegrityError, match="raw capability declarations differ"):
        uci.verify_raw_bundle(fetched_root)


def test_raw_manifest_rejects_uncontracted_fields(
    fetched_root: Path,
) -> None:
    manifest_path = uci.raw_directory(fetched_root) / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["transaction_row"] = "must not exist"
    manifest_path.write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(IntegrityError, match="raw manifest keys differ"):
        uci.verify_raw_bundle(fetched_root)


@pytest.mark.skipif(os.name != "posix", reason="POSIX permission contract")
def test_raw_bundle_rejects_public_file_permissions(fetched_root: Path) -> None:
    archive_path = uci.raw_directory(fetched_root) / uci.ARCHIVE_NAME
    archive_path.chmod(0o644)

    with pytest.raises(IntegrityError, match="permission mode differs"):
        uci.verify_raw_bundle(fetched_root)


@pytest.mark.skipif(os.name != "posix", reason="symlink rejection contract")
def test_raw_bundle_rejects_symlink_bundle_or_member(
    tmp_path: Path,
    fetched_root: Path,
) -> None:
    raw_directory = uci.raw_directory(fetched_root)
    linked_root = tmp_path / "linked-root"
    linked_root.mkdir()
    linked_bundle = uci.raw_directory(linked_root)
    linked_bundle.parent.mkdir(parents=True)
    linked_bundle.symlink_to(raw_directory, target_is_directory=True)

    with pytest.raises(IntegrityError, match="not a real directory"):
        uci.verify_raw_bundle(linked_root)

    manifest_path = raw_directory / "manifest.json"
    manifest_copy = tmp_path / "manifest-copy.json"
    manifest_copy.write_bytes(manifest_path.read_bytes())
    manifest_path.unlink()
    manifest_path.symlink_to(manifest_copy)
    with pytest.raises(IntegrityError, match="not a real regular file"):
        uci.verify_raw_bundle(fetched_root)
