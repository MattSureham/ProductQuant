# ProductQuant

ProductQuant is an experimental system for backtestable, explainable quantitative research on e-commerce product selection. The current implementation is deliberately restricted to a local UCI Online Retail II transaction-event data foundation.

It does **not** reconstruct historical marketplace listings, supply, competition, availability, independent external demand, or a complete product-opportunity universe. It does not yet implement a universe, factor, target, ranking, backtest, or research result. Historical product-demand ranking from observed transaction events is a possible later phase; marketplace opportunity ranking remains unsupported.

## Repository protocol

Before changing the project, read these sources in authority order:

1. [`BOOTSTRAP.md`](BOOTSTRAP.md) — normative collaboration and evidence protocol;
2. [`PROJECT_SPEC.md`](PROJECT_SPEC.md) — accepted product requirements, including Restricted Phase 1;
3. [`ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md`](ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md) — accepted architecture and data contracts;
4. [`HANDOFF.md`](HANDOFF.md) — current operational snapshot and exactly one next action.

Phase 0 source evidence and unresolved marketplace/demand constraints remain in [`SOURCE_REGISTRY.md`](SOURCE_REGISTRY.md), [`PHASE_0_SOURCE_RECOMMENDATION.md`](PHASE_0_SOURCE_RECOMMENDATION.md), and [`ISSUES/`](ISSUES/). A handoff summary never overrides the specification, an accepted ADR, executable contracts/tests, or evidence.

## Setup

Install [`uv`](https://docs.astral.sh/uv/), then create the exact Python 3.12.13 environment and install the locked dependencies:

```bash
uv python install 3.12.13
uv sync --frozen
```

The lockfile is authoritative. Do not substitute pandas, a persistent DuckDB database, or a different source artifact without a separately accepted change.

## UCI data CLI

Prepare the pinned raw ZIP, normalize it to Parquet, and verify both bundles:

```bash
uv run --frozen productquant uci prepare --data-root ./data
```

The four supported commands are exactly:

```bash
uv run --frozen productquant uci fetch     --data-root ./data
uv run --frozen productquant uci normalize --data-root ./data
uv run --frozen productquant uci verify    --data-root ./data
uv run --frozen productquant uci prepare   --data-root ./data
```

`fetch` and `prepare` also accept `--offline`. Offline mode never opens a network connection and requires an already complete, valid raw bundle:

```bash
uv run --frozen productquant uci prepare --data-root ./data --offline
```

The default data root is `./data`. Success prints exactly one row-free JSON summary to stdout. Failure prints one sanitized JSON error to stderr. Exit codes are `0` success, `2` usage, `3` network, `4` source integrity/schema drift, `5` local I/O/state conflict, and `1` unexpected internal failure. Re-running against valid bundles is an idempotent verification; partial, corrupt, changed, or extra bundle content fails closed and is never overwritten.

A custom data root outside a Git worktree is supported. A custom root inside a worktree is accepted only when the data-root directory itself is matched by a Git ignore rule, which covers final and staging descendants; the command fails before writing or opening the network otherwise. Complete bundles and receipts are published with an atomic no-replace operation, so a competing final target is preserved and reported as a state conflict.

## Local data and provenance

The pinned source and generated artifacts remain outside Git beneath the selected data root:

```text
data/
  raw/uci-online-retail-ii/<archive-sha256>/
    online-retail-ii.zip
    manifest.json
  normalized/uci-online-retail-ii/<archive-sha256>/transaction-event-v1/
    events.parquet
    manifest.json
  receipts/uci-online-retail-ii/<run-id>.json
```

The raw archive SHA-256 is `572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb`. Its only workbook member has SHA-256 `bcbe73b35f5b7babf197fb0cb983a11f5d9ff929078d4aa53d171b1f2df2e980`. A digest, member, sheet, header, required type, precision, normalized schema, or full-data invariant change is treated as an unverified new source version.

Normalization applies one provenance-preserving rule: keep `Year 2009-2010` only before naïve local `2010-12-01T00:00:00`, and keep `Year 2010-2011` at or after that boundary. This removes the verified 22,523-row cross-sheet overlap and yields 1,044,848 events. Within-sheet duplicate tuples, cancellations, signed quantities/prices, nulls, extreme values, observed strings, and customer references remain intact. Event times have no documented timezone, and the pipeline does not invent one.

The machine-readable source, event, manifest, and receipt contracts are under [`src/productquant/contracts/`](src/productquant/contracts/). Parquet is the only normalized truth; DuckDB is used ephemerally for validation and does not create a persistent catalog.

## Privacy and local permissions

`Customer ID` is provider-published pseudonymous data and is preserved locally as `customer_reference`; it is not a ProductQuant user identity. Raw rows, normalized rows, customer-reference values, and receipts stay under a Git-ignored data root. On POSIX, newly created data directories and files are owner-only (`0700` and `0600`); the CLI does not change permissions on pre-existing roots, ancestors, or shared directories.

Do not commit, log, publish, remotely store, enrich, or link customer references to another identity. Any publication, remote storage, merchant linkage, enrichment, or new consumer requires a separate privacy and authority decision. Receipts contain only aggregate/provenance information and are retained indefinitely in this phase; no deletion service is provided.

## Verification

Run the synthetic unit/integration suite without downloading the official dataset:

```bash
uv run --frozen pytest
```

After `prepare` has produced the canonical local bundles, run the pinned full-data acceptance test:

```bash
uv run --frozen pytest -m full_data --data-root ./data
```

The full-data test intentionally fails with acquisition instructions when the pinned bundle is absent; it is not silently skipped. It verifies the archive and workbook digests, exact normalized schema, stitch boundary, 1,044,848-row profile, provenance identifiers, Parquet readability, capability denials, and idempotent verification. The operational verification command is:

```bash
uv run --frozen productquant uci verify --data-root ./data
```

Same-lock, same-platform rebuilds are expected to produce identical Parquet bytes. Across platforms, logical schema, order, content, and aggregate profile are required to match; byte identity is not claimed.

## Dataset attribution

The local historical substrate is distributed under [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/):

> Chen, D. (2012). *Online Retail II* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CG6D

See the [official UCI dataset record](https://archive.ics.uci.edu/dataset/502/online+retail+ii). The raw and normalized data are intentionally not redistributed by this repository.
