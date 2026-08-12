# Marketplace Source Access and Research-Use Authorization

## Metadata

- **ID:** `ISSUE-20260812T061002Z-marketplace-source-authorization`
- **Title:** `Clear a marketplace source for archival quantitative research`
- **Status:** `BLOCKED`
- **Severity:** `HIGH`
- **Owner:** `human:technical-owner`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-12T06:10:02Z`
- **Updated UTC:** `2026-08-12T06:10:02Z`
- **Requirements:** [`PROJECT_SPEC.md` sections 9–11, 16–18, 21, 40–42, 50–51, and 53](../PROJECT_SPEC.md)
- **ADRs:** `NONE`
- **Evidence:** [`EVIDENCE-20260812T060100Z-ebay-source-feasibility`](../EVIDENCE/EVIDENCE-20260812T060100Z-ebay-source-feasibility.md); [`EVIDENCE-20260812T060102Z-amazon-tiktok-source-feasibility`](../EVIDENCE/EVIDENCE-20260812T060102Z-amazon-tiktok-source-feasibility.md)

## Problem

No investigated marketplace source is both currently accessible and demonstrably licensed for ProductQuant's intended long-term raw archival, category/pricing analysis, ranking, model use, and point-in-time research. Implementing a collector now could create an unusable data asset or violate provider terms.

## Evidence or reproduction

The linked Phase 0 evidence establishes that eBay Browse and Feed are the strongest technical forward-collection candidates, but require production approval and expose no pre-collection historical state. Published eBay API licence clauses appear materially incompatible with the intended archival and analytical use unless eBay grants written permission or a specific contract governs that use. Amazon Creators API is affiliate-oriented current content with short caching restrictions; Amazon SP-API and TikTok Shop require merchant authorisation and do not provide a marketplace-wide historical universe.

## Expected behavior

`PROJECT_SPEC.md` requires evidence-backed source capabilities, immutable raw observations where permitted, reconstructable historical universes, and point-in-time-safe factors. Section 53 requires escalation before accepting restrictive commercial terms, using unauthorised credentials, or creating material costs. The repository must defer marketplace implementation until those requirements can be met honestly.

## Assumptions

- **CONFIRMED:** Public unauthenticated probes cannot validate production field coverage, actual quota, account eligibility, or credential-scoped terms.
- **INFERRED:** eBay Browse plus Feed is the least-bad examined route for prospective marketplace collection, subject to explicit provider permission and authenticated validation.
- **UNKNOWN:** Whether eBay will permit ProductQuant's research purpose, permanent raw preservation, derived ranking/model work, and necessary retention under a written agreement.

## Investigation and decision

Do not adopt or implement an eBay, Amazon, or TikTok marketplace dependency from the Phase 0 recommendation alone. If the owner chooses to pursue eBay, obtain and review written provider permission or a specific governing contract, then perform a minimal authenticated response probe before proposing any specification/dependency decision. A different marketplace may be substituted only after equivalent licence, access, field, history, timestamp, and raw-retention evidence is recorded.

## Change

- **Files or components:** Issue, evidence, source registry, recommendation, human checkpoint, and handoff documentation only.
- **Behavior changed:** No source dependency or collector is adopted; the marketplace portion of Phase 1 remains explicitly gated.
- **Out-of-scope work deliberately excluded:** Account creation, credential use, production API calls, legal acceptance, paid access, collector implementation, storage design, and changes to `PROJECT_SPEC.md` or ADRs.
- **Rollback or recovery:** Not applicable; this record preserves an unresolved external constraint.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| External provider dependency, credentials, contract, and continuous snapshot process | Would be required only if a marketplace source is later adopted. | Phase 0 evidence covers public feasibility only. | This issue remains open until the exact dependency and permitted use are verified and authorised. |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-12T06:10:02Z` | `agent:codex-phase0-recovery` | Review eBay, Amazon, and TikTok official documentation and credential-free endpoint probes; compare fields/history/terms with `PROJECT_SPEC.md`. | Public feasibility evidence completed; no marketplace source cleared. | Evidence links in Metadata. | Contract interpretation is not legal advice; no production account or authenticated response was available. |

## Self-review

- **Participant:** `NOT APPLICABLE`
- **Reviewed UTC:** `NOT APPLICABLE`
- **Reviewed repository state:** `NOT APPLICABLE`
- **Scope and authority references:** `NOT APPLICABLE`
- **Checks and evidence reviewed:** `NOT APPLICABLE`
- **Findings and corrections:** `NOT APPLICABLE`
- **Limitations:** `NOT APPLICABLE`
- **Residual risks:** `NOT APPLICABLE`
- **Outcome:** `NOT_APPLICABLE`

## Independent review rounds

- **Required:** `YES — resolving this issue would adopt an external dependency/contract and define permitted data retention and use.`

No review round has occurred. The issue is blocked before implementation.

## Blocker

- **Blocked from:** `INVESTIGATING`
- **Blocker:** No written provider permission or reviewed contract establishes that ProductQuant may archive raw marketplace data and use it for category/pricing research, rankings, derived models, and reproducible backtests; no authorised production credential/sample exists.
- **Unblock owner:** `human:technical-owner`, with provider and legal/contract review as appropriate.
- **Unblock condition:** Record written permission or a specific reviewed contract covering the intended use, owner-authorised production credentials, and an authenticated minimal sample confirming required fields, timestamps, actual quota, raw-retention rights, and operational constraints. Persist the resulting product/dependency decision in its protocol-owned authoritative artifact before implementation.

## Residual uncertainty

- Whether eBay or another marketplace will grant the necessary research and retention rights; the owner of this uncertainty is `human:technical-owner`.
- Whether authenticated production responses match public documentation; resolve only after authorised access exists.
- Historical marketplace backfill remains unavailable even if forward access is granted.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-12T06:10:02Z` | `agent:codex-phase0-recovery` | `NONE` | `OPEN` | Created a durable issue because public source research found a material marketplace access/contract uncertainty that outlives Phase 0. |
| `2026-08-12T06:10:02Z` | `agent:codex-phase0-recovery` | `OPEN` | `INVESTIGATING` | Compared the examined providers against archival, timestamp, historical-universe, and point-in-time requirements. |
| `2026-08-12T06:10:02Z` | `agent:codex-phase0-recovery` | `INVESTIGATING` | `BLOCKED` | Only the human owner and provider/contract evidence can authorise the required external use; no safe collector implementation can continue. |

## Closure checklist

- [ ] Expected behavior is tied to a higher-authority source.
- [ ] The change or resolution is recorded.
- [ ] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [ ] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies.
- [ ] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [ ] Required human authority is recorded in the owning artifact: product/contract in `PROJECT_SPEC.md`, architecture in an accepted ADR, or both for a mixed decision.
- [ ] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [ ] Residual uncertainty is absent or explicitly owned.
- [ ] HANDOFF reflects the resulting current state and exactly one next action.
