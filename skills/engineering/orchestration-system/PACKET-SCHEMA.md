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
- `requiredOutputSchema`

### Modes

- `gather`
- `fix`
- `validate`
- `clarify-support`

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

Required minimum fields for all responses:

- task ID
- status
- findings or changes
- confidence
- next action recommendation
- memory delta
- blockers
- compression note

Sub-agent memory deltas may also include `OperationalFacts` for environment and tooling discoveries that affect future command choice.

## Packet sizing guidance

Budget modes:

- `micro`
- `lean`
- `standard`
- `deep`

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
