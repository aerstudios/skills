# Orchestration System Architecture

## Intent

This system exists to make multi-step engineering work more reliable and cheaper by separating:

- orchestration and memory ownership
- evidence gathering and validation
- bounded implementation

Prompt brevity alone is not enough. The core design levers are:

- canonical memory owned by the orchestrator
- bounded task packets
- explicit workflow selection
- repo-local runtime artifacts
- reusable bootstrap/setup

## System boundaries

The system has three layers.

### 1. Source of truth

Reusable skills and design docs live in:

- `~/Sites/aer/skills`

This is where the system is authored and evolved.

### 2. Installed global surface

Installed agents and synced skills live in:

- `~/.agents`

This layer provides the globally available runtime entrypoints.

### 3. Repo-local runtime surface

Each target repo may contain:

- `.agents/system/`
- `.agents/state/`
- `.agents/knowledge/`

This layer holds the repo-scoped scaffold, runtime state, and curated knowledge.

## Core roles

## `orchestrator`

Purpose:

- public entry point for multi-step engineering work
- owns canonical memory
- chooses workflows
- emits bounded task packets
- decides when to clarify, delegate, validate, escalate, or stop

Authority:

- may perform light `read`/`search` for planning
- may invoke bootstrap when scaffold is missing or partial
- may persist repo-local orchestration state
- may write repo-local orchestration artifacts under `.agents/**`
- may update the managed `.gitignore` block for `.agents/state/`
- may use approved advisor skills to refine plans

Forbidden:

- editing product code directly
- broad command execution
- handing process truth to sub-agents or skills
- silently mutating committed shared repo artifacts outside repo-local orchestration artifacts

## `investigator`

Purpose:

- low-cost evidence gathering, targeted execution, and independent validation

Authority:

- may inspect code and docs in assigned scope
- may run default-safe commands in assigned scope
- may report blockers, contradictions, and recommended next steps

Forbidden:

- editing product files
- autonomous workflow switching
- broadening scope without authorization

## `implementer`

Purpose:

- bounded code changes backed by evidence and explicit constraints

Authority:

- may make minimal edits in assigned scope
- may perform local targeted validation
- may perform limited local discovery near named targets

Forbidden:

- broad refactors without assignment
- proceeding after scope-breach triggers
- changing public API or shared surfaces unless explicitly allowed

## Public vs internal surface

- `orchestrator` is public
- `investigator` is internal
- `implementer` is internal

Users should normally enter through `orchestrator`.

## Repo-local artifact model

## `.agents/system/`

Committed.

Contains:

- scaffold manifest/version markers
- local README
- schemas, policies, workflows, eval pointers
- repo-local overlays and overrides

Written by:

- bootstrap/setup flow
- deliberate upgrade/setup operations
- humans making explicit repo-level changes

## `.agents/state/`

Gitignored runtime state.

Contains:

- task index
- task directories
- active views
- event history
- compact transcripts
- archive material

Written by:

- the `orchestrator` at runtime

## `.agents/knowledge/`

Committed curated knowledge, scoped narrowly to **orchestration-process** facts: which workflow tends to fit which request shape in this repo, model-routing outcomes, budget-mode tuning, and delegation heuristics that are specific to running this orchestration system in this repo.

Written by:

- humans or explicit curation flows
- approved knowledge-promotion flows where the git diff is the review gate
- not by ordinary runtime task execution in v1

### Relationship to Serena memories

Codebase and architecture knowledge — conventions, build/test setup, module ownership, hazards, and validation rules that live in the *product code* rather than the orchestration process — belongs in Serena's project memories (`.serena/memories/**`), not in `.agents/knowledge/**`.

Rule of thumb before writing a promotion candidate:

- "this is a fact about the codebase" (e.g. "auth module owns session refresh", "run `pnpm test:auth` for auth changes") → propose it as a Serena memory update
- "this is a fact about how to run orchestration in this repo" (e.g. "feature-decomposition workflow underperforms here, prefer specify→decompose→execute with a smaller slice size") → propose it for `.agents/knowledge/**`

Do not duplicate the same fact in both places. If Serena memories already exist and are current, prefer reading them over re-deriving the same knowledge through fresh investigation.

## Memory architecture

The memory model is task-centric.

Each persisted task consists of:

- an append-mostly graph of task history
- a compact active materialized view
- a closure/checkpoint record when paused or terminal

Key rules:

- canonical memory is owned by the `orchestrator`
- sub-agents return deltas, not direct state mutations
- history is append-mostly, using supersession rather than silent rewrite
- summaries and indexes may be rewritten as derived state

The active view keeps the hot working set small:

- objective
- constraints
- active clusters
- top hypotheses
- latest decisions
- latest validations
- blockers
- rejected-path summaries
- workflow and budget working fields

## Task model

Tasks are created lazily, once work becomes non-trivial.

Typical triggers:

- clarification loop begins
- reconnaissance goes beyond the lightest layer
- a sub-agent packet is dispatched
- a workflow/skill is selected
- the task is likely to span multiple turns

Lifecycle states:

- `active`
- `blocked`
- `paused`
- `completed`
- `abandoned`
- `superseded`

Every paused or terminal task gets a closure/checkpoint record.

The system defaults to a new task unless evidence strongly supports resume or fork.

## Workflow model

The orchestrator works from an explicit workflow library with override only when justified.

Initial workflow families:

- clarify → plan
- inspect → gather → decide
- diagnose → cluster → fix → validate
- specify → decompose → execute
- tdd loop
- review/audit loop
- prototype/version loop

This keeps orchestration predictable and easier to evaluate.

## Skill integration model

Approved skills are advisors only.

They may produce:

- refinements
- plans
- decompositions
- structured findings

They may not:

- mutate canonical task memory directly
- override lifecycle or packet invariants

The `orchestrator` translates their output into:

- canonical memory updates
- workflow choices
- bounded task packets

## Validation model

Validation is two-tiered.

### Implementer

Performs local targeted validation:

- affected tests
- narrow lint/type checks
- immediate regression sanity

### Investigator

Performs independent affected-surface validation:

- repro checks
- broader local surface checks
- contradiction reporting

Default validation is affected-surface, not repo-wide. Broader validation is used when blast radius or risk increases.

## Parallelism model

### Investigator

Parallelism is allowed only for clearly independent branches, with a small cap.

### Implementer

Parallelism is forbidden in v1.

This keeps edit conflict and memory-merge complexity low.

## Risk and execution policy

Command execution follows risk tiers.

- Tier 0: read-only / validation-safe — allowed by default in scope
- Tier 1: low-risk local side effects — only with explicit packet authorization
- Tier 2: tracked workspace or environment mutation — explicit user approval
- Tier 3: destructive or external actions — out of scope by default

This policy applies to both `investigator` and `implementer`.

## Repo customization model

Repo-local customization should live in overlay/config files, not bespoke prompt edits.

Examples:

- `repo-policy.json`
- `workflow-overrides.json`
- `skill-overrides.json`

Overlays may tune:

- workflow availability
- thresholds
- budget defaults
- repo-specific heuristics

They may not override:

- canonical packet invariants
- canonical memory ownership
- lifecycle semantics
- the v1 ban on parallel implementers

## Versioning and updates

Repo-local scaffold versioning lives in the manifest.

Bootstrap/update behavior is conservative:

- install missing scaffold
- repair partial scaffold
- warn on outdated scaffold
- preserve overlays
- do not silently overwrite curated artifacts

## v1 constraints

Not supported in v1:

- same-task merge/reconciliation across concurrent orchestrators
- parallel implementers
- fully supported non-git mode
- automatic promotion into shared knowledge
- full executable replay harness
- arbitrary graph expansion beyond defined node and edge vocabularies

## Design priorities

Priority order:

1. correctness and task success
2. memory coherence and scope discipline
3. token efficiency
4. autonomy and speed
5. convenience features
