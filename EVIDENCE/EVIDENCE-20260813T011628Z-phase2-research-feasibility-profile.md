# Phase 2 Transaction-Event Research Feasibility Profile

## Metadata

- **ID:** `EVIDENCE-20260813T011628Z-phase2-research-feasibility-profile`
- **Title:** `Aggregate-only feasibility profile of the UCI transaction-event substrate for weekly point-in-time demand research`
- **Captured UTC:** `2026-08-13T01:16:28Z`
- **Recorded by:** `agent:claude-code-phase2-proposal`
- **Claim supported or challenged:** The Restricted Phase 1 `transaction_event.v1` substrate supports a weekly point-in-time transaction-demand research design (trailing-30-day factor windows, 30-day forward targets, and ≥3 factors) over a stock-code product-proxy universe, without any marketplace, competition, or independent-demand data.
- **Related requirements:** [`PROJECT_SPEC.md` sections 20–32, 37–38, 45–46, 50 and Restricted Phase 1](../PROJECT_SPEC.md)
- **Related ADRs/issues:** [`ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec`](../ISSUES/ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec.md)
- **Repository revision/state:** `e21dd45` on `main`, clean working tree; canonical ignored normalized artifact `events.parquet` SHA-256 `49bec25b022823c63b56ddb3379aed3bd1117eeef418862a7514b66c935b189f`, verified by `productquant uci verify` at `2026-08-13T01:03:58Z`.
- **Environment:** macOS 26.3 arm64; Python 3.12.13; DuckDB 1.5.5 in-memory (ephemeral, no persistent database created).

## Method

- **Procedure:** Read the canonical normalized Parquet through an in-memory DuckDB view and compute aggregate-only coverage, history-depth, cancellation, price-variability, and backtest-support statistics. No transaction row, product description, or customer reference was emitted; all outputs are counts and distribution summaries.
- **Exact command/input:** `uv run --frozen python` executing DuckDB aggregate queries over `data/normalized/uci-online-retail-ii/572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb/transaction-event-v1/events.parquet`. Query families: dataset span; weekly distinct active products; events-per-product distribution; products meeting ≥20-event and 28/90-day history-span thresholds; cancellation/negative-quantity counts and signed-quantity ratio; distinct-prices-per-product distribution; weekly cutoffs where trailing-30-day history (≥5 events) and 30-day forward activity both exist; counts of weekly cutoffs with complete 30/60/90-day history and forward room inside the dataset span.
- **Exit status:** `0`
- **Repeatability:** Re-run the same aggregate queries against the same digest-pinned Parquet from revision `e21dd45` with `uv run --frozen python`. The substrate is immutable and content-addressed; identical aggregates must result.

## Raw observation

```json
{
 "span": ["2009-12-01 07:45:00", "2011-12-09 12:50:00", 1044848, 5305, 104],
 "weekly_active_products": [1470, 1947, 1890, 2447],
 "events_per_product": [1, 197.0, 74, 517.6, 5711],
 "history_support": [3869, 3858, 3691, 5305],
 "cancellations": [19165, 22557, 3393, 1.83, -9.12],
 "price_variability": [595, 2903, 1807, 1291],
 "backtest_support": [104, 0, 1570.0, 2192, 159644],
 "usable_cutoffs": [96, 92, 78]
}
```

Field order, matching the query order in Method:

- `span`: min/max `event_time_local`, total events, distinct stock codes, distinct ISO weeks (104).
- `weekly_active_products`: min/mean/median/max distinct active products per week (1,470 / 1,947 / 1,890 / 2,447).
- `events_per_product`: min/mean/median/p90/max events per stock code (1 / 197 / 74 / 517.6 / 5,711).
- `history_support`: stock codes with ≥20 events (3,869), additionally ≥28-day observed span (3,858), ≥90-day span (3,691), of 5,305 total.
- `cancellations`: cancellation-flagged rows (19,165), negative-quantity rows (22,557), negative-quantity rows not flagged as cancellations (3,393), cancellation-row share in percent (1.83), net negative-quantity volume as percent of positive-quantity volume (-9.12).
- `price_variability`: stock codes with exactly 1 distinct unit price (595), 2–5 (2,903), more than 5 (1,807), and the maximum distinct-price count (1,291).
- `backtest_support`: weekly cutoffs (104); minimum eligible products in a week (0, reflecting boundary partial weeks); mean (1,570) and maximum (2,192) products per cutoff with ≥5 trailing-30-day events; product-weeks with both ≥5 trailing-30-day events and any forward-30-day activity (159,644).
- `usable_cutoffs`: weekly cutoffs with complete trailing history and forward room inside the dataset span — 96 for 30-day history + 30-day forward, 92 for 60-day history + 30-day forward, 78 for 90-day history + 90-day forward.

## Interpretation

- **CONFIRMED:** The substrate provides ~96 usable weekly point-in-time cutoffs with a mean of ~1,570 eligible products per cutoff under a ≥5-trailing-event rule — sufficient cross-sectional width and time depth for weekly Rank IC and quintile analysis with a 30-day forward target.
- **CONFIRMED:** Signed quantities are material: negative-quantity volume equals ~9.1% of positive volume, and 3,393 negative-quantity rows lack the cancellation flag. A cancellation/return/netting policy is therefore a load-bearing research decision, exactly as the accepted Restricted Phase 1 specification anticipated.
- **CONFIRMED:** Unit prices vary within most products over time (only 595 of 5,305 have a single distinct price), so price-level and price-stability factors are computable but must tolerate multi-price products.
- **INFERRED:** A restricted Phase 2 limited to transaction-event demand factors, a stock-code product-proxy universe, forward demand targets, weekly ranking, baselines, IC/quantile evaluation, and a reproducible report is feasible on this substrate alone; the open marketplace/demand blocker issues do not block it.
- **UNKNOWN:** Whether any resulting factor has predictive information (that is the research question, not a feasibility fact); whether dataset-local naïve time or unknown provider revision state distorts weekly seasonality; whether wholesale transaction demand generalizes to consumer marketplace demand (it must not be assumed to).

## Limitations and residual uncertainty

- Aggregates describe this fixed historical wholesale dataset only. They establish feasibility of the research design, not the validity of any factor or the existence of any marketplace opportunity signal.
- The ≥5-event eligibility rule and cutoff grid are exploratory parameters used to size the design space, not an adopted universe definition; the adopted rule requires an accepted Phase 2 specification.
- Timezone is unknown and timestamps are dataset-local naïve; weekly seasonality interpretation is limited accordingly.
- No row-level values, product descriptions, or customer references were inspected or emitted; `customer_reference` plays no role in any proposed factor.

## Integrity and provenance

- **Artifact location:** Canonical ignored artifact `data/normalized/uci-online-retail-ii/572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb/transaction-event-v1/events.parquet` (not committed to Git).
- **Artifact digest:** Parquet SHA-256 `49bec25b022823c63b56ddb3379aed3bd1117eeef418862a7514b66c935b189f`; raw ZIP SHA-256 `572e36277c2390fbfde10664750731e0a86f55e33470d91919085f0408e67bfb` (see [Phase 1 verification](EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md)).
- **External retention risk:** The local ignored artifacts are not Git-protected; reproduction depends on retaining the verified raw bundle or UCI continuing to serve the pinned bytes.
- **Supersedes / superseded by:** Complements [`EVIDENCE-20260812T060103Z-historical-dataset-probes`](EVIDENCE-20260812T060103Z-historical-dataset-probes.md), [`EVIDENCE-20260812T073451Z-uci-schema-contract-probe`](EVIDENCE-20260812T073451Z-uci-schema-contract-probe.md), and [`EVIDENCE-20260812T091334Z-phase1-data-foundation-verification`](EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md); superseded by `NONE`.

## Corrections

| UTC time | Participant | Correction | Reason and supporting evidence |
|---|---|---|---|
| `2026-08-13T01:16:28Z` (recorded) / `2026-08-13T01:45:00Z` (corrected) | `agent:claude-code-phase2-proposal` | The metadata phrase "clean working tree" described the tracked tree only; this evidence record itself and the two companion proposal records (Phase 2 issue and proposed ADR) existed as untracked files while the profile was finalized. No observation above is affected. | Independent review round 1 (LOW finding) on [`ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec`](../ISSUES/ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec.md); `git status` at `e21dd45`. |
