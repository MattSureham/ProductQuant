# Human Checkpoint

This file is a low-bandwidth synchronization point for the human technical owner. It should preserve an accurate mental model and surface authority decisions without narrating every diff. Read [`BOOTSTRAP.md`](BOOTSTRAP.md) for normative rules.

This checkpoint is a summary and decision queue, not a source of project truth. Persist accepted product decisions in `PROJECT_SPEC.md` and accepted architectural decisions in `ADR/` before agents rely on them.

## Checkpoint metadata

- **Generated UTC:** `2026-08-12T07:47:28Z`
- **Prepared by:** `agent:codex-phase1`
- **Period covered:** Phase 0 completion commit `9efee6d` through owner authorization of the restricted Phase 1 foundation.
- **Specification status reviewed:** `PROJECT_SPEC.md` v0.1 now contains an accepted Restricted Phase 1 contract limited to UCI transaction events.
- **Implementation/reference state:** Authority and independent proposal review are complete; the Phase 1 ADR is accepted and its issue is `IMPLEMENTING`. No code or dependency exists at this exact checkpoint.
- **Prior checkpoint:** Phase 0 checkpoint generated `2026-08-12T06:39:43Z` and retained in Git history.

## System mental model

ProductQuant remains a research prototype with no runtime implementation yet. The owner has now authorised one deliberately restricted Phase 1 data foundation: UCI Online Retail II transaction events, immutable local raw storage, normalized Parquet, ephemeral DuckDB verification, and a four-command developer CLI. The exact product contract is in [`PROJECT_SPEC.md`](PROJECT_SPEC.md); the architecture proposal is in [`ADR-20260812T072420Z-uci-transaction-data-foundation`](ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md).

**CONFIRMED:** no examined source currently provides an accessible, authorised, reconstructable historical marketplace universe plus independent historical demand. **CONFIRMED:** UCI Online Retail II can support a narrow transaction-event backtest after its verified 22,523-row cross-sheet overlap is removed by provenance boundary and only invoices known by each cutoff are used; it contains no marketplace listing state or external demand. **INFERRED:** eBay is the strongest forward marketplace candidate and Google Trends is the strongest demand family, but both remain gated by access, retention/use terms, and authenticated evidence.

The authorised milestone builds only the transaction-event data foundation. It does not authorise Phase 2 factors or any ranking/backtest, and it does not resolve marketplace or demand access. Proposal review round 1 lacked the newest owner approval and identified under-specified contracts; round 2 confirmed authority and the revised architecture, independently reproduced the workbook schema probe, and requested three record-level corrections. Those corrections are now ready for final re-review.

## Material changes since the prior checkpoint

| Change | Why | Product/architecture effect | Evidence and review |
|---|---|---|---|
| Phase 0 source registry and recommendation completed | Establish the first backtestable data path without unsupported provider assumptions. | No runtime effect; records that only UCI is presently recommended, and only for transaction-event history. | [`SOURCE_REGISTRY.md`](SOURCE_REGISTRY.md); [`PHASE_0_SOURCE_RECOMMENDATION.md`](PHASE_0_SOURCE_RECOMMENDATION.md); [Phase 0 issue](ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md) |
| Four durable evidence records added | Preserve reproducible official-document observations, credential-free endpoint responses, data digests, and negative findings. | Makes source claims auditable; does not grant provider permission or adopt a dependency. | [`EVIDENCE/`](EVIDENCE/) |
| Marketplace and demand blockers separated from the completed spike | Keep unresolved human/provider work alive after Phase 0 documentation closes. | Phase 1 marketplace/demand collection remains blocked. | [Marketplace issue](ISSUES/ISSUE-20260812T061002Z-marketplace-source-authorization.md); [demand issue](ISSUES/ISSUE-20260812T061003Z-demand-source-validation.md) |
| Restricted Phase 1 scope and contract accepted | Persist `DECISION-PHASE0-01` and the approved decision-complete implementation plan. | Authorises only UCI transaction-event raw/normalized persistence, schema, CLI, dependencies, and local verification; Phase 2+ remains unauthorised. | [`PROJECT_SPEC.md`](PROJECT_SPEC.md); [Phase 1 issue](ISSUES/ISSUE-20260812T072420Z-uci-transaction-data-foundation.md); [proposed ADR](ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md) |
| Workbook schema/precision contract probed | Resolve required/null/type/time/price representation uncertainty before implementation. | Confirms the pinned workbook fits the accepted lossless schema while preserving fail-closed source-version behavior. | [`EVIDENCE-20260812T073451Z-uci-schema-contract-probe`](EVIDENCE/EVIDENCE-20260812T073451Z-uci-schema-contract-probe.md); independently reproduced in ADR review round 2. |

## Architecture decisions

### Accepted, rejected, or superseded

| ADR | Status | Decision and consequence | Owner authority evidence |
|---|---|---|---|
| [`ADR-20260812T072420Z-uci-transaction-data-foundation`](ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md) | `ACCEPTED` | Adopts the exact restricted local Python/immutable raw/Parquet/ephemeral DuckDB/event/CLI foundation. | `DECISION-PHASE1-01`; independent proposal review round 3 `APPROVED`. |

### Proposed or disputed

| ADR or issue | Decision needed | Alternatives and tradeoff | Deadline/blocking impact |
|---|---|---|---|
| [Marketplace blocker](ISSUES/ISSUE-20260812T061002Z-marketplace-source-authorization.md) | Whether to pursue written eBay permission/production access for archival quantitative research. | Seek explicit permission before implementation, or select and validate another licensed marketplace; Amazon/TikTok are not suitable substitutes under current evidence. | Blocks marketplace collector and forward snapshot accumulation. |
| [Demand blocker](ISSUES/ISSUE-20260812T061003Z-demand-source-validation.md) | Whether to apply for official Trends alpha and/or authorise a no-purchase provider trial. | Prefer official alpha; use DataForSEO Standard trial only for a controlled raw-retention/revision probe. | Blocks demand collector and strict point-in-time classification. |

## Complexity and architecture drift

### New or retired complexity

| Cost | Why introduced/removed | Coverage | Residual debt |
|---|---|---|---|
| Proposed Python packaging and five locked packages | Required for streaming XLSX, fixed-schema Parquet, ephemeral SQL verification, packaging, and tests. | Planned lock/build/unit/integration/full-data/independent checks. | Unverified until implementation and independent review. |
| Proposed immutable local data/manifests and `transaction_event.v1` | Required Phase 1 persistence and cross-module contracts. | Planned digest, atomicity, drift, schema, PIT, and reproducibility tests. | Unverified until implementation and independent review. |

### Drift assessment

- **Last independent drift review:** `NOT PERFORMED — implementation still does not exist.`
- **Classification:** `UNKNOWN — proposal review pending`
- **Owner-relevant differences:** The accepted restricted specification deliberately implements only UCI transaction events. It does not satisfy the integrated marketplace/demand v0.1 architecture described by the longer-term specification.

## Assumptions and uncertainty that changed

| Certainty | Earlier understanding | Current understanding | Consequence and evidence |
|---|---|---|---|
| `CONFIRMED` | eBay was the preferred candidate in the specification. | Browse/Feed can at most support approved forward collection; historical reconstruction and ProductQuant research-use permission are absent. | Marketplace work is blocked; [evidence](EVIDENCE/EVIDENCE-20260812T060100Z-ebay-source-feasibility.md). |
| `CONFIRMED` | Google Trends was a candidate external signal. | Official API access remains limited alpha; website/provider histories are retrospective and do not prove historical provider state. | Demand history must be labelled pseudo-historical pending a controlled probe; [evidence](EVIDENCE/EVIDENCE-20260812T060101Z-demand-source-feasibility.md). |
| `CONFIRMED` | A cheap historical bootstrap was unknown. | UCI Online Retail II is accessible, digest-verified, CC BY 4.0, and temporally usable after its 22,523-row cross-sheet overlap is removed by a provenance-preserving sheet boundary. | Enables a constrained owner-approved next phase, but not the integrated v0.1 demonstration; [evidence](EVIDENCE/EVIDENCE-20260812T060103Z-historical-dataset-probes.md). |

## Confidence and verification

- **What is directly verified:** Phase 0 source evidence remains current. A fifth evidence record now scans every UCI workbook row and confirms required/null/type/integrality/naïve-time/decimal constraints with a complete reproduction command.
- **What was independently reviewed:** Phase 0 is approved. Restricted Phase 1 proposal review round 1 blocked on omitted authority context and incomplete contracts; round 2 confirmed the newest exact owner approval, independently reproduced the workbook schema/precision counts, and requested three record corrections. Final re-review is pending.
- **What was not run or remains unverified:** No implementation, lock, package build, Parquet artifact, or CLI test exists yet. No authenticated provider response, paid/trial task, long-term revision study, or legal review occurred.
- **Known regressions or unresolved risks:** No runtime regression is possible. Source access, permitted raw retention, provider revisions, historical marketplace availability, and restrictive licences remain unresolved in the blocker issues.

## Human attention required

| Decision ID | Decision requested | Recommendation and rationale | Alternatives | Needed by | Response | Responder | Decision UTC | Durable authority reference |
|---|---|---|---|---|---|---|---|---|
| `DECISION-PHASE0-01` | May Phase 1 be scoped initially to UCI Online Retail II transaction events while marketplace and demand collectors remain deferred? | Approve the constrained scope because it enables an honest transaction-event foundation without pretending the integrated source stack exists. | Reject and wait for a complete marketplace/demand stack; or separately evaluate another licensed source. | Before any Phase 1 implementation | `APPROVED WITH SCOPE CONSTRAINTS` | `human:technical-owner` | `2026-08-12T07:24:20Z` (durably recorded) | [`PROJECT_SPEC.md` Restricted Phase 1](PROJECT_SPEC.md#restricted-phase-1--uci-transaction-event-data-foundation) |
| `DECISION-PHASE1-01` | May the project adopt the exact dependencies, persistence model, core event contract, and CLI in the Restricted Phase 1 plan? | Approve the smallest local, immutable, point-in-time-explicit UCI foundation; require independent proposal and implementation review. | Defer implementation or request a different architecture before accepting an ADR. | Before accepting the ADR or writing code | `APPROVED` | `human:technical-owner` | `2026-08-12T07:24:20Z` (durably recorded) | [`PROJECT_SPEC.md` Restricted Phase 1](PROJECT_SPEC.md#restricted-phase-1--uci-transaction-event-data-foundation); [ADR proposal](ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md) |
| `DECISION-PHASE0-02` | May the project apply for official Trends API alpha and, separately, create a DataForSEO account using only trial credit for a controlled Standard-queue probe? | Apply for the official alpha first; authorise DataForSEO only as a zero-purchase fallback probe with no paid top-up and with retention/revision evidence required. | Defer demand access and accumulate no external-demand snapshots; or later evaluate another documented provider under equivalent gates. | Before demand-source implementation | `PENDING` | `PENDING` | `PENDING` | `PENDING` |
| `DECISION-PHASE0-03` | Should the project pursue eBay written permission and production eligibility for the intended archival, pricing/category, ranking, and model research use? | Do not implement eBay first; pursue it only if the owner is willing to obtain written use/retention permission and independent contract review. | Select another marketplace and repeat the full Phase 0 evidence criteria; Amazon/TikTok are not current substitutes. | Before marketplace-source implementation | `PENDING` | `PENDING` | `PENDING` | `PENDING` |

A response is approval evidence only when its decision, responder identity, UTC time, and durable authority reference are all recorded. The responsible participant must then update the affected specification, ADR, or both and link this decision before implementation relies on it. A product or public-contract decision must update `PROJECT_SPEC.md`; an ADR alone is insufficient.

## No human attention required

- No further owner response is needed for the already approved restricted Phase 1 foundation.
- `DECISION-PHASE0-02` and `DECISION-PHASE0-03` may remain pending; no demand/marketplace access work will occur in this milestone.

## Next checkpoint trigger

- **Trigger:** Independent ADR review, restricted Phase 1 completion/review, source documentation older than 30 days, provider access/terms change, or owner response to another pending decision.
- **Expected owner action before then:** None; implementation may proceed after the independent ADR review accepts the proposal.
