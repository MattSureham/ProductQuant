from __future__ import annotations

import json
from pathlib import Path

from productquant import uci


CONTRACT_DIRECTORY = Path(uci.__file__).parent / "contracts"


def _contract(name: str) -> dict[str, object]:
    value = json.loads((CONTRACT_DIRECTORY / name).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_transaction_event_contract_matches_runtime_arrow_schema() -> None:
    contract = _contract("transaction-event.v1.json")
    fields = contract["fields"]

    assert [field["name"] for field in fields] == uci.EVENT_SCHEMA.names
    assert [field["nullable"] for field in fields] == [
        field.nullable for field in uci.EVENT_SCHEMA
    ]
    assert [field["type"] for field in fields] == [
        str(field.type).replace(", ", ",") for field in uci.EVENT_SCHEMA
    ]
    assert contract["constants"] == {
        "currency_code": "GBP",
        "schema_version": uci.EVENT_SCHEMA_VERSION,
        "source_id": uci.SOURCE_ID,
        "source_member": uci.MEMBER_NAME,
    }
    assert contract["event_id"]["sheet_tokens"] == uci.SHEET_TOKENS
    assert contract["point_in_time"]["as_of_rule"].endswith(
        "event_time_local <= t."
    )
    assert "inclusive signed-int64 range" in contract["coercion"]["quantity"]


def test_source_contract_matches_pinned_runtime_and_full_data_invariants() -> None:
    contract = _contract("uci-online-retail-ii.v1.json")
    expected_full_data = {
        **uci.EXPECTED_PROFILE,
        **uci.EXPECTED_STITCH,
        "row_count": uci.EXPECTED_DATASET_ROW_COUNT,
    }

    assert contract["source"]["id"] == uci.SOURCE_ID
    assert contract["source"]["download_url"] == uci.SOURCE_URL
    assert contract["archive"] == {
        "bytes": uci.ARCHIVE_BYTES,
        "member_count": 1,
        "path": uci.ARCHIVE_NAME,
        "sha256": uci.ARCHIVE_SHA256,
    }
    assert contract["member"] == {
        "bytes": uci.MEMBER_BYTES,
        "name": uci.MEMBER_NAME,
        "sha256": uci.MEMBER_SHA256,
    }
    assert contract["artifact_identifiers"] == {
        "raw_artifact_id": uci.RAW_ARTIFACT_ID,
        "normalized_artifact_id": uci.NORMALIZED_ARTIFACT_ID,
    }
    assert contract["workbook_schema"]["headers"] == list(uci.HEADERS)
    assert contract["workbook_schema"]["sheet_order"] == list(uci.SHEETS)
    assert "reject formula or Excel-error cells" in contract["workbook_schema"][
        "cell_type_policy"
    ]
    assert contract["full_data_invariants"] == expected_full_data


def test_manifest_contract_keeps_dataset_stitch_and_profile_ownership_distinct() -> None:
    contract = _contract("artifact-manifests.v1.json")
    normalized = contract["normalized_manifest"]

    assert normalized["dataset"]["required_keys"] == [
        "path",
        "bytes",
        "sha256",
        "row_count",
        "pyarrow_schema",
    ]
    assert set(normalized["profile_keys"]) == set(uci.EXPECTED_PROFILE)
    assert normalized["stitch"] == {
        "rule_id": uci.STITCH_RULE_ID,
        "cutoff_local": uci.CUTOFF.isoformat(timespec="microseconds"),
        **uci.EXPECTED_STITCH,
    }
    assert normalized["fixed_values"]["artifact_id"] == uci.NORMALIZED_ARTIFACT_ID
    assert normalized["build"] == {
        "dependency_version_keys": ["duckdb", "openpyxl", "pyarrow"],
        "parquet_compression": uci.PARQUET_COMPRESSION,
        "required_keys": [
            "built_at_utc",
            "git_revision",
            "git_dirty",
            "python_version",
            "dependency_versions",
            "parquet_compression",
            "row_group_size",
        ],
        "row_group_size": uci.PARQUET_ROW_GROUP_SIZE,
    }
    assert contract["parquet_writer_configuration"] == {
        "emitted_in_normalized_manifest": False,
        "parquet_format_version": uci.PARQUET_FORMAT_VERSION,
        "use_dictionary": uci.PARQUET_USE_DICTIONARY,
        "write_statistics": uci.PARQUET_WRITE_STATISTICS,
    }
    assert contract["publication"]["in_worktree_data_root"].startswith(
        "the data-root directory itself must be matched"
    )
    assert contract["raw_manifest"]["fixed_values"] == {
        "adapter_version": uci.ADAPTER_VERSION,
        "artifact_id": uci.RAW_ARTIFACT_ID,
        "raw_response_reference": uci.ARCHIVE_NAME,
        "schema_version": uci.RAW_MANIFEST_SCHEMA,
    }
    assert set(contract["raw_manifest"]["required_keys"]) == {
        "schema_version",
        "artifact_id",
        "source",
        "retrieval",
        "archive",
        "member",
        "adapter_version",
        "raw_response_reference",
        "capabilities",
    }
    assert contract["raw_manifest"]["capabilities"] == uci.CAPABILITIES


def test_receipt_contract_matches_supported_cli_and_exit_codes() -> None:
    contract = _contract("command-receipt.v1.json")

    assert contract["receipt"]["schema_version"] == uci.RECEIPT_SCHEMA
    assert contract["cli"]["commands"] == [
        "uci.fetch",
        "uci.normalize",
        "uci.verify",
        "uci.prepare",
    ]
    assert contract["cli"]["exit_codes"] == {
        "success": 0,
        "unexpected_internal_failure": 1,
        "usage_error": 2,
        "network_failure": 3,
        "integrity_or_schema_drift": 4,
        "local_io_or_state_conflict": 5,
    }
    assert contract["privacy"]["forbidden_content"] == [
        "transaction row values",
        "customer-reference values",
        "raw response bodies",
    ]
    assert contract["receipt"]["failure_progress"].startswith(
        "A failed multi-step command preserves"
    )
