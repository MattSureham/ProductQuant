# UCI Transaction-Event Data Foundation

## Metadata

- **ID:** `ADR-20260812T072420Z-uci-transaction-data-foundation`
- **Title:** `UCI transaction-event data foundation`
- **Status:** `ACCEPTED`
- **Created UTC:** `2026-08-12T07:24:20Z`
- **Author:** `agent:codex-phase1`
- **Human technical owner:** `human:technical-owner`
- **Owner approval:** `APPROVED — DECISION-PHASE1-01, durably recorded 2026-08-12T07:24:20Z`
- **Related specification:** [`PROJECT_SPEC.md` section 51, Restricted Phase 1](../PROJECT_SPEC.md#restricted-phase-1--uci-transaction-event-data-foundation)
- **Related issues:** [`ISSUE-20260812T072420Z-uci-transaction-data-foundation`](../ISSUES/ISSUE-20260812T072420Z-uci-transaction-data-foundation.md)
- **Supersedes / superseded by:** `NONE`

## Context

Phase 0 established that UCI Online Retail II is the only currently authorised historical substrate suitable for an initial, narrow transaction-event research loop. It does not reconstruct marketplace listings, supply, competition, independent demand, or a complete opportunity universe. Phase 1 needs a reproducible local foundation without adopting a mutable database as a second source of truth or building a generic source framework before a second source is cleared.

The decision crosses the Human Authority Boundary because it introduces significant dependencies, persistent raw and normalized state, a core cross-module event schema, and a supported CLI.

## Decision

1. ProductQuant Phase 1 uses CPython 3.12.13 and `uv`, with exact dependency resolution committed in `uv.lock`. The build backend is `uv_build>=0.11.8,<0.12`; runtime constraints are `openpyxl>=3.1.5,<4`, `pyarrow>=25.0.1,<26`, and `duckdb>=1.5.5,<2`; the development constraint is `pytest>=9.1.1,<10`.
2. `openpyxl` owns read-only XLSX streaming, `pyarrow` owns fixed-schema Parquet writing, and `duckdb` owns ephemeral read-only validation/querying. No pandas, Polars, CLI framework, schema framework, HTTP client, database server, scheduler, or generic plugin abstraction is adopted. Python's standard-library `urllib` performs the one fixed public download.
3. The byte-exact UCI ZIP is preserved outside Git in a content-addressed directory. The inner workbook is verified and extracted only to transient staging. A digest or schema change fails closed and requires a separately evidenced source version.
4. Parquet is the authoritative normalized artifact. DuckDB MUST NOT create a persistent catalog or second mutable truth. Raw, normalized, manifest, receipt, and staging writes use immutable/versioned targets and atomic publication; existing valid targets are verified no-ops and invalid targets are never overwritten.
5. `transaction_event.v1` is the accepted cross-module data contract. It preserves source-row provenance, dataset-local naïve event time, source identifiers, description, signed quantity, exact three-decimal unit price, provider-declared GBP currency, nullable customer reference, country, provider-defined cancellation flag, and schema version. It does not claim normalized marketplace product or listing identity.
6. The cross-sheet stitch is `uci-online-retail-ii-sheet-boundary-v1`: retain `Year 2009-2010` only before naïve `2010-12-01T00:00:00`, and retain `Year 2010-2011` at or after that boundary. Within-sheet tuple duplicates remain distinct physical events.
7. The supported software interface is the developer CLI `productquant uci {fetch,normalize,verify,prepare}` with `--data-root`, plus `--offline` on `fetch` and `prepare`. Success produces a JSON summary; failure is nonzero and does not emit row-level data. No public Python API is introduced.
8. Per-invocation immutable receipts record success or failure. Manifests carry retrieval/build provenance, digests, versioning, quality profiles, and explicit capability denials. Customer references and transaction rows remain local ignored data and MUST NOT appear in repository evidence or logs.
9. Phase 1 does not implement a universe, factors, targets, ranking, backtest, report, marketplace/demand adapter, background service, or external publication.

### Identifier and storage contract

- `raw_artifact_id` is exactly `uci-online-retail-ii:sha256:<lowercase-archive-sha256>`.
- `event_id` is exactly `<raw_artifact_id>:<sheet-token>:<source-row-number>`, where the only sheet-token mappings are `Year 2009-2010 -> year-2009-2010` and `Year 2010-2011 -> year-2010-2011`; the row number is the 1-based physical Excel row including the header, so the first data row is `2`.
- `normalized_artifact_id` is exactly `<raw_artifact_id>:transaction-event.v1`.
- The raw bundle is `data/raw/uci-online-retail-ii/<archive-sha256>/` containing only `online-retail-ii.zip` and `manifest.json`.
- The normalized bundle is `data/normalized/uci-online-retail-ii/<archive-sha256>/transaction-event-v1/` containing only `events.parquet` and `manifest.json`.
- Receipts are retained indefinitely under `data/receipts/uci-online-retail-ii/<run-id>.json`; `run-id` is a compact UTC timestamp with microseconds plus eight lowercase UUID4 hex characters. Phase 1 supplies no deletion or retention service.
- Raw and normalized bundles are built as sibling temporary directories, file-synced, and atomically renamed as complete directories. A valid existing bundle is a no-op; any missing/extra/invalid content in an existing final bundle fails closed. Receipt files use same-directory temporary files and atomic rename. Concurrent writers are unsupported and fail if a target appears during publication.

### Manifest contract

All manifests are UTF-8, sorted-key JSON with no row-level values.

The raw manifest uses `schema_version=productquant.raw-artifact-manifest.v1` and contains:

```text
artifact_id
source {id, original_url, final_url, licence_spdx, licence_url, attribution}
retrieval {retrieved_at_utc, mode, http_status, etag, last_modified,
           content_type, content_length, rate_limit_state, query_parameters}
archive {path, bytes, sha256}
member {name, bytes, sha256}
adapter_version
raw_response_reference
```

`mode` is `download` for an online acquisition. Offline fetch never opens a network connection and only verifies an already complete raw bundle; it cannot manufacture missing retrieval metadata. HTTP fields absent from a response are JSON `null`; headers are allowlisted to the named fields.

The normalized manifest uses `schema_version=productquant.normalized-manifest.v1` and contains:

```text
artifact_id, raw_artifact_id, raw_manifest_reference
dataset {path, bytes, sha256, row_count, pyarrow_schema}
source_schema_version, normalizer_version
build {built_at_utc, git_revision, git_dirty, python_version,
       dependency_versions, parquet_compression, row_group_size}
stitch {rule_id, cutoff_local, first_sheet_input, first_sheet_retained,
        second_sheet_input, second_sheet_retained, excluded_cross_sheet_rows}
time_semantics {field, timezone, cutoff_inclusive}
profile {event_time_min, event_time_max, unique_event_ids, unique_stock_codes,
         unique_invoices, cancellation_rows, negative_quantity_rows,
         zero_price_rows, negative_price_rows, missing_description_rows,
         missing_customer_rows, numeric_description_rows,
         quantity_min, quantity_max, unit_price_min, unit_price_max}
capabilities {transaction_event_history, marketplace_listing_state,
              marketplace_supply_competition, independent_external_demand,
              complete_product_opportunity_universe,
              integrated_productquant_v0_1, historical_provider_revision_state,
              timezone}
```

Capability values are the exact `supported`, `unsupported`, or `unknown` values required by the specification. The manifest's volatile build/provenance time does not enter Parquet rows. Same-lock, same-platform reruns must produce identical Parquet bytes; cross-platform byte identity remains unclaimed, while logical schema/order/content must match.

### Receipt and CLI contract

Receipts use `schema_version=productquant.command-receipt.v1` and contain `run_id`, `command`, `started_at_utc`, `finished_at_utc`, `status`, absolute `data_root`, Git revision/dirty state, referenced artifact/manifest IDs, a row-free result summary, and either `error=null` or `{code,message}`. Failure-receipt publication is attempted whenever the data root is writable; if it is not, stderr reports `receipt_path=null` without masking the primary failure.

Each successful invocation writes exactly one sorted-key JSON object plus newline to stdout:

```text
{command, status, data_root, artifacts, statistics, receipt_path}
```

`command` is `uci.fetch`, `uci.normalize`, `uci.verify`, or `uci.prepare`; `status` is `created` if any requested artifact was created and otherwise `verified`; `artifacts` maps `raw` and `normalized` to `{artifact_id, manifest_path, data_path, action}` or JSON `null`; and `action` is `created` or `verified`. `statistics` contains aggregate counts only. Paths are absolute.

Each failure writes exactly one row-free JSON error object plus newline to stderr:

```text
{command, status: "error", error: {code, message}, receipt_path}
```

For errors after command recognition, `command` is the recognized command and a receipt is attempted. For parser/usage errors before recognition, `command` and `receipt_path` are JSON `null`, no receipt is attempted, and exit `2` is returned. Help is ordinary text on stdout and creates no receipt.

Exit codes are `0` success, `2` usage, `3` network, `4` source-integrity/schema drift, `5` local I/O/state conflict, and `1` unexpected internal failure. `fetch --offline` and `prepare --offline` never call the network and require a complete valid raw bundle. `normalize` requires a complete valid raw bundle and creates or verifies the normalized bundle. `verify` requires and validates both bundles, their manifests, fixed full-data invariants, Parquet schema, hashes, and DuckDB-readable aggregates. `prepare` executes fetch, normalize, and verify but emits only its final single JSON summary.

### Privacy and retention contract

`Customer ID` is provider-published pseudonymous data, not a ProductQuant user identity. The owner-approved schema preserves it as the exact nullable `customer_reference` string because stable customer grouping may later support separately authorised transaction-demand research; hashing without a secret would not materially anonymize it, and dropping it would make the normalized contract lossy. Raw and normalized bundles and receipts remain under ignored local `data/`; row values never enter logs, receipts, manifests, tests using the official artifact, evidence, or Git. On POSIX, created directories and files are owner-only (`0700`/`0600`). Any publication, remote storage, merchant linkage, enrichment, or new consumer requires a separate privacy/authority decision.

## Human Authority Boundary assessment

- **Boundary crossed:** `YES`
- **Reason:** Dependencies, persistence/state ownership, CLI contract, core data model, cross-module contract, and handling of a public pseudonymous customer reference.
- **Existing authorization:** `DECISION-PHASE0-01` authorises the constrained UCI product scope; `DECISION-PHASE1-01` explicitly approves this architecture and contract.
- **Approval evidence:** `human:technical-owner`; owner approval supplied in the approved Restricted Phase 1 plan and durably recorded at `2026-08-12T07:24:20Z` in [`PROJECT_SPEC.md`](../PROJECT_SPEC.md) and [`HUMAN_CHECKPOINT.md`](../HUMAN_CHECKPOINT.md).

## Alternatives considered

### Persistent DuckDB database as normalized truth

- **Benefits:** Convenient views, metadata, and SQL access.
- **Costs and risks:** Creates mutable state and a second truth beside export files; complicates recovery and migration.
- **Reason not selected:** A single immutable Parquet artifact plus ephemeral DuckDB satisfies current local research needs with less state.

### pandas or Polars ingestion

- **Benefits:** Familiar dataframe transformation APIs.
- **Costs and risks:** Adds a large transformation abstraction and encourages whole-workbook materialization or implicit type inference.
- **Reason not selected:** `openpyxl` streaming plus fixed PyArrow batches is sufficient and keeps coercion rules explicit.

### DuckDB-only Excel ingestion

- **Benefits:** Fewer direct runtime libraries in application code.
- **Costs and risks:** Depends on an extension and its installation/runtime behaviour; gives less direct control over physical Excel row provenance and cell coercion.
- **Reason not selected:** The verified workbook and provenance requirements favour explicit read-only workbook iteration.

### Generic source adapter or plugin framework

- **Benefits:** Could standardize future source additions.
- **Costs and risks:** Premature abstraction while marketplace and demand sources remain blocked and their contracts are unknown.
- **Reason not selected:** Implement one source-specific adapter; revisit only after a second authorised source creates demonstrated commonality.

### Commit raw or normalized data to Git

- **Benefits:** Immediate local availability.
- **Costs and risks:** Large binaries, pseudonymous transaction data, and derived artifacts would burden repository history and publication boundaries.
- **Reason not selected:** Digests, manifests, tests, and regeneration instructions provide reproducibility without publishing data.

## Consequences

### Positive

- Raw bytes, physical source rows, normalization rules, and outputs remain traceable and reproducible.
- Point-in-time event semantics and the cross-sheet correction become executable contracts.
- The design remains local, cheap, replaceable, and honest about unsupported marketplace capabilities.

### Negative and tradeoffs

- Three runtime dependencies and one development dependency must be maintained.
- Local raw and normalized artifacts consume disk and are not supplied by Git.
- No concurrent-writer guarantee is provided in Phase 1.
- UCI revision history and timezone remain unknown; event times are not evidence of when the provider first published each row.

### Compatibility and migration

- This is the first implementation, so no runtime migration is required.
- A future source or schema version must use a new content/schema version and explicit migration or adapter; it must not mutate `transaction_event.v1` artifacts in place.

## Unverified complexity

| Cost introduced | Why necessary | Contract/test/evidence coverage | Residual gap and linked issue |
|---|---|---|---|
| `openpyxl`, `pyarrow`, `duckdb`, `pytest`, and `uv_build` | Stream the XLSX, preserve exact types, write/query Parquet, package, and test the foundation. | Lockfile, dependency review, unit/integration/full-data tests, and independent review. | Provider/library upgrades require deliberate re-locking and revalidation; owned by the Phase 1 issue. |
| Immutable local raw/normalized state and manifests | Requirements 16, 18, 43, and 51 require reproducible raw persistence and normalized datasets. | Digest, atomicity, idempotence, corruption, and deterministic rebuild tests. | Concurrent invocation is deliberately unsupported and documented. |
| `transaction_event.v1` cross-module contract | Later factor/backtest work needs stable event-time and provenance semantics. | Machine-readable contract, exact-schema tests, synthetic leakage tests, and full-data acceptance. | Downstream cancellation/return/netting policy is deliberately deferred to a separately authorised phase. |
| Customer reference preservation | Retains lossless source fidelity for potential demand-diversity research. | Local-only storage, no row logging/evidence, raw provenance, and tracked-data scans. | Any publication or broader use requires separate privacy/authority review. |

## Evidence and assumptions

- **CONFIRMED:** The official artifact and workbook digests, two-sheet overlap, row ranges, and anomalies were reproduced in [`EVIDENCE-20260812T060103Z-historical-dataset-probes`](../EVIDENCE/EVIDENCE-20260812T060103Z-historical-dataset-probes.md).
- **CONFIRMED:** A complete follow-up type/precision probe found no null in a required source field, no non-integral quantity/identifier number, no timezone-aware source timestamp, and no price scale above three decimals; see [`EVIDENCE-20260812T073451Z-uci-schema-contract-probe`](../EVIDENCE/EVIDENCE-20260812T073451Z-uci-schema-contract-probe.md).
- **CONFIRMED:** The UCI record declares CC BY 4.0 and unit price in sterling.
- **CONFIRMED:** The owner approved UCI solely as a transaction-event historical research substrate and explicitly withheld marketplace-state claims.
- **INFERRED:** Content-addressed raw ZIP plus one normalized Parquet truth is the smallest durable storage design satisfying the accepted Phase 1 requirements.
- **UNKNOWN:** Dataset-local timezone, provider revision/as-of state, cross-platform byte-identical Parquet output, and future source commonality remain unestablished.

## Independent review rounds

- **Required:** `YES — the decision introduces dependencies, persistent state, a public CLI, and a core cross-module contract.`

### 2026-08-12T07:31:28Z — agent:codex-phase1-architecture-review

- **Reviewed repository state:** Base `9efee6d17735b1bb1c9d11a2bd720a64bc617499` plus the initial five authority-record changes; no implementation.
- **Scope:** Protocol, specification, Phase 0 recommendation/evidence, checkpoint/handoff, proposed ADR, issue, authority, schema/CLI/persistence/privacy, links, and placeholders.
- **Commands or procedures:** Git state/diff checks, relative-link resolution, template-placeholder scan, and requirement/evidence comparison. An unrelated fresh download attempt timed out and supplied no new evidence.
- **Findings and resolution conditions:** `CRITICAL`: reviewer context did not contain the later human message approving the reproduced decision-complete Phase 1 plan and therefore classified `DECISION-PHASE1-01` as unauthorised; re-review must inspect that newest approval. `HIGH`: event/manifest/receipt/CLI contracts were insufficiently exact. `HIGH`: customer-reference minimization and controls needed explicit evaluation. `MEDIUM`: required/null/type/decimal assumptions needed reproducible evidence. `MEDIUM`: receipts and exact runtime/build pinning needed explicit contract/justification.
- **Limitations:** No implementation/tests existed; reviewer lacked the latest exact-plan approval; new external archive download did not finish.
- **Residual risks:** Dataset timezone/provider revisions, future cancellation/netting policy, and marketplace/demand capabilities remain deferred.
- **Evidence:** Initial diff and Phase 0 evidence.
- **Disposition:** `BLOCKED`
- **Prior-round resolution:** `FIRST ROUND`

### 2026-08-12T07:39:00Z — agent:codex-phase1-architecture-review

- **Reviewed repository state:** Base `9efee6d17735b1bb1c9d11a2bd720a64bc617499` plus revised authority records and schema evidence; no implementation.
- **Scope:** Newest exact human plan approval; protocol/specification; Phase 0 evidence; revised ADR/issue/checkpoint/handoff; complete workbook probe.
- **Commands or procedures:** Git state/diff/whitespace, complete changed-file and link inspection, plus independent full-workbook `openpyxl` scan.
- **Findings and resolution conditions:** Authority is confirmed and prior contract/privacy/evidence findings are materially resolved. Remaining: embed the exact evidence command, define pre-command usage-error JSON, and reconcile checkpoint/handoff with the new evidence/reviews before acceptance.
- **Limitations:** No implementation, lock, Parquet, CLI, or tests yet; cross-platform Parquet byte identity remains unclaimed.
- **Residual risks:** Provider revision/timezone, cancellation/netting, and marketplace/demand work remain deferred.
- **Evidence:** Phase 0 probe, new schema probe, current diff, and independently reproduced aggregates.
- **Disposition:** `CHANGES_REQUIRED`
- **Prior-round resolution:** The authority blocker and contract/privacy/schema findings from round 1 were resolved; three record-level corrections remained.

### 2026-08-12T07:46:48Z — agent:codex-phase1-architecture-review

- **Reviewed repository state:** Base `9efee6d17735b1bb1c9d11a2bd720a64bc617499` plus the corrected specification, ADR, issue, checkpoint, handoff, and schema evidence; no implementation or dependency.
- **Scope:** Exact owner approvals, protocol/specification, Phase 0 recommendation/evidence, corrected contracts and privacy controls, prior review rounds, and their resolutions.
- **Commands or procedures:** Git state/stat/diff/whitespace; complete file inspection; relative-link, placeholder, unique-ID/reference, tracked-data, and large-file scans; comparison with round-2 independent workbook reproduction.
- **Findings and resolution conditions:** `NONE` at proposal stage. Authority, scope, dependencies, identifiers, persistence ownership, manifests, receipts, atomicity, CLI/offline/error semantics, privacy, evidence, and negative capability claims are decision-complete and compatible.
- **Limitations:** No implementation, lock, package, CLI, Parquet, or test exists yet; separate implementation verification/review remains mandatory. Cross-platform Parquet byte identity remains unclaimed.
- **Residual risks:** Dataset timezone/provider revisions, cancellation/netting, future customer-reference use, and marketplace/demand sources remain separately gated.
- **Evidence:** Linked Phase 0 and schema probes, corrected authoritative records, and round-2 independent scan.
- **Disposition:** `APPROVED`
- **Prior-round resolution:** Round 1 authority/contract/privacy/schema findings and round 2 evidence-command/usage-JSON/current-record findings are all resolved.

## Status history

| UTC time | From | To | Actor | Reason and authority evidence |
|---|---|---|---|---|
| `2026-08-12T07:24:20Z` | `NONE` | `PROPOSED` | `agent:codex-phase1` | Exact owner-approved Phase 1 architecture recorded for independent proposal review before implementation. |
| `2026-08-12T07:47:28Z` | `PROPOSED` | `ACCEPTED` | `agent:codex-phase1` | Owner authority `DECISION-PHASE1-01` plus independent review round 3 `APPROVED`; implementation review remains required. |
