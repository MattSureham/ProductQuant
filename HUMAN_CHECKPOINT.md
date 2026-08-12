# Human Checkpoint

This file is a low-bandwidth synchronization point for the human technical owner. It should preserve an accurate mental model and surface authority decisions without narrating every diff. Read [`BOOTSTRAP.md`](BOOTSTRAP.md) for normative rules.

This checkpoint is a summary and decision queue, not a source of project truth. Persist accepted product decisions in `PROJECT_SPEC.md` and accepted architectural decisions in `ADR/` before agents rely on them.

## Checkpoint metadata

- **Generated UTC:** `2026-08-12T06:39:43Z`
- **Prepared by:** `agent:codex-phase0-recovery`
- **Period covered:** Initial commit `3ff8644` through completion of the Phase 0 source-feasibility evidence package.
- **Specification status reviewed:** `PROJECT_SPEC.md` v0.1 is sufficient for Phase 0 research; no specification change was made or accepted.
- **Implementation/reference state:** Documentation-only working tree based on `3ff8644ca6cf01feb43e25aadb6ef6d23d094cf1`; no application code, dependency, schema, collector, or test exists.
- **Prior checkpoint:** `NONE`

## System mental model

ProductQuant remains a research specification, not an implemented system. Phase 0 tested whether real sources could support the future raw-data → point-in-time observations → factors → ranking → backtest loop. No provider, data licence, external contract, persistence design, or public interface has been adopted.

**CONFIRMED:** no examined source currently provides an accessible, authorised, reconstructable historical marketplace universe plus independent historical demand. **CONFIRMED:** UCI Online Retail II can support a narrow transaction-event backtest after its verified 22,523-row cross-sheet overlap is removed by provenance boundary and only invoices known by each cutoff are used; it contains no marketplace listing state or external demand. **INFERRED:** eBay is the strongest forward marketplace candidate and Google Trends is the strongest demand family, but both remain gated by access, retention/use terms, and authenticated evidence.

The next owner decision is whether to permit a deliberately constrained UCI-only Phase 1 scope while marketplace and demand collectors remain deferred. That experiment would be an honest historical transaction bootstrap, not completion of ProductQuant's required integrated v0.1 demonstration.

## Material changes since the prior checkpoint

| Change | Why | Product/architecture effect | Evidence and review |
|---|---|---|---|
| Phase 0 source registry and recommendation completed | Establish the first backtestable data path without unsupported provider assumptions. | No runtime effect; records that only UCI is presently recommended, and only for transaction-event history. | [`SOURCE_REGISTRY.md`](SOURCE_REGISTRY.md); [`PHASE_0_SOURCE_RECOMMENDATION.md`](PHASE_0_SOURCE_RECOMMENDATION.md); [Phase 0 issue](ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md) |
| Four durable evidence records added | Preserve reproducible official-document observations, credential-free endpoint responses, data digests, and negative findings. | Makes source claims auditable; does not grant provider permission or adopt a dependency. | [`EVIDENCE/`](EVIDENCE/) |
| Marketplace and demand blockers separated from the completed spike | Keep unresolved human/provider work alive after Phase 0 documentation closes. | Phase 1 marketplace/demand collection remains blocked. | [Marketplace issue](ISSUES/ISSUE-20260812T061002Z-marketplace-source-authorization.md); [demand issue](ISSUES/ISSUE-20260812T061003Z-demand-source-validation.md) |

## Architecture decisions

### Accepted, rejected, or superseded

| ADR | Status | Decision and consequence | Owner authority evidence |
|---|---|---|---|
| `NONE` | `NOT APPLICABLE` | No architecture decision was made in Phase 0. | `PROJECT_SPEC.md` remains unchanged. |

### Proposed or disputed

| ADR or issue | Decision needed | Alternatives and tradeoff | Deadline/blocking impact |
|---|---|---|---|
| [Marketplace blocker](ISSUES/ISSUE-20260812T061002Z-marketplace-source-authorization.md) | Whether to pursue written eBay permission/production access for archival quantitative research. | Seek explicit permission before implementation, or select and validate another licensed marketplace; Amazon/TikTok are not suitable substitutes under current evidence. | Blocks marketplace collector and forward snapshot accumulation. |
| [Demand blocker](ISSUES/ISSUE-20260812T061003Z-demand-source-validation.md) | Whether to apply for official Trends alpha and/or authorise a no-purchase provider trial. | Prefer official alpha; use DataForSEO Standard trial only for a controlled raw-retention/revision probe. | Blocks demand collector and strict point-in-time classification. |

## Complexity and architecture drift

### New or retired complexity

| Cost | Why introduced/removed | Coverage | Residual debt |
|---|---|---|---|
| `NONE introduced` | Phase 0 changed documentation only. | Full source evidence and repository diff review. | Provider dependencies remain proposals in the two blocker issues. |

### Drift assessment

- **Last independent drift review:** `NOT PERFORMED — no implementation exists.`
- **Classification:** `ALIGNED`
- **Owner-relevant differences:** No implementation/architecture exists to drift. The specification's suggested eBay/Trends strategy is now known to be conditional rather than operational; this is a feasibility finding, not a specification rewrite.

## Assumptions and uncertainty that changed

| Certainty | Earlier understanding | Current understanding | Consequence and evidence |
|---|---|---|---|
| `CONFIRMED` | eBay was the preferred candidate in the specification. | Browse/Feed can at most support approved forward collection; historical reconstruction and ProductQuant research-use permission are absent. | Marketplace work is blocked; [evidence](EVIDENCE/EVIDENCE-20260812T060100Z-ebay-source-feasibility.md). |
| `CONFIRMED` | Google Trends was a candidate external signal. | Official API access remains limited alpha; website/provider histories are retrospective and do not prove historical provider state. | Demand history must be labelled pseudo-historical pending a controlled probe; [evidence](EVIDENCE/EVIDENCE-20260812T060101Z-demand-source-feasibility.md). |
| `CONFIRMED` | A cheap historical bootstrap was unknown. | UCI Online Retail II is accessible, digest-verified, CC BY 4.0, and temporally usable after its 22,523-row cross-sheet overlap is removed by a provenance-preserving sheet boundary. | Enables a constrained owner-approved next phase, but not the integrated v0.1 demonstration; [evidence](EVIDENCE/EVIDENCE-20260812T060103Z-historical-dataset-probes.md). |

## Confidence and verification

- **What is directly verified:** Official documentation was checked; credential-free eBay, Amazon, TikTok, DataForSEO, SerpApi, BigQuery, and Trends access boundaries were probed; UCI/Olist archives and Amazon Reviews sample bytes were downloaded outside the repository, hashed, and structurally inspected. See the four evidence records.
- **What was independently reviewed:** Although not required for this documentation-only change, a fresh agent adversarially reviewed the complete package, discovered and verified the UCI overlap and two evidence/certainty inconsistencies, then approved the corrected package after independently rerunning artifact, archive, link, scope, secret, and diff checks. Any future source adoption still requires independent review as recorded by the blockers.
- **What was not run or remains unverified:** No authenticated provider response, account quota, paid/trial task, SLA test, long-term revision study, or legal review occurred. No build/tests exist because there is no implementation.
- **Known regressions or unresolved risks:** No runtime regression is possible. Source access, permitted raw retention, provider revisions, historical marketplace availability, and restrictive licences remain unresolved in the blocker issues.

## Human attention required

| Decision ID | Decision requested | Recommendation and rationale | Alternatives | Needed by | Response | Responder | Decision UTC | Durable authority reference |
|---|---|---|---|---|---|---|---|---|
| `DECISION-PHASE0-01` | May Phase 1 be scoped initially to UCI Online Retail II transaction events while marketplace and demand collectors remain deferred? | Approve the constrained scope because it enables an honest point-in-time transaction backtest without pretending the integrated source stack exists. | Reject and wait for a complete marketplace/demand stack; or explicitly accept Olist's CC BY-NC-SA 4.0 constraints as a separate specification/dependency decision. | Before any Phase 1 implementation | `PENDING` | `PENDING` | `PENDING` | `PENDING` |
| `DECISION-PHASE0-02` | May the project apply for official Trends API alpha and, separately, create a DataForSEO account using only trial credit for a controlled Standard-queue probe? | Apply for the official alpha first; authorise DataForSEO only as a zero-purchase fallback probe with no paid top-up and with retention/revision evidence required. | Defer demand access and accumulate no external-demand snapshots; or later evaluate another documented provider under equivalent gates. | Before demand-source implementation | `PENDING` | `PENDING` | `PENDING` | `PENDING` |
| `DECISION-PHASE0-03` | Should the project pursue eBay written permission and production eligibility for the intended archival, pricing/category, ranking, and model research use? | Do not implement eBay first; pursue it only if the owner is willing to obtain written use/retention permission and independent contract review. | Select another marketplace and repeat the full Phase 0 evidence criteria; Amazon/TikTok are not current substitutes. | Before marketplace-source implementation | `PENDING` | `PENDING` | `PENDING` | `PENDING` |

A response is approval evidence only when its decision, responder identity, UTC time, and durable authority reference are all recorded. The responsible participant must then update the affected specification, ADR, or both and link this decision before implementation relies on it. A product or public-contract decision must update `PROJECT_SPEC.md`; an ADR alone is insufficient.

## No human attention required

- Phase 0 used only public documentation, credential-free failures, and public dataset downloads; it created no account, external cost, remote change, or production implementation.
- No owner response is needed merely to preserve the Phase 0 evidence and close its documentation issue.

## Next checkpoint trigger

- **Trigger:** Owner response to any `DECISION-PHASE0-*` row, source documentation older than 30 days, or a provider access/terms change.
- **Expected owner action before then:** Decide `DECISION-PHASE0-01`; the other decisions may remain pending if marketplace and demand work stay deferred.
