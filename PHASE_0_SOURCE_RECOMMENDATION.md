# Phase 0 Source Feasibility Recommendation

**Verification date:** 2026-08-12

**Status:** Phase 0 research complete; source adoption remains blocked on the human decisions and provider evidence identified below.

**Authority:** This is an evidence-backed recommendation, not an accepted product requirement, architecture decision, provider contract, or permission to incur cost.

## Executive conclusion

- **CONFIRMED:** There is no currently accessible and authorised combination of marketplace, independent demand, and historical data that supports a strict point-in-time integrated ProductQuant backtest.
- **CONFIRMED:** UCI Online Retail II can support a genuine but narrow transaction-event backtest. It cannot reconstruct marketplace listings or supply an independent demand signal.
- **INFERRED:** eBay Browse plus Feed is the most plausible examined marketplace path for prospective collection, but production access and licence compatibility with raw archival, category/pricing research, ranking, and model use must be resolved first.
- **INFERRED:** The official Google Trends API alpha is the strongest strategic demand candidate. DataForSEO Google Trends Explore Standard is the most practical conditional trial candidate, but both return or advertise retrospective demand data whose historical revision state is unproven.

The project must not label a UCI-only experiment, a current Google Trends export, or future eBay snapshots as a historical marketplace-and-demand backtest.

## Recommended initial source positions

| Role | Recommendation | Status | What it can support | What it cannot support |
|---|---|---|---|---|
| Marketplace | eBay Browse API plus Feed API beta | `CONDITIONAL / BLOCKED` | After written permission and production validation: forward listing snapshots and a filtered prospective panel. | Pre-collection listing states, complete sold outcomes, historical marketplace universe, or presently authorised archival/model use. |
| External demand | Official Google Trends API alpha; DataForSEO Google Trends Explore Standard only as a conditional practical probe | `CONDITIONAL / BLOCKED` | If access and retention terms are verified: independently retrieved demand estimates and future snapshot accumulation. | Reconstructing the exact sample/revision that was available at historical factor time `t`; strict point-in-time history is not established. |
| Historical bootstrap | UCI Online Retail II | `RECOMMENDED — HISTORICAL ONLY` | A reproducible transaction-event research loop after the mandatory provenance-preserving sheet-boundary stitch, using invoice events up to `t` and later transactions as targets. | Marketplace listing state, current e-commerce representativeness, external demand, ratings, inventory, or the full section 50 minimum demonstration. |

The detailed feasibility dimensions and candidate alternatives are in [`SOURCE_REGISTRY.md`](SOURCE_REGISTRY.md).

## Why the historical recommendation is valid but narrow

The UCI workbook contains 1,067,371 physical invoice rows spanning December 2009 through December 2011, but its two sheets duplicate the same 22,523 rows from 2010-12-01 through 2010-12-09. A provenance-preserving stitch yields 1,044,848 physical rows before any separate transaction-quality policy. Its event times permit a point-in-time discipline only when the overlap is handled explicitly:

1. preserve sheet provenance, retain `Year 2009-2010` only through 2010-11-30, and use `Year 2010-2011` from 2010-12-01 onward;
2. do not blanket-deduplicate exact tuples within a retained sheet, because repeated invoice-line tuples may be legitimate and require separate identity evidence;
3. define each observation cutoff `t` using dataset-local naïve time;
4. derive the eligible product-code universe and all features only from stitched transactions with `InvoiceDate <= t`;
5. derive targets only from stitched transactions after `t`;
6. treat cancellations, returns, negative quantities, missing customers, and extreme prices explicitly;
7. never enrich historical rows with later catalog metadata unless that metadata has its own valid observation time.

That is a genuine historical transaction backtest, supported by the [download and schema probe](EVIDENCE/EVIDENCE-20260812T060103Z-historical-dataset-probes.md). It is not marketplace state reconstruction. The absence of listing, inventory, rating, seller-state, and independent-demand history must remain visible in every experiment and report.

## Why retrospective demand is only pseudo-historical

Google Trends website-derived series are produced at retrieval time, sampled/noised, and normalized within a request context. A request window that extends after factor time `t` directly leaks future information into the earlier 0–100 scale. Ending a request at `t` removes that particular future window but still does not prove that the current sample, filtering, or revisions equal what was available at `t`.

The official alpha advertises more consistent scaling, but its public documentation does not establish endpoint details, quota, cost, permanent raw-retention terms, immutable values, or revision timestamps. DataForSEO and SerpApi expose useful retrieval metadata but do not document historical provider-state reconstruction. Therefore all presently accessible Trends histories are `pseudo-historical` for ProductQuant unless an authorised repeatability/revision probe establishes more. See the [demand-source evidence](EVIDENCE/EVIDENCE-20260812T060101Z-demand-source-feasibility.md).

## Negative findings preserved

- **eBay:** Browse is current-state only; Feed begins a limited prospective panel; Marketplace Insights is not open to new users; Product Research/Terapeak is a seller UI, not a documented raw API. Current licence language creates a material unresolved research-use conflict. See [eBay evidence](EVIDENCE/EVIDENCE-20260812T060100Z-ebay-source-feasibility.md).
- **Amazon:** Creators API is affiliate-oriented current product content with short caching restrictions and no historical `as_of`; SP-API requires seller/vendor authorisation and is not a marketplace-wide historical interface. See [Amazon/TikTok evidence](EVIDENCE/EVIDENCE-20260812T060102Z-amazon-tiktok-source-feasibility.md).
- **TikTok Shop:** Product APIs cover authorised shops, not an anonymous marketplace universe. Current records, webhooks, and recent bestseller analytics cannot reconstruct pre-authorisation states, and published data-use terms do not establish ProductQuant's long-term research archival rights. See [Amazon/TikTok evidence](EVIDENCE/EVIDENCE-20260812T060102Z-amazon-tiktok-source-feasibility.md).
- **Google Trends website and BigQuery:** manual CSV is suitable only for validation; query-bearing Explore automation is excluded; the BigQuery top/rising dataset is selection-leaky when current top terms are backfilled into history.
- **Olist:** richer and more recent order history than UCI, but current metadata says CC BY-NC-SA 4.0. Adoption requires explicit human acceptance of restrictive terms.
- **Amazon Reviews 2023:** reviews have event timestamps, while product metadata lacks historical observation time; licensing sufficient for ProductQuant archival/reuse was not established.

Licence interpretations in this milestone are risk flags based on published terms, not legal advice.

## Phase boundary and next decision

Phase 0 is sufficiently resolved to reject a misleading integrated backtest and to offer the owner a constrained next step. No Phase 1 implementation was started.

The recommended owner decision is:

1. approve or reject scoping a UCI-only, transaction-event Phase 1 bootstrap while explicitly deferring marketplace and external-demand collectors;
2. separately decide whether to apply for the official Google Trends alpha and/or authorise a zero-purchase DataForSEO trial-credit probe;
3. do not begin eBay implementation unless written provider permission or a reviewed contract confirms that the intended archival and analytical use is allowed.

These pending decisions and exact unblock conditions are recorded in [`HUMAN_CHECKPOINT.md`](HUMAN_CHECKPOINT.md), the [marketplace-source blocker](ISSUES/ISSUE-20260812T061002Z-marketplace-source-authorization.md), and the [demand-source blocker](ISSUES/ISSUE-20260812T061003Z-demand-source-validation.md). Even if the constrained UCI path is approved, the integrated marketplace-plus-demand success criteria in `PROJECT_SPEC.md` remain unmet until independently point-in-time-safe sources are validated.
