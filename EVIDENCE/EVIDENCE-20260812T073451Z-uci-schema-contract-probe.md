# UCI Schema and Precision Contract Probe

## Metadata

- **ID:** `EVIDENCE-20260812T073451Z-uci-schema-contract-probe`
- **Title:** `UCI workbook required-field, type, and decimal precision validation`
- **Captured UTC:** `2026-08-12T07:34:51Z`
- **Recorded by:** `agent:codex-phase1`
- **Claim supported or challenged:** The pinned UCI workbook can be represented losslessly by the accepted `transaction_event.v1` required/null/type and `decimal128(18,3)` rules after the specified stitch.
- **Related requirements:** [`PROJECT_SPEC.md` Restricted Phase 1](../PROJECT_SPEC.md#restricted-phase-1--uci-transaction-event-data-foundation)
- **Related ADRs/issues:** [`ADR-20260812T072420Z-uci-transaction-data-foundation`](../ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md); [`ISSUE-20260812T072420Z-uci-transaction-data-foundation`](../ISSUES/ISSUE-20260812T072420Z-uci-transaction-data-foundation.md)
- **Repository revision/state:** Base `9efee6d17735b1bb1c9d11a2bd720a64bc617499` plus uncommitted Phase 1 authority records; no implementation.
- **Environment:** Darwin 25.3.0 arm64; Python 3.9.6; openpyxl 3.1.5; pinned workbook `/tmp/productquant-recovery.RrGEIv/online_retail_II.xlsx`, SHA-256 `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`.

## Method

- **Procedure:** Open the complete workbook with `read_only=True` and `data_only=True`; require the exact eight headers; scan every physical row; count nulls and Python cell types by field; reject fractional numeric identifiers or quantities; count timezone-aware datetimes; and derive decimal scale from `Decimal(str(Price))` without persisting row values.
- **Exact command/input:** The complete aggregate-only probe was:

```bash
python3 - <<'PY'
from collections import Counter
from datetime import datetime
from decimal import Decimal
from openpyxl import load_workbook

path = "/tmp/productquant-recovery.RrGEIv/online_retail_II.xlsx"
workbook = load_workbook(path, read_only=True, data_only=True)
expected = (
    "Invoice", "StockCode", "Description", "Quantity",
    "InvoiceDate", "Price", "Customer ID", "Country",
)
summary = {}
for sheet in workbook.worksheets:
    rows = sheet.iter_rows(values_only=True)
    header = tuple(next(rows))
    assert header == expected, (sheet.title, header)
    nulls = Counter()
    types = {name: Counter() for name in expected}
    scales = Counter()
    invalid_quantities = []
    invalid_identifiers = []
    aware_times = 0
    row_count = 0
    for row_number, row in enumerate(rows, start=2):
        row_count += 1
        for name, value in zip(expected, row):
            if value is None:
                nulls[name] += 1
            else:
                types[name][type(value).__name__] += 1
        quantity = row[3]
        if not isinstance(quantity, int) and not (
            isinstance(quantity, float) and quantity.is_integer()
        ):
            invalid_quantities.append((row_number, repr(quantity)))
        event_time = row[4]
        if isinstance(event_time, datetime) and event_time.tzinfo is not None:
            aware_times += 1
        price = row[5]
        if price is not None:
            decimal_price = Decimal(str(price))
            scales[max(0, -decimal_price.as_tuple().exponent)] += 1
        for index in (0, 1, 6):
            value = row[index]
            if isinstance(value, float) and not value.is_integer():
                invalid_identifiers.append(
                    (row_number, expected[index], repr(value))
                )
    summary[sheet.title] = {
        "rows": row_count,
        "nulls": dict(nulls),
        "types": {name: dict(counts) for name, counts in types.items()},
        "price_scales": dict(scales),
        "invalid_qty": invalid_quantities[:5],
        "invalid_identifiers": invalid_identifiers[:5],
        "aware_times": aware_times,
    }
workbook.close()

import json
print(json.dumps(summary, indent=2, sort_keys=True))
PY
```
- **Exit status:** `0`
- **Repeatability:** Verify the workbook digest above, install openpyxl 3.1.5, and repeat the described complete row scan. A source or dependency change requires a new evidence record.

## Raw observation

```text
Year 2009-2010 rows: 525,461
Year 2010-2011 rows: 541,910

Nulls:
  Description: 2,928 / 1,454
  Customer ID: 107,927 / 135,080
  all other fields: 0 / 0

Cell types by sheet:
  Invoice: int 515,252 + str 10,209 / int 532,619 + str 9,291
  StockCode: int 445,349 + str 80,112 / int 487,036 + str 54,874
  Description: int 3 + str 522,530 + null 2,928 /
               int 1 + str 540,455 + null 1,454
  Quantity: int 525,461 / int 541,910
  InvoiceDate: datetime 525,461 / datetime 541,910
  Price: int 5,520 + float 519,941 / int 4,504 + float 537,406
  Customer ID: int 417,534 + null 107,927 /
               int 406,830 + null 135,080
  Country: str 525,461 / str 541,910

Observed decimal scales from Decimal(str(Price)):
  scale 0: 5,520 / 4,504
  scale 1: 35,723 / 26,770
  scale 2: 484,204 / 510,632
  scale 3: 14 / 4
  scale >3: 0 / 0

Fractional numeric identifiers: 0
Non-integral quantities: 0
Timezone-aware InvoiceDate values: 0
```

## Interpretation

- **CONFIRMED:** Only `Description` and `Customer ID` are null in the pinned workbook; every Phase 1-required source field is populated.
- **CONFIRMED:** All quantities and numeric source identifiers are integral, so the contract's exact int64/base-10 conversions require no rounding.
- **CONFIRMED:** All prices observed through `Decimal(str(value))` have scale at most three and fit the previously observed magnitude, supporting lossless `decimal128(18,3)` conversion for this pinned source version.
- **CONFIRMED:** All source event times are naïve Python datetimes. This supports the no-timezone representation but does not establish the real-world timezone.
- **CONFIRMED:** Exactly four non-null descriptions are numeric cells and require the documented explicit integral-text representation.
- **UNKNOWN:** A different UCI artifact or different workbook parser could expose different cell types/precision; digest and dependency pinning plus fail-closed validation are required.

## Limitations and residual uncertainty

- This probe validates physical source values and types, not the future PyArrow/Parquet implementation.
- Excel numeric cells are already decoded by openpyxl; the raw OOXML remains the ultimate byte-preserved evidence.
- Customer IDs are pseudonymous source references. The probe records only aggregate type/null counts, not any identifier value.
- The provider's timezone and historical revision/publication semantics remain unknown.

## Integrity and provenance

- **Artifact location:** Official URL recorded in Phase 0; validated transient workbook path above, excluded from Git.
- **Artifact digest:** SHA-256 `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`.
- **External retention risk:** Official artifact may change or disappear; the accepted pipeline preserves the pinned ZIP locally.
- **Supersedes / superseded by:** Complements, but does not supersede, [`EVIDENCE-20260812T060103Z-historical-dataset-probes`](EVIDENCE-20260812T060103Z-historical-dataset-probes.md).

## Corrections

| UTC time | Participant | Correction | Reason and supporting evidence |
|---|---|---|---|
| `NONE` | `NONE` | `NONE` | `NONE` |
