# Restricted Phase 2 Transaction-Event Research Architecture

## Metadata

- **ID:** `ADR-20260813T011628Z-phase2-transaction-research-architecture`
- **Title:** `Adopt a read-only, contract-versioned, ephemeral-compute research layer over the Phase 1 substrate`
- **Status:** `PROPOSED`
- **Created UTC:** `2026-08-13T01:16:28Z`
- **Author:** `agent:claude-code-phase2-proposal`
- **Human technical owner:** `human:technical-owner`
- **Owner approval:** `PENDING — DECISION-PHASE2-01`
- **Related specification:** [`PROJECT_SPEC.md` sections 20–32, 37–39, 45–46, 49–50, Restricted Phase 1, and the proposed Restricted Phase 2 wording in the linked issue](../PROJECT_SPEC.md)
- **Related issues:** [`ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec`](../ISSUES/ISSUE-20260813T011628Z-phase2-transaction-demand-research-spec.md)
- **Supersedes / superseded by:** `NONE — extends ADR-20260812T072420Z-uci-transaction-data-foundation without altering it`

## Context

Restricted Phase 1 delivered an immutable, digest-pinned `transaction_event.v1` substrate and a four-command CLI, and explicitly deferred all research semantics. The proposed Restricted Phase 2 specification (exact wording in the linked issue, pending `DECISION-PHASE2-01`) requires universes, five versioned factors, a versioned forward target, a weekly point-in-time backtest, baselines, IC/quantile evaluation, declarative experiments, and reproducible reports. These introduce cross-module contracts and a new local persistence class (experiment outputs), so the architecture requires a durable decision before implementation.

The feasibility profile (`EVIDENCE-20260813T011628Z-phase2-research-feasibility-profile`) shows the design is small: ~1.6 GB uncompressed events read as an 11.9 MB Parquet, ~96 weekly cutoffs, ~1,570 products per cutoff. No distributed or persistent infrastructure is warranted.

## Decision

If the owner accepts the proposed Restricted Phase 2 specification, the research layer adopts these rules:

1. **Module structure.** Add `productquant/research/` with single-responsibility modules: `universe`, `factors`, `targets`, `signals`, `backtest`, `evaluation`, `experiments`, `reports`. The existing `uci.py` data foundation is unchanged; research modules consume it only through the normalized artifact path and its manifest.
2. **Read-only ephemeral compute.** The substrate Parquet is opened read-only. All aggregation runs through in-memory DuckDB or PyArrow compute; no persistent database, no writes into `data/raw/` or `data/normalized/`, and no network access. Any DuckDB use remains ephemeral exactly as in Phase 1.
3. **Versioned machine-readable contracts.** Universe, factor, target, and signal definitions are JSON documents carrying explicit `*_version` fields, stored under `src/productquant/contracts/` with the same packaging and contract-test treatment as the Phase 1 contracts. Changing a formula creates a new version; old versions remain readable. The exact statistical conventions — window bounds, percentile/tie handling, missing-data rules, and direction adjustment — live in these versioned contracts and the accepted specification, never in ad-hoc code.
4. **Experiment persistence.** Each run writes a self-contained directory `data/experiments/<experiment_id>/` containing the resolved JSON configuration, per-cutoff factor/target matrices (Parquet), evaluation results (JSON), the Markdown report, and a row-free-of-customer-data manifest with the reproducibility fields required by specification section 38. Experiment outputs are Git-ignored and owner-only on POSIX, matching the Phase 1 privacy posture. Experiment outputs are derived state: they are reproducible from the immutable substrate plus configuration and are never a second source of truth.
5. **No new runtime dependencies.** Experiment configurations and contracts use JSON (PyYAML is not adopted). The locked dependency set (`openpyxl`, `pyarrow`, `duckdb`, `pytest`, `uv_build`) is unchanged. If implementation discovers a hard need for an additional package, that need returns here as an ADR amendment before adoption.
6. **Determinism.** Factor/target matrices are deterministic functions of the substrate and configuration. The random baseline uses a recorded seed; ties and ordering use explicit stable keys. Re-running an experiment with the same configuration, substrate digest, and code revision reproduces identical evaluation results; the manifest records any legitimate non-determinism rather than hiding it.
7. **CLI extension.** Add `productquant experiment run <config.json> --data-root PATH` and `productquant experiment report <experiment_id> --data-root PATH`, following the Phase 1 conventions: one JSON result object on stdout, structured errors on stderr, the same exit-code vocabulary extended only if a new failure class is genuinely needed, and receipts under `data/receipts/`. No command logs transaction rows, product descriptions, or customer references.
8. **Leakage posture.** Point-in-time enforcement lives in the universe/factor/target query layer (cutoff predicates), not in caller discipline. The test suite adds the specification section 37 safeguards: a synthetic dataset with intentional future information must be rejected or isolated, plus improperly-joined-timestamp and survivor-only probes, and per-factor boundary tests proving rows after the cutoff cannot affect the factor value.

## Human Authority Boundary assessment

- **Boundary crossed:** `YES`
- **Reason:** New cross-module contracts (universe/factor/target/signal), a new persistence class (experiment outputs), CLI surface extension, and product requirements (the proposed Restricted Phase 2 specification). This is a mixed product/architecture decision.
- **Existing authorization:** `NONE for Phase 2` — the accepted Restricted Phase 1 specification explicitly requires a separate accepted specification for Phase 2 transaction-demand factor semantics. Sections 20–32 and 45–46 describe v0.1 goals but do not authorize these exact semantics.
- **Approval evidence:** `PENDING — DECISION-PHASE2-01 in HUMAN_CHECKPOINT.md`; on approval, the exact wording is persisted in `PROJECT_SPEC.md` and this ADR moves to `ACCEPTED`.

## Alternatives considered

### Wait for marketplace/demand sources before building any research machinery

- **Benefits:** Research would run on data closer to the long-term product question.
- **Costs and risks:** Both blockers are owner/provider-gated with no timeline; the project would idle. The machinery (universes, factors, backtest, evaluation, registry) is source-independent and must exist regardless.
- **Reason not selected:** Idle time with no evidence gain; the UCI-only phase is honestly bounded and explicitly non-generalizing.

### Generic plugin-based factor framework

- **Benefits:** Superficially more reusable across future sources.
- **Costs and risks:** Premature abstraction over a single substrate; manufactures generality without a second consumer; larger review surface.
- **Reason not selected:** The proposal keeps modules concrete against `transaction_event.v1`; generalization waits for a second authorized source.

### pandas-based research scripts instead of packaged modules

- **Benefits:** Less packaging overhead.
- **Costs and risks:** New heavyweight dependency, weaker determinism and typing guarantees, scripts instead of versioned contracts, harder independent review, and weaker reproducibility evidence.
- **Reason not selected:** The locked stack already provides DuckDB/PyArrow; contract-versioned packaged modules are the smallest design that satisfies sections 22, 38, and 45.

### Persistent DuckDB research database

- **Benefits:** Faster repeated ad-hoc queries.
- **Costs and risks:** Creates a second mutable source of truth, migration burden, and staleness risk; contradicts the Phase 1 ephemeral-DuckDB rule.
- **Reason not selected:** Derived matrices are written per experiment under `data/experiments/`; the Parquet substrate remains the only truth.

## Consequences

### Positive

- The repository gains the full research loop machinery (universe → factors → signal → backtest → IC/quantiles → report) on a verified substrate, with versioned contracts that later sources can reuse or replace deliberately.
- Point-in-time enforcement is structural (query-layer predicates plus leakage tests), not convention.
- No dependency, network, or privacy-surface growth; `customer_reference` is architecturally untouched.

### Negative and tradeoffs

- Conclusions remain limited to one fixed wholesale dataset; the report layer must actively prevent over-interpretation.
- Five contracts plus experiment persistence expand the maintained surface; each version change requires deliberate review.
- Percentile-rank compositing discards magnitude information; it is chosen for robustness to outliers (observed extremes reach ±80,995 units) at the cost of some sensitivity.

### Compatibility and migration

- No change to the accepted Phase 1 ADR, substrate, or CLI. Research outputs are additive and ignored by Git. Rejection of this ADR leaves Phase 1 fully intact.

## Unverified complexity

| Cost introduced | Why necessary | Contract/test/evidence coverage | Residual gap and linked issue |
|---|---|---|---|
| `productquant/research/` modules (8) | Specification sections 20–32, 45–46 require universe/factor/target/signal/backtest/evaluation/experiment/report capability. | Planned: contract tests per versioned definition, synthetic-fixture unit tests, leakage suite, full-substrate experiment gate. | Unverified until implementation and independent review; owned by the linked issue. |
| Four new JSON contract families | Section 22 requires machine-readable versioned factor definitions; the same rigor extends to universe/target/signal. | Planned: schema validation tests and packaging checks mirroring Phase 1 contracts. | Same as above. |
| Experiment output persistence under `data/experiments/` | Section 38 reproducibility and section 46 reports require durable run records. | Planned: manifest schema tests, idempotent rerun/no-clobber behavior, owner-only mode checks. | Same as above. |
| CLI `experiment` commands | Research interface required by section 44 conventions. | Planned: CLI JSON/exit-code/error tests mirroring Phase 1. | Same as above. |

## Evidence and assumptions

- **CONFIRMED:** The substrate digest, schema, and verification state are recorded in [`EVIDENCE-20260812T091334Z-phase1-data-foundation-verification`](../EVIDENCE/EVIDENCE-20260812T091334Z-phase1-data-foundation-verification.md); feasibility for the weekly design is recorded in [`EVIDENCE-20260813T011628Z-phase2-research-feasibility-profile`](../EVIDENCE/EVIDENCE-20260813T011628Z-phase2-research-feasibility-profile.md).
- **CONFIRMED:** The accepted Restricted Phase 1 specification requires a separate accepted specification for Phase 2 semantics and forbids Phase 1 from materializing universes, factors, targets, rankings, or backtests.
- **INFERRED:** Eight focused modules plus JSON contracts is the smallest structure satisfying sections 20–32, 37–39, and 45–46 without new dependencies; this judgment awaits independent review.
- **UNKNOWN:** Whether percentile-rank compositing and the chosen factor set survive empirical evaluation (that is the research output, not an architectural assumption); whether a second authorized source will later justify generalizing the module boundaries.

## Independent review rounds

- **Required:** `YES — cross-module contracts, a new persistence class, CLI extension, and a boundary-crossing product decision.`

### 2026-08-13T01:30:00Z — agent:claude-phase2-proposal-review

- **Reviewed repository state:** `e21dd45` on `main`, tracked tree clean; untracked proposal records (Phase 2 issue, this ADR, feasibility evidence); `PROJECT_SPEC.md` verified unmodified.
- **Scope:** Protocol, accepted specification and Phase 1 ADR, proposal records, checkpoint/HANDOFF; authority, specification compliance, point-in-time correctness, decision-completeness, proportionality, evidence reproduction.
- **Commands or procedures:** Git state/diff; complete reads; independent in-memory DuckDB aggregate-only reproduction of the feasibility profile and edge-case probes.
- **Findings and resolution conditions:** ADR architecture found well-scoped with no unnecessary abstraction; all material findings targeted the proposed specification wording (composite missing-data rule, percentile/tie convention, decision-queue omission, price guards, window truncation, cutoff grid, capability-block amendment) and are recorded in full in the linked issue. ADR-specific condition: assign exact statistical conventions to the versioned contracts and accepted specification.
- **Limitations:** No implementation exists to review.
- **Residual risks:** Factor predictive value, timezone, and generalization remain `UNKNOWN`.
- **Evidence:** Reviewer command outputs and independent aggregate reproduction; no repository files changed by the reviewer.
- **Disposition:** `CHANGES_REQUIRED`
- **Prior-round resolution:** `FIRST ROUND`

### 2026-08-13T01:39:07Z — agent:claude-phase2-proposal-review

- **Reviewed repository state:** `e21dd45` on `main`; tracked modifications limited to `HANDOFF.md`/`HUMAN_CHECKPOINT.md`; revised untracked proposal records.
- **Scope:** Direct verification of every round-1 resolution plus fresh defect hunt, including independent cutoff-grid enumeration.
- **Commands or procedures:** Git state/diff; complete re-reads; aggregate-only DuckDB queries including grid enumeration (no row-level values emitted).
- **Findings and resolution conditions:** All round-1 resolutions verified, including the strengthened decision item 3. New findings target the proposed specification text (97-vs-96 cutoff arithmetic, review-round transcription, volatility bucket phrasing) and HANDOFF snapshot staleness; no ADR architecture defect found. Full text in the linked issue.
- **Limitations:** Grid arithmetic independently enumerated; implementation still absent.
- **Residual risks:** Unchanged.
- **Evidence:** Reviewer command outputs and grid enumeration; no repository files changed by the reviewer.
- **Disposition:** `CHANGES_REQUIRED`
- **Prior-round resolution:** All round-1 ADR-relevant findings resolved; MEDIUM-3 partially resolved pending the grid fix now applied in the issue.

### 2026-08-13T01:42:50Z — agent:claude-phase2-proposal-review

- **Reviewed repository state:** `e21dd45` on `main`; tracked modifications limited to `HANDOFF.md`/`HUMAN_CHECKPOINT.md`; untracked proposal records with post-round-2 revisions; `PROJECT_SPEC.md` verified unmodified.
- **Scope:** Close-out verification of every round-2 resolution, independent reproduction of the corrected cutoff-grid arithmetic, and final decision-completeness pass over the proposal.
- **Commands or procedures:** Git state/diff; complete re-reads; independent aggregate-only DuckDB grid enumeration (104 event-week Mondays, 96 eligible cutoffs reproduced; no row-level values emitted).
- **Findings and resolution conditions:** No correctness, authority, compliance, or architecture findings remain. One low-severity housekeeping note: an untracked `.claude/` local-tooling lock file must be excluded from the proposal commit.
- **Limitations:** Grid arithmetic verified by independent enumeration; implementation review remains mandatory after code exists.
- **Residual risks:** Factor predictive value, dataset timezone, and wholesale-to-consumer generalization remain `UNKNOWN`; post-approval implementation requires fresh independent review.
- **Evidence:** Reviewer command outputs and grid enumeration; full text in the linked issue; no repository files changed by the reviewer.
- **Disposition:** `APPROVED`
- **Prior-round resolution:** All round-1 and round-2 findings verifiably resolved. The proposal is ready for owner decision `DECISION-PHASE2-01`; this ADR remains `PROPOSED` until that decision is durably recorded.

## Status history

| UTC time | From | To | Actor | Reason and authority evidence |
|---|---|---|---|---|
| `2026-08-13T01:16:28Z` | `NONE` | `PROPOSED` | `agent:claude-code-phase2-proposal` | Boundary-crossing Phase 2 architecture recorded for independent review and owner decision `DECISION-PHASE2-01`; no implementation authorized. |
| `2026-08-13T01:31:12Z` | `PROPOSED` | `PROPOSED` | `agent:claude-code-phase2-proposal` | Strengthened decision item 3 (exact statistical conventions live in versioned contracts/specification) in response to independent review round 1; remains `PROPOSED` pending `DECISION-PHASE2-01`. |
