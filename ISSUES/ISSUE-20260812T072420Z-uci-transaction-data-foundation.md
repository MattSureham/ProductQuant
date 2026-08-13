# Build the Restricted UCI Transaction-Event Data Foundation

## Metadata

- **ID:** `ISSUE-20260812T072420Z-uci-transaction-data-foundation`
- **Title:** `Build the restricted UCI transaction-event data foundation`
- **Status:** `CLOSED`
- **Severity:** `HIGH`
- **Owner:** `agent:codex-phase1`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-12T07:24:20Z`
- **Updated UTC:** `2026-08-12T10:20:12Z`
- **Requirements:** [`PROJECT_SPEC.md` sections 15–19, 21, 37, 40–44, 50–53 and Restricted Phase 1](../PROJECT_SPEC.md)
- **ADRs:** [`ADR-20260812T072420Z-uci-transaction-data-foundation`](../ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md) (`ACCEPTED`)
- **Evidence:** [`EVIDENCE-20260812T060103Z-historical-dataset-probes`](../EVIDENCE/EVIDENCE-20260812T060103Z-historical-dataset-probes.md); [`EVIDENCE-20260812T073451Z-uci-schema-contract-probe`](../EVIDENCE/EVIDENCE-20260812T073451Z-uci-schema-contract-probe.md); [`EVIDENCE-20260812T091334Z-phase1-data-foundation-verification`](../EVIDENCE/EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md)

## Problem

At issue creation, ProductQuant had no implementation, raw persistence, normalized event schema, executable point-in-time contract, or reproducible local dataset. Phase 0 found no authorised integrated marketplace-and-demand history, but the owner approved a restricted Phase 1 using UCI Online Retail II solely as historical transaction events. The completed foundation preserves this boundary while establishing durable infrastructure for later separately authorised research.

## Evidence or reproduction

The Phase 0 historical-dataset probe verified the official ZIP and workbook, exact fields, two overlapping sheets, a safe sheet-boundary stitch, 1,044,848 retained physical rows, dataset-local naïve timestamps, and material anomalies. The owner then explicitly approved `DECISION-PHASE0-01` with scope constraints and the decision-complete Restricted Phase 1 implementation plan as `DECISION-PHASE1-01`.

## Expected behavior

The implementation MUST satisfy the accepted Restricted Phase 1 section of [`PROJECT_SPEC.md`](../PROJECT_SPEC.md) and, after acceptance, the linked ADR. It MUST create only a local reproducible UCI transaction-event foundation, preserve raw/provenance and point-in-time semantics, fail closed on source drift, and keep every marketplace/opportunity/demand capability explicitly unsupported.

## Assumptions

- **CONFIRMED:** The owner approved the UCI-only restricted scope, architecture, dependencies, schema, persistence, and CLI recorded in the specification and ADR.
- **CONFIRMED:** UCI is anonymous, no-cost, CC BY 4.0, and the approved work requires no credential or external account.
- **INFERRED:** One source-specific adapter and immutable Parquet dataset are sufficient for this milestone.
- **UNKNOWN:** Cross-platform byte-level Parquet determinism and provider revision/as-of history are not established; logical reproducibility and same-lock/environment determinism will be tested without overstating them.

## Investigation and decision

Implement the accepted plan without a generic collector framework or persistent database. Before code, obtain an independent review of the proposed ADR and specification for scope, authority, and unnecessary complexity; then accept and commit the authority records. After implementation, run synthetic, failure, integration, official full-data, reproducibility, packaging, scope, and repository-integrity checks. A fresh non-implementing participant must independently inspect and rerun the critical gates before closure.

## Change

- **Files or components:** Specification/checkpoint/ADR/issue/handoff records; Python package and lockfile; machine-readable source/schema contracts; tests; README; Phase 1 evidence and registry status.
- **Behavior changed:** From documentation-only to a local CLI that can fetch, normalize, and verify the pinned UCI transaction-event dataset with immutable provenance.
- **Out-of-scope work deliberately excluded:** Phase 2+ work, factors, ranking, universe/targets, backtesting, reports, marketplace/demand integrations, generic plugins, persistent DB, services, credentials, costs, data publication, remote push, and resolution of existing source blockers.
- **Rollback or recovery:** Revert the local implementation and documentation commits; ignored content-addressed data remains independent and can be removed later only with explicit scope/target validation.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| Dependencies and Python packaging | Required for streaming XLSX, typed Parquet, local SQL verification, and executable tests/CLI. | Exact lock, build, unit/integration/full-data tests, and independent review passed. | Any dependency or Python-version change requires deliberate re-locking and revalidation. |
| Immutable raw/normalized local state and manifests | Required for raw preservation, reproducibility, and provenance. | Hash, drift, atomicity, idempotence, corruption, fault/race, and deterministic-rerun tests passed. | Linux/Windows native publication and real power loss remain unexercised limitations, not hidden completion claims. |
| Core transaction-event schema and CLI | Required Phase 1 contracts. | Machine-readable schema, contract tests, README, full-data acceptance, and independent architecture review passed. | Any new consumer or contract version requires separate authority and review. |
| Local pseudonymous customer reference | Lossless source fidelity without repository publication. | No-row logging/evidence and tracked-data/secret/large-file scans. | Any later publication/use requires a new authority review. |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-12T07:24:20Z` | `agent:codex-phase1` | Implementation verification | `NOT RUN — authority records and proposal review precede implementation.` | Phase 1 evidence was not yet available at that timestamp. | No implementation existed yet. |
| `2026-08-12T09:13:34Z` | `agent:codex-phase1` | Locked synthetic/integration tests, explicit official full-data acceptance, clean-revision online/offline CLI, isolated deterministic rebuild, build/compile/help, repository/privacy/state scans | `PASS — 100 synthetic/integration tests; 1 explicit full-data test; exact raw/member and normalized digests/profile; byte-identical isolated rebuild; all final commands exit 0.` | [`EVIDENCE-20260812T091334Z-phase1-data-foundation-verification`](../EVIDENCE/EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md) | Cross-platform byte identity, source timezone/revision history, and marketplace/demand capabilities remain explicitly unverified/unsupported. |
| `2026-08-12T09:54:59Z` | `agent:codex-phase1` | Correct every implementation-review finding; rebuild normalized state from clean `0ca3d86`; run locked compile/default/full-data/build/help/offline/verify gates; isolated deterministic rebuild; exact repository/privacy/link/local-state scans | `PASS — 132 synthetic/integration tests; 1 explicit full-data test; exact raw/member/profile; byte-identical corrected rebuild; all final commands exit 0; clean implementation tree.` | Corrected/appended section in [`EVIDENCE-20260812T091334Z-phase1-data-foundation-verification`](../EVIDENCE/EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md) | Linux/Windows no-replace path, real power loss, cross-platform rebuild, source revision/timezone, and marketplace/demand remain unverified or unsupported. |
| `2026-08-12T10:12:21Z` | `agent:codex-phase1` | Correct the remaining Round 2 in-worktree privacy defect at clean `c937c3f`; rebuild normalized state; run locked compile/default/full-data/build/help/offline/verify gates; compare a second isolated rebuild; inspect aggregate-only local state | `PASS — 133 synthetic/integration tests; 1 explicit full-data test; final-files-only ignore regression; exact artifacts/profile; byte-identical Parquet and equal schema/order/manifest invariants; all final commands exit 0.` | Final appended section in [`EVIDENCE-20260812T091334Z-phase1-data-foundation-verification`](../EVIDENCE/EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md) | Independent approval still required; Linux/Windows no-replace path, real power loss, cross-platform rebuild, source revision/timezone, and marketplace/demand remain unverified or unsupported. |

## Self-review

- **Participant:** `NOT_APPLICABLE — this issue requires a fresh independent reviewer.`
- **Reviewed UTC:** `2026-08-12T10:12:21Z` (implementor verification cutoff only)
- **Reviewed repository state:** Clean implementation revision `c937c3f8eca6b9d54ad77c47313647710abbe7d8`, followed by implementor-owned evidence/issue updates.
- **Scope and authority references:** Accepted Restricted Phase 1 specification, `DECISION-PHASE0-01`, `DECISION-PHASE1-01`, and accepted ADR.
- **Checks and evidence reviewed:** Expanded locked synthetic/integration suite, literal official full-data gate, root-level Git-ignore regression, clean normalized rebuild, isolated determinism comparison, package/CLI checks, and exact repository/privacy/local-state scripts linked above.
- **Findings and corrections:** Implementor corrected the Round 2 residual privacy defect after the reviewer accepted ten earlier resolutions. No self-approval is claimed, and a later independent round must verify the final correction and every prior resolution directly.
- **Limitations:** No cross-platform host, real power-loss test, new network acquisition, source timezone/revision history, or marketplace/external-demand evidence.
- **Residual risks:** Native no-replace paths outside macOS remain unexercised; local ignored raw data are not Git-protected; concurrent writers only fail safely; Phase 2 and cancellation/netting semantics remain unauthorised.
- **Outcome:** `NOT_APPLICABLE — independent review is required.`

## Independent review rounds

- **Required:** `YES — dependencies, persistent state, public CLI, privacy handling, and a cross-module data contract are introduced.`

### 2026-08-12T07:31:28Z — agent:codex-phase1-architecture-review

- **Reviewed repository state:** Base `9efee6d17735b1bb1c9d11a2bd720a64bc617499` plus the initial specification/checkpoint/handoff/ADR/issue changes; no implementation.
- **Scope:** Requirements, Phase 0 evidence, proposed architecture/contracts, authority, privacy, complexity, links, and repository state.
- **Commands or procedures:** Git state/diff/whitespace, relative links, placeholders, and direct requirement/evidence comparison.
- **Specification compliance:** UCI-only scope, stitch, naïve time, PIT boundary, duplicate preservation, and negative capability claims aligned.
- **Correctness and regression findings:** Initial reviewer context omitted the newest exact-plan approval and therefore treated `DECISION-PHASE1-01` as missing. Exact ID/manifest/receipt/CLI contracts, customer-reference controls, and source type/precision evidence still required work.
- **Architecture and complexity findings:** Dependency/state choices were compatible with the approved plan but needed explicit build dependency, receipt retention, failure/atomicity, concurrency, and privacy consequences.
- **Material findings and resolution conditions:** Inspect newest owner approval; complete the contracts and privacy evaluation; add a full-workbook schema/precision probe; repeat review before ADR acceptance.
- **Limitations:** No code/tests; review's authority conclusion lacked the newest user message.
- **Residual risks:** Source timezone/revision state, cancellation/netting semantics, and marketplace/demand sources remain open by design.
- **Evidence:** ADR review round and linked Phase 0 evidence.
- **Disposition:** `BLOCKED`
- **Prior-round resolution:** `FIRST ROUND`

### 2026-08-12T07:39:00Z — agent:codex-phase1-architecture-review

- **Reviewed repository state:** Base `9efee6d17735b1bb1c9d11a2bd720a64bc617499` plus revised authority records and schema evidence; no implementation.
- **Scope:** Newest exact human plan approval, protocol/specification, Phase 0 evidence, revised architecture/contracts/privacy controls, and complete workbook probe.
- **Commands or procedures:** Git state/diff/whitespace, complete changed-file/link inspection, and independent full-workbook `openpyxl` scan.
- **Specification compliance:** Passed; explicit owner authority and all restricted UCI/negative-capability boundaries were confirmed.
- **Correctness and regression findings:** Workbook scan independently reproduced the new evidence. The evidence command itself needed durable inclusion, and pre-command usage JSON semantics needed definition.
- **Architecture and complexity findings:** Contract, privacy, dependencies, receipts, atomicity, and state ownership were decision-complete; checkpoint/handoff required reconciliation.
- **Material findings and resolution conditions:** Embed exact evidence command, define `command=null` for pre-command parser errors, and reconcile current records before re-review.
- **Limitations:** No implementation, dependencies, Parquet, CLI, or tests yet.
- **Residual risks:** Source timezone/revisions, cancellation/netting semantics, and marketplace/demand sources remain deferred.
- **Evidence:** Phase 0 and schema probes, revised ADR/specification, current diff.
- **Disposition:** `CHANGES_REQUIRED`
- **Prior-round resolution:** Round 1 authority and contract/privacy/schema findings were resolved; three record-level corrections remained.

### 2026-08-12T07:46:48Z — agent:codex-phase1-architecture-review

- **Reviewed repository state:** Base `9efee6d17735b1bb1c9d11a2bd720a64bc617499` plus all corrected proposal records; no implementation.
- **Scope:** Exact owner approvals, specification/ADR/contracts/privacy, evidence, prior review findings, repository integrity, and scope boundaries.
- **Commands or procedures:** Git state/diff/whitespace; complete file, link, placeholder, ID/reference, tracked-data, and size scans; comparison with independently reproduced workbook evidence.
- **Specification compliance:** Passed; restricted UCI scope and all negative capability boundaries are preserved.
- **Correctness and regression findings:** Passed for proposal stage; evidence is complete/reproducible and no runtime exists yet.
- **Architecture and complexity findings:** Passed; introduced complexity is exact, authorised, justified, and assigned verification coverage.
- **Material findings and resolution conditions:** `NONE` at proposal stage; implementation may begin under the accepted ADR.
- **Limitations:** Implementation and all runtime behavior remain unverified and require a later fresh independent review.
- **Residual risks:** Timezone/revisions, cancellation/netting, future customer-reference use, and marketplace/demand sources remain deferred.
- **Evidence:** ADR round 3 and linked source/schema evidence.
- **Disposition:** `APPROVED`
- **Prior-round resolution:** All round 1 and round 2 findings are resolved.

### 2026-08-12T09:31:09Z — agent:codex-phase1-final-independent-review

- **Reviewed repository state:** `c599a5e245b923764df672aecf6973abdc29e638` (tree `fb04307fa6ab3468fb817be7c4ac6c377257b0c2`) on `main`, plus the implementor-owned modified issue and untracked draft verification evidence; ignored canonical artifacts were inspected aggregate-only.
- **Scope:** Normative protocol, accepted specification and ADR, four machine-readable contracts, Phase 0 evidence, issue, README, package/lock, tests, implementation, draft evidence, ignored artifact manifests, and architecture drift.
- **Commands or procedures:** Complete record/code/test inspection; Git state/tree/diff scans; locked dependency, compilation, 100-test synthetic/integration, explicit full-data, offline prepare/verify, package/build/help, wheel-content, link/privacy/repository/artifact/process checks; aggregate-only DuckDB provenance checks; and safe temporary-root adversarial probes for publication races/failures, permission mutation, manifest self-verification, formula cells, and quantity overflow.
- **Specification compliance:** Toolchain, source-specific architecture, content addressing, Parquet truth, ephemeral DuckDB, event schema/IDs/order, sheet-boundary stitch, signed/null/duplicate preservation, point-in-time boundary, CLI scope, negative capabilities, and Phase 2 exclusions are aligned. Bounded exact HTTP Range recovery is a justified compatible deviation supported by the preserved proxy truncation evidence.
- **Correctness and regression findings:** `HIGH` — bundle/receipt publication can overwrite a competing target, leave a final-path symlink, and accepts symlink artifacts; existing arbitrary data-root permissions are mutated; fetch can publish a generated manifest that immediately fails verification. `MEDIUM` — formula/error cells can be silently transformed, quantity lacks signed-int64 bounds, initial download is unbounded, custom in-repository roots need not be ignored, failed prepare receipts lose completed artifact references, and mandated literal/failure coverage is incomplete. `LOW` — the static Parquet-writer-setting contract is ambiguous.
- **Architecture and complexity findings:** Publication/immutability, privacy boundary, and staged-manifest behavior are unjustified drift and require correction. Range recovery remains justified. Cross-platform rebuild and crash/concurrency behavior remain unknown.
- **Material findings and resolution conditions:** Implement no-clobber publication with no final symlink and adversarial fault/race coverage; preserve existing path modes; validate staged state before publication; reject unsupported workbook cells and int64 overflow; bound downloads; require ignored in-worktree roots; retain partial prepare provenance; add the specified literal/write/size/full-data tests; reconcile the manifest contract; and append an accurate `e049af3` raw-acquisition/c599 verification evidence correction plus exact comparison/repository scripts.
- **Limitations:** No cross-platform host or real power-loss test; no fresh network acquisition; no official row/customer value was emitted; source revision/timezone and future providers remain out of scope.
- **Residual risks:** Ignored raw data are not Git-protected; provider availability/revision/timezone are unknown; local customer reference remains sensitive/pseudonymous; concurrency remains unsupported and must fail safely; cancellation/netting and Phase 2 remain unauthorised; source blockers remain open.
- **Evidence:** Reviewer command outputs and adversarial temporary-path reproductions; linked canonical manifests/digests and draft Phase 1 evidence; no repository files changed by the reviewer.
- **Disposition:** `CHANGES_REQUIRED`
- **Prior-round resolution:** All proposal-stage findings remain resolved; this first post-implementation round identified new runtime and evidence defects. The issue returns to `IMPLEMENTING` pending corrections and a later independent review round.

### 2026-08-12T10:06:07Z — agent:codex-phase1-final-independent-review

- **Reviewed repository state:** `0ca3d86f4935e2538d950c6da46b7bb7c5e5d8f7` (tree `0f1191ddec5e408c86bf35fdd925505ca7c6ffbe`) on `main`, plus implementor-owned Phase 1 issue/evidence changes; canonical ignored artifacts were inspected aggregate-only.
- **Scope:** Complete protocol/specification/ADR/contracts/code/tests/evidence review, every prior finding, architecture drift, canonical manifests/artifacts, package, and repository/privacy state.
- **Commands or procedures:** Locked sync/lock/compile; 132 default tests; explicit full-data test; offline prepare/verify; build and six CLI help commands; wheel and digest checks; exact link/contract/tracked-data/large-file/secret/artifact-mode/receipt/symlink/partial/DuckDB/process scans; isolated rebuild; and direct safe temporary adversarial probes.
- **Specification compliance:** Toolchain, UCI-only scope, raw/Parquet/DuckDB ownership, event contract/stitch/PIT semantics, CLI/receipts, negative capabilities, and Phase 2 exclusions remain aligned. Bounded fixed-source Range recovery remains a justified deviation.
- **Correctness and regression findings:** Ten of eleven round-1 findings are resolved. `MEDIUM` — the in-worktree privacy guard checks only five final filenames, not all descendants/staging paths as the packaged contract claims. Granular final-only ignore patterns passed policy while raw, normalized, and receipt staging paths remained trackable.
- **Architecture and complexity findings:** The narrower ignore enforcement is `UNJUSTIFIED_DRIFT` from the accepted all-local-data Git-ignore privacy boundary. All other corrected architecture is aligned; native no-replace paths outside macOS remain `UNKNOWN`.
- **Material findings and resolution conditions:** Require the in-worktree data root itself, or all three complete raw/normalized/receipt subtrees, to be Git-ignored before any write; reject granular final-only patterns before network, write, or mode mutation; add regression; rerun gates; obtain another independent round.
- **Limitations:** macOS/APFS only; no fresh network, real power cut, Linux/Windows host, or cross-platform rebuild; independent isolated rebuild was dirty only because implementor review documents remained present; no official transaction/customer row was emitted.
- **Residual risks:** The staging-ignore defect remains; other residuals are unexercised OS publication paths, non-Git-protected ignored data, provider availability/revision/timezone, sensitive local customer references, safe-failure-only concurrency, unauthorised cancellation/netting/Phase 2, and open source blockers.
- **Evidence:** Corrected implementation/contracts/tests/evidence at `0ca3d86`; canonical digests; direct granular-ignore reproduction and gate outputs summarized above.
- **Disposition:** `CHANGES_REQUIRED`
- **Prior-round resolution:** Runtime round 1 findings 1–6 and 8–11 are resolved; finding 7 remains only partially resolved. Proposal approvals remain valid.

### 2026-08-12T10:19:24Z — agent:codex-phase1-final-independent-review

- **Reviewed repository state:** `c937c3f8eca6b9d54ad77c47313647710abbe7d8` (tree `7b7e50e376c1377ea43d267741f9ef81ba7cd4bd`) on `main`, plus implementor-owned modified Phase 1 issue and untracked verification evidence. Ignored canonical artifacts were inspected aggregate/provenance-only; no transaction or customer row was emitted.
- **Scope:** Normative protocol; accepted Restricted Phase 1 specification and ADR; all four executable contracts; implementation, CLI, tests, README, lock/package state, current issue/evidence; every proposal/runtime review finding; architecture drift; canonical raw/normalized artifacts; privacy and repository state.
- **Commands or procedures:** Inspected the complete `0ca3d86..c937c3f` correction and cumulative `c599a5e..c937c3f` remediation; ran frozen sync/lock/compilation, 133-test default suite, explicit full-data test, offline prepare/verify, package build, and all six CLI help commands; checked package contents/hashes, whitespace, Git state/history, four JSON contracts, relative Markdown links, placeholders, tracked data, large files, secret patterns, artifact hashes/modes/contents, receipts, symlinks, partials, persistent DuckDB files, and live processes. A private temporary Git repository independently reproduced both the rejected final-files-only policy and accepted whole-root policy, then was moved to Trash.
- **Specification compliance:** `ALIGNED` — exact Python/uv dependencies, source-specific UCI-only adapter, immutable content-addressed raw ZIP, Parquet truth, ephemeral DuckDB, `transaction_event.v1`, physical-row provenance, boundary stitch, signed/null/duplicate preservation, as-of semantics, CLI/receipts, root-level ignored local state, capability denials, and Phase 2 prohibitions match higher authority.
- **Correctness and regression findings:** `PASS` — `133 passed, 1 deselected`; explicit official gate `1 passed, 133 deselected`; offline prepare/verify returned verified/verified; build/help gates passed. The Round 2 privacy defect is resolved: final-files-only rules fail before network, child creation, writes, or mode mutation; a data-root rule covers representative raw, normalized, receipt, and staging descendants. Every earlier correction remains covered. Canonical raw/normalized and package hashes match the final evidence; repository/privacy/link/contract scans found no prohibited state.
- **Architecture and complexity findings:** `ALIGNED` for approved persistence, schema, dependencies, CLI, privacy, and scope. Bounded exact-source HTTP Range recovery is a documented `JUSTIFIED_DEVIATION`, compatible with the fixed-source contract and preserved proxy-truncation evidence. Linux/Windows native no-replace execution, real power-loss behavior, cross-platform Parquet byte identity, and provider revision/timezone remain `UNKNOWN`, explicitly bounded rather than drift. No `UNJUSTIFIED_DRIFT` remains.
- **Material findings and resolution conditions:** `NONE`. Round 1 findings 1–6 and 8–11 remain resolved; finding 7 is fully resolved by root-level ignore enforcement, aligned documentation/contracts, the committed regression, and independent adversarial reproduction.
- **Limitations:** macOS/APFS only; no new network acquisition, real power interruption, Linux/Windows host, or cross-platform build. This round did not repeat another full isolated normalization because the only delta was the pre-write ignore-policy guard; it reconciled the unchanged Parquet digest, clean canonical manifest, implementor's final isolated comparison, prior independent rebuild, and full-data gate. No official row-level value was inspected or emitted.
- **Residual risks:** Ignored local raw data remain outside Git protection; provider availability/revision history and timezone are unknown; local customer references remain sensitive pseudonymous data; concurrent writers are unsupported but fail safely; cancellation/netting and every Phase 2 semantic remain unauthorised; marketplace and demand blocker issues remain open.
- **Evidence:** Direct Round 3 command outputs and temporary-root privacy reproduction; current canonical manifests/digests; corrected/appended [`EVIDENCE-20260812T091334Z-phase1-data-foundation-verification`](../EVIDENCE/EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md); no repository files changed by the reviewer.
- **Disposition:** `APPROVED`
- **Prior-round resolution:** Proposal-stage approvals remain valid. Runtime round 1 findings 1–6 and 8–11 were accepted in round 2; finding 7, only partially resolved at `0ca3d86`, is fully resolved at `c937c3f`. No material finding remains, so the required independent-review gate is satisfied.

## Blocker

- **Blocked from:** `NOT BLOCKED`
- **Blocker:** `NONE`
- **Unblock owner:** `NONE`
- **Unblock condition:** `NONE`

## Residual uncertainty

- Provider revision/as-of semantics and dataset timezone remain unknown and must remain explicit in manifests and downstream work.
- Cancellation/return/adjustment inclusion or netting is a future dataset/factor policy, not a Phase 1 normalization decision.
- Marketplace and demand source access remains owned by the two existing blocked issues.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-12T07:24:20Z` | `agent:codex-phase1` | `NONE` | `OPEN` | Created after owner approval to persist the boundary-crossing Phase 1 work. |
| `2026-08-12T07:24:20Z` | `agent:codex-phase1` | `OPEN` | `INVESTIGATING` | Recorded exact specification/ADR proposal and requested independent architecture review before implementation. |
| `2026-08-12T07:31:28Z` | `agent:codex-phase1-architecture-review` | `INVESTIGATING` | `BLOCKED` | First review required exact contract/privacy/evidence changes and lacked the newest human plan approval. |
| `2026-08-12T07:34:51Z` | `agent:codex-phase1` | `BLOCKED` | `INVESTIGATING` | Supplied the omitted approval context, made contracts decision-complete, and added the required full-workbook schema/precision evidence for re-review. |
| `2026-08-12T07:39:00Z` | `agent:codex-phase1-architecture-review` | `INVESTIGATING` | `INVESTIGATING` | Round 2 confirmed authority and architecture but required three record-level corrections before acceptance. |
| `2026-08-12T07:41:52Z` | `agent:codex-phase1` | `INVESTIGATING` | `INVESTIGATING` | Embedded the exact probe command, defined pre-command error JSON, and reconciled checkpoint/handoff for final proposal re-review. |
| `2026-08-12T07:46:48Z` | `agent:codex-phase1-architecture-review` | `INVESTIGATING` | `INVESTIGATING` | Round 3 approved the corrected proposal with no material finding. |
| `2026-08-12T07:47:28Z` | `agent:codex-phase1` | `INVESTIGATING` | `IMPLEMENTING` | Marked the owner-authorised, independently approved ADR accepted; implementation is now permitted. |
| `2026-08-12T08:27:52Z` | `agent:codex-phase1` | `IMPLEMENTING` | `IMPLEMENTING` | During implementation review, reconciled the accidentally narrowed manifest wording against the exact higher-authority plan: raw and normalized manifests both carry all eight negative capability declarations. |
| `2026-08-12T09:13:34Z` | `agent:codex-phase1` | `IMPLEMENTING` | `VERIFYING` | Completed the clean-revision official build, full-data gate, isolated deterministic rebuild, package/CLI checks, failure coverage, and repository/privacy scans; durable evidence linked. |
| `2026-08-12T09:31:09Z` | `agent:codex-phase1-final-independent-review` | `VERIFYING` | `IMPLEMENTING` | Independent implementation and architecture-drift review reproduced publication overwrite/symlink, permission-mutation, invalid-manifest, workbook-type, quantity-bound, privacy-root, receipt-provenance, coverage, and evidence defects; disposition `CHANGES_REQUIRED`. |
| `2026-08-12T09:54:59Z` | `agent:codex-phase1` | `IMPLEMENTING` | `VERIFYING` | Corrected all round-1 findings in amended implementation revision `0ca3d86`, rebuilt normalized state from that clean revision, passed 132 default and one explicit full-data test plus deterministic/package/CLI/repository gates, and appended corrected evidence for independent re-review. |
| `2026-08-12T10:06:07Z` | `agent:codex-phase1-final-independent-review` | `VERIFYING` | `IMPLEMENTING` | Round 2 approved ten prior resolutions but reproduced one remaining privacy defect: granular final-only ignore patterns can leave staging descendants trackable. Disposition `CHANGES_REQUIRED`. |
| `2026-08-12T10:12:21Z` | `agent:codex-phase1` | `IMPLEMENTING` | `VERIFYING` | Revision `c937c3f` now requires the in-worktree data-root directory itself to be ignored and rejects final-files-only rules before network, writes, or mode mutation. Clean 133-test, full-data, package/CLI, official-artifact, and deterministic-rebuild gates passed; final independent re-review requested. |
| `2026-08-12T10:19:24Z` | `agent:codex-phase1-final-independent-review` | `VERIFYING` | `REVIEW` | Round 3 directly reproduced both privacy-policy branches, reran all critical gates, reconciled every earlier finding, found no unjustified drift, and returned `APPROVED`. |
| `2026-08-12T10:20:12Z` | `agent:codex-phase1` | `REVIEW` | `CLOSED` | Closed only after owner authority, clean full verification, durable evidence, and the required independent `APPROVED` implementation/architecture review were all present. Remaining source and Phase 2 questions stay explicitly blocked or unauthorised. |

## Closure checklist

- [x] Expected behavior is tied to a higher-authority source.
- [x] The change or resolution is recorded.
- [x] Required verification ran and evidence is linked; unavailable checks remain explicit.
- [x] If `Review: SELF`, the Self-review outcome is `COMPLETE` and no independent-review risk category applies. (`NOT_APPLICABLE`; review is independent.)
- [x] If `Review: INDEPENDENT`, the latest review round is `APPROVED` and shows that prior material findings are resolved.
- [x] Required human authority is recorded in the owning artifact: product/contract in `PROJECT_SPEC.md`, architecture in an accepted ADR, or both for a mixed decision.
- [x] New complexity is covered, removed, or linked to an explicitly accepted open debt issue.
- [x] Residual uncertainty is absent or explicitly owned.
- [x] HANDOFF reflects the resulting current state and exactly one next action.
