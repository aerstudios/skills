# Task State Schema

This document defines the canonical task-memory model for the orchestration system.

The model is task-centric and owned by the `orchestrator`. It is not intended to be a general knowledge graph.

## Storage layout

```text
.agents/
  state/
    index.json
    tasks/
      tsk_001/
        active.json
        history.jsonl
        closure.json
        transcript.jsonl
        archive/
```

## Ownership rules

- Canonical task state is owned by the `orchestrator`.
- `investigator`, `implementer`, and advisor skills return deltas only.
- Sub-agents do not write canonical task files directly.
- Derived summaries and indexes may be rewritten by the `orchestrator`.
- Historical/provenance records are append-mostly.

## Task identity

Task IDs are sequential per repo, with optional labels/slugs.

Examples:

- `tsk_001`
- `tsk_002`
- `tsk_003` with label `auth-timeout-race`

## Task lifecycle states

Allowed task states:

- `active`
- `blocked`
- `paused`
- `completed`
- `abandoned`
- `superseded`

All paused or terminal tasks should have a closure/checkpoint record.

## Task index

`.agents/state/index.json` is the repo-level entry point.

Minimum fields:

- `version`
- `nextTaskSequence`
- `tasksByStatus`
- `activeLocks`

## Graph model

The canonical memory model is a small typed graph.

### Required node types

- `task`
- `cluster`
- `evidence`
- `hypothesis`
- `decision`
- `action`
- `validation`
- `version`

Operational environment/tooling discoveries are tracked as a first-class state section called `OperationalFacts`, not as graph nodes in v1.

Durable team-useful discoveries that will help future repo work should be recorded as `promotionCandidates` in task state or closure. Codebase/architecture discoveries route to a Serena memory update; orchestration-process discoveries route to `.agents/knowledge/**`. Committed `.agents/knowledge/**` writes happen only during an explicit curation/update flow or when knowledge promotion is allowed for the task. The git diff is the human review gate.

### Allowed edge types

Structural:

- `parent_of`
- `depends_on`

Reasoning/provenance:

- `derived_from`
- `supports`
- `contradicts`
- `supersedes`

Execution/verification:

- `implemented_by`
- `tests`
- `blocks`

Versioning:

- `variant_of`

## Active view

`active.json` should contain a compact derived snapshot plus orchestrator working fields.

Derived state:

- `taskId`
- `status`
- `label`
- `objective`
- `constraints`
- `activeTaskIds`
- `activeClusterIds`
- `topHypotheses`
- `latestDecisions`
- `latestValidations`
- `blockers`
- `rejectedPaths`
- `lineageSummary`
- `operationalFacts`

Working fields:

- `selectedWorkflow`
- `budgetMode`
- `blastRadius`
- `loopCountsByCluster`
- `nextQueuedDelegations`
- `escalationPending`
- `escalationReason`
- `debugMode`
- `revision`
- `lock`

## Operational facts

`OperationalFacts` record environment and tooling discoveries that affect command choice or execution strategy.

They are distinct from product/code evidence.

Examples:

- `rg` missing in the current environment
- `python3` present and preferred over `python`
- `pnpm` works for this repo
- a test runner is unavailable in the current environment

Operational facts should:

- be learned from observed execution first
- be tagged with a lightweight environment fingerprint
- become hard temporary rules within the current task/environment
- be cleared or superseded when the environment changes or new evidence overrides them
- become promotion candidates only when they are durable enough to help future teammates, not merely useful to the current task

Suggested shape:

```json
{
  "tool": "rg",
  "status": "missing",
  "scope": "environment",
  "evidence": "command not found",
  "environmentFingerprint": {
    "os": "macos",
    "shell": "zsh",
    "cwdRootType": "git",
    "toolHints": ["rg:missing", "python3:present"]
  },
  "firstSeenTaskId": "tsk_004",
  "confidence": "high",
  "promoteCandidate": false
}
```

Keep only a small hot set in `active.json`. Older or superseded operational facts should be compacted like other task memory.

## Closure record

Every paused or terminal task should write `closure.json`.

Minimum fields:

- `taskId`
- `status`
- `summary`
- `finalOutcome` or `pauseReason`
- `validatedResults`
- `remainingBlockers`
- `rejectedPaths`
- `promotionCandidates`
- `followOnTaskIds`
- `updatedAt`

If operational facts materially shaped command choices or blocked work, include the relevant summaries in the closure summary or promotion candidates.

## Revision and locking

`active.json` should include revision metadata.

Rules:

- increment revision on each meaningful persisted state change
- write using temp-file + atomic rename
- if same-task conflict is detected, block in v1 rather than attempting merge
- same-task concurrent orchestration is unsupported in v1
