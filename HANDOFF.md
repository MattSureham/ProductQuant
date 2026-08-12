# Operational Handoff

Read [`BOOTSTRAP.md`](BOOTSTRAP.md) before using this file. This is operational continuity, not long-term project truth. Preserve attributable activity and evidence.

- Prefix material claims with `CONFIRMED`, `INFERRED`, or `UNKNOWN` and link their support.
- Reconcile shared snapshot fields from evidence, then add your own activity entry.
- Never silently rewrite another participant's activity, evidence, or disagreement.
- Keep exactly one bounded entry under `Next Action`.

## Current State

### Snapshot

- **Snapshot updated UTC:** `2026-08-12T06:43:14Z`
- **Repository state at handoff completion:** Branch `main`, upstream `origin/main`; local `HEAD` is the documentation commit `docs: complete Phase 0 source feasibility spike` containing this snapshot, one commit ahead of `origin/main` base `3ff8644ca6cf01feb43e25aadb6ef6d23d094cf1`; working tree verified clean after the local commit; no push performed.
- **Evidence cutoff:** Public-source checks and probes captured 2026-08-12T06:03:04Z–06:10:26Z; historical archive/schema revalidation captured through 2026-08-12T06:04:56Z; repository verification through this snapshot and the final local commit.
- **External checks:** [eBay](EVIDENCE/EVIDENCE-20260812T060100Z-ebay-source-feasibility.md), [demand](EVIDENCE/EVIDENCE-20260812T060101Z-demand-source-feasibility.md), [Amazon/TikTok](EVIDENCE/EVIDENCE-20260812T060102Z-amazon-tiktok-source-feasibility.md), and [historical datasets](EVIDENCE/EVIDENCE-20260812T060103Z-historical-dataset-probes.md), all checked 2026-08-12.
- **Stale when:** Branch/upstream/ahead/dirty state differs; the expected local Phase 0 commit or evidence files are absent; any cited external documentation, pricing, access rule, licence, endpoint, or dataset digest changes or is older than 30 days; an authenticated response contradicts these findings; a non-terminal task appears; or higher authority changes the scope.
- **CONFIRMED — Recovery state:** Git history, reflogs, and `git fsck` showed that the interrupted run persisted only the initial HANDOFF edit and Phase 0 issue. No hidden commit, recoverable evidence object, implementation, or live process existed. Those valid partial records were preserved; non-persisted probes/tasks were classified `ORPHANED` and rerun.
- **CONFIRMED — Product state:** The repository remains documentation-only. No collector, schema, dependency, executable contract, test, accepted ADR, dataset, credential, or runtime implementation exists.
- **CONFIRMED — Phase 0 state:** [`ISSUE-20260812T031400Z-phase-0-source-feasibility`](ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md) is closed after the cross-sheet UCI finding and evidence/certainty inconsistencies were corrected and an independent adversarial re-review returned `APPROVED`. The [registry](SOURCE_REGISTRY.md) covers 17 candidate interfaces/datasets and the [recommendation](PHASE_0_SOURCE_RECOMMENDATION.md) explicitly rejects a misleading integrated historical claim.
- **CONFIRMED — Source position:** No marketplace or external-demand source is currently cleared for strict point-in-time v0.1 use. UCI Online Retail II is recommended only for a narrow transaction-event historical bootstrap after its 22,523-row cross-sheet overlap is removed by the recorded provenance boundary; eBay remains a blocked prospective candidate; Google Trends/DataForSEO remain blocked demand candidates; Amazon and TikTok are not suitable.
- **CONFIRMED — Verification state:** Four reusable evidence records exist; 79 relative links resolved; all 17 registry rows contain the 11 grouped feasibility dimensions; changed-file placeholder, file-size, and whitespace checks passed; raw probe/download artifacts remained outside Git.

Do not refresh only the timestamp. When a staleness trigger fires, mark affected claims `UNKNOWN`, reconcile them from higher-precedence artifacts and actual repository state, and record the reconciliation as new activity.

### Constraints

- Preserve point-in-time correctness and distinguish transaction-event history, pseudo-historical demand, and forward-only marketplace snapshots.
- Prefer official/documented structured access. Do not introduce Trends browser automation, `pytrends`, undocumented collectors, or fragile scraping under the current evidence.
- Do not push, publish data, create accounts, buy services, accept restrictive terms, use unauthorised credentials, or begin substantial Phase 1 work without the recorded human decision and protocol-owned authority update.
- Do not treat the Phase 0 recommendation as provider permission, legal advice, an accepted dependency, or a change to `PROJECT_SPEC.md`.
- `README.md` remains absent; `BOOTSTRAP.md` is the normative protocol entry point.

### Unverified complexity

No implementation complexity was introduced. Potential provider dependencies, credentials, recurring snapshot processes, retention rules, normalization calibration, and external costs remain unadopted and are owned by the two active blocker issues.

### Background tasks

No non-terminal background task exists. All recovery research/probe agents completed, and their durable results are in the four evidence records. Pre-outage work that had no durable process/reference was recorded as `ORPHANED` in the closed Phase 0 issue rather than represented as active.

## Active Issues

| Issue | Status | Severity | Owner | Authority | Review | Summary | Evidence or unblock condition |
|---|---|---|---|---|---|---|---|
| [`ISSUE-20260812T061002Z-marketplace-source-authorization`](ISSUES/ISSUE-20260812T061002Z-marketplace-source-authorization.md) | `BLOCKED` | `HIGH` | `human:technical-owner` | `HUMAN` | `INDEPENDENT` | Clear a marketplace source for archival quantitative research. | Written provider permission/reviewed contract, owner-authorised production access, authenticated field/quota sample, and raw-retention/use confirmation. |
| [`ISSUE-20260812T061003Z-demand-source-validation`](ISSUES/ISSUE-20260812T061003Z-demand-source-validation.md) | `BLOCKED` | `HIGH` | `human:technical-owner` | `HUMAN` | `INDEPENDENT` | Validate demand access, retention, timestamps, sampling, and revisions. | Owner-authorised no-purchase access, complete safe raw response, repeatability/revision study, retention clarification, and independent point-in-time review. |

## Next Action

Human technical owner: decide `DECISION-PHASE0-01` in [`HUMAN_CHECKPOINT.md`](HUMAN_CHECKPOINT.md)—whether to authorise a constrained UCI Online Retail II transaction-event Phase 1 scope while marketplace and demand collectors remain deferred.

## Recent Activity

### 2026-08-12T06:43:14Z — agent:codex-phase0-recovery — Phase 0 recovery and completion

- **Task:** Reconstruct the interrupted repository state, preserve valid partial work, rerun missing source research, and complete Phase 0 without entering implementation.
- **Context inspected:** Missing `README.md`; complete `BOOTSTRAP.md`, `PROJECT_SPEC.md`, ADR/issue/evidence templates, partial HANDOFF/issue, Git history/reflogs/object integrity, provider documentation/endpoints, and public historical datasets.
- **Actions performed:** Preserved the partial HANDOFF/issue; classified non-persisted work `ORPHANED`; reran credential-free probes and dataset validation; added four evidence records, a 17-source registry, recommendation, two blockers, and owner checkpoint; reopened the Phase 0 issue after adversarial review exposed the UCI cross-sheet overlap; corrected the evidence/stitch rule, registry evidence chain, and certainty convention; closed after independent approval; created one local commit without pushing.
- **Files modified:** `HANDOFF.md`, `HUMAN_CHECKPOINT.md`; four new evidence records; three issue records; `SOURCE_REGISTRY.md`; `PHASE_0_SOURCE_RECOMMENDATION.md`.
- **Findings:** **CONFIRMED** — no valid integrated historical marketplace/demand stack is presently cleared. **CONFIRMED** — UCI supports only a transaction-event historical bootstrap. **INFERRED** — eBay and official Trends remain the strongest strategic candidates but require human/provider unblocks. **UNKNOWN** — authenticated behaviour, retention permission, revisions, and operational reliability.
- **Verification performed:** Git reconstruction and integrity checks; official-document review; safe unauthenticated endpoint probes; UCI/Olist archive/digest/schema/time-range/overlap checks; Amazon Reviews range/field probe; independent artifact/ZIP/UCI/link/scope/secret review; relative-link, registry-dimension, placeholder, size, `git diff --check`, staged-diff, commit-content, clean-worktree, and local/remote divergence checks. No implementation tests exist.
- **Issues created or updated:** Reopened, corrected, and closed [Phase 0 issue](ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md); created [marketplace blocker](ISSUES/ISSUE-20260812T061002Z-marketplace-source-authorization.md) and [demand blocker](ISSUES/ISSUE-20260812T061003Z-demand-source-validation.md).
- **Remaining uncertainty:** Explicitly owned by the two active issues and the pending checkpoint decision; none is represented as completed.
- **Recommended next action:** Decide `DECISION-PHASE0-01`; do not infer approval for marketplace/demand accounts or implementation.

### 2026-08-12T03:14:00Z — agent:codex-phase0 — Phase 0 research owner

- **Task:** Establish repository state and initiate the source-feasibility milestone.
- **Context inspected:** Missing `README.md`; complete `PROJECT_SPEC.md`, `BOOTSTRAP.md`, ADR/issue/evidence templates, `HANDOFF.md`, `HUMAN_CHECKPOINT.md`, example/prompts, Git state, repository tree, local probe tools, and credential variable names.
- **Actions performed:** Reconciled the template HANDOFF and opened the Phase 0 issue; no source or external account was mutated.
- **Files modified:** `HANDOFF.md`; `ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md`.
- **Findings:** **CONFIRMED** — source validation is the specification's first milestone; no implementation or prior evidence exists. **UNKNOWN** — every candidate's current historical and operational suitability awaits evidence.
- **Verification performed:** `git status`, `git log`, repository file inventory, full protocol/specification reads, template-directory inspection, `command -v`, and environment variable-name inspection; commands exited `0` except the expected absence of `README.md` was handled explicitly.
- **Issues created or updated:** [`ISSUE-20260812T031400Z-phase-0-source-feasibility`](ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md).
- **Remaining uncertainty:** Candidate source capabilities, costs, terms, access, rate limits, timestamps, raw preservation, and historical reconstruction.
- **Recommended next action:** Execute reproducible public documentation checks and unauthenticated probes for Phase 0 candidates.

## Archived Summary

- Phase 0 source-feasibility history and closure are retained in [`ISSUE-20260812T031400Z-phase-0-source-feasibility`](ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md), with the four immutable evidence records and negative findings linked there. No activity entry has otherwise been compacted or removed.
