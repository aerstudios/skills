# Compaction Policy

This document defines how the orchestration system keeps task memory small enough to be useful without losing the provenance needed for debugging, reuse, and safe decision-making.

The core idea is simple:

- keep the active working set small
- keep history available
- summarize aggressively
- delete canonical history only in exceptional administrative cases, not normal operation

## Core principles

### 1. Hot state should stay small

The `orchestrator` should only keep the minimum working set in the active view:

- current objective
- current constraints
- active clusters
- top active hypotheses
- latest decisions
- latest validations
- active blockers
- rejected-path summaries
- current workflow/budget fields
- a tiny hot set of current `OperationalFacts`

### 2. Canonical history is not prompt history

Canonical memory lives in task state:

- `active.json`
- `history.jsonl`
- `closure.json`
- `archive/`

Prompts should consume slices of this memory, not raw accumulated chat.

### 3. Prefer supersession over rewrite

If understanding changes:

- keep the old node/event in history
- create a newer node/event that supersedes it
- update active summaries to point to the current truth

### 4. Archive, don’t erase

Normal compaction should summarize and move material out of the hot path. It should not delete canonical historical records in normal operation.

## Memory layers

### Hot layer

Stored primarily in `active.json`.

Includes:

- active task status
- objective and constraints
- active clusters
- top hypotheses still under consideration
- latest relevant decisions
- latest validations
- active blockers
- workflow/budget working fields
- compact rejected-path summaries
- currently relevant operational facts and tool preferences

### Warm layer

Stored primarily in `history.jsonl` and graph/history references.

Includes:

- superseded hypotheses still explaining past decisions
- earlier validations relevant to current risk
- completed actions with residual relevance
- previous branch summaries still useful for resume/fork reasoning

### Cold layer

Stored primarily in `archive/`.

Includes:

- closed clusters
- superseded prototype/version branches
- archived negative paths with full details
- compacted snapshots

## Compaction triggers

Compaction should be both event-driven and threshold-driven.

### Event-driven

Run compaction:

- before every delegation
- after every sub-agent or advisor delta merge
- when closing a cluster
- when pausing/completing/abandoning/superseding a task
- when forking a task or creating a version branch
- before generating a long user-facing summary

### Threshold-driven

Run extra compaction when:

- active view exceeds its target size
- hot node count exceeds threshold
- too many stale superseded nodes remain hot
- repeated evidence/hypothesis duplication is detected
- transcript summary is growing too noisy
- too many operational facts accumulate in the hot set

## Rejected-path policy

Failed hypotheses and abandoned prototypes are valuable.

Keep them as explicit archived negatives, but compress them in the active view.

Examples of hot summaries:

- `cache invalidation race disproved by val_007`
- `prototype B failed SSR compatibility`
- `broad refactor path rejected due to API stability constraint`

## What compaction must not do

It must not:

- silently delete canonical history
- erase why a decision was made
- drop unresolved blockers
- remove the only link between a hot summary and its provenance
- rewrite user intent history into something stronger than what was actually decided

## Active view size discipline

Prefer:

- IDs over raw copied text
- canonical fact summaries over repeated logs
- latest decision summaries over historical narration
- one-line rejected-path summaries over detailed negative branches
- one-line operational facts over repeated command failure narration

Avoid:

- long prose summaries of everything so far
- multiple versions of the same hypothesis
- repeated restatement of unchanged constraints
- embedding raw skill transcripts
- carrying full validation logs hot
- repeated command failure details once an operational fact has been recorded

## Compaction and delegation

Compaction should run before every packet is emitted.

Delegate from:

- current objective
- minimal relevant context slice
- latest relevant decisions
- relevant rejected-path summary
- relevant operational facts for the current environment
- required constraints
- budget mode

Keep the active operational-fact set small: dedupe by tool + status + environment fingerprint, and keep at most a handful of currently relevant entries hot in normal operation.

Do not delegate from stale or un-compacted state.
