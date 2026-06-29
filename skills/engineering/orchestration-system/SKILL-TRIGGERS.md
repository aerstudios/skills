# Advisor Skill Triggers

This document defines which skills the `orchestrator` may use as advisors, when it should use them, and how their output must be handled.

The goal is to keep the `orchestrator` broadly capable without turning it into a bag of ad hoc prompt hops.

## Core rule

Advisor skills are advisors only.

They may:

- refine objectives
- expose ambiguity
- suggest decomposition
- provide process discipline
- produce structured findings or artifacts

They may not:

- directly mutate canonical task memory
- replace the `orchestrator` as workflow owner
- redefine task lifecycle semantics
- broaden scope without an explicit orchestrator decision

All advisor outputs must be translated by the `orchestrator` into:

- canonical memory updates
- workflow transitions
- bounded task packets
- user-facing decisions or clarification questions

## Approved v1 advisor set

### Clarification
- `grill-me`
- `grill-with-docs` when repo language/docs materially matter

### Diagnosis
- `diagnose`

### Specification / decomposition
- `to-prd`
- `to-issues`

### Implementation discipline
- `tdd`

### Review / quality
- `review`

### Specialist guidance
Only when domain-triggered, for example:

- accessibility
- architect-css
- typescript-magician
- modern-web-guidance where required by repo policy and task type

## Trigger: `grill-me`

Use when:

- objective is ambiguous
- acceptance criteria are weak or missing
- constraints conflict
- multiple solution classes exist with materially different costs
- success depends on user intent rather than code facts

Do not use when:

- quick repo inspection can answer the question
- the task is already narrowly scoped and reversible
- the uncertainty is about code facts, not intent

## Trigger: `diagnose`

Use when:

- a bug, regression, or failure exists
- the cause is unclear
- a disciplined reproduce → minimize → hypothesize → instrument loop is likely useful

Do not use when:

- the cause is already clear enough for a bounded implementation
- the task is primarily feature work rather than diagnosis
- the issue can be closed with trivial inspection

## Trigger: `to-prd`

Use when:

- the user wants a feature or broader change
- intent is mostly clear
- acceptance criteria and scope need formalization
- implementation should follow a durable spec rather than direct improvisation

## Trigger: `to-issues`

Use when:

- a plan/spec already exists
- work needs decomposition into independent slices
- the orchestrator needs bounded execution units

## Trigger: `tdd`

Use when:

- a bounded implementation slice has a practical test-first path
- a failing test can be created cheaply
- stronger implementation discipline is worth the added cost

## Trigger: `review`

Use when:

- the task is evaluative rather than generative
- a change set exists and needs standards/spec review
- the user asked for review or audit

## Skill cost discipline

The `orchestrator` should prefer:

1. direct resolution via existing memory or repo knowledge
2. light inspection
3. bounded `investigator` work
4. advisor skill invocation
5. user escalation

Skill invocation should not be the reflexive first move.

## Skill chaining rules

Skill chaining is allowed but should be rare and intentional.

Reasonable examples:

- `grill-me` → `to-prd`
- `diagnose` → `tdd`
- `to-prd` → `to-issues`

When chaining skills, summarize the artifact from the first skill before invoking the second. Do not pass raw sprawling transcripts as handoff.

## Repo-local overrides

Repo-local overlays may tune:

- whether a skill is enabled
- trigger thresholds
- whether a specialist skill is preferred in a specific subsystem

Repo-local overlays may not:

- allow a skill to mutate canonical memory directly
- bypass packet/memory invariants
- change the public/internal role split
- promote unrestricted skill use
