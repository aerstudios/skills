# Orchestration Workflows

Status: non-normative reference.

The public `orchestrator` and `controller` agent prompts are the canonical owners of workflow definitions. This file is retained as background guidance and historical rationale.

<!-- markdownlint-disable MD024 -->

This document defines the default workflow library used by the `orchestrator`.

The goal is not to encode every possible path. The goal is to give the `orchestrator` a small set of repeatable, inspectable workflow shapes so it does not improvise its process from scratch on every task.

## Workflow selection principles

Choose the cheapest workflow that can plausibly achieve the objective without sacrificing correctness.

Selection is based on:

- request ambiguity
- need for repo inspection
- expected blast radius
- whether the task is diagnostic, implementation, review, or planning
- whether existing memory or knowledge already narrows the problem
- whether a specialized advisor workflow would materially reduce uncertainty

The `orchestrator` may override the default workflow choice when:

- the repo shape makes a different path clearly cheaper
- a previous workflow has already failed
- a user explicitly requests another mode
- local overrides/policies require it

## Shared workflow rules

All workflows must respect these rules:

- canonical memory is owned by the `orchestrator`
- `investigator` and `implementer` receive bounded task packets only
- advisor skills are advisors, not canonical state mutators
- task state is persisted after meaningful state changes
- clarification is used only when inspection cannot cheaply resolve the uncertainty and the answer would materially change the plan, artifact, or validation strategy
- default validation is affected-surface, not repo-wide
- no more than 2 fix/validate loops per cluster before escalation
- durable team-useful discoveries are promoted automatically into `.agents/knowledge/**` when stable enough; useful but unstable discoveries remain promotion candidates in closure

## Workflow 1: clarify → plan

### Use when

- objective is ambiguous
- acceptance criteria are missing
- constraints conflict
- there are multiple materially different solution classes
- success depends on product intent, not just code facts

### Typical steps

1. create or open task state if the work is non-trivial
2. capture initial objective, uncertainty, and constraints
3. perform stage-0 or stage-1 reconnaissance only if it may reduce unnecessary questions
4. ask a constrained clarification question, usually with a recommended option
5. optionally use `grill-me` or `grill-with-docs` as an advisor
6. normalize clarified intent into objective, acceptance criteria, constraints, and likely workflow choice
7. transition into a more specific workflow

### Stop / escalate conditions

- user cannot clarify and repo inspection also cannot decide
- architectural choice remains unresolved
- constraints remain internally inconsistent

## Workflow 2: inspect → gather → decide

### Use when

- the request likely can be scoped by repo inspection
- the task is bounded but the exact affected area is not yet known
- a small amount of inspection can avoid useless clarification

### Typical steps

1. perform layered reconnaissance
2. consult relevant repo knowledge entries if available
3. if uncertainty remains and evidence requires execution, delegate a bounded `investigator` packet
4. collect findings into evidence, candidate scope, and initial blast radius
5. choose the cheapest next workflow

## Workflow 3: diagnose → cluster → fix → validate

### Use when

- the user reports a bug, regression, failure, or unclear incorrect behavior
- the cause is not yet known
- the task likely needs evidence before implementation

### Typical steps

1. define or restate repro/acceptance target
2. delegate bounded `investigator` packets to gather evidence
3. cluster findings by likely shared cause or dependency
4. decide whether confidence is sufficient for implementation
5. if yes, issue a bounded `implementer` packet for one cluster
6. implementer performs local targeted validation
7. delegate independent affected-surface validation to `investigator`
8. if validation fails, either retry once with a tighter packet or return to diagnosis
9. if validation passes, close the cluster

## Workflow 4: specify → decompose → execute

### Use when

- the task is a feature or enhancement rather than a bug
- the request is reasonably clear but too large for one implementation packet
- decomposition is needed before coding

### Typical steps

1. confirm or refine objective and constraints
2. inspect enough of the repo to understand affected surfaces
3. optionally use `to-prd` or `to-issues`
4. normalize output into acceptance criteria, slices, and likely order of work
5. create child task/task links as needed
6. execute slices through `investigator` and `implementer`

## Workflow 5: tdd loop

### Use when

- bounded implementation is well-suited to test-first work
- a reliable local failing test can be added cheaply
- stronger implementation discipline is desired

### Typical steps

1. decide whether a failing test is practical and useful
2. optionally use `tdd` as an advisor
3. issue an `implementer` packet with explicit test-first constraints
4. require failing test first, minimal implementation, and targeted validation
5. perform independent `investigator` validation

## Workflow 6: review / audit loop

### Use when

- the user wants review rather than implementation
- there is an existing change set or branch to inspect
- standards/spec alignment matters more than immediate code changes

### Typical steps

1. determine review scope and base reference
2. inspect relevant repo standards/docs/specs
3. optionally use `review` as an advisor
4. gather and cluster findings
5. return review output or convert selected findings into execution tasks

## Workflow 7: prototype / version loop

### Use when

- the user wants to explore alternatives
- the work is intentionally throwaway or branchy
- versions/variants need explicit lineage

### Typical steps

1. define prototype objective and evaluation criteria
2. create version/task lineage in memory
3. choose lightweight path
4. use `prototype` as an advisor if helpful
5. treat each alternative as a bounded version branch
6. validate each branch against explicit criteria
7. supersede or abandon branches explicitly

## Reconnaissance ladder

- Stage 0: structural scan
- Stage 1: targeted inspection
- Stage 2: focused investigator pass
- Stage 3: deeper branch-specific investigation

Proceed autonomously unless a user answer would materially reduce search cost or resolve intent ambiguity.

## Clarification pattern

Default clarification questions should be:

- constrained-choice
- 2–4 options
- with a recommended option
- with one-line consequences
- with an “other / inspect further” escape hatch

Ask only when at least two plausible solution paths remain after cheap inspection.

## Recovery pattern

If workflow execution degrades:

1. normalize trivial formatting issues
2. retry once with a tighter packet
3. choose a better-fit workflow
4. escalate to the user when confidence, scope, or budget no longer justify autonomy

## v1 workflow constraints

- implementer parallelism is forbidden
- same-task concurrent orchestration is unsupported
- repo-wide validation is opt-in by risk, not default
- workflows may consult overlays, but overlays cannot break core invariants

<!-- markdownlint-enable MD024 -->
