# Task Packet Schema

This document defines the bounded task packets used by the `orchestrator` to delegate work to `investigator` and `implementer`.

The packet model exists to:

- keep delegation small and explicit
- prevent sub-agent scope drift
- reduce repeated interpretation of the original user request
- make sub-agent outputs easier to normalize into canonical memory
- support budget-aware orchestration

## Design principles

Task packets should be:

- bounded
- outcome-oriented
- cheap to generate
- easy to validate
- role-aware
- small enough to fit budget targets without losing necessary constraints

The default unit is a small outcome-based task, not a micromanaged atomic instruction.

## Base packet schema

Every packet should include:

- `taskId`
- `parentTaskId`
- `clusterId`
- `mode`
- `objective`
- `scope`
- `constraints`
- `acceptanceCriteria`
- `relevantContext`
- `budgetMode`
- `maxRiskTier`
- `authorizedCommandsOrPatterns`
- `sideEffectsAllowed`
- `userApprovalReference`
- `knowledgePromotionAllowed`
- `requiredOutputSchema`

### Modes

- `gather`
- `fix`
- `validate`
- `clarify-support`
- `maintenance`

### Authorization fields

Command-running packets must be explicit enough for a small model to follow literally.

- `maxRiskTier`: highest allowed execution tier, from `0` to `3`
- `authorizedCommandsOrPatterns`: exact commands or narrow command patterns the sub-agent may run; use an empty list when no command execution is allowed
- `sideEffectsAllowed`: whether the packet permits local side effects
- `userApprovalReference`: short note proving approval for repo-visible mutation, or `null` when not applicable
- `knowledgePromotionAllowed`: whether the agent may write committed `.agents/knowledge/**` entries, normally `false`

If a needed command or mutation is not covered by these fields, the sub-agent must checkpoint instead of inferring permission from prose.

## Investigator packet extensions

`investigator` packets may add:

- `commandsOrSearchTargets`
- `evidenceQuestions`

## Implementer packet extensions

`implementer` packets may add:

- `targetFilesOrSymbols`
- `changeConstraints`
- `validationPlan`

## Output schema expectations

Sub-agent outputs are schema-first but tolerant.

All sub-agent responses should use this shared envelope:

- `taskId`
- `status`: `completed`, `checkpoint`, `blocked`, or `failed`
- `confidence`: `low`, `medium`, or `high`
- `summary`
- `rolePayload`: role-specific findings, changes, or validation detail
- `memoryDelta`
- `blockers`
- `nextAction`
- `compressionNote`
- `budgetStatus`

Sub-agent memory deltas may also include `OperationalFacts` for environment and tooling discoveries that affect future command choice.

If a sub-agent discovers durable team-useful knowledge, it should return that as a memory delta or promotion candidate. The `orchestrator` records promotion candidates in task state or closure. It writes committed `.agents/knowledge/**` entries only during an explicit curation/update flow or when `knowledgePromotionAllowed` is true.

## Packet sizing guidance

Budget modes:

- `micro`
- `lean`
- `standard`
- `deep`

Default interpretation:

- `micro`: trivial or one-file/symbol work; usually no persistent task state
- `lean`: small repo inspection, one bounded change or validation
- `standard`: multi-step work that needs task state, delegation, or independent validation
- `deep`: ambiguous architecture, multi-slice work, repeated failure, or high blast radius

Use the lightest mode compatible with correctness. `deep` is not a license to dump the full conversation into the packet.

## Scope discipline rules

Good packets specify:

- named files/symbols or narrow subsystem scope
- explicit constraints
- concrete acceptance criteria
- clear out-of-scope boundaries

If the true required scope is broader than the packet, the sub-agent should checkpoint rather than stretching the packet silently.

## Checkpoint policy

Sub-agents should checkpoint when:

- scope breach triggers fire
- contradictory evidence suggests the wrong workflow
- required command risk tier exceeds authorization
- the packet is missing critical information
- blast radius appears much higher than expected

Checkpoint responses should stay small and decision-oriented.

## User request handling

Sub-agents should not receive the full raw user request by default.

Instead they receive:

- normalized objective
- bounded scope
- relevant context slice
- acceptance criteria
- constraints

A short excerpt of original user wording may be included when product nuance matters.

## Relationship to memory

Packets are scoped instructions derived from canonical memory. They are not canonical memory themselves.

When relevant, the `orchestrator` may include a small slice of current `OperationalFacts` in the relevant context so sub-agents avoid retrying tools that have already failed in the same task/environment.
