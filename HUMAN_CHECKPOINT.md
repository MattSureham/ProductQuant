# Human Checkpoint

This file is a low-bandwidth synchronization point for the human technical owner. It should preserve an accurate mental model and surface authority decisions without narrating every diff. Read [`BOOTSTRAP.md`](BOOTSTRAP.md) for normative rules.

This checkpoint is a summary and decision queue, not a source of project truth. Persist accepted product decisions in `PROJECT_SPEC.md` and accepted architectural decisions in `ADR/` before agents rely on them.

## Checkpoint metadata

- **Generated UTC:** `[timestamp or NOT YET GENERATED]`
- **Prepared by:** `[participant]`
- **Period covered:** `[prior checkpoint/revision/time through current state]`
- **Specification status reviewed:** `[status and reference]`
- **Implementation/reference state:** `[commit, file hashes, or other durable state]`
- **Prior checkpoint:** `[reference or NONE]`

## System mental model

In a few paragraphs, explain the system's current responsibilities, major boundaries, important data/control flow, and externally visible contracts. Emphasize what the owner needs to remember if they read nothing else.

`[Current mental model. Label unverified parts INFERRED or UNKNOWN.]`

## Material changes since the prior checkpoint

| Change | Why | Product/architecture effect | Evidence and review |
|---|---|---|---|
| `[material change]` | `[reason]` | `[effect]` | `[links]` |

Do not list routine local refactors unless they alter risk, complexity, confidence, or the owner's mental model.

## Architecture decisions

### Accepted, rejected, or superseded

| ADR | Status | Decision and consequence | Owner authority evidence |
|---|---|---|---|
| `[link]` | `[status]` | `[concise consequence]` | `[reference]` |

### Proposed or disputed

| ADR or issue | Decision needed | Alternatives and tradeoff | Deadline/blocking impact |
|---|---|---|---|
| `[link]` | `[question]` | `[concise choices]` | `[impact]` |

## Complexity and architecture drift

### New or retired complexity

| Cost | Why introduced/removed | Coverage | Residual debt |
|---|---|---|---|
| `[abstraction/dependency/state/config/process/concurrency/coupling]` | `[reason]` | `[contracts/tests/evidence]` | `[issue or NONE]` |

### Drift assessment

- **Last independent drift review:** `[reference or NOT PERFORMED]`
- **Classification:** `[ALIGNED/JUSTIFIED_DEVIATION/UNJUSTIFIED_DRIFT/UNKNOWN]`
- **Owner-relevant differences:** `[summary and issue links]`

## Assumptions and uncertainty that changed

| Certainty | Earlier understanding | Current understanding | Consequence and evidence |
|---|---|---|---|
| `[CONFIRMED/INFERRED/UNKNOWN]` | `[before]` | `[now]` | `[effect/link]` |

## Confidence and verification

- **What is directly verified:** `[claims and evidence]`
- **What was independently reviewed:** `[scope and review result]`
- **What was not run or remains unverified:** `[omission and consequence]`
- **Known regressions or unresolved risks:** `[issues or NONE]`

## Human attention required

List only matters that require owner authority or materially affect the owner's mental model.

| Decision ID | Decision requested | Recommendation and rationale | Alternatives | Needed by | Response | Responder | Decision UTC | Durable authority reference |
|---|---|---|---|---|---|---|---|---|
| `[stable ID]` | `[question]` | `[recommendation]` | `[meaningful alternatives]` | `[date/milestone]` | `PENDING` | `PENDING` | `PENDING` | `PENDING` |

A response is approval evidence only when its decision, responder identity, UTC time, and durable authority reference are all recorded. The responsible participant must then update the affected specification, ADR, or both and link this decision before implementation relies on it. A product or public-contract decision must update `PROJECT_SPEC.md`; an ADR alone is insufficient.

## No human attention required

- `[Routine implementation or verification work the owner can safely ignore, or NONE.]`

## Next checkpoint trigger

- **Trigger:** `[release, milestone, accepted ADR, drift finding, owner request, or date]`
- **Expected owner action before then:** `[action or NONE]`
