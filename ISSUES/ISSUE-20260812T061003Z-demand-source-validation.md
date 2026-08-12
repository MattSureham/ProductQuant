# Demand Source Access, Retention, and Revision Validation

## Metadata

- **ID:** `ISSUE-20260812T061003Z-demand-source-validation`
- **Title:** `Validate a demand source without overstating historical correctness`
- **Status:** `BLOCKED`
- **Severity:** `HIGH`
- **Owner:** `human:technical-owner`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-12T06:10:03Z`
- **Updated UTC:** `2026-08-12T06:10:03Z`
- **Requirements:** [`PROJECT_SPEC.md` sections 12–17, 21, 40–42, 50–51, and 53](../PROJECT_SPEC.md)
- **ADRs:** `NONE`
- **Evidence:** [`EVIDENCE-20260812T060101Z-demand-source-feasibility`](../EVIDENCE/EVIDENCE-20260812T060101Z-demand-source-feasibility.md)

## Problem

No investigated external-demand interface currently proves both authorised permanent raw-response retention and reconstruction of the demand values that were knowable at historical factor time `t`. Treating a present-day retrospective Google Trends series as strict point-in-time history would invalidate the backtest.

## Evidence or reproduction

The official Google Trends API remains limited-access alpha and its public documentation omits endpoint, auth, price, quota, retention, revision, and response-schema details. Manual Trends data and documented third-party interfaces return present estimates of past interest under sampling, noise, filtering, and request-window normalization. DataForSEO and SerpApi reject credential-free calls, so raw payload shape, actual quota, repeatability, and retention rights remain unverified. The official BigQuery top/rising dataset is selection-leaky for historical universe construction.

## Expected behavior

`PROJECT_SPEC.md` sections 13 and 21 require preservation of normalization context and prohibit future information in factors, universe construction, and model inputs. Sections 40–42 require evidence-backed access, rate, history, automation, legal, retention, and reliability claims. Section 53 requires human approval before account/cost/terms commitments.

## Assumptions

- **CONFIRMED:** A query whose normalization window extends beyond factor time `t` uses future information in earlier relative values.
- **INFERRED:** The official Trends alpha is the best strategic candidate; DataForSEO Google Trends Explore Standard is the most practical small probe if the owner authorises account creation and trial-credit use without purchase.
- **UNKNOWN:** Whether identical historical queries are stable across retrievals, how revisions are surfaced, whether permanent internal raw storage is permitted, and how interval/timezone semantics appear in actual responses.

## Investigation and decision

Apply to the official Trends alpha first if the owner wishes to pursue demand collection. Separately, the owner may authorise a zero-purchase DataForSEO trial-credit probe using its Google Trends Explore Standard queue. Do not adopt DataForSEO's opaque proprietary Trends signal. A successful probe must preserve complete redacted raw JSON and digests, compare repeated fixed windows ending at historical cutoffs, include high- and low-volume terms, check missingness and timezone/interval semantics, compare one result with a manual CSV export, and obtain written clarification on permanent internal raw-response retention.

## Change

- **Files or components:** Issue, evidence, source registry, recommendation, human checkpoint, and handoff documentation only.
- **Behavior changed:** No demand dependency or collector is adopted; retrospective series remain labelled pseudo-historical.
- **Out-of-scope work deliberately excluded:** Account creation, API keys, paid top-up, provider contract acceptance, automated Trends-page access, `pytrends`, undocumented endpoint collection, and Phase 1 implementation.
- **Rollback or recovery:** Not applicable; this record preserves an unresolved external constraint.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| External account/dependency, normalization calibration, repeated sampling, and snapshot retention | Would be required only if a demand source is later adopted. | Public documentation and credential-free probes cover feasibility, not authenticated behaviour. | This issue remains open until authorised response and terms evidence exists. |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-12T06:10:03Z` | `agent:codex-phase0-recovery` | Review official Google Trends, BigQuery, DataForSEO, and SerpApi documentation; run credential-free endpoint/UI probes; analyse point-in-time normalization and revision risk. | Public feasibility evidence completed; no demand source cleared as strict point-in-time history. | Evidence link in Metadata. | No account, alpha access, API key, paid call, or repeat-response sample was available. |

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

- **Required:** `YES — resolving this issue would adopt an external dependency/contract and define point-in-time and retention behaviour.`

No review round has occurred. The issue is blocked before implementation.

## Blocker

- **Blocked from:** `INVESTIGATING`
- **Blocker:** No authorised alpha/provider account, complete raw response, repeatability/revision study, or written permanent-retention clarification exists.
- **Unblock owner:** `human:technical-owner`, with provider clarification as needed.
- **Unblock condition:** Owner authorises a no-purchase access path; an authorised probe records complete safe raw JSON, digests, actual cost/quota and timestamp semantics; repeated cutoff-ended queries quantify variation/revision; permanent internal retention is confirmed; and an independent review approves the point-in-time classification. Persist any adopted product/dependency decision in its protocol-owned authoritative artifact before implementation.

## Residual uncertainty

- Official Trends alpha admission, quota, price, schema, revision, and storage terms remain unknown.
- Provider-returned retrospective history may be useful as a pseudo-historical proxy but cannot be promoted to strict point-in-time evidence without the required study.
- If no provider is approved, external-demand history remains unavailable and only forward snapshot accumulation is honest.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-12T06:10:03Z` | `agent:codex-phase0-recovery` | `NONE` | `OPEN` | Created a durable issue because demand access, retention, and revision uncertainty remains after public-source research. |
| `2026-08-12T06:10:03Z` | `agent:codex-phase0-recovery` | `OPEN` | `INVESTIGATING` | Compared official and third-party Trends routes against normalization and point-in-time requirements. |
| `2026-08-12T06:10:03Z` | `agent:codex-phase0-recovery` | `INVESTIGATING` | `BLOCKED` | The remaining evidence requires human-authorised account access and provider clarification; no safe implementation can continue. |

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
