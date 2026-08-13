# Human Checkpoint

This file is a low-bandwidth synchronization point for the human technical owner. It should preserve an accurate mental model and surface authority decisions without narrating every diff. Read [`BOOTSTRAP.md`](BOOTSTRAP.md) for normative rules.

This checkpoint is a summary and decision queue, not a source of project truth. Persist accepted product decisions in `PROJECT_SPEC.md` and accepted architectural decisions in `ADR/` before agents rely on them.

## Checkpoint metadata

- **Generated UTC:** `2026-08-13T01:04:45Z`
- **Prepared by:** `agent:claude-code-reconciliation`
- **Period covered:** Owner authorization of the restricted Phase 1 foundation through implementation, independent review, issue closure, and takeover reconciliation at `c937c3f`.
- **Specification status reviewed:** `PROJECT_SPEC.md` v0.1 contains the accepted Restricted Phase 1 contract limited to UCI transaction events; it is unchanged by this milestone's closure.
- **Implementation/reference state:** Restricted Phase 1 is implemented at `c937c3f8eca6b9d54ad77c47313647710abbe7d8` (local only, three commits ahead of `origin/main`; no push authorised). The required independent post-implementation review returned `APPROVED` and the Phase 1 issue is `CLOSED`. Local ignored raw/normalized artifacts verify against the recorded digests.
- **Prior checkpoint:** Phase 1 authorization checkpoint generated `2026-08-12T07:47:28Z` and retained in Git history.

## System mental model

ProductQuant now has exactly one runtime capability: the owner-authorised restricted Phase 1 data foundation. A four-command CLI (`productquant uci fetch|normalize|verify|prepare`) acquires the pinned UCI Online Retail II ZIP, preserves it byte-exact under Git-ignored owner-only `data/`, normalizes 1,044,848 retained transaction events into the versioned `transaction_event.v1` Parquet artifact with physical source-row provenance and the approved sheet-boundary stitch, and verifies aggregates through ephemeral in-memory DuckDB. The exact product contract is in [`PROJECT_SPEC.md`](PROJECT_SPEC.md); the accepted architecture is in [`ADR-20260812T072420Z-uci-transaction-data-foundation`](ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md); complete verification is in [`EVIDENCE-20260812T091334Z-phase1-data-foundation-verification`](EVIDENCE/EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md).

The foundation contains no factor, universe, target, ranking, backtest, marketplace state, or independent demand, and every manifest carries the eight capability declarations saying so. **CONFIRMED:** no examined source currently provides an accessible, authorised, reconstructable historical marketplace universe plus independent historical demand. **INFERRED:** eBay is the strongest forward marketplace candidate and Google Trends is the strongest demand family, but both remain gated by access, retention/use terms, and authenticated evidence.

## Material changes since the prior checkpoint

| Change | Why | Product/architecture effect | Evidence and review |
|---|---|---|---|
| Phase 0 source registry and recommendation completed | Establish the first backtestable data path without unsupported provider assumptions. | No runtime effect; records that only UCI is presently recommended, and only for transaction-event history. | [`SOURCE_REGISTRY.md`](SOURCE_REGISTRY.md); [`PHASE_0_SOURCE_RECOMMENDATION.md`](PHASE_0_SOURCE_RECOMMENDATION.md); [Phase 0 issue](ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md) |
| Four durable evidence records added | Preserve reproducible official-document observations, credential-free endpoint responses, data digests, and negative findings. | Makes source claims auditable; does not grant provider permission or adopt a dependency. | [`EVIDENCE/`](EVIDENCE/) |
| Marketplace and demand blockers separated from the completed spike | Keep unresolved human/provider work alive after Phase 0 documentation closes. | Phase 1 marketplace/demand collection remains blocked. | [Marketplace issue](ISSUES/ISSUE-20260812T061002Z-marketplace-source-authorization.md); [demand issue](ISSUES/ISSUE-20260812T061003Z-demand-source-validation.md) |
| Restricted Phase 1 scope and contract accepted | Persist `DECISION-PHASE0-01` and the approved decision-complete implementation plan. | Authorises only UCI transaction-event raw/normalized persistence, schema, CLI, dependencies, and local verification; Phase 2+ remains unauthorised. | [`PROJECT_SPEC.md`](PROJECT_SPEC.md); [Phase 1 issue](ISSUES/ISSUE-20260812T072420Z-uci-transaction-data-foundation.md); [proposed ADR](ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md) |
| Workbook schema/precision contract probed | Resolve required/null/type/time/price representation uncertainty before implementation. | Confirms the pinned workbook fits the accepted lossless schema while preserving fail-closed source-version behavior. | [`EVIDENCE-20260812T073451Z-uci-schema-contract-probe`](EVIDENCE/EVIDENCE-20260812T073451Z-uci-schema-contract-probe.md); independently reproduced in ADR review round 2. |
| Restricted Phase 1 implemented and closed | Deliver the owner-approved UCI transaction-event foundation under the accepted ADR. | Adds a locked Python package, four-command CLI, immutable content-addressed raw state, `transaction_event.v1` Parquet, ephemeral DuckDB verification, and row-free manifests/receipts; no Phase 2 capability added. | [`ISSUE-20260812T072420Z-uci-transaction-data-foundation`](ISSUES/ISSUE-20260812T072420Z-uci-transaction-data-foundation.md) `CLOSED`; [`EVIDENCE-20260812T091334Z-phase1-data-foundation-verification`](EVIDENCE/EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md); [registry status](SOURCE_REGISTRY.md) |
| Two independent implementation-review rounds corrected defects | Independent reviewers reproduced publication-overwrite/symlink, permission-mutation, workbook-cell, quantity-bound, download-bound, and staging-ignore defects before closure. | Publication is now atomic no-clobber with preserved modes, bounded fail-closed download with exact range recovery, rejected formula/error cells and int64 overflow, and root-level Git-ignore enforcement for in-worktree data roots. | Append-only review rounds and corrections in the Phase 1 issue and evidence; final round `APPROVED` at `2026-08-12T10:19:24Z` |

## Architecture decisions

### Accepted, rejected, or superseded

| ADR | Status | Decision and consequence | Owner authority evidence |
|---|---|---|---|
| [`ADR-20260812T072420Z-uci-transaction-data-foundation`](ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md) | `ACCEPTED` | Adopts the exact restricted local Python/immutable raw/Parquet/ephemeral DuckDB/event/CLI foundation. | `DECISION-PHASE1-01`; independent proposal review round 3 `APPROVED`; independent post-implementation architecture review `APPROVED` at `2026-08-12T10:19:24Z`. |

### Proposed or disputed

| ADR or issue | Decision needed | Alternatives and tradeoff | Deadline/blocking impact |
|---|---|---|---|
| [Marketplace blocker](ISSUES/ISSUE-20260812T061002Z-marketplace-source-authorization.md) | Whether to pursue written eBay permission/production access for archival quantitative research. | Seek explicit permission before implementation, or select and validate another licensed marketplace; Amazon/TikTok are not suitable substitutes under current evidence. | Blocks marketplace collector and forward snapshot accumulation. |
| [Demand blocker](ISSUES/ISSUE-20260812T061003Z-demand-source-validation.md) | Whether to apply for official Trends alpha and/or authorise a no-purchase provider trial. | Prefer official alpha; use DataForSEO Standard trial only for a controlled raw-retention/revision probe. | Blocks demand collector and strict point-in-time classification. |

## Complexity and architecture drift

### New or retired complexity

| Cost | Why introduced/removed | Coverage | Residual debt |
|---|---|---|---|
| Python packaging and five locked packages | Required for streaming XLSX, fixed-schema Parquet, ephemeral SQL verification, packaging, and tests. | Exact lock, build, 133-test suite, explicit full-data gate, and independent review passed. | Dependency or Python-version changes require deliberate re-locking and revalidation. |
| Immutable local data/manifests and `transaction_event.v1` | Required Phase 1 persistence and cross-module contracts. | Digest, no-clobber atomicity, fault/race, drift, schema, PIT, privacy, and reproducibility tests passed; byte-identical isolated rebuild. | Linux/Windows native publication, real power loss, and cross-platform byte identity remain unexercised/unknown and are explicitly recorded. |

### Drift assessment

- **Last independent drift review:** `2026-08-12T10:19:24Z` by `agent:codex-phase1-final-independent-review` at clean revision `c937c3f`.
- **Classification:** `ALIGNED` for all approved persistence, schema, dependency, CLI, privacy, and scope decisions; one `JUSTIFIED_DEVIATION` (bounded exact-source HTTP Range recovery, backed by preserved proxy-truncation evidence); remaining items `UNKNOWN` (Linux/Windows publication, power loss, cross-platform bytes, provider revision/timezone) and explicitly bounded. No `UNJUSTIFIED_DRIFT` remains.
- **Owner-relevant differences:** The accepted restricted specification deliberately implements only UCI transaction events. It does not satisfy the integrated marketplace/demand v0.1 architecture described by the longer-term specification; section 50 remains unmet.

## Assumptions and uncertainty that changed

| Certainty | Earlier understanding | Current understanding | Consequence and evidence |
|---|---|---|---|
| `CONFIRMED` | eBay was the preferred candidate in the specification. | Browse/Feed can at most support approved forward collection; historical reconstruction and ProductQuant research-use permission are absent. | Marketplace work is blocked; [evidence](EVIDENCE/EVIDENCE-20260812T060100Z-ebay-source-feasibility.md). |
| `CONFIRMED` | Google Trends was a candidate external signal. | Official API access remains limited alpha; website/provider histories are retrospective and do not prove historical provider state. | Demand history must be labelled pseudo-historical pending a controlled probe; [evidence](EVIDENCE/EVIDENCE-20260812T060101Z-demand-source-feasibility.md). |
| `CONFIRMED` | A cheap historical bootstrap was unknown. | UCI Online Retail II is accessible, digest-verified, CC BY 4.0, and temporally usable after its 22,523-row cross-sheet overlap is removed by a provenance-preserving sheet boundary. | Enables a constrained owner-approved next phase, but not the integrated v0.1 demonstration; [evidence](EVIDENCE/EVIDENCE-20260812T060103Z-historical-dataset-probes.md). |

## Confidence and verification

- **What is directly verified:** Phase 0 source evidence remains current through 2026-09-11. The Phase 1 foundation at `c937c3f` passed the locked 133-test suite, explicit official full-data gate, clean offline prepare/verify, byte-identical isolated rebuild, package/CLI gates, and repository/privacy scans; artifact digests match the recorded values. A fresh takeover participant independently reran the critical gates at `2026-08-13T01:04:45Z` with identical results.
- **What was independently reviewed:** Phase 0 is approved. The Restricted Phase 1 proposal was approved in review round 3 before implementation. Post-implementation independent review rounds 1–2 required and verified corrections; round 3 approved the final revision and classified architecture drift with no remaining material finding.
- **What was not run or remains unverified:** Linux/Windows native no-replace publication, real power-loss behavior, cross-platform Parquet byte identity, provider revision history, and dataset timezone. No authenticated provider response, paid/trial task, long-term revision study, or legal review occurred.
- **Known regressions or unresolved risks:** No runtime regression is known. Local ignored raw data are not Git-protected; reproduction depends on retaining the verified raw bundle or UCI continuing to serve the pinned bytes. Customer references remain sensitive local pseudonymous data. Source access, permitted raw retention, provider revisions, historical marketplace availability, and restrictive licences remain unresolved in the blocker issues.

## Human attention required

| Decision ID | Decision requested | Recommendation and rationale | Alternatives | Needed by | Response | Responder | Decision UTC | Durable authority reference |
|---|---|---|---|---|---|---|---|---|
| `DECISION-PHASE0-01` | May Phase 1 be scoped initially to UCI Online Retail II transaction events while marketplace and demand collectors remain deferred? | Approve the constrained scope because it enables an honest transaction-event foundation without pretending the integrated source stack exists. | Reject and wait for a complete marketplace/demand stack; or separately evaluate another licensed source. | Before any Phase 1 implementation | `APPROVED WITH SCOPE CONSTRAINTS` | `human:technical-owner` | `2026-08-12T07:24:20Z` (durably recorded) | [`PROJECT_SPEC.md` Restricted Phase 1](PROJECT_SPEC.md#restricted-phase-1--uci-transaction-event-data-foundation) |
| `DECISION-PHASE1-01` | May the project adopt the exact dependencies, persistence model, core event contract, and CLI in the Restricted Phase 1 plan? | Approve the smallest local, immutable, point-in-time-explicit UCI foundation; require independent proposal and implementation review. | Defer implementation or request a different architecture before accepting an ADR. | Before accepting the ADR or writing code | `APPROVED` | `human:technical-owner` | `2026-08-12T07:24:20Z` (durably recorded) | [`PROJECT_SPEC.md` Restricted Phase 1](PROJECT_SPEC.md#restricted-phase-1--uci-transaction-event-data-foundation); [ADR proposal](ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md) |
| `DECISION-PHASE0-02` | May the project apply for official Trends API alpha and, separately, create a DataForSEO account using only trial credit for a controlled Standard-queue probe? | Apply for the official alpha first; authorise DataForSEO only as a zero-purchase fallback probe with no paid top-up and with retention/revision evidence required. | Defer demand access and accumulate no external-demand snapshots; or later evaluate another documented provider under equivalent gates. | Before demand-source implementation | `PENDING` | `PENDING` | `PENDING` | `PENDING` |
| `DECISION-PHASE0-03` | Should the project pursue eBay written permission and production eligibility for the intended archival, pricing/category, ranking, and model research use? | Do not implement eBay first; pursue it only if the owner is willing to obtain written use/retention permission and independent contract review. | Select another marketplace and repeat the full Phase 0 evidence criteria; Amazon/TikTok are not current substitutes. | Before marketplace-source implementation | `PENDING` | `PENDING` | `PENDING` | `PENDING` |

A response is approval evidence only when its decision, responder identity, UTC time, and durable authority reference are all recorded. The responsible participant must then update the affected specification, ADR, or both and link this decision before implementation relies on it. A product or public-contract decision must update `PROJECT_SPEC.md`; an ADR alone is insufficient.

## No human attention required

- Restricted Phase 1 is complete and closed; no further owner response is needed for it.
- `DECISION-PHASE0-02` and `DECISION-PHASE0-03` may remain pending; no demand/marketplace access work is authorised.
- No push or publication is requested; all Phase 1 commits remain local.

## Next checkpoint trigger

- **Trigger:** Owner response to a pending decision, a Phase 2 proposal, dependency/contract changes, source documentation older than 30 days (after 2026-09-11), or provider access/terms/digest changes.
- **Expected owner action before then:** None required; optionally respond to `DECISION-PHASE0-02`/`DECISION-PHASE0-03` when ready.
