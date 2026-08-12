from __future__ import annotations

import json
from pathlib import Path

import duckdb
import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from productquant import uci


@pytest.mark.full_data
def test_pinned_official_uci_artifacts_pass_full_acceptance(
    full_data_root: Path,
) -> None:
    raw_directory = uci.raw_directory(full_data_root)
    normalized_directory = uci.normalized_directory(full_data_root)
    required = (
        raw_directory / uci.ARCHIVE_NAME,
        raw_directory / "manifest.json",
        normalized_directory / "events.parquet",
        normalized_directory / "manifest.json",
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        pytest.fail(
            "full-data acceptance requires complete canonical ignored bundles; "
            f"missing {missing}. Run: productquant uci prepare --data-root "
            f"{full_data_root}"
        )

    result = uci.verify(full_data_root)
    raw_manifest = json.loads((raw_directory / "manifest.json").read_text())
    normalized_manifest = json.loads(
        (normalized_directory / "manifest.json").read_text()
    )

    assert result["raw"]["artifact_id"] == (
        "uci-online-retail-ii:sha256:"
        "572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb"
    )
    assert result["normalized"]["artifact_id"] == (
        "uci-online-retail-ii:sha256:"
        "572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb:"
        "transaction-event.v1"
    )
    assert raw_manifest["archive"] == {
        "path": "online-retail-ii.zip",
        "bytes": 45_622_418,
        "sha256": "572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb",
    }
    assert raw_manifest["member"] == {
        "name": "online_retail_II.xlsx",
        "bytes": 45_622_278,
        "sha256": "bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980",
    }
    expected_profile = {
        "event_time_min": "2009-12-01T07:45:00.000000",
        "event_time_max": "2011-12-09T12:50:00.000000",
        "unique_event_ids": 1_044_848,
        "unique_stock_codes": 5_305,
        "unique_invoices": 53_628,
        "cancellation_rows": 19_165,
        "negative_quantity_rows": 22_557,
        "zero_price_rows": 6_024,
        "negative_price_rows": 5,
        "missing_description_rows": 4_275,
        "missing_customer_rows": 235_287,
        "numeric_description_rows": 4,
        "quantity_min": -80_995,
        "quantity_max": 80_995,
        "unit_price_min": "-53594.360",
        "unit_price_max": "38970.000",
    }
    assert result["statistics"] == normalized_manifest["profile"]
    assert result["statistics"] == expected_profile
    assert normalized_manifest["dataset"]["row_count"] == 1_044_848
    assert {
        key: normalized_manifest["stitch"][key]
        for key in (
            "first_sheet_input",
            "first_sheet_retained",
            "second_sheet_input",
            "second_sheet_retained",
            "excluded_cross_sheet_rows",
        )
    } == {
        "first_sheet_input": 525_461,
        "first_sheet_retained": 502_938,
        "second_sheet_input": 541_910,
        "second_sheet_retained": 541_910,
        "excluded_cross_sheet_rows": 22_523,
    }
    assert normalized_manifest["capabilities"] == {
        "transaction_event_history": "supported",
        "marketplace_listing_state": "unsupported",
        "marketplace_supply_competition": "unsupported",
        "independent_external_demand": "unsupported",
        "complete_product_opportunity_universe": "unsupported",
        "integrated_productquant_v0_1": "unsupported",
        "historical_provider_revision_state": "unknown",
        "timezone": "unknown",
    }

    parquet_path = normalized_directory / "events.parquet"
    expected_schema = pa.schema(
        [
            pa.field("event_id", pa.string(), nullable=False),
            pa.field("raw_artifact_id", pa.string(), nullable=False),
            pa.field("source_id", pa.string(), nullable=False),
            pa.field("source_member", pa.string(), nullable=False),
            pa.field("source_sheet", pa.string(), nullable=False),
            pa.field("source_row_number", pa.int64(), nullable=False),
            pa.field("event_time_local", pa.timestamp("us"), nullable=False),
            pa.field("source_invoice_id", pa.string(), nullable=False),
            pa.field("source_product_code", pa.string(), nullable=False),
            pa.field("description_observed", pa.string(), nullable=True),
            pa.field("quantity", pa.int64(), nullable=False),
            pa.field("unit_price", pa.decimal128(18, 3), nullable=False),
            pa.field("currency_code", pa.string(), nullable=False),
            pa.field("customer_reference", pa.string(), nullable=True),
            pa.field("country_observed", pa.string(), nullable=False),
            pa.field("invoice_is_cancellation", pa.bool_(), nullable=False),
            pa.field("schema_version", pa.string(), nullable=False),
        ]
    )
    assert pq.ParquetFile(parquet_path).schema_arrow == expected_schema
    connection = duckdb.connect(":memory:")
    try:
        point_in_time = connection.execute(
            """
            SELECT
              count(*)::BIGINT,
              count(DISTINCT event_id)::BIGINT,
              count(*) FILTER (
                WHERE source_sheet = 'Year 2009-2010'
                  AND event_time_local >= TIMESTAMP '2010-12-01'
              )::BIGINT,
              count(*) FILTER (
                WHERE source_sheet = 'Year 2010-2011'
                  AND event_time_local < TIMESTAMP '2010-12-01'
              )::BIGINT
            FROM read_parquet(?)
            """,
            [str(parquet_path)],
        ).fetchone()
    finally:
        connection.close()

    assert point_in_time == (1_044_848, 1_044_848, 0, 0)
    assert not list(full_data_root.rglob("*.duckdb"))
