# Build the Restricted UCI Transaction-Event Data Foundation

## Metadata

- **ID:** `ISSUE-20260812T072420Z-uci-transaction-data-foundation`
- **Title:** `Build the restricted UCI transaction-event data foundation`
- **Status:** `IMPLEMENTING`
- **Severity:** `HIGH`
- **Owner:** `agent:codex-phase1`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-12T07:24:20Z`
- **Updated UTC:** `2026-08-12T07:47:28Z`
- **Requirements:** [`PROJECT_SPEC.md` sections 15–19, 21, 37, 40–44, 50–53 and Restricted Phase 1](../PROJECT_SPEC.md)
- **ADRs:** [`ADR-20260812T072420Z-uci-transaction-data-foundation`](../ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md) (`ACCEPTED`)
- **Evidence:** [`EVIDENCE-20260812T060103Z-historical-dataset-probes`](../EVIDENCE/EVIDENCE-20260812T060103Z-historical-dataset-probes.md); [`EVIDENCE-20260812T073451Z-uci-schema-contract-probe`](../EVIDENCE/EVIDENCE-20260812T073451Z-uci-schema-contract-probe.md)

## Problem

ProductQuant has no implementation, raw persistence, normalized event schema, executable point-in-time contract, or reproducible local dataset. Phase 0 found no authorised integrated marketplace-and-demand history, but the owner approved a restricted Phase 1 using UCI Online Retail II solely as historical transaction events. The foundation must preserve this boundary while establishing enough durable infrastructure for later separately authorised research.

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
| Dependencies and Python packaging | Required for streaming XLSX, typed Parquet, local SQL verification, and executable tests/CLI. | Lockfile, build, unit/integration/full-data tests, independent review. | This issue until closed. |
| Immutable raw/normalized local state and manifests | Required for raw preservation, reproducibility, and provenance. | Hash, drift, atomicity, idempotence, corruption, and rerun tests. | This issue until closed. |
| Core transaction-event schema and CLI | Required Phase 1 contracts. | Machine-readable schema, contract tests, README, and independent architecture review. | This issue until closed. |
| Local pseudonymous customer reference | Lossless source fidelity without repository publication. | No-row logging/evidence and tracked-data/secret/large-file scans. | Any later publication/use requires a new authority review. |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-12T07:24:20Z` | `agent:codex-phase1` | Implementation verification | `NOT RUN — authority records and proposal review precede implementation.` | Pending Phase 1 evidence. | No implementation exists yet. |

## Self-review

- **Participant:** `agent:codex-phase1`
- **Reviewed UTC:** `PENDING`
- **Reviewed repository state:** `PENDING`
- **Scope and authority references:** `PENDING`
- **Checks and evidence reviewed:** `PENDING`
- **Findings and corrections:** `PENDING`
- **Limitations:** `PENDING`
- **Residual risks:** `PENDING`
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
