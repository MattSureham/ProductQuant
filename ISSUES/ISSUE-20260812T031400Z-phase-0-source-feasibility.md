# Phase 0 Source Feasibility Spike

## Metadata

- **ID:** `ISSUE-20260812T031400Z-phase-0-source-feasibility`
- **Title:** `Establish a feasible v0.1 source stack`
- **Status:** `CLOSED`
- **Severity:** `HIGH`
- **Owner:** `agent:codex-phase0-recovery`
- **Authority:** `AGENT`
- **Review:** `SELF`
- **Created UTC:** `2026-08-12T03:14:00Z`
- **Updated UTC:** `2026-08-12T06:39:43Z`
- **Requirements:** [`PROJECT_SPEC.md` sections 8–18, 21, 40–42, 50–51, and 53](../PROJECT_SPEC.md)
- **ADRs:** `NONE`
- **Evidence:** [`EVIDENCE-20260812T060100Z-ebay-source-feasibility`](../EVIDENCE/EVIDENCE-20260812T060100Z-ebay-source-feasibility.md); [`EVIDENCE-20260812T060101Z-demand-source-feasibility`](../EVIDENCE/EVIDENCE-20260812T060101Z-demand-source-feasibility.md); [`EVIDENCE-20260812T060102Z-amazon-tiktok-source-feasibility`](../EVIDENCE/EVIDENCE-20260812T060102Z-amazon-tiktok-source-feasibility.md); [`EVIDENCE-20260812T060103Z-historical-dataset-probes`](../EVIDENCE/EVIDENCE-20260812T060103Z-historical-dataset-probes.md)

## Problem

ProductQuant cannot begin a point-in-time-safe research loop until current marketplace, external-demand, and historical bootstrap sources are verified for accessibility, fields, timestamps, history, cost, operational constraints, and permitted preservation. Documentation-only assumptions could cause the project to build against unavailable, prohibited, or non-historical interfaces.

## Evidence or reproduction

Repository reconstruction after the interrupted run found base commit `3ff8644ca6cf01feb43e25aadb6ef6d23d094cf1`, with only `HANDOFF.md` modified and this issue untracked. `git fsck --full --no-reflogs` reported no recoverable dangling work; reflogs contained only the initial commit/fetch/push; no durable evidence, hidden commit, implementation, or live background process existed. The partial HANDOFF/issue initialization was valid and was preserved. Pre-outage source probes and delegated work had not been persisted and were therefore treated as interrupted/unverified until independently rerun.

The four evidence records link official documentation, exact safe probe commands and responses, and historical-dataset download/schema/digest checks. [`SOURCE_REGISTRY.md`](../SOURCE_REGISTRY.md) compares 17 interfaces/datasets against every requested feasibility dimension. [`PHASE_0_SOURCE_RECOMMENDATION.md`](../PHASE_0_SOURCE_RECOMMENDATION.md) records the resulting source position and preserves negative findings.

## Expected behavior

`PROJECT_SPEC.md` sections 40–42 and 51 require an evidence-backed source registry, lightweight feasibility validation, cost and historical-data assessment, and recommendations for the initial marketplace and demand sources before substantial factor infrastructure is built. Section 21 makes point-in-time correctness a hard requirement, and section 53 forbids purchases, material external costs, restrictive-term acceptance, and unauthorised private credentials without escalation.

## Assumptions

- **CONFIRMED:** Public documentation, public endpoints, and locally available credential-free probes were authorised by `PROJECT_SPEC.md` section 53 and the owner's Phase 0 instruction.
- **CONFIRMED:** No examined provider currently supplies an accessible and authorised combination of reconstructable marketplace state and independent historical demand.
- **CONFIRMED:** UCI Online Retail II is anonymously downloadable under CC BY 4.0 and supports a dated transaction-event backtest after the verified cross-sheet overlap is removed by provenance boundary and every feature/universe decision uses only invoice rows available by cutoff `t`.
- **INFERRED:** eBay Browse plus Feed is the strongest examined prospective marketplace path, subject to written use/retention permission and authenticated production validation.
- **INFERRED:** Official Google Trends alpha is the strongest strategic demand candidate, while DataForSEO Google Trends Explore Standard is the strongest practical conditional probe; neither currently proves historical provider-state reconstruction.
- **UNKNOWN:** Source-specific permissions, authenticated payloads, historical revisions, production quotas, and long-term operational reliability remain unresolved and are now owned by the marketplace and demand blocker issues.

## Investigation and decision

Phase 0 makes no provider adoption decision and introduces no dependency. The evidence supports these non-binding recommendations:

1. **Marketplace:** none is cleared for v0.1. Keep eBay `CONDITIONAL/BLOCKED` and consider it only for forward collection after written permission and an authenticated probe.
2. **External demand:** none is cleared as strict historical point-in-time data. Prefer the official Trends alpha strategically and DataForSEO Standard only for a human-authorised, zero-purchase validation; label present retrospective histories pseudo-historical.
3. **Historical bootstrap:** recommend UCI Online Retail II for a narrow transaction-event research loop. Do not represent it as historical listing state, external demand, or completion of the integrated v0.1 demonstration.
4. **Alternatives:** Amazon and TikTok interfaces are not suitable; Olist remains conditional on human acceptance of CC BY-NC-SA 4.0; Amazon Reviews 2023 remains excluded because product metadata lacks historical observation time and sufficient archival licensing was not established.

The remaining authority/access work was transferred to [`ISSUE-20260812T061002Z-marketplace-source-authorization`](ISSUE-20260812T061002Z-marketplace-source-authorization.md) and [`ISSUE-20260812T061003Z-demand-source-validation`](ISSUE-20260812T061003Z-demand-source-validation.md).

## Change

- **Files or components:** Four `EVIDENCE/` records, `SOURCE_REGISTRY.md`, `PHASE_0_SOURCE_RECOMMENDATION.md`, two blocker issues, this issue, `HUMAN_CHECKPOINT.md`, and `HANDOFF.md`.
- **Behavior changed:** No product/runtime behavior. Phase 0 research became durable and resumable; invalid source paths and residual blockers are explicit.
- **Out-of-scope work deliberately excluded:** Phase 1 collectors/storage, schemas, dependencies, browser automation, scraping, account creation, credentials, paid subscriptions, external publication/push, raw datasets, and changes to `PROJECT_SPEC.md` or ADRs.
- **Rollback or recovery:** Revert the documentation commit. No external source or account state was mutated.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| `NONE introduced` | Phase 0 introduced documentation only. | Full diff, evidence, link, registry, scope, and Git-state checks. | Proposed provider dependencies and processes remain deferred in the two blocker issues. |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-12T03:14:00Z` | `agent:codex-phase0` | Inspect repository files, Git state, source/evidence directories, local tool paths, and credential variable names. | Exit `0`; clean base revision, templates only, `curl`/`jq`/`python3` available, no matching credential variable names. | Inline initial repository inspection. | Variable-name inspection does not prove credentials cannot exist outside the process environment. |
| `2026-08-12T06:00:01Z` | `agent:codex-phase0-recovery` | Re-read protocol/spec/templates; run `git status`, `git log`, `git rev-parse`, `git fsck --full --no-reflogs`, and reflog inspection. | Exit `0`; HEAD and `origin/main` both `3ff8644`; only the partial HANDOFF and Phase 0 issue persisted; no recoverable hidden commit/object or implementation found. | This issue and recovered HANDOFF activity. | A power-loss process with no filesystem or remote artifact cannot be reconstructed; its outputs were rerun instead. |
| `2026-08-12T06:03:04Z–06:10:26Z` | `agent:codex-phase0-evidence-team` | Run the credential-free endpoint commands and official-document comparisons recorded in the eBay, demand, and Amazon/TikTok evidence files. | Transport commands exited `0`; expected authentication/throttling HTTP responses were preserved and interpreted only as access-boundary evidence. | First three evidence links in Metadata. | No successful authenticated provider payload, account quota, SLA, or negotiated contract was available. |
| `2026-08-12T06:04:56Z` | `agent:codex-phase0-recovery` | Validate UCI/Olist archives and digests; stream workbook/CSV records; range-probe Amazon Reviews; inspect official dataset metadata. | Exit `0`; archive integrity, schemas, row counts, event ranges, anomalies, and digests recorded. | Historical dataset evidence in Metadata. | Raw downloads remain transient under `/tmp`; dataset timezone/revision limits remain documented uncertainty. |
| `2026-08-12T06:12:25Z–06:18:22Z` | `agent:codex-phase0-recovery` | Run `git diff --check`; targeted placeholder/large-file scans; relative Markdown-link checker; registry row/dimension checker; inspect source documents and changed files. | Checks exited `0`: 79 relative links resolved; 17 registry rows each contained 11 non-empty grouped dimensions; no file over 1 MiB; no placeholder diagnostic or whitespace error. | Inline command output and full repository diff. | The first registry checker expected 16 rows and failed because 17 candidates were intentionally recorded; it was corrected to the actual explicit registry count and rerun successfully. External URLs were not guaranteed by the relative-link checker. A later adversarial review found an untested cross-sheet overlap, so this was not the final verification. |
| `2026-08-12T06:29:18Z` | `agent:codex-phase0-recovery` | Compare complete UCI rows for `2010-12-01 <= InvoiceDate < 2010-12-10` as `Counter` multisets across the two workbook sheets. | Exit `0`; each slice had 22,523 rows and 22,202 unique tuples; Counters were equal; retaining one overlap copy yields 1,044,848 physical rows. | Historical dataset evidence correction. | Within-sheet duplicate tuples may be legitimate; the rule stitches by sheet provenance rather than blanket tuple deduplication. |
| `2026-08-12T06:39:43Z` | `agent:codex-independent-phase0-review` | Re-read the protocol/spec/package; re-hash transient artifacts; revalidate both ZIPs and UCI Counter probe; check cached/working diffs, 79 relative links, HANDOFF structure, scope, sizes, secrets, and prohibited files. | `APPROVED`; no remaining material finding. All checks passed. | Independent review summary below and evidence files. | Review cannot establish authenticated provider behaviour, legal permission, or external SLA; those remain in the blocker issues. |

## Self-review

- **Participant:** `agent:codex-phase0-recovery`
- **Reviewed UTC:** `2026-08-12T06:39:43Z`
- **Reviewed repository state:** Base `3ff8644ca6cf01feb43e25aadb6ef6d23d094cf1` plus the documentation files listed under Change; no staged or committed state was assumed during review.
- **Scope and authority references:** Documentation-only Phase 0 work under `PROJECT_SPEC.md` sections 8–18, 21, 40–42, 50–51, and 53; no accepted ADR required.
- **Checks and evidence reviewed:** All four evidence records, all 17 registry entries, recommendation, blocker ownership/unblock conditions, checkpoint, handoff requirements, relative links, placeholders, file sizes, diff whitespace, Git history/state, and exclusion of implementation/data/credentials.
- **Findings and corrections:** Corrected the registry's TikTok Bestsellers lookback from an unsupported numeric range to `UNKNOWN`; explicitly separated pseudo-historical demand from event history; retained the failed initial registry-count assertion and successful correction in Verification. Adversarial review found an unrecorded 22,523-row cross-sheet UCI overlap; the evidence, registry, recommendation, checkpoint, and handoff now require a provenance-preserving stitch. Review also corrected an evidence-chain gap for SerpApi/DataForSEO proprietary Trends and an overbroad registry certainty convention.
- **Limitations:** No authenticated source response, legal opinion, provider account, longitudinal revision study, external SLA measurement, or implementation test exists.
- **Residual risks:** Marketplace access/contract and demand access/retention/revision risks are explicitly owned by the two open human-authority issues; UCI-only scope still requires the owner decision recorded in `HUMAN_CHECKPOINT.md`.
- **Outcome:** `COMPLETE`

## Independent review rounds

- **Required:** `NO — the completed change is local, reversible research documentation and adopts no external contract, dependency, persistent state, public behavior, security boundary, concurrency, or long-term implementation complexity.`

An optional adversarial review was nevertheless performed because recovery work and external-source evidence benefit from a fresh perspective.

### 2026-08-12T06:39:43Z — agent:codex-independent-phase0-review

- **Reviewed repository state:** Staged Phase 0 package over base `3ff8644ca6cf01feb43e25aadb6ef6d23d094cf1`.
- **Scope:** Protocol and relevant specification sections; registry, recommendation, checkpoint, handoff, four evidence records, three issues, staged/working diffs, transient archive integrity, and UCI workbook overlap.
- **Commands or procedures:** Re-hashed the UCI/Olist/Amazon range artifacts; ran ZIP validation; independently compared the UCI overlap slices as full-row `Counter` multisets; checked 79 relative links, five HANDOFF sections, exactly one Next Action, placeholders, large files, secrets, prohibited paths, `git diff --cached --check`, and `git diff --check`.
- **Specification compliance:** Phase 0 documents access, cost, rates, fields, history, timestamps, reconstructability, point-in-time safety, reliability, terms, raw preservation, and v0.1 status without adopting a dependency or entering Phase 1.
- **Correctness and regression findings:** Initial review found the UCI cross-sheet overlap, a SerpApi/DataForSEO registry-to-evidence inconsistency, and overbroad certainty wording. All were reproduced and corrected. The UCI rule now yields 1,044,848 physical rows by sheet provenance and does not remove possibly legitimate within-sheet duplicates.
- **Architecture and complexity findings:** No runtime architecture, dependency, persistent state, public contract, or implementation complexity was introduced.
- **Material findings and resolution conditions:** `NONE REMAINING`.
- **Limitations:** No authenticated provider response, legal opinion, negotiated permission, external SLA measurement, or Phase 1 implementation was reviewed.
- **Residual risks:** Explicitly owned by the marketplace/demand blocker issues and pending owner decision.
- **Evidence:** Four evidence records and this issue's Verification rows.
- **Disposition:** `APPROVED`
- **Prior-round resolution:** First complete independent disposition; the material adversarial findings delivered during the round are enumerated above and resolved in the staged package.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE — this Phase 0 investigation is complete; unresolved source adoption work has separate issue ownership.`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- No residual uncertainty is silently owned by this closed investigation. Marketplace permission/access uncertainty is owned by `ISSUE-20260812T061002Z-marketplace-source-authorization`; demand access/retention/revision uncertainty is owned by `ISSUE-20260812T061003Z-demand-source-validation`; the constrained Phase 1 scope decision is pending in `HUMAN_CHECKPOINT.md`.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-12T03:14:00Z` | `agent:codex-phase0` | `NONE` | `OPEN` | Created the issue because source feasibility gates Phase 1 and material uncertainty must survive the session. |
| `2026-08-12T03:14:00Z` | `agent:codex-phase0` | `OPEN` | `INVESTIGATING` | Began repository-grounded public-source research under the owner-authorised Phase 0 scope. |
| `2026-08-12T06:00:01Z` | `agent:codex-phase0-recovery` | `INVESTIGATING` | `INVESTIGATING` | Reconstructed Git/disk state after the interruption. The partial issue/HANDOFF were valid; missing prior probes and agent work were classified `ORPHANED` because no process, evidence file, commit, or recoverable Git object existed. Research was rerun rather than inferred. |
| `2026-08-12T06:16:11Z` | `agent:codex-phase0-recovery` | `INVESTIGATING` | `VERIFYING` | Completed the registry, recommendation, four evidence records, historical probes, and durable residual blocker records. |
| `2026-08-12T06:16:12Z` | `agent:codex-phase0-recovery` | `VERIFYING` | `REVIEW` | Performed protocol, source-coverage, link, scope, and repository-diff self-review; corrected the unsupported TikTok lookback and registry-count expectation. |
| `2026-08-12T06:16:13Z` | `agent:codex-phase0-recovery` | `REVIEW` | `CLOSED` | Self-review outcome `COMPLETE`; evidence-backed recommendations are durable, and all remaining uncertainty has explicit open issue/owner/unblock conditions. |
| `2026-08-12T06:29:18Z` | `agent:codex-phase0-recovery` | `CLOSED` | `OPEN` | Reopened under the protocol after adversarial review found that the two UCI sheets duplicate 22,523 physical rows across their nine-day overlap. |
| `2026-08-12T06:29:19Z` | `agent:codex-phase0-recovery` | `OPEN` | `VERIFYING` | Reproduced the overlap and began correcting every affected claim and future ingestion rule. |
| `2026-08-12T06:39:42Z` | `agent:codex-phase0-recovery` | `VERIFYING` | `REVIEW` | All corrections were staged and verification rerun; requested a fresh full-package adversarial disposition. |
| `2026-08-12T06:39:43Z` | `agent:codex-phase0-recovery` | `REVIEW` | `CLOSED` | Independent adversarial disposition `APPROVED`; self-review updated to `COMPLETE`; no material finding remains, and all residual uncertainty has explicit ownership. |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source.
- [x] The change or resolution is recorded.
- [x] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies.
- [x] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved. `NOT APPLICABLE — Review is SELF.`
- [x] Required human authority is recorded in the owning artifact: no dependency/product decision was adopted; pending decisions are in `HUMAN_CHECKPOINT.md` and blocker issues.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue. `NONE introduced.`
- [x] Residual uncertainty is absent or explicitly owned.
- [x] HANDOFF reflects the resulting current state and exactly one next action.
