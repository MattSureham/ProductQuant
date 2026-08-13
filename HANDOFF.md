# Operational Handoff

Read [`BOOTSTRAP.md`](BOOTSTRAP.md) before using this file. This is operational continuity, not long-term project truth. Preserve attributable activity and evidence.

- Prefix material claims with `CONFIRMED`, `INFERRED`, or `UNKNOWN` and link their support.
- Reconcile shared snapshot fields from evidence, then add your own activity entry.
- Never silently rewrite another participant's activity, evidence, or disagreement.
- Keep exactly one bounded entry under `Next Action`.

## Current State

### Snapshot

- **Snapshot updated UTC:** `2026-08-13T01:42:50Z`
- **Repository state:** Branch `main`, upstream `origin/main`; `HEAD` is the Phase 1 milestone-closure commit `e21dd45`, four commits ahead of upstream. The independently approved Restricted Phase 2 proposal records (issue, proposed ADR, feasibility evidence) plus checkpoint/HANDOFF updates are committed locally in this run; an untracked `.claude/` local-tooling lock file is deliberately excluded. No push is authorised.
- **Evidence cutoff:** Phase 0 external/source checks through 2026-08-12T06:10:26Z; UCI schema/precision revalidation `2026-08-12T07:34:51Z`; Phase 1 implementation verification through `2026-08-12T10:12:21Z`; takeover revalidation `2026-08-13T01:04:45Z`; Phase 2 feasibility profile `2026-08-13T01:16:28Z` (independently reproduced twice).
- **External checks:** [eBay](EVIDENCE/EVIDENCE-20260812T060100Z-ebay-source-feasibility.md), [demand](EVIDENCE/EVIDENCE-20260812T060101Z-demand-source-feasibility.md), [Amazon/TikTok](EVIDENCE/EVIDENCE-20260812T060102Z-amazon-tiktok-source-feasibility.md), and [historical datasets](EVIDENCE/EVIDENCE-20260812T060103Z-historical-dataset-probes.md), all checked 2026-08-12 and stale after 2026-09-11.
- **Stale when:** Branch/upstream/ahead/dirty state differs; the expected local commits or evidence files are absent; any cited external documentation, pricing, access rule, licence, endpoint, or dataset digest changes or is older than 30 days; an authenticated response contradicts these findings; a non-terminal task appears; or higher authority changes the scope.
- **CONFIRMED — Recovery state:** Git history, reflogs, and `git fsck` showed that the interrupted run persisted only the initial HANDOFF edit and Phase 0 issue. No hidden commit, recoverable evidence object, implementation, or live process existed. Those valid partial records were preserved; non-persisted probes/tasks were classified `ORPHANED` and rerun.
- **CONFIRMED — Product state:** The Restricted Phase 1 UCI transaction-event foundation is implemented at `c937c3f`: a locked Python package with a four-command CLI (`uci fetch|normalize|verify|prepare`), immutable content-addressed raw ZIP, `transaction_event.v1` Parquet, ephemeral DuckDB verification, and row-free manifests/receipts under Git-ignored `data/`. No factor, universe, target, ranking, backtest, marketplace/demand adapter, persistent database, or service exists; Phase 2 remains unauthorised.
- **CONFIRMED — Phase 0 state:** [`ISSUE-20260812T031400Z-phase-0-source-feasibility`](ISSUES/ISSUE-20260812T031400Z-phase-0-source-feasibility.md) is closed after the cross-sheet UCI finding and evidence/certainty inconsistencies were corrected and an independent adversarial re-review returned `APPROVED`. The [registry](SOURCE_REGISTRY.md) covers 17 candidate interfaces/datasets and the [recommendation](PHASE_0_SOURCE_RECOMMENDATION.md) explicitly rejects a misleading integrated historical claim.
- **CONFIRMED — Source position:** No marketplace or external-demand source is currently cleared for strict point-in-time v0.1 use. UCI Online Retail II is [`IMPLEMENTED — RESTRICTED HISTORICAL FOUNDATION`](SOURCE_REGISTRY.md): the pinned 22,523-row-overlap-corrected transaction-event substrate is preserved and normalized locally, with no marketplace, competition, or independent-demand capability implied. eBay remains a blocked prospective candidate; Google Trends/DataForSEO remain blocked demand candidates; Amazon and TikTok are not suitable.
- **CONFIRMED — Owner authority:** `DECISION-PHASE0-01` approved UCI only as a transaction-event substrate; `DECISION-PHASE1-01` approved the exact restricted dependency, persistence, event-contract, and CLI plan. Both are durably recorded in [`PROJECT_SPEC.md`](PROJECT_SPEC.md) and [`HUMAN_CHECKPOINT.md`](HUMAN_CHECKPOINT.md). `DECISION-PHASE0-02` and `DECISION-PHASE0-03` remain `PENDING` with the owner.
- **CONFIRMED — Milestone state:** [`ISSUE-20260812T072420Z-uci-transaction-data-foundation`](ISSUES/ISSUE-20260812T072420Z-uci-transaction-data-foundation.md) is `CLOSED` at `2026-08-12T10:20:12Z`. Its [ADR](ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md) is `ACCEPTED`; the required post-implementation independent review returned `APPROVED` at `2026-08-12T10:19:24Z` with no remaining material finding and no unjustified drift.
- **CONFIRMED — Verification state:** Six reusable evidence records exist. [Phase 1 verification](EVIDENCE/EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md) records the clean official build, 133-test suite, explicit full-data gate, byte-identical isolated rebuild, package/CLI gates, and repository/privacy scans at `c937c3f`, with append-only corrections from two independent review rounds. A fresh takeover participant independently reran the critical gates at `2026-08-13T01:04:45Z`: raw ZIP and Parquet digests match the record, `133 passed, 1 deselected`, full-data gate `1 passed, 133 deselected`, and `uci verify` returned `verified` with the recorded aggregate profile.
- **CONFIRMED — Review state:** Phase 1 proposal review rounds 1–3 approved the ADR before implementation. Implementation review round 1 (`CHANGES_REQUIRED`) and round 2 (`CHANGES_REQUIRED`) findings were corrected and append-preserved; round 3 approved the final revision and classified architecture drift. For Restricted Phase 2, independent proposal review rounds 1–2 required and verified wording corrections; round 3 returned `APPROVED` at `2026-08-13T01:42:50Z` after independently reproducing the corrected cutoff-grid arithmetic. Both pending source blockers and the Phase 2 decision stay with the human owner.
- **CONFIRMED — Phase 2 proposal state:** [`ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec`](ISSUES/ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec.md) carries the exact proposed Restricted Phase 2 specification wording (UCI-only stock-code universe, five versioned factors, 30-day forward target, weekly point-in-time backtest over 96 verified cutoffs, baselines, IC/quantile evaluation, JSON experiments, reports) and is `BLOCKED` solely on owner decision `DECISION-PHASE2-01`. The [proposed ADR](ADR/ADR-20260813T011628Z-phase2-transaction-research-architecture.md) remains `PROPOSED`; [`PROJECT_SPEC.md`](PROJECT_SPEC.md) is deliberately unmodified; [feasibility evidence](EVIDENCE/EVIDENCE-20260813T011628Z-phase2-research-feasibility-profile.md) is aggregate-only and was independently reproduced. No Phase 2 implementation is authorised.

Do not refresh only the timestamp. When a staleness trigger fires, mark affected claims `UNKNOWN`, reconcile them from higher-precedence artifacts and actual repository state, and record the reconciliation as new activity.

### Constraints

- Preserve point-in-time correctness and distinguish transaction-event history, pseudo-historical demand, and forward-only marketplace snapshots.
- Prefer official/documented structured access. Do not introduce Trends browser automation, `pytrends`, undocumented collectors, or fragile scraping under the current evidence.
- Do not push, publish data, create accounts, buy services, accept restrictive terms, use unauthorised credentials, or exceed the accepted Restricted Phase 1 scope.
- Do not implement factors, universes, targets, rankings, backtests, marketplace/demand adapters, a persistent database, generic source framework, or background service without a separately accepted specification and owner authority.
- Any dependency, Python-version, contract, or persistence change requires deliberate re-locking, revalidation, and independent review under the accepted ADR.
- Local `data/` artifacts are Git-ignored and owner-only; never commit, publish, or externally link raw/normalized data or customer references.

### Unverified complexity

The implemented foundation introduces locked Python packaging, five packages across runtime/development/build, immutable local raw/normalized state, manifests/receipts, a CLI, and `transaction_event.v1`. All are covered by the locked test suites, full-data gate, deterministic rebuild, and independent review recorded in the Phase 1 evidence. Residual unverified items: Linux/Windows native no-replace publication, real power-loss behavior, cross-platform Parquet byte identity, provider revision history, and dataset timezone. Concurrent writers are unsupported but fail closed. Provider credentials, recurring snapshots, external costs, and marketplace/demand integrations remain unadopted.

### Background tasks

No non-terminal background task exists. All recovery research/probe agents completed, and their durable results are in the four evidence records. Pre-outage work that had no durable process/reference was recorded as `ORPHANED` in the closed Phase 0 issue rather than represented as active.

## Active Issues

| Issue | Status | Severity | Owner | Authority | Review | Summary | Evidence or unblock condition |
|---|---|---|---|---|---|---|---|
| [`ISSUE-20260812T061002Z-marketplace-source-authorization`](ISSUES/ISSUE-20260812T061002Z-marketplace-source-authorization.md) | `BLOCKED` | `HIGH` | `human:technical-owner` | `HUMAN` | `INDEPENDENT` | Clear a marketplace source for archival quantitative research. | Written provider permission/reviewed contract, owner-authorised production access, authenticated field/quota sample, and raw-retention/use confirmation. |
| [`ISSUE-20260812T061003Z-demand-source-validation`](ISSUES/ISSUE-20260812T061003Z-demand-source-validation.md) | `BLOCKED` | `HIGH` | `human:technical-owner` | `HUMAN` | `INDEPENDENT` | Validate demand access, retention, timestamps, sampling, and revisions. | Owner-authorised no-purchase access, complete safe raw response, repeatability/revision study, retention clarification, and independent point-in-time review. |
| [`ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec`](ISSUES/ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec.md) | `BLOCKED` | `HIGH` | `agent:claude-code-phase2-proposal` | `HUMAN` | `INDEPENDENT` | Specify Restricted Phase 2: point-in-time transaction-event demand research on the UCI substrate. Proposal complete; independent review `APPROVED`. | Owner decision `DECISION-PHASE2-01` recorded with decision, responder, UTC time, and durable reference; then persist accepted wording in `PROJECT_SPEC.md` and move the ADR to `ACCEPTED`. |

## Next Action

Await the human technical owner's response to `DECISION-PHASE2-01`, presented with full links in [`HUMAN_CHECKPOINT.md`](HUMAN_CHECKPOINT.md); on approval, persist the accepted wording in `PROJECT_SPEC.md`, accept the ADR, and only then begin Phase 2 implementation under fresh independent review. No push is permitted.

## Recent Activity

### 2026-08-13T01:42:50Z — agent:claude-code-phase2-proposal — Restricted Phase 2 specification proposal

- **Task:** Determine the highest-value next milestone from durable state, build a decision-complete proposal within existing authority, and route the boundary-crossing decision to the owner without implementing anything.
- **Context inspected:** Protocol, full specification, accepted Phase 1 ADR and closed issue, all six prior evidence records, registry/recommendation, both open source blockers, checkpoint, HANDOFF, Git history/state, and the pinned normalized substrate (aggregate-only).
- **Actions performed:** Confirmed the marketplace/demand blockers do not gate UCI transaction-event research; gathered aggregate-only feasibility evidence (independently reproduced twice); drafted exact proposed Restricted Phase 2 specification wording in a new issue; drafted the proposed research-architecture ADR; obtained three independent proposal-review rounds and resolved every finding (composite missing-data rule, percentile/tie/direction/weight conventions, pinned half-open windows and event-week cutoff grid with verified 96 eligible cutoffs, price guards, verbatim-plus-one capability declarations, decision-queue/HANDOFF reconciliation); recorded `DECISION-PHASE2-01` in the checkpoint; committed the proposal records locally.
- **Files modified:** New Phase 2 issue, proposed ADR, and feasibility evidence; `HUMAN_CHECKPOINT.md` and `HANDOFF.md` reconciled. `PROJECT_SPEC.md` deliberately untouched pending owner authority.
- **Findings:** **CONFIRMED** — the substrate supports the proposed weekly design (104 event-week Mondays, 96 eligible 30/30 cutoffs, mean ~1,570 eligible products/cutoff; negative-quantity volume ~9.1% of positive; 4,710 of 5,305 products have multiple prices). **CONFIRMED** — Phase 2 implementation requires owner authority under the accepted Phase 1 specification. **UNKNOWN** — all factor predictive value; that is the research question the proposal exists to answer.
- **Verification performed:** Aggregate-only DuckDB feasibility profile (exit 0); independent reviewer reproduction of every headline number and the final grid arithmetic; relative-link scan (no broken links); `git diff --check`; proposal-scope diff inspection. Implementation tests are `NOT RUN` — correctly, since no implementation is authorised.
- **Issues created or updated:** Created [`ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec`](ISSUES/ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec.md) (`BLOCKED` on `DECISION-PHASE2-01`).
- **Remaining uncertainty:** Owner decision pending; timezone/provider-revision caveats inherited from Phase 1; wholesale-to-consumer generalization is unsupported and explicitly forbidden by the proposal's interpretation boundary.
- **Recommended next action:** See Next Action — await `DECISION-PHASE2-01`; do not implement Phase 2 or touch marketplace/demand sources without the recorded owner authority.

### 2026-08-13T01:04:45Z — agent:claude-code-reconciliation — Takeover reconstruction and milestone-closure bookkeeping

- **Task:** Reconstruct actual repository state after an interrupted session, independently revalidate material completion claims, and finish the interrupted Phase 1 closure bookkeeping without redoing valid work.
- **Context inspected:** Git HEAD/history/reflog, working tree, `BOOTSTRAP.md`, `PROJECT_SPEC.md`, accepted ADR, all six evidence records, source registry/recommendation, both open blocker issues, the Phase 1 issue, tracked implementation/contracts/tests, ignored local data artifacts, and the stale HANDOFF/checkpoint.
- **Actions performed:** Confirmed the reflog matches the evidence-recorded amended revisions (`e049af3` → `c599a5e` → `0ca3d86` → `c937c3f`); verified the working tree equals the independently approved revision plus only implementor-owned closure records; reran the critical gates; reconciled HANDOFF and the human checkpoint; committed the closure records locally without pushing.
- **Files modified:** `HANDOFF.md` and `HUMAN_CHECKPOINT.md` reconciled to post-closure truth; the pre-existing uncommitted ADR/issue/registry/evidence closure records were preserved and committed, not rewritten.
- **Findings:** **CONFIRMED** — implementation at `c937c3f` is complete and matches the approved record: raw ZIP `572e36…bfb`, Parquet `49bec2…89f` digests match evidence; `133 passed, 1 deselected`; full-data gate `1 passed, 133 deselected`; `uci verify` returned `verified` with the recorded 1,044,848-event profile. **CONFIRMED** — independent review round 3 `APPROVED` and the issue closure checklist were durably recorded before the interruption; only HANDOFF/checkpoint reconciliation and the local commit were missing. **UNKNOWN** — Linux/Windows publication paths, real power loss, cross-platform byte identity, provider revision history, and dataset timezone remain exactly as bounded in the closed issue.
- **Verification performed:** Digest comparison against the evidence record; locked default and full-data pytest gates; `productquant uci verify`; tracked-file inventory; Git state/history/reflog inspection. All exit statuses `0`.
- **Issues created or updated:** None; [`ISSUE-20260812T072420Z-uci-transaction-data-foundation`](ISSUES/ISSUE-20260812T072420Z-uci-transaction-data-foundation.md) remains `CLOSED` on its recorded approval.
- **Remaining uncertainty:** The two owner-owned source blockers and every deferred Phase 2 semantic are unchanged; local ignored raw data are not Git-protected.
- **Recommended next action:** See Next Action; do not begin Phase 2 or source work without the recorded owner authority.

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
- Restricted Phase 1 implementation, three independent proposal-review rounds, three independent implementation/architecture-review rounds, all corrections, and closure are retained in [`ISSUE-20260812T072420Z-uci-transaction-data-foundation`](ISSUES/ISSUE-20260812T072420Z-uci-transaction-data-foundation.md), the accepted [ADR](ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md), and the append-only [verification evidence](EVIDENCE/EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md).
