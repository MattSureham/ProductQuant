# Operational Handoff

Read [`BOOTSTRAP.md`](BOOTSTRAP.md) before using this file. This is operational continuity, not long-term project truth. Preserve attributable activity and evidence.

- Prefix material claims with `CONFIRMED`, `INFERRED`, or `UNKNOWN` and link their support.
- Reconcile shared snapshot fields from evidence, then add your own activity entry.
- Never silently rewrite another participant's activity, evidence, or disagreement.
- Keep exactly one bounded entry under `Next Action`.

## Current State

### Snapshot

- **Snapshot updated UTC:** `2026-08-12T07:47:28Z`
- **Repository state:** Branch `main`, upstream `origin/main`; base `HEAD` is Phase 0 commit `9efee6d17735b1bb1c9d11a2bd720a64bc617499`, one commit ahead of upstream. Restricted Phase 1 authority records are in progress and no push is authorised.
- **Evidence cutoff:** Phase 0 external/source checks through 2026-08-12T06:10:26Z; complete UCI schema/precision revalidation captured `2026-08-12T07:34:51Z` and independently reproduced in architecture review round 2; repository verification through this snapshot.
- **External checks:** [eBay](EVIDENCE/EVIDENCE-20260812T060100Z-ebay-source-feasibility.md), [demand](EVIDENCE/EVIDENCE-20260812T060101Z-demand-source-feasibility.md), [Amazon/TikTok](EVIDENCE/EVIDENCE-20260812T060102Z-amazon-tiktok-source-feasibility.md), and [historical datasets](EVIDENCE/EVIDENCE-20260812T060103Z-historical-dataset-probes.md), all checked 2026-08-12.
- **Stale when:** Branch/upstream/ahead/dirty state differs; the expected local Phase 0 commit or evidence files are absent; any cited external documentation, pricing, access rule, licence, endpoint, or dataset digest changes or is older than 30 days; an authenticated response contradicts these findings; a non-terminal task appears; or higher authority changes the scope.
- **CONFIRMED — Recovery state:** Git history, reflogs, and `git fsck` showed that the interrupted run persisted only the initial HANDOFF edit and Phase 0 issue. No hidden commit, recoverable evidence object, implementation, or live process existed. Those valid partial records were preserved; non-persisted probes/tasks were classified `ORPHANED` and rerun.
- **CONFIRMED — Product state:** The repository remains documentation-only while the approved Restricted Phase 1 product contract and proposed architecture undergo the required pre-implementation review. No collector, dependency, test, or runtime implementation exists yet.
- **CONFIRMED — Phase 0 state:** [`ISSUE-20260812T031400Z-phase-0-source-feasibility`](ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md) is closed after the cross-sheet UCI finding and evidence/certainty inconsistencies were corrected and an independent adversarial re-review returned `APPROVED`. The [registry](SOURCE_REGISTRY.md) covers 17 candidate interfaces/datasets and the [recommendation](PHASE_0_SOURCE_RECOMMENDATION.md) explicitly rejects a misleading integrated historical claim.
- **CONFIRMED — Source position:** No marketplace or external-demand source is currently cleared for strict point-in-time v0.1 use. UCI Online Retail II is recommended only for a narrow transaction-event historical bootstrap after its 22,523-row cross-sheet overlap is removed by the recorded provenance boundary; eBay remains a blocked prospective candidate; Google Trends/DataForSEO remain blocked demand candidates; Amazon and TikTok are not suitable.
- **CONFIRMED — Owner authority:** `DECISION-PHASE0-01` approved UCI only as a transaction-event substrate; `DECISION-PHASE1-01` approved the exact restricted dependency, persistence, event-contract, and CLI plan. Both are durably recorded in [`PROJECT_SPEC.md`](PROJECT_SPEC.md) and [`HUMAN_CHECKPOINT.md`](HUMAN_CHECKPOINT.md).
- **CONFIRMED — Active milestone:** [`ISSUE-20260812T072420Z-uci-transaction-data-foundation`](ISSUES/ISSUE-20260812T072420Z-uci-transaction-data-foundation.md) is `IMPLEMENTING`. Its [ADR](ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md) is `ACCEPTED` after independent proposal-review round 3 approved it.
- **CONFIRMED — Verification state:** Five reusable evidence records exist. The newest complete workbook scan confirms required/null/type/integrality/naïve-time/decimal constraints and contains its full reproduction command. Proposal review round 2 independently reproduced it; link and whitespace checks pass. Implementation verification has not started.
- **CONFIRMED — Review state:** Architecture review round 1 is preserved as `BLOCKED`; its authority context was corrected. Round 2 confirmed exact owner authority and revised architecture, then required a durable evidence command, pre-command usage JSON, and checkpoint/handoff reconciliation. These corrections are applied and await final proposal re-review.

Do not refresh only the timestamp. When a staleness trigger fires, mark affected claims `UNKNOWN`, reconcile them from higher-precedence artifacts and actual repository state, and record the reconciliation as new activity.

### Constraints

- Preserve point-in-time correctness and distinguish transaction-event history, pseudo-historical demand, and forward-only marketplace snapshots.
- Prefer official/documented structured access. Do not introduce Trends browser automation, `pytrends`, undocumented collectors, or fragile scraping under the current evidence.
- Do not push, publish data, create accounts, buy services, accept restrictive terms, use unauthorised credentials, or exceed the accepted Restricted Phase 1 scope.
- Implementation may proceed only within the accepted ADR and Restricted Phase 1 specification; a fresh independent implementation review is still required before issue closure.
- Do not implement factors, universes, targets, rankings, backtests, marketplace/demand adapters, a persistent database, generic source framework, or background service.
- `README.md` remains absent until the implementation package adds the approved adoption guide; `BOOTSTRAP.md` remains the normative protocol entry point.

### Unverified complexity

The approved but not yet implemented design introduces locked Python packaging, five packages across runtime/development/build, immutable local raw/normalized state, manifests/receipts, a CLI, and `transaction_event.v1`. Their justification and planned coverage are recorded in the Phase 1 issue/ADR. Provider credentials, recurring snapshots, external costs, and marketplace/demand integrations remain unadopted.

### Background tasks

No non-terminal background task exists. All recovery research/probe agents completed, and their durable results are in the four evidence records. Pre-outage work that had no durable process/reference was recorded as `ORPHANED` in the closed Phase 0 issue rather than represented as active.

## Active Issues

| Issue | Status | Severity | Owner | Authority | Review | Summary | Evidence or unblock condition |
|---|---|---|---|---|---|---|---|
| [`ISSUE-20260812T061002Z-marketplace-source-authorization`](ISSUES/ISSUE-20260812T061002Z-marketplace-source-authorization.md) | `BLOCKED` | `HIGH` | `human:technical-owner` | `HUMAN` | `INDEPENDENT` | Clear a marketplace source for archival quantitative research. | Written provider permission/reviewed contract, owner-authorised production access, authenticated field/quota sample, and raw-retention/use confirmation. |
| [`ISSUE-20260812T061003Z-demand-source-validation`](ISSUES/ISSUE-20260812T061003Z-demand-source-validation.md) | `BLOCKED` | `HIGH` | `human:technical-owner` | `HUMAN` | `INDEPENDENT` | Validate demand access, retention, timestamps, sampling, and revisions. | Owner-authorised no-purchase access, complete safe raw response, repeatability/revision study, retention clarification, and independent point-in-time review. |
| [`ISSUE-20260812T072420Z-uci-transaction-data-foundation`](ISSUES/ISSUE-20260812T072420Z-uci-transaction-data-foundation.md) | `IMPLEMENTING` | `HIGH` | `agent:codex-phase1` | `HUMAN` | `INDEPENDENT` | Build the owner-approved restricted UCI raw/normalized transaction-event foundation. | Implement, run full verification, and obtain independent implementation/architecture review under the accepted ADR. |

## Next Action

Commit the independently approved Restricted Phase 1 authority records locally, then implement only the accepted UCI data foundation.

## Recent Activity

### 2026-08-12T07:41:52Z — agent:codex-phase1 — Proposal-review corrections

- **Task:** Resolve all pre-implementation review findings without beginning code.
- **Context inspected:** Both independent review rounds, newest exact owner approval, specification/ADR/issue/checkpoint/handoff, Phase 0 evidence, and complete pinned workbook.
- **Actions performed:** Made event/storage/manifest/receipt/CLI contracts decision-complete; documented privacy minimization and owner-only local controls; ran and durably recorded a full-workbook schema/precision probe; preserved both review rounds; embedded its exact command; defined pre-command usage JSON; reconciled current records.
- **Files modified:** Phase 1 specification, ADR, issue, checkpoint/handoff, and new schema evidence.
- **Findings:** **CONFIRMED** — newest human message explicitly authorises the exact Phase 1 plan. **CONFIRMED** — pinned workbook fits the required schema and decimal contract. **UNKNOWN** — implementation behavior remains unverified.
- **Verification performed:** Full-workbook scan, independent reproduction, relative-link resolution, placeholder scan, and `git diff --check`.
- **Issues created or updated:** Phase 1 issue remains `INVESTIGATING` pending final proposal approval.
- **Remaining uncertainty:** Runtime/package/Parquet behavior awaits implementation; longer-term source/time/cancellation limitations remain explicit.
- **Recommended next action:** Final independent proposal re-review, then ADR acceptance and first local commit if approved.

### 2026-08-12T07:24:20Z — agent:codex-phase1 — Restricted Phase 1 authority capture

- **Task:** Persist the owner's UCI-only scope approval and decision-complete Phase 1 architecture before implementation.
- **Context inspected:** Clean Phase 0 commit, complete protocol/specification, checkpoint/handoff, source registry/recommendation/evidence, templates, Git state, and available local tooling.
- **Actions performed:** Recorded `DECISION-PHASE0-01` and `DECISION-PHASE1-01`; added the restricted product/data/CLI contract to the specification; opened the independently reviewed Phase 1 issue; drafted the architecture ADR.
- **Files modified:** `PROJECT_SPEC.md`, `HUMAN_CHECKPOINT.md`, `HANDOFF.md`, the new Phase 1 issue, and the new ADR proposal.
- **Findings:** **CONFIRMED** — owner authority is sufficient for the exact restricted plan. **CONFIRMED** — protocol still requires an accepted ADR and independent review before/after implementation. **UNKNOWN** — implementation correctness and complexity coverage remain unverified.
- **Verification performed:** Repository/state reconciliation and authority/source cross-check only; implementation checks are not yet applicable.
- **Issues created or updated:** Created [`ISSUE-20260812T072420Z-uci-transaction-data-foundation`](ISSUES/ISSUE-20260812T072420Z-uci-transaction-data-foundation.md).
- **Remaining uncertainty:** Recorded in the issue/ADR; marketplace/demand blockers are unchanged.
- **Recommended next action:** Independently review the specification/ADR proposal before acceptance and code.

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
