# Specify Restricted Phase 2 — UCI Transaction-Event Demand Research

## Metadata

- **ID:** `ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec`
- **Title:** `Specify Restricted Phase 2: point-in-time transaction-event demand research on the UCI substrate`
- **Status:** `BLOCKED`
- **Severity:** `HIGH`
- **Owner:** `agent:claude-code-phase2-proposal`
- **Authority:** `HUMAN`
- **Review:** `INDEPENDENT`
- **Created UTC:** `2026-08-13T01:16:28Z`
- **Updated UTC:** `2026-08-13T01:42:50Z`
- **Requirements:** [`PROJECT_SPEC.md` sections 4–6, 20–34, 37–39, 45–46, 49–50 and Restricted Phase 1](../PROJECT_SPEC.md)
- **ADRs:** [`ADR-20260812T072420Z-uci-transaction-data-foundation`](../ADR/ADR-20260812T072420Z-uci-transaction-data-foundation.md) (`ACCEPTED`); [`ADR-20260813T011628Z-phase2-transaction-research-architecture`](../ADR/ADR-20260813T011628Z-phase2-transaction-research-architecture.md) (`PROPOSED`)
- **Evidence:** [`EVIDENCE-20260813T011628Z-phase2-research-feasibility-profile`](../EVIDENCE/EVIDENCE-20260813T011628Z-phase2-research-feasibility-profile.md); [`EVIDENCE-20260812T091334Z-phase1-data-foundation-verification`](../EVIDENCE/EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md)

## Problem

Restricted Phase 1 is complete and closed: the UCI transaction-event substrate is preserved, normalized, and verified, but the repository still has no universe, factor, target, ranking, backtest, evaluation, or research-report capability. The core objective — a backtestable, explainable, iteratively improvable product ranking/signal system — cannot advance without them. The accepted Restricted Phase 1 specification explicitly states that any Phase 2 transaction-demand factor semantics, including cancellation/return/netting policy, require a separate accepted specification before implementation. `PROJECT_SPEC.md` is accepted product authority, so adding Phase 2 product requirements is a human technical-owner decision. The work that is already authorized is investigation, evidence gathering, and a decision-complete proposal; implementation is not authorized.

The open marketplace (`ISSUE-20260812T061002Z`) and demand (`ISSUE-20260812T061003Z`) blockers were examined for dependency: they gate marketplace/demand collectors and the integrated v0.1 demonstration of section 50, but they do **not** block transaction-event demand research on the already-accepted UCI substrate.

## Evidence or reproduction

[`EVIDENCE-20260813T011628Z-phase2-research-feasibility-profile`](../EVIDENCE/EVIDENCE-20260813T011628Z-phase2-research-feasibility-profile.md) establishes, aggregate-only: 104 weekly cutoffs (96 with complete 30-day history plus 30-day forward room; 78 with 90/90); a mean of ~1,570 eligible products per cutoff under a ≥5-trailing-event rule; 3,691 stock codes with ≥20 events and ≥90-day spans; negative-quantity volume equal to ~9.1% of positive volume including 3,393 negative rows without the cancellation flag; and within-product price variation in 4,710 of 5,305 products. The design below is sized by that profile; it manufactures no marketplace, competition, or external-demand data.

## Expected behavior

An owner-accepted Restricted Phase 2 specification (exact proposed wording below) and an accepted architecture ADR, after which implementation may proceed under independent review exactly as Phase 1 did. Until then, no factor, universe, target, ranking, backtest, or report implementation may be written.

## Assumptions

- **CONFIRMED:** Owner authority for Phase 1 (`DECISION-PHASE0-01`, `DECISION-PHASE1-01`) covers only the data foundation; Phase 2 semantics were explicitly deferred to a separate accepted specification (PROJECT_SPEC Restricted Phase 1, final paragraphs).
- **CONFIRMED:** The substrate's feasibility profile supports the proposed weekly point-in-time design (linked evidence).
- **INFERRED:** A UCI-only transaction-demand phase is the highest-value next milestone because it builds the reusable research machinery (versioned universes, machine-readable factors, targets, backtest, IC/quantile evaluation, experiment registry/report) that every later source will use, and it yields a real point-in-time backtest instead of another documentation phase.
- **UNKNOWN:** Whether any proposed factor carries predictive information (that is the research question); whether dataset-local naïve time distorts weekly patterns; whether wholesale transaction demand generalizes (it must not be assumed to).

## Investigation and decision

Alternatives considered:

1. **Wait for the marketplace/demand blockers before any research implementation.** Rejected: both blockers are owner/provider-gated with no timeline; the UCI substrate already supports an honest, bounded research phase, and the machinery built here is source-independent.
2. **Build generic research infrastructure without a Phase 2 specification.** Rejected: it would manufacture unapproved cross-module contracts and data semantics (netting policy, universe rules, targets) behind no authority, violating the accepted Phase 1 boundary.
3. **Propose the smallest decision-complete Restricted Phase 2 specification and ADR, then stop for owner authority.** Selected. The proposal below is exact proposed `PROJECT_SPEC.md` wording; nothing is inserted into the accepted specification unless the owner approves `DECISION-PHASE2-01`.

### Exact proposed specification wording

The following is the exact text proposed for insertion into `PROJECT_SPEC.md` as a subsection of section 51, immediately after the Restricted Phase 1 subsection. It is **proposed**, not accepted; it becomes authority only through `DECISION-PHASE2-01`.

---

### Restricted Phase 2 — UCI Transaction-Event Demand Research

**Status:** `PROPOSED — pending DECISION-PHASE2-01`

**Scope authority:** This subsection, if accepted, authorizes transaction-event demand research solely on the accepted `transaction_event.v1` substrate produced by Restricted Phase 1. It does not authorize any marketplace, listing, availability, supply, competition, or independent external-demand capability; it does not satisfy section 50; and it does not authorize publication, remote storage, or any use of `customer_reference`.

**Data boundary.** The only input is the digest-pinned `transaction_event.v1` Parquet artifact, consumed read-only. Phase 2 MUST NOT access the network, modify raw/normalized state, use `customer_reference`, or aggregate at customer level. Dataset-local naïve timestamps remain of unknown timezone; all semantics are defined in that dataset-local time.

**Point-in-time rule.** For any cutoff `t`, universes and factors MUST use only rows with `event_time_local <= t`; targets MUST use only rows with `event_time_local > t`. A trailing window of `w` days covers `event_time_local` in `(t − w days, t]`; a forward window of `h` days covers `(t, t + h days]`; adjacent windows share an endpoint without gap or overlap. No later description, price, code, or aggregate may fill earlier state. Cutoffs are Mondays `00:00:00` dataset-local; the candidate grid is exactly the Mondays of weeks containing at least one dataset event (104 Mondays under the pinned substrate, excluding event-free holiday weeks). A cutoff is backtest-eligible when its complete primary windows lie inside the dataset span (`t − 30 days >= min(event_time_local)` and `t + 30 days <= max(event_time_local)`); under the pinned substrate this yields 96 weekly cutoffs.

**Universe.** The only entity is the stock-code product proxy (`source_product_code`). `uci-stockcode-universe.v1` at cutoff `t` includes a stock code when, using only rows at or before `t`: it has ≥20 lifetime events, its first event is ≥28 days before `t`, and it has ≥5 events in the trailing 30 days. Universe definitions are versioned; membership is reconstructable per cutoff; no product is removed retrospectively.

**Quantity semantics.** `net-quantity-policy.v1`: no row is dropped or imputed. Gross demand is the sum of positive quantities over all rows regardless of unit price, including zero-priced rows; return/cancellation intensity uses negative quantities separately; net quantity (signed sum) is a distinct input. Each factor and target declares which measure it uses. Weekly aggregation buckets follow the Monday cutoff grid; a bucket with no events contributes gross `0` (observed absence of demand, not missing data).

**Factors.** Exactly five versioned, machine-readable factor definitions, each computed per cutoff from rows at or before `t`. A factor value is missing (never zero-filled) when its declared condition is unmet, and a factor whose full declared window extends before the first dataset event is missing rather than truncated:

1. `demand_level_30d.v1` — `ln(1 + gross, (t−30d, t])`.
2. `demand_momentum_30d.v1` — `ln(1 + gross, (t−30d, t]) − ln(1 + gross, (t−60d, t−30d])`; missing until the complete 60-day span lies inside the dataset.
3. `return_intensity_90d.v1` — `|sum of negative quantities, (t−90d, t]| / (gross, (t−90d, t] + 1)`; missing until the complete 90-day window lies inside the dataset. A window containing only returns yields gross `0`, and the formula remains defined.
4. `price_position_30d.v1` — `ln(median unit price of the product's positive-quantity rows with unit_price > 0, (t−30d, t]) − ln(median of those product medians across universe members at that cutoff)`; missing when the product has no qualifying row in the window.
5. `demand_volatility_13w.v1` — population coefficient of variation (population standard deviation ÷ mean) of weekly gross quantity over the 13 Monday-grid weeks covering `(t−91d, t]`; missing when fewer than 4 of those weeks contain an event, when the mean is `0`, or until the complete 91-day span lies inside the dataset.

Changing any formula creates a new factor version.

**Target.** `forward_demand_growth_30d.v1` — `(gross, (t, t+30d] − gross, (t−30d, t]) / (gross, (t−30d, t] + 1)`, computed only for universe members; products with no forward activity yield a defined value, not a missing one. Horizons 7/60/90 days MAY be evaluated for IC decay. Targets are versioned.

**Signal.** Per cutoff, each factor is converted to a percentile over the universe members with a non-missing value: values are ranked ascending with average ranks for ties, and with `n` non-missing values the percentile is `(average_rank − 1) / (n − 1)`, or `0.5` when `n = 1`. Each factor definition declares an expected direction as a hypothesis (`demand_level_30d` and `demand_momentum_30d` positive; `return_intensity_90d`, `price_position_30d`, and `demand_volatility_13w` negative); the composite uses direction-adjusted percentiles (`q = p` for positive direction, `q = 1 − p` for negative). The composite score is `S_i = (Σ_j w_j q_ij) / (Σ_j w_j)` over factors with non-missing values only, so a member with a missing factor is scored on its available factors with proportionally renormalized weights; a member missing every factor is unranked, and per-entity factor coverage is recorded. Reference weights are `level 0.25, momentum 0.25, return_intensity 0.15, price_position 0.20, volatility 0.15`. Weights and directions are unvalidated research parameters. No model fitting occurs in this phase, so walk-forward training is not yet applicable; any future fitted model requires walk-forward evaluation per section 31.

**Backtest and baselines.** Weekly rebalancing over the backtest-eligible cutoffs defined above. Selection is Top-N with N recorded per experiment. Every strategy is compared against seeded random selection from the same universe, a popularity baseline (`demand_level_30d`), and a momentum baseline (`demand_momentum_30d`); the fixed-weight composite doubles as the section 30 simple-heuristic baseline.

**Evaluation.** Per cutoff and in aggregate: Spearman Rank IC (primary) and Pearson IC for each factor and the composite; mean/median/standard deviation/hit rate; IC decay by horizon; quintile forward-outcome analysis with monotonicity reported but not required; Top-N average/median forward outcome versus every baseline. The report MUST state the number of factors tested and MUST record negative results.

**Experiment and report.** Experiments are declarative JSON configurations. Every run records `experiment_id`, `git_commit`, dataset digest, universe/factor/target/signal versions, parameters, seed, and execution timestamps, and writes outputs plus a manifest under Git-ignored, owner-only `data/experiments/<experiment_id>/`. Each experiment produces a human-readable report per section 46 that distinguishes observations from interpretations and carries the capability declarations below. Factor results are entered into a machine-readable research registry with section 39 statuses; rejected factors are retained.

**Leakage safeguards.** The test suite MUST include section 37 safeguards, including at least one synthetic dataset intentionally containing future information that the pipeline rejects or isolates, plus improperly-joined-timestamp and survivor-only probes.

**Capability declarations.** Every experiment manifest and report MUST carry the eight declarations mandated by Restricted Phase 1 verbatim:

```text
transaction-event history: supported
marketplace listing state: unsupported
marketplace supply/competition: unsupported
independent external demand: unsupported
complete product/opportunity universe: unsupported
integrated ProductQuant v0.1 demonstration: unsupported
historical provider revision state: unknown
timezone: unknown
```

plus exactly one additional line:

```text
transaction-event demand research: supported (this experiment)
```

**Interpretation boundary.** Findings are statements about transaction-event demand within one fixed historical wholesale dataset. They MUST NOT be presented as marketplace opportunity ranking, and they MUST NOT be generalized to consumer marketplaces without separately sourced evidence.

---

### Proposed architecture

The accompanying [`ADR-20260813T011628Z-phase2-transaction-research-architecture`](../ADR/ADR-20260813T011628Z-phase2-transaction-research-architecture.md) (`PROPOSED`) covers module structure, read-only substrate consumption, experiment output persistence, contracts, dependency policy, and determinism. Both decisions are mixed product/architecture and travel together under `DECISION-PHASE2-01`.

## Change

- **Files or components:** This issue, the proposed ADR, the feasibility evidence, `HUMAN_CHECKPOINT.md` decision queue, and `HANDOFF.md`. No specification, source, or test change occurs before owner acceptance.
- **Behavior changed:** None yet; this is a reversible proposal.
- **Out-of-scope work deliberately excluded:** All implementation; marketplace/demand collectors; new data sources; customer-level analysis; use of `customer_reference`; fitted models; publication; push.
- **Rollback or recovery:** Reject or revise the proposal; the issue, ADR, and evidence remain as durable negative/exploratory records.

## Unverified complexity

| Cost | Justification | Coverage | Residual issue |
|---|---|---|---|
| Proposed research modules, contracts, and experiment persistence | Required by specification sections 20–32, 37–39, and 45–46 for any factor/backtest work. | Proposed ADR assigns planned contract/test/evidence coverage; feasibility evidence sizes the design. | Unverified until implementation and independent review under an accepted specification. |

## Verification

| UTC time | Participant | Command or procedure | Result and exit status | Evidence | Limitations |
|---|---|---|---|---|---|
| `2026-08-13T01:16:28Z` | `agent:claude-code-phase2-proposal` | Aggregate-only DuckDB feasibility profile against the digest-pinned Parquet | `PASS — exit 0; 96 usable 30/30 weekly cutoffs, mean ~1,570 eligible products/cutoff, signed-quantity and price-variation structure quantified` | [`EVIDENCE-20260813T011628Z-phase2-research-feasibility-profile`](../EVIDENCE/EVIDENCE-20260813T011628Z-phase2-research-feasibility-profile.md) | Establishes design feasibility only; no factor validity claimed |
| `2026-08-13T01:16:28Z` | `agent:claude-code-phase2-proposal` | Implementation verification | `NOT RUN — implementation is not authorized before owner acceptance of the proposed specification and ADR.` | `NONE` | Correctly absent |

## Self-review

- **Participant:** `NOT_APPLICABLE — this issue requires a fresh independent reviewer.`
- **Reviewed UTC:** `2026-08-13T01:16:28Z`
- **Reviewed repository state:** Clean `e21dd45` plus this issue, the proposed ADR, and the feasibility evidence.
- **Scope and authority references:** Restricted Phase 1 acceptance boundary; PROJECT_SPEC sections 20–32, 37–39, 45–46, 49–50.
- **Checks and evidence reviewed:** Feasibility evidence reproduction path; consistency of the proposed wording with the accepted Phase 1 contract (cutoff rule, capability declarations, no-`customer_reference`, no-network, no-persistent-DB).
- **Findings and corrections:** None yet; no self-approval is claimed.
- **Limitations:** The proposal has not yet been independently reviewed; the owner has not decided.
- **Residual risks:** Over-specification risk (parameters may need owner adjustment); risk that reviewers conflate transaction-demand research with marketplace ranking — mitigated by the interpretation boundary.
- **Outcome:** `NOT_APPLICABLE — independent review is required.`

## Independent review rounds

- **Required:** `YES — the proposal introduces cross-module contracts, a new persistence class (experiment outputs), and product requirements that cross the Human Authority Boundary.`

### 2026-08-13T01:30:00Z — agent:claude-phase2-proposal-review

- **Reviewed repository state:** `e21dd45` on `main`, tracked tree clean; the three untracked proposal records (this issue, the proposed ADR, the feasibility evidence). `PROJECT_SPEC.md` verified unmodified.
- **Scope:** Normative protocol, accepted specification and Phase 1 ADR, the proposal issue/ADR/evidence, checkpoint, HANDOFF; authority analysis, specification compliance, point-in-time correctness, decision-completeness, proportionality, evidence reproduction, cross-reference consistency.
- **Commands or procedures:** Git state/diff; complete file reads; independent in-memory DuckDB aggregate-only reproduction of the feasibility profile against the digest-pinned Parquet (no rows, descriptions, or customer references emitted), plus edge-case probes (zero/negative prices, never-priced codes).
- **Specification compliance:** Passed. Authority analysis confirmed correct (Phase 2 requires a separate accepted specification; nothing smuggled). Cutoff rule matches Phase 1; universe rule PIT- and survivorship-safe; no-network/no-persistent-DB/read-only/`customer_reference` exclusions consistent; spec sections 26, 27, 30, 34, 37, 38, 39, 45–46 covered; JSON-over-YAML a justified documented deviation.
- **Correctness and regression findings:** `HIGH` — composite missing-data rule absent; percentile-rank tie/normalization convention undefined; checkpoint decision queue and HANDOFF omitted the pending decision. `MEDIUM` — `price_position_30d` guards incomplete (zero/negative prices, undefined "universe median"); dataset left-edge window truncation unspecified; cutoff grid origin/extent not numeric; capability block replaced rather than extended the owner-approved eight declarations. `LOW` — volatility std/bucketing unspecified and 90d/13-week naming mismatch; gross treatment of zero-priced rows unstated; momentum prior-window boundary undefined; returns-only-window edge note; fourth section-30 baseline not identified; evidence "clean working tree" phrase imprecise.
- **Architecture and complexity findings:** ADR well-scoped; no unnecessary abstraction; no findings beyond the decision-completeness items.
- **Material findings and resolution conditions:** Define composite behavior under factor missingness; pin percentile/tie conventions; add `DECISION-PHASE2-01` to the checkpoint and reconcile HANDOFF; tighten the MEDIUM wording defects. Every headline feasibility number reproduced exactly.
- **Limitations:** Aggregates reproduced independently, not via the proposer's scripts; no implementation exists to review.
- **Residual risks:** Factor predictive value, timezone, and wholesale-to-consumer generalization remain honestly `UNKNOWN`.
- **Evidence:** Reviewer command outputs and independent aggregate reproduction; no repository files changed by the reviewer.
- **Disposition:** `CHANGES_REQUIRED`
- **Prior-round resolution:** `FIRST ROUND`

### 2026-08-13T01:39:07Z — agent:claude-phase2-proposal-review

- **Reviewed repository state:** `e21dd45` on `main`; tracked modifications limited to `HANDOFF.md`/`HUMAN_CHECKPOINT.md`; the three untracked proposal records with post-round-1 revisions. `PROJECT_SPEC.md` verified unmodified.
- **Scope:** Direct verification of every round-1 resolution plus a fresh defect hunt, including an independent grid enumeration of the pinned cutoff rule.
- **Commands or procedures:** Git state/diff; complete re-reads of revised records; in-memory DuckDB aggregate-only queries including cutoff-grid enumeration (no row-level values emitted).
- **Specification compliance:** Passed; point-in-time rule, quantity semantics, universe rule, target formula, and capability declarations fully consistent with the accepted Phase 1 spec/ADR; the eight declarations character-matched against `PROJECT_SPEC.md`.
- **Correctness and regression findings:** All round-1 findings verified resolved except MEDIUM-3: `MEDIUM` (M-1) — the pinned grid ("Monday preceding the first event through the Monday of the last event's week", 106 Mondays including two event-free holiday weeks) plus the eligibility rule yields 97 eligible cutoffs, not the claimed 96; 96 reproduces only under the activity-week grid. `MEDIUM` (M-2, process) — round 1 was not yet appended to this issue and `Updated UTC`/activity were stale. `LOW` (L-1) — volatility bucket alignment ambiguous and full-window missing rule not restated; (L-2) — HANDOFF snapshot revision stale; (L-3) — ADR status history lacked a post-round-1 edit row.
- **Architecture and complexity findings:** None new.
- **Material findings and resolution conditions:** Correct the 96-vs-97 inconsistency (pin the grid to event-containing weeks or correct the figure); append both review rounds and refresh issue metadata; one-clause cleanups for L-1..L-3.
- **Limitations:** Grid arithmetic verified with an independent enumeration; both grids and predicates cross-checked.
- **Residual risks:** Unchanged — factor predictive value, timezone, and generalization honestly `UNKNOWN`.
- **Evidence:** Reviewer command outputs and independent grid enumeration; no repository files changed by the reviewer.
- **Disposition:** `CHANGES_REQUIRED`
- **Prior-round resolution:** HIGH-1..3, MEDIUM-1/2/4, LOW-1..6, and the ADR conventions item verified resolved; MEDIUM-3 partially resolved (M-1 remainder).

### 2026-08-13T01:42:50Z — agent:claude-phase2-proposal-review

- **Reviewed repository state:** `e21dd45` on `main`; tracked modifications limited to `HANDOFF.md`/`HUMAN_CHECKPOINT.md`; untracked proposal records with post-round-2 revisions; `PROJECT_SPEC.md` verified unmodified.
- **Scope:** Close-out verification of every round-2 resolution, independent reproduction of the corrected grid arithmetic, and final decision-completeness/consistency pass.
- **Commands or procedures:** Git state/diff; complete re-reads of issue/ADR/HANDOFF/evidence corrections; independent in-memory DuckDB aggregate-only grid enumeration (no row-level values emitted).
- **Specification compliance:** Passed. Final wording satisfies decision-completeness: half-open windows with shared endpoints; exact numerically verified grid (104 event-week Mondays, 96 eligible cutoffs spanning 2010-01-04 through 2011-11-07); per-factor missing conditions including left-edge rules; pinned percentile/tie/direction/weight conventions; exact composite missing-data rule; verbatim-plus-one capability declarations; PIT- and survivorship-safe universe; guarded target formula. Authority handling correct — nothing inserted into `PROJECT_SPEC.md`; ADR `PROPOSED`; `DECISION-PHASE2-01` queued with complete links.
- **Correctness and regression findings:** All round-2 findings verified resolved. One new `LOW` housekeeping note: an untracked `.claude/` local-tooling lock file (130 bytes, no data) is not Git-ignored and must be excluded from the proposal commit.
- **Architecture and complexity findings:** None.
- **Material findings and resolution conditions:** `NONE`. Follow-up bookkeeping (not conditions): present `DECISION-PHASE2-01`, commit the proposal records locally without pushing, exclude `.claude/`.
- **Limitations:** Grid arithmetic verified by independent enumeration; implementation review remains mandatory after code exists.
- **Residual risks:** Unchanged — factor predictive value, dataset timezone, and wholesale-to-consumer generalization are `UNKNOWN`; post-approval implementation requires fresh independent review.
- **Evidence:** Reviewer command outputs and independent grid enumeration; no repository files changed by the reviewer.
- **Disposition:** `APPROVED`
- **Prior-round resolution:** All round-1 and round-2 findings verifiably resolved; the only new item is the `.claude/` housekeeping note, handled at commit.

## Blocker

- **Blocked from:** `INVESTIGATING`
- **Blocker:** `Owner decision DECISION-PHASE2-01 is required before any implementation; the independently approved proposal is complete and presented in HUMAN_CHECKPOINT.md.`
- **Unblock owner:** `human:technical-owner`
- **Unblock condition:** `DECISION-PHASE2-01 response recorded with decision, responder identity, UTC time, and durable authority reference; accepted wording then persisted in PROJECT_SPEC.md and the ADR moved to ACCEPTED.`

## Residual uncertainty

- Predictive value of every proposed factor: unknown by design; negative results are acceptable outcomes.
- Timezone/provider-revision caveats inherited from Phase 1 apply to all weekly semantics.
- Wholesale transaction demand must not be assumed to generalize to consumer marketplaces.

## Activity history

| UTC time | Participant | From | To | Action, evidence, and reason |
|---|---|---|---|---|
| `2026-08-13T01:16:28Z` | `agent:claude-code-phase2-proposal` | `NONE` | `OPEN` | Created to carry the boundary-crossing Phase 2 product/architecture proposal after Phase 1 closure. |
| `2026-08-13T01:16:28Z` | `agent:claude-code-phase2-proposal` | `OPEN` | `INVESTIGATING` | Gathered aggregate-only feasibility evidence and drafted the exact proposed specification wording and proposed ADR for independent review before requesting owner authority. |
| `2026-08-13T01:30:00Z` | `agent:claude-phase2-proposal-review` | `INVESTIGATING` | `INVESTIGATING` | Round 1 independently reproduced the feasibility profile and returned `CHANGES_REQUIRED`: composite missing-data and percentile conventions, decision-queue omission, price guards, window truncation, cutoff grid, capability-block amendment, and low-severity wording items. |
| `2026-08-13T01:31:12Z` | `agent:claude-code-phase2-proposal` | `INVESTIGATING` | `INVESTIGATING` | Resolved all round-1 findings: exact composite/percentile/direction conventions, pinned windows and grid, price guards, verbatim-plus-one capability declarations, checkpoint `DECISION-PHASE2-01` row, HANDOFF reconciliation, ADR conventions clause, evidence correction row. |
| `2026-08-13T01:39:07Z` | `agent:claude-phase2-proposal-review` | `INVESTIGATING` | `INVESTIGATING` | Round 2 verified all round-1 resolutions and returned `CHANGES_REQUIRED` on one arithmetic defect (pinned grid yields 97 eligible cutoffs, not 96), the missing review-round transcription, and three low-severity cleanups. |
| `2026-08-13T01:39:07Z` | `agent:claude-code-phase2-proposal` | `INVESTIGATING` | `INVESTIGATING` | Resolved round-2 findings: grid pinned to Mondays of event-containing weeks (reproduces 96), volatility window pinned to the 13 weeks covering `(t−91d, t]` with the full-window missing rule restated, both review rounds appended, HANDOFF snapshot revision corrected, ADR status history row added. |
| `2026-08-13T01:42:50Z` | `agent:claude-phase2-proposal-review` | `INVESTIGATING` | `INVESTIGATING` | Round 3 independently reproduced the corrected grid arithmetic (104 event-week Mondays, 96 eligible cutoffs), verified every prior resolution, and returned `APPROVED` with one low-severity `.claude/` housekeeping note. |
| `2026-08-13T01:42:50Z` | `agent:claude-code-phase2-proposal` | `INVESTIGATING` | `BLOCKED` | Proposal complete and independently approved; recorded the owner decision request `DECISION-PHASE2-01` in HUMAN_CHECKPOINT.md. No implementation is authorized until the owner responds. |

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
