# Operational Handoff

Read [`BOOTSTRAP.md`](BOOTSTRAP.md) before using this file. This is operational continuity, not long-term project truth. Replace template statements only after inspecting the repository; preserve attributable activity and evidence.

- Prefix material claims with `CONFIRMED`, `INFERRED`, or `UNKNOWN` and link their support.
- Reconcile shared snapshot fields from evidence, then add your own activity entry.
- Never silently rewrite another participant's activity, evidence, or disagreement.
- Keep exactly one bounded entry under `Next Action`.

## Current State

### Snapshot

- **Snapshot updated UTC:** `[timestamp or NOT YET RECONCILED]`
- **Repository state:** `[revision/branch/upstream when available, plus exact dirty-state summary]`
- **Evidence cutoff:** `[latest evidence UTC/revision inspected for this snapshot]`
- **External checks:** `[reference, checked UTC, result, and declared refresh condition; or NONE]`
- **Stale when:** `[revision/branch differs; dirty files are not represented; newer evidence changes a claim; an external reference changes/expires; a non-terminal task is not reconciled; or higher authority conflicts with this snapshot]`
- **UNKNOWN — Product state:** The adopting repository has not yet been inspected through this template.
- **UNKNOWN — Specification status:** Read `PROJECT_SPEC.md` and record whether it is accepted and sufficient for the next action.
- **UNKNOWN — Working state:** Inspect version-control state when available and preserve unrelated changes.
- **UNKNOWN — Verification state:** No repository-specific commands have been recorded in this template.

Do not refresh only the timestamp. When a staleness trigger fires, mark affected claims `UNKNOWN`, reconcile them from higher-precedence artifacts and actual repository state, and record the reconciliation as new activity.

### Constraints

- Read current constraints from `PROJECT_SPEC.md`, accepted ADRs, and higher-priority execution instructions.
- `[Add only current operational constraints that the next participant must know.]`

### Unverified complexity

No complexity is recorded by the template. This is not evidence that none exists. Link every discovered cost to an open issue until it is covered or removed. Human acceptance may authorize uncovered debt to remain, but the debt issue stays open with its acceptance evidence, conditions, and residual risk.

### Background tasks

No background tasks are recorded by the template. Inspect the environment before relying on this statement.

For each task, record:

| Task ID | Purpose | Owner | Started UTC | Process or remote reference | Query/recovery command | Last observed UTC | State | Terminal evidence |
|---|---|---|---|---|---|---|---|---|
| `[TASK-id]` | `[purpose]` | `[participant]` | `[time]` | `[durable reference]` | `[exact command/procedure]` | `[time]` | `[QUEUED/RUNNING/SUCCEEDED/FAILED/CANCELLED/ORPHANED]` | `[link or pending]` |

Remove the placeholder row when recording the first real task. Keep only non-terminal tasks in this live table. When a task becomes terminal, move its durable result to the owning issue/evidence record and retain a concise Recent Activity or Archived Summary link.

## Active Issues

No issues have been recorded yet. This does not establish that none exist.

Index meaningful issue files compactly:

| Issue | Status | Severity | Owner | Authority | Review | Summary | Evidence or unblock condition |
|---|---|---|---|---|---|---|---|
| `[ISSUE-id; record: ISSUES/filename.md]` | `[state]` | `[LOW/MEDIUM/HIGH/CRITICAL]` | `[participant or UNASSIGNED]` | `[AGENT/HUMAN]` | `[SELF/INDEPENDENT]` | `[one sentence]` | `[link or condition]` |

Remove the placeholder row when indexing the first issue.

## Next Action

Inspect the repository, complete the Start or Resume procedure in `BOOTSTRAP.md`, and replace this template snapshot with evidence-backed project state.

## Recent Activity

No repository-specific activity has been recorded. Prepend new entries using this shape:

### [UTC timestamp] — [participant] — [temporary role]

- **Task:** `[bounded task]`
- **Context inspected:** `[files, ranges, state, external references]`
- **Actions performed:** `[actions]`
- **Files modified:** `[paths or NONE]`
- **Findings:** `[certainty-labeled findings and evidence links]`
- **Verification performed:** `[exact commands/results or NOT RUN with reason]`
- **Issues created or updated:** `[links or NONE]`
- **Remaining uncertainty:** `[unknowns or NONE]`
- **Recommended next action:** `[one bounded action]`

Delete only these instructional placeholder lines after the first real entry. Never edit another participant's entry except to append an attributable correction for an objectively broken reference.

## Archived Summary

No activity has been archived.

When this file approaches 1,000 lines or becomes hard to scan, preserve at least the ten newest entries and every entry required by unresolved work. Move closed issue bodies, long evidence narratives, terminal-task ledgers, and older diary entries to their owning durable records or immutable version-control history. Summarize them here with links to retained ADRs, issues, evidence, rejected approaches, disputes, major reasoning, and the pre-compaction revision/digest. Record the compaction as new Recent Activity.
