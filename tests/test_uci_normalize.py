from __future__ import annotations

import json
import os
import stat
from decimal import Decimal
from pathlib import Path

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from productquant import uci
from productquant.errors import IntegrityError, StateError

from conftest import SyntheticSource


def _parquet_path(data_root: Path) -> Path:
    return uci.normalized_directory(data_root) / "events.parquet"


def _normalized_manifest(data_root: Path) -> dict[str, object]:
    return json.loads(
        (uci.normalized_directory(data_root) / "manifest.json").read_text(
            encoding="utf-8"
        )
    )


def _write_manifest(path: Path, value: dict[str, object]) -> None:
    path.write_text(
        json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def test_iter_workbook_events_applies_boundary_and_preserves_physical_duplicates(
    tmp_path: Path,
    synthetic_source: SyntheticSource,
) -> None:
    workbook_path = tmp_path / uci.MEMBER_NAME
    workbook_path.write_bytes(synthetic_source.workbook_bytes)

    rows = list(uci.iter_workbook_events(workbook_path))
    events = [event for event, _numeric_description in rows]

    assert [
        (event["source_sheet"], event["source_row_number"])
        for event in events
    ] == [
        ("Year 2009-2010", 2),
        ("Year 2009-2010", 4),
        ("Year 2009-2010", 5),
        ("Year 2010-2011", 3),
        ("Year 2010-2011", 4),
        ("Year 2010-2011", 5),
    ]
    assert all(
        event["event_time_local"] < uci.CUTOFF
        for event in events
        if event["source_sheet"] == "Year 2009-2010"
    )
    assert all(
        event["event_time_local"] >= uci.CUTOFF
        for event in events
        if event["source_sheet"] == "Year 2010-2011"
    )
    # Repeated complete source tuples remain separate events by physical row.
    assert events[0] | {"event_id": None, "source_row_number": None} == events[2] | {
        "event_id": None,
        "source_row_number": None,
    }
    assert events[3] | {"event_id": None, "source_row_number": None} == events[5] | {
        "event_id": None,
        "source_row_number": None,
    }
    assert len({event["event_id"] for event in events}) == len(events) == 6
    assert sum(int(numeric) for _event, numeric in rows) == 1


def test_normalize_writes_exact_parquet_contract_and_manifest(
    normalized_root: Path,
    synthetic_source: SyntheticSource,
) -> None:
    parquet_path = _parquet_path(normalized_root)
    manifest = _normalized_manifest(normalized_root)
    parquet = pq.ParquetFile(parquet_path)
    table = parquet.read()

    assert parquet.schema_arrow == uci.EVENT_SCHEMA
    assert table.schema == uci.EVENT_SCHEMA
    assert table.num_rows == 6
    assert table.column("source_row_number").to_pylist() == [2, 4, 5, 3, 4, 5]
    assert table.column("description_observed").to_pylist() == [
        "  Widget observed  ",
        "12345",
        "  Widget observed  ",
        None,
        "  ",
        None,
    ]
    assert table.column("source_invoice_id").to_pylist() == [
        "100",
        "C001 ",
        "100",
        "C-RETURN",
        " INV-PRIVATE-ROW-99381 ",
        "C-RETURN",
    ]
    assert table.column("source_product_code").to_pylist() == [
        "200",
        " SKU-1 ",
        "200",
        "200",
        " SKU-WHITESPACE ",
        "200",
    ]
    assert table.column("quantity").to_pylist() == [
        80_995,
        -80_995,
        80_995,
        -1,
        0,
        -1,
    ]
    assert table.column("unit_price").to_pylist() == [
        Decimal("1.200"),
        Decimal("-1.125"),
        Decimal("1.200"),
        Decimal("0.000"),
        Decimal("3.141"),
        Decimal("0.000"),
    ]
    assert table.column("customer_reference").to_pylist() == [
        "300",
        None,
        "300",
        "400",
        None,
        "400",
    ]
    assert table.column("invoice_is_cancellation").to_pylist() == [
        False,
        True,
        False,
        True,
        False,
        True,
    ]
    assert table.column("currency_code").to_pylist() == ["GBP"] * 6
    assert table.column("schema_version").to_pylist() == [
        "transaction_event.v1"
    ] * 6
    assert manifest["artifact_id"] == synthetic_source.normalized_artifact_id
    assert manifest["dataset"]["row_count"] == 6
    assert manifest["profile"] == synthetic_source.expected_profile
    assert manifest["dataset"]["row_count"] == synthetic_source.expected_row_count
    assert {
        key: manifest["stitch"][key] for key in synthetic_source.expected_stitch
    } == synthetic_source.expected_stitch
    assert manifest["time_semantics"] == {
        "field": "event_time_local",
        "timezone": "unknown",
        "cutoff_inclusive": True,
    }
    assert manifest["capabilities"] == {
        "transaction_event_history": "supported",
        "marketplace_listing_state": "unsupported",
        "marketplace_supply_competition": "unsupported",
        "independent_external_demand": "unsupported",
        "complete_product_opportunity_universe": "unsupported",
        "integrated_productquant_v0_1": "unsupported",
        "historical_provider_revision_state": "unknown",
        "timezone": "unknown",
    }
    metadata = parquet.metadata
    assert metadata is not None
    assert metadata.format_version == uci.PARQUET_FORMAT_VERSION
    assert metadata.num_row_groups == 1
    for column_index in range(metadata.row_group(0).num_columns):
        column = metadata.row_group(0).column(column_index)
        assert column.compression == uci.PARQUET_COMPRESSION.upper()
        assert column.statistics is not None
    assert "RLE_DICTIONARY" in metadata.row_group(0).column(0).encodings
    if os.name == "posix":
        directory = uci.normalized_directory(normalized_root)
        assert stat.S_IMODE(directory.stat().st_mode) == 0o700
        assert stat.S_IMODE(parquet_path.stat().st_mode) == 0o600
        assert stat.S_IMODE((directory / "manifest.json").stat().st_mode) == 0o600


def test_duckdb_reads_values_and_enforces_as_of_filter_without_persistent_db(
    normalized_root: Path,
) -> None:
    parquet_path = _parquet_path(normalized_root)
    before = {path.name for path in normalized_root.rglob("*")}
    connection = duckdb.connect(":memory:")
    try:
        schema_rows = connection.execute(
            "DESCRIBE SELECT * FROM read_parquet(?)", [str(parquet_path)]
        ).fetchall()
        point_in_time = connection.execute(
            """
            SELECT
              count(*) FILTER (WHERE event_time_local <= ?) AS known_at_cutoff,
              count(*) FILTER (WHERE event_time_local > ?) AS future_after_cutoff,
              count(*) FILTER (
                WHERE source_sheet = 'Year 2009-2010'
                  AND event_time_local >= ?
              ) AS invalid_first,
              count(*) FILTER (
                WHERE source_sheet = 'Year 2010-2011'
                  AND event_time_local < ?
              ) AS invalid_second
            FROM read_parquet(?)
            """,
            [uci.CUTOFF, uci.CUTOFF, uci.CUTOFF, uci.CUTOFF, str(parquet_path)],
        ).fetchone()
    finally:
        connection.close()

    assert [row[0] for row in schema_rows] == uci.EVENT_SCHEMA.names
    assert point_in_time == (5, 1, 0, 0)
    assert {path.name for path in normalized_root.rglob("*")} == before
    assert not list(normalized_root.rglob("*.duckdb"))


def test_normalize_and_verify_are_idempotent_without_rewriting_artifacts(
    normalized_root: Path,
) -> None:
    parquet_path = _parquet_path(normalized_root)
    manifest_path = uci.normalized_directory(normalized_root) / "manifest.json"
    before = (
        uci.sha256_file(parquet_path),
        parquet_path.stat().st_mtime_ns,
        manifest_path.read_bytes(),
        manifest_path.stat().st_mtime_ns,
    )

    normalized = uci.normalize(normalized_root)
    verified = uci.verify(normalized_root)

    assert normalized["action"] == "verified"
    assert verified["raw"]["action"] == "verified"
    assert verified["normalized"]["action"] == "verified"
    assert verified["statistics"]["unique_event_ids"] == 6
    assert (
        uci.sha256_file(parquet_path),
        parquet_path.stat().st_mtime_ns,
        manifest_path.read_bytes(),
        manifest_path.stat().st_mtime_ns,
    ) == before


def test_same_source_rebuild_has_deterministic_parquet_bytes(
    tmp_path: Path,
    synthetic_source: SyntheticSource,
    mocked_download: list[str],
) -> None:
    roots = [tmp_path / "one", tmp_path / "two"]
    digests: list[str] = []
    schemas: list[pa.Schema] = []
    for root in roots:
        uci.fetch(root)
        uci.normalize(root)
        path = _parquet_path(root)
        digests.append(uci.sha256_file(path))
        schemas.append(pq.ParquetFile(path).schema_arrow)

    assert len(mocked_download) == 2
    assert digests[0] == digests[1]
    assert schemas == [uci.EVENT_SCHEMA, uci.EVENT_SCHEMA]


def test_normalize_rejects_invalid_existing_target_without_overwriting(
    fetched_root: Path,
) -> None:
    destination = uci.normalized_directory(fetched_root)
    destination.mkdir(parents=True)
    sentinel = destination / "do-not-overwrite.txt"
    sentinel.write_text("preserve me", encoding="utf-8")

    with pytest.raises(IntegrityError, match="bundle contents differ"):
        uci.normalize(fetched_root)

    assert sentinel.read_text(encoding="utf-8") == "preserve me"


def test_verify_rejects_parquet_hash_drift_before_querying(
    normalized_root: Path,
) -> None:
    parquet_path = _parquet_path(normalized_root)
    original = parquet_path.read_bytes()
    parquet_path.write_bytes(original + b"drift")

    with pytest.raises(IntegrityError, match="byte count differs"):
        uci.verify_normalized_bundle(normalized_root)


def test_verify_rejects_parquet_schema_drift_even_with_updated_file_digest(
    normalized_root: Path,
) -> None:
    directory = uci.normalized_directory(normalized_root)
    parquet_path = directory / "events.parquet"
    manifest_path = directory / "manifest.json"
    table = pq.read_table(parquet_path).drop(["customer_reference"])
    pq.write_table(table, parquet_path, compression="zstd", version="2.6")
    manifest = _normalized_manifest(normalized_root)
    manifest["dataset"]["bytes"] = parquet_path.stat().st_size
    manifest["dataset"]["sha256"] = uci.sha256_file(parquet_path)
    _write_manifest(manifest_path, manifest)

    with pytest.raises(IntegrityError, match="schema differs"):
        uci.verify_normalized_bundle(normalized_root)


def test_verify_rejects_manifest_profile_or_capability_drift(
    normalized_root: Path,
) -> None:
    directory = uci.normalized_directory(normalized_root)
    manifest_path = directory / "manifest.json"
    manifest = _normalized_manifest(normalized_root)
    manifest["capabilities"]["marketplace_listing_state"] = "supported"
    _write_manifest(manifest_path, manifest)

    with pytest.raises(IntegrityError, match="capability declarations"):
        uci.verify_normalized_bundle(normalized_root)


def test_verify_rejects_normalized_profile_tampering(
    normalized_root: Path,
) -> None:
    directory = uci.normalized_directory(normalized_root)
    manifest_path = directory / "manifest.json"
    manifest = _normalized_manifest(normalized_root)
    manifest["profile"]["unique_invoices"] = 5
    _write_manifest(manifest_path, manifest)

    with pytest.raises(IntegrityError, match="profile.*differs|invariant differs"):
        uci.verify_normalized_bundle(normalized_root)


def test_stale_staging_directory_is_never_treated_as_normalized_artifact(
    fetched_root: Path,
) -> None:
    destination = uci.normalized_directory(fetched_root)
    stale = destination.parent / ".transaction-event-v1.part-interrupted"
    stale.mkdir(parents=True)
    (stale / "events.parquet").write_bytes(b"interrupted")

    result = uci.normalize(fetched_root)

    assert result["action"] == "created"
    assert uci.verify_normalized_bundle(fetched_root)["dataset"]["row_count"] == 6
    assert (stale / "events.parquet").read_bytes() == b"interrupted"


def test_atomic_publication_failure_leaves_no_final_bundle(
    fetched_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    if not hasattr(uci, "atomic_publish_directory"):
        pytest.fail("production must expose the accepted atomic publication seam")

    def fail_publish(_stage: Path, _destination: Path) -> None:
        raise StateError("injected atomic publication failure")

    monkeypatch.setattr(uci, "atomic_publish_directory", fail_publish)
    destination = uci.normalized_directory(fetched_root)

    with pytest.raises(StateError, match="injected atomic publication failure"):
        uci.normalize(fetched_root)

    assert not destination.exists()
    assert not list(destination.parent.glob(".transaction-event-v1.part-*"))


def test_parquet_write_failure_never_publishes_normalized_bundle(
    fetched_root: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_writer = uci.pq.ParquetWriter

    class FailingParquetWriter:
        def __init__(self, *args: object, **kwargs: object) -> None:
            self.writer = original_writer(*args, **kwargs)

        def write_table(self, *args: object, **kwargs: object) -> None:
            self.writer.write_table(*args, **kwargs)
            raise OSError("injected Parquet write failure")

        def close(self) -> None:
            self.writer.close()

    monkeypatch.setattr(uci.pq, "ParquetWriter", FailingParquetWriter)
    destination = uci.normalized_directory(fetched_root)

    with pytest.raises(OSError, match="injected Parquet write failure"):
        uci.normalize(fetched_root)

    assert not destination.exists()
    assert not list(destination.parent.glob(".transaction-event-v1.part-*"))


@pytest.mark.skipif(os.name != "posix", reason="symlink rejection contract")
def test_normalized_bundle_rejects_symlink_parquet(
    normalized_root: Path,
    tmp_path: Path,
) -> None:
    parquet_path = _parquet_path(normalized_root)
    parquet_copy = tmp_path / "events-copy.parquet"
    parquet_copy.write_bytes(parquet_path.read_bytes())
    parquet_path.unlink()
    parquet_path.symlink_to(parquet_copy)

    with pytest.raises(IntegrityError, match="not a real regular file"):
        uci.verify_normalized_bundle(normalized_root)


def test_normalized_manifests_do_not_contain_transaction_or_customer_rows(
    normalized_root: Path,
) -> None:
    raw_manifest = (uci.raw_directory(normalized_root) / "manifest.json").read_text(
        encoding="utf-8"
    )
    normalized_manifest = (
        uci.normalized_directory(normalized_root) / "manifest.json"
    ).read_text(encoding="utf-8")
    serialized = raw_manifest + normalized_manifest

    assert "INV-PRIVATE-ROW-99381" not in serialized
    assert "SKU-WHITESPACE" not in serialized
    assert '"400"' not in serialized
