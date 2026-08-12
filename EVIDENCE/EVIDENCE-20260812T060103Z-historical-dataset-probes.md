# Historical Dataset Download and Schema Probes

## Metadata

- **ID:** `EVIDENCE-20260812T060103Z-historical-dataset-probes`
- **Title:** `Historical bootstrap dataset accessibility, integrity, and time semantics`
- **Captured UTC:** `2026-08-12T06:04:56Z`
- **Recorded by:** `agent:codex-phase0-recovery`
- **Claim supported or challenged:** UCI Online Retail II can support a genuine transaction-event backtest, while Olist and Amazon Reviews 2023 have licensing or point-in-time limitations that prevent their default adoption.
- **Related requirements:** [`PROJECT_SPEC.md` sections 18, 21, 40–42, 50–51, and 53](../PROJECT_SPEC.md)
- **Related ADRs/issues:** [`ISSUE-20260812T031400Z-phase-0-source-feasibility`](../ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md)
- **Repository revision/state:** Base revision `3ff8644ca6cf01feb43e25aadb6ef6d23d094cf1` on `main`; pre-existing modified `HANDOFF.md` and untracked Phase 0 issue; probe artifacts remained under `/tmp` and were not added to the repository.
- **Environment:** Darwin 25.3.0 arm64; curl 8.7.1; Info-ZIP 6.00; Python 3.9.6; openpyxl 3.1.5; no authenticated account or private credential used.

## Method

- **Procedure:** Recheck official landing pages and unauthenticated download endpoints; validate downloaded archives; compute SHA-256 digests; stream the UCI workbook and Olist CSVs to inspect schemas, row counts, event-time ranges, missingness, cancellations, and timestamp outliers; range-download a public Amazon Reviews file and inspect only its field names and timestamps.
- **Exact command/input:**

```bash
curl -sS -o /dev/null -w 'UCI page HTTP %{http_code} content_type=%{content_type}\n' \
  'https://archive.ics.uci.edu/dataset/502/online+retail+ii'
curl -sS -o /dev/null -w 'UCI archive HTTP %{http_code} size=%{size_download}\n' -r 0-0 \
  'https://cdn.uci-ics-mlr-prod.aws.uci.edu/502/online%2Bretail%2Bii.zip'
unzip -t /tmp/productquant-recovery.RrGEIv/online-retail-ii.zip
unzip -l /tmp/productquant-recovery.RrGEIv/online-retail-ii.zip
shasum -a 256 /tmp/productquant-recovery.RrGEIv/online-retail-ii.zip
wc -c /tmp/productquant-recovery.RrGEIv/online-retail-ii.zip
```

```bash
curl -sS 'https://www.kaggle.com/api/v1/datasets/view/olistbr/brazilian-ecommerce' |
  jq '{title,subtitle,licenseName,ownerName,totalBytes,lastUpdated}'
unzip -t /tmp/productquant-recovery.RrGEIv/olist.zip
unzip -l /tmp/productquant-recovery.RrGEIv/olist.zip
shasum -a 256 /tmp/productquant-recovery.RrGEIv/olist.zip
wc -c /tmp/productquant-recovery.RrGEIv/olist.zip
```

```bash
curl -sS -r 0-1048575 \
  -o /tmp/productquant-recovery.RrGEIv/amazon-all-beauty.range \
  'https://mcauleylab.ucsd.edu/public_datasets/data/amazon_2023/raw/review_categories/All_Beauty.jsonl.gz'
wc -c /tmp/productquant-recovery.RrGEIv/amazon-all-beauty.range
shasum -a 256 /tmp/productquant-recovery.RrGEIv/amazon-all-beauty.range
```

```bash
python3 - <<'PY'
from collections import Counter
from datetime import datetime
from openpyxl import load_workbook

workbook = load_workbook(
    "/tmp/productquant-recovery.RrGEIv/online_retail_II.xlsx",
    read_only=True,
    data_only=True,
)
counters = []
for sheet in workbook.worksheets:
    rows = sheet.iter_rows(values_only=True)
    header = next(rows)
    time_index = header.index("InvoiceDate")
    overlap = [
        tuple(row)
        for row in rows
        if isinstance(row[time_index], datetime)
        and datetime(2010, 12, 1) <= row[time_index] < datetime(2010, 12, 10)
    ]
    counter = Counter(overlap)
    counters.append(counter)
    print(sheet.title, len(overlap), len(counter), sum(value - 1 for value in counter.values()))
print("counter_equal", counters[0] == counters[1])
print("intersection", sum((counters[0] & counters[1]).values()))
PY
```

The workbook was opened read-only and every physical row was counted. A follow-up cross-sheet overlap probe selected rows with `2010-12-01 <= InvoiceDate < 2010-12-10`, converted each complete eight-field row to a tuple, and compared the two slices as Python `collections.Counter` multisets. The Olist archive was opened in place and its CSVs were streamed with Python's `csv` module. Reproduce the reported aggregates using those operations and the named field headers below; no derived file is required.

- **Exit status:** All reported HTTP, archive-validation, digest, workbook, and CSV checks exited `0`. A truncated gzip stream was expected for the Amazon one-mebibyte range response and was used only to read the first 100 complete JSON lines.
- **Repeatability:** Download from the official URLs, verify the recorded digest for the version observed on 2026-08-12, then run the commands above. A digest change requires a new evidence record and schema/time-range revalidation rather than silently treating the artifact as identical.

## Raw observation

### UCI Online Retail II

Official record: [UCI Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii). Official download: [ZIP archive](https://cdn.uci-ics-mlr-prod.aws.uci.edu/502/online%2Bretail%2Bii.zip).

```text
landing page: HTTP 200, text/html
one-byte range probe: HTTP 206
archive bytes: 45,622,418
archive SHA-256: 572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb
archive validation: OK; one member, online_retail_II.xlsx, 45,622,278 uncompressed bytes
official page: 1,067,371 instances; CC BY 4.0; UK non-store retailer transactions from 2009-12-01 through 2011-12-09

sheet Year 2009-2010
fields: Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country
rows: 525,461
event-time range: 2009-12-01T07:45:00 through 2010-12-09T20:01:00
cancellation rows: 10,206; negative-quantity rows: 12,326; missing customer: 107,927
observed price range: -53,594.36 through 25,111.09

sheet Year 2010-2011
same eight fields
rows: 541,910
event-time range: 2010-12-01T08:26:00 through 2011-12-09T12:50:00
cancellation rows: 9,288; negative-quantity rows: 10,624; missing customer: 135,080
observed price range: -11,062.06 through 38,970.00

physical rows across both sheets: 1,067,371
unique StockCode values: 5,305

cross-sheet overlap probe
interval selected: 2010-12-01T00:00:00 <= InvoiceDate < 2010-12-10T00:00:00
Year 2009-2010: 22,523 rows; 22,202 unique complete-row tuples; 321 within-sheet duplicate excess
Year 2010-2011: 22,523 rows; 22,202 unique complete-row tuples; 321 within-sheet duplicate excess
Counter multisets equal: true
overlap event-time range: 2010-12-01T08:26:00 through 2010-12-09T20:01:00
cross-sheet duplicated physical rows: 22,523
physical rows after retaining only one copy of the overlapping sheet slice: 1,044,848
```

### Olist Brazilian E-Commerce

Official provider page: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). The unauthenticated Kaggle metadata endpoint and dataset download both responded successfully.

```text
metadata: HTTP 200, application/json
owner: Olist
licenseName: CC BY-NC-SA 4.0
lastUpdated: 2021-10-01T19:08:27.97Z
archive bytes: 44,717,580
archive SHA-256: 967e41e04fc306fe604e2a693f488995a8b41e5047418f8a5c8e4abd6deca784
archive validation: OK; nine CSV members

orders: 99,441
order items: 112,650
products: 32,951
sellers: 3,095
order_purchase_timestamp: 2016-09-04 21:15:19 through 2018-10-17 17:30:18
shipping_limit_date: 2016-09-19 00:15:34 through 2020-04-09 22:35:08
```

Observed tables cover customers, geolocation, orders, items, payments, reviews, products, sellers, and category-name translations. Order items include product, seller, price, freight, and shipping-limit fields; orders supply purchase and fulfillment lifecycle timestamps.

### Amazon Reviews 2023

Official project page: [Amazon Reviews 2023](https://amazon-reviews-2023.github.io/main.html). A public All Beauty review-file range request returned `HTTP 206`, `Content-Range: bytes 0-1048575/94441517`, and one mebibyte of gzip data.

```text
range bytes: 1,048,576
range SHA-256: d1514fb62c372260a8a2c425a87b11eede384f79806aa66ec9ff7cab854ce31e
first 100 complete review records fields:
asin, helpful_vote, images, parent_asin, rating, text, timestamp, title, user_id, verified_purchase
sample review timestamp range:
2014-07-03T15:47:43Z through 2023-02-08T03:18:53.052Z
```

The project page describes 571.54 million reviews from May 1996 through September 2023 and separate product metadata. It does not attach an observation/as-of timestamp to the product metadata.

## Interpretation

- **CONFIRMED:** UCI Online Retail II is anonymously downloadable, archive-valid, licensed CC BY 4.0 on its official page, and contains dated transaction events with product codes, quantities, prices, cancellations, and country over approximately two years.
- **CONFIRMED:** The workbook's two sheets duplicate the same 22,523-row multiset for 2010-12-01 through 2010-12-09. The 1,067,371 official/physical row count must not be treated as 1,067,371 independent events when the sheets are combined.
- **CONFIRMED:** UCI's invoice times can support a genuine event-time backtest only after a provenance-preserving stitch. The safe default is to retain `Year 2009-2010` only through 2010-11-30 and `Year 2010-2011` from 2010-12-01 onward, yielding 1,044,848 physical rows before any separate transaction-quality policy.
- **INFERRED:** A blanket exact-row deduplication is unsafe because 321 duplicate-tuple excess rows already occur within each overlap slice and may represent legitimate repeated line items. Sheet provenance and the explicit boundary, not tuple uniqueness alone, must control stitching.
- **INFERRED:** UCI is the best examined default historical bootstrap because its event records and permissive licence support an honest, reproducible transaction-only research loop without adopting a paid dependency.
- **CONFIRMED:** UCI does not contain marketplace listings, inventory, ratings, external demand, listing-state versions, or a marketplace-wide catalog. It cannot validate an integrated marketplace-plus-demand strategy or reconstruct listing state.
- **UNKNOWN:** UCI does not document an explicit timezone. Treat `InvoiceDate` as dataset-local naïve time, use documented daily boundaries, and do not append a timezone assumption.
- **CONFIRMED:** Olist provides richer marketplace-adjacent order, seller, product, review, price, and freight relationships and genuine order-event timestamps.
- **CONFIRMED:** Olist's current official Kaggle metadata labels the dataset `CC BY-NC-SA 4.0`; accepting that restrictive non-commercial/share-alike licence for the ProductQuant data foundation crosses the human authority boundary in `PROJECT_SPEC.md` section 53.
- **INFERRED:** Olist is a useful secondary research candidate but not the default v0.1 bootstrap until the owner explicitly accepts the licence constraints. The 2020 shipping-limit outlier also requires a field-specific data-quality rule rather than defining dataset coverage from that column.
- **CONFIRMED:** Amazon Reviews review events have per-review timestamps, but the companion product metadata does not expose historical observation times or versions.
- **INFERRED:** Joining current/crawl-time product metadata to old review events would leak later product state into historical features. Amazon Reviews 2023 is therefore not point-in-time safe as a listing/catalog bootstrap without isolating review-event-only fields.
- **UNKNOWN:** The reviewed Amazon Reviews project page does not establish a licence granting ProductQuant permanent preservation and redistribution rights. This blocks default adoption independently of the metadata timing problem.

## Limitations and residual uncertainty

- The probes establish accessibility from one environment on one date, not an availability SLA.
- Dataset-local timezones, later corrections, and provider revision policies remain undocumented or unverified.
- The overlap probe establishes the cross-sheet duplication and safe boundary rule; it does not determine whether exact duplicate tuples within a retained sheet are legitimate transactions. Any later removal of within-sheet duplicates requires separate invoice-line identity evidence and tests.
- The UCI and Olist downloads were held only in `/tmp`; this repository intentionally preserves digests and reproduction instructions rather than raw data.
- No personal review text or user identifier from Amazon Reviews is persisted in this evidence record.
- Licence observations describe published metadata and are not legal advice.

## Integrity and provenance

- **Artifact location:** Official URLs above; transient validation copies under `/tmp/productquant-recovery.RrGEIv` were excluded from Git.
- **Artifact digest:** UCI ZIP SHA-256 `572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb`; Olist ZIP SHA-256 `967e41e04fc306fe604e2a693f488995a8b41e5047418f8a5c8e4abd6deca784`; Amazon one-mebibyte range SHA-256 `d1514fb62c372260a8a2c425a87b11eede384f79806aa66ec9ff7cab854ce31e`.
- **External retention risk:** Provider URLs and artifacts can change or disappear. Recheck downloads and published licences after 30 days or before implementation, whichever comes first.
- **Supersedes / superseded by:** `NONE`

## Corrections

| UTC time | Participant | Correction | Reason and supporting evidence |
|---|---|---|---|
| `2026-08-12T06:29:18Z` | `agent:codex-phase0-recovery` | The original physical-row summary did not identify that the sheets repeat the same 22,523-row multiset for 2010-12-01 through 2010-12-09. The safe stitched count is 1,044,848 physical rows, using the first sheet only through 2010-11-30 and the second from 2010-12-01. | Adversarial review identified the overlap; the exact `Counter` probe above reproduced equal multisets. Blanket tuple deduplication is not prescribed because each sheet contains 321 within-slice duplicate excess rows. |
