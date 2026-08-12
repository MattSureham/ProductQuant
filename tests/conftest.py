from __future__ import annotations

import hashlib
import io
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pytest
from openpyxl import Workbook

from productquant import uci


HEADERS = (
    "Invoice",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "Price",
    "Customer ID",
    "Country",
)


@dataclass(frozen=True)
class SyntheticSource:
    archive_bytes: bytes
    workbook_bytes: bytes
    archive_sha256: str
    workbook_sha256: str
    raw_artifact_id: str
    normalized_artifact_id: str
    expected_row_count: int
    expected_stitch: dict[str, int]
    expected_profile: dict[str, Any]


class FakeResponse(io.BytesIO):
    def __init__(
        self,
        body: bytes,
        *,
        final_url: str = "https://fixtures.invalid/online-retail-ii.zip",
        status: int = 200,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(body)
        self._final_url = final_url
        self.status = status
        self.headers = headers or {
            "Content-Type": "application/zip",
            "Content-Length": str(len(body)),
            "ETag": '"synthetic-etag"',
            "Last-Modified": "Wed, 12 Aug 2026 00:00:00 GMT",
            "X-Private-Header": "must-not-be-persisted",
        }

    def geturl(self) -> str:
        return self._final_url

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *_args: object) -> None:
        self.close()


@pytest.fixture
def full_data_root(request: pytest.FixtureRequest) -> Path:
    return Path(request.config.getoption("--data-root")).resolve()


def _workbook_bytes(
    *,
    headers: tuple[str, ...] = HEADERS,
    sheets: tuple[str, str] = ("Year 2009-2010", "Year 2010-2011"),
) -> bytes:
    workbook = Workbook()
    first = workbook.active
    first.title = sheets[0]
    second = workbook.create_sheet(sheets[1])
    first.append(headers)
    second.append(headers)

    # First-sheet rows at or after the cutoff are intentionally excluded.
    duplicate_before_cutoff = (
        100,
        200,
        "  Widget observed  ",
        80_995,
        datetime(2010, 11, 30, 23, 59, 59),
        1.2,
        300,
        "United Kingdom",
    )
    first.append(duplicate_before_cutoff)
    first.append(
        (
            "DROP-FIRST",
            "DROP-SKU",
            "excluded at boundary",
            1,
            datetime(2010, 12, 1),
            2,
            None,
            "United Kingdom",
        )
    )
    first.append(
        (
            "C001 ",
            " SKU-1 ",
            12345,
            -80_995,
            datetime(2010, 11, 30, 12),
            -1.125,
            None,
            "EIRE",
        )
    )
    first.append(duplicate_before_cutoff)

    # Second-sheet rows before the cutoff are intentionally excluded. Exact
    # boundary rows are retained, including a repeated physical row.
    second.append(
        (
            "DROP-SECOND",
            "DROP-SKU",
            "excluded before boundary",
            1,
            datetime(2010, 11, 30, 23, 59, 59),
            2,
            None,
            "France",
        )
    )
    duplicate_at_cutoff = (
        "C-RETURN",
        200,
        None,
        -1,
        datetime(2010, 12, 1),
        0,
        400,
        "France",
    )
    second.append(duplicate_at_cutoff)
    second.append(
        (
            " INV-PRIVATE-ROW-99381 ",
            " SKU-WHITESPACE ",
            "  ",
            0,
            datetime(2010, 12, 2, 1, 2, 3),
            3.141,
            None,
            " France ",
        )
    )
    second.append(duplicate_at_cutoff)

    output = io.BytesIO()
    workbook.save(output)
    workbook.close()
    return output.getvalue()


def make_archive(
    workbook_bytes: bytes,
    *,
    member_name: str = "online_retail_II.xlsx",
) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(member_name, workbook_bytes)
    return output.getvalue()


@pytest.fixture
def synthetic_source(monkeypatch: pytest.MonkeyPatch) -> SyntheticSource:
    workbook_bytes = _workbook_bytes()
    archive_bytes = make_archive(workbook_bytes)
    archive_sha256 = hashlib.sha256(archive_bytes).hexdigest()
    workbook_sha256 = hashlib.sha256(workbook_bytes).hexdigest()
    raw_artifact_id = f"uci-online-retail-ii:sha256:{archive_sha256}"
    normalized_artifact_id = f"{raw_artifact_id}:transaction-event.v1"
    expected_row_count = 6
    expected_stitch = {
        "first_sheet_input": 4,
        "first_sheet_retained": 3,
        "second_sheet_input": 4,
        "second_sheet_retained": 3,
        "excluded_cross_sheet_rows": 2,
    }
    expected_profile = {
        "event_time_min": "2010-11-30T12:00:00.000000",
        "event_time_max": "2010-12-02T01:02:03.000000",
        "unique_event_ids": 6,
        "unique_stock_codes": 3,
        "unique_invoices": 4,
        "cancellation_rows": 3,
        "negative_quantity_rows": 3,
        "zero_price_rows": 2,
        "negative_price_rows": 1,
        "missing_description_rows": 2,
        "missing_customer_rows": 2,
        "numeric_description_rows": 1,
        "quantity_min": -80_995,
        "quantity_max": 80_995,
        "unit_price_min": "-1.125",
        "unit_price_max": "3.141",
    }

    replacements = {
        "SOURCE_URL": "https://fixtures.invalid/online-retail-ii.zip",
        "ARCHIVE_BYTES": len(archive_bytes),
        "ARCHIVE_SHA256": archive_sha256,
        "MEMBER_BYTES": len(workbook_bytes),
        "MEMBER_SHA256": workbook_sha256,
        "RAW_ARTIFACT_ID": raw_artifact_id,
        "NORMALIZED_ARTIFACT_ID": normalized_artifact_id,
        "EXPECTED_DATASET_ROW_COUNT": expected_row_count,
        "EXPECTED_STITCH": expected_stitch,
        "EXPECTED_PROFILE": expected_profile,
    }
    for name, value in replacements.items():
        monkeypatch.setattr(uci, name, value)

    return SyntheticSource(
        archive_bytes=archive_bytes,
        workbook_bytes=workbook_bytes,
        archive_sha256=archive_sha256,
        workbook_sha256=workbook_sha256,
        raw_artifact_id=raw_artifact_id,
        normalized_artifact_id=normalized_artifact_id,
        expected_row_count=expected_row_count,
        expected_stitch=expected_stitch,
        expected_profile=expected_profile,
    )


@pytest.fixture
def mocked_download(
    monkeypatch: pytest.MonkeyPatch,
    synthetic_source: SyntheticSource,
) -> list[str]:
    calls: list[str] = []

    def open_response(request: Any, *, timeout: int) -> FakeResponse:
        calls.append(request.full_url)
        assert timeout == 60
        return FakeResponse(synthetic_source.archive_bytes)

    monkeypatch.setattr(uci.urllib.request, "urlopen", open_response)
    return calls


@pytest.fixture
def fetched_root(
    tmp_path: Path,
    synthetic_source: SyntheticSource,
    mocked_download: list[str],
) -> Path:
    data_root = tmp_path / "data"
    result = uci.fetch(data_root)
    assert result["action"] == "created"
    assert mocked_download == [uci.SOURCE_URL]
    return data_root


@pytest.fixture
def normalized_root(fetched_root: Path) -> Path:
    result = uci.normalize(fetched_root)
    assert result["action"] == "created"
    return fetched_root
