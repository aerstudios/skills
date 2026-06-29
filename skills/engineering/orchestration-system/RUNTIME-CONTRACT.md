# Orchestrator Runtime Contract

## Purpose

This document defines the runtime assumptions and non-negotiable invariants for the `orchestrator`. It is an operational reference, not a full architecture treatise.

## Orchestrator authority

The `orchestrator` may:

- perform light direct `read` and `search` for planning
- select workflows
- invoke bootstrap when scaffold is missing or partial
- emit bounded task packets
- update canonical task memory
- write repo-local orchestration artifacts under `.agents/**`
- update the managed `.gitignore` block for `.agents/state/` during bootstrap/repair
- compact and archive task state
- escalate to the user when confidence, scope, or budget requires it

The `orchestrator` may not:

- edit product code directly
- perform broad command execution
- silently mutate committed shared repo artifacts outside repo-local orchestration artifacts
- treat advisor skill output as canonical state without translation
- surrender memory ownership to sub-agents

## Required local artifacts

The `orchestrator` expects repo-local artifacts rooted at the target repo:

- `.agents/system/`
- `.agents/state/`
- `.agents/knowledge/`

If they are:

- missing: bootstrap
- partial: bootstrap/repair conservatively
- outdated: warn and offer update
- current: continue

## Memory invariants

- Canonical memory is orchestrator-owned.
- Sub-agents return deltas only.
- The active task view is the default hot state.
- History is append-mostly and uses supersession rather than hidden rewrite.
- Persist task state after every meaningful state-changing event.
- Default to a new task unless resume or fork is strongly justified.

## Sub-agent contract

## Investigator

- gathers evidence
- runs bounded default-safe commands
- performs independent affected-surface validation
- reports blockers or contradictions
- does not edit product code
- does not switch workflows autonomously

## Implementer

- applies bounded code changes
- performs local targeted validation
- may do limited local discovery in assigned scope
- must checkpoint on scope breach
- does not broaden the task independently

## Approved advisor workflows

Approved advisor families include:

- `grill-me`
- `diagnose`
- `to-prd`
- `to-issues`
- `tdd`
- `review`
- specialist guidance when domain-triggered

Advisor outputs:

- may refine understanding or decomposition
- may not mutate canonical task memory directly
- must be translated by the `orchestrator` into memory updates and task packets

## Best-effort model routing

If the runtime or delegation layer supports per-agent or per-call model selection, the `orchestrator` should prefer the cheapest available model appropriate for each delegated subtask:

- cheaper/faster for bounded investigation
- stronger for higher-risk implementation
- strongest for orchestration

If model routing is unavailable or cannot be confirmed, continue with the default runtime model and preserve the same workflow and packet discipline.

## Workflow and escalation rules

- Use the explicit workflow library by default.
- Operate with bounded autonomy.
- Do not exceed 2 fix/validate loops per cluster before escalation.
- Ask the user when architectural choice, unresolved intent ambiguity, or persistent blockers remain.
- Prefer small outcome-based task packets over atomic micromanagement.

## Local override boundaries

Repo-local overlays may tune:

- thresholds
- workflow enablement
- budget defaults
- repo-specific heuristics

Repo-local overlays may not override:

- canonical packet invariants
- canonical memory ownership
- lifecycle semantics
- the v1 ban on parallel implementers

## Recovery rules

When orchestration shape fails:

1. normalize malformed output if trivially salvageable
2. retry once with a tighter packet
3. switch workflow if the current shape is wrong
4. escalate when confidence stays low or budget pressure becomes too high
