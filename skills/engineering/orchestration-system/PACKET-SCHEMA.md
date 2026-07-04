# Task Packet Schema

This document defines bounded task packets used by the `orchestrator` to delegate work to `investigator` and `implementer`.

## Packet aim

Each packet should be a small, outcome-oriented instruction that:

- constrains scope and risk
- makes authorization explicit
- gives enough context to execute safely
- produces output that is easy to merge into canonical task memory

Use the lightest packet that can still succeed safely.

## Canonical packet JSON

```json
{
    "taskId": "tsk_042",
    "parentTaskId": "tsk_041",
    "clusterId": "cluster_bootstrap",
    "mode": "maintenance",
    "objective": "Verify and, if approved, repair missing orchestration scaffold",
    "scope": {
        "paths": [".agents/**", ".gitignore"],
        "outOfScope": ["product code", "tests", "build config"]
    },
    "constraints": [
        "No product-code edits",
        "Prefer deterministic bootstrap script"
    ],
    "acceptanceCriteria": [
        "Check result recorded",
        "Apply only with explicit approval"
    ],
    "relevantContext": [
        "Repo root resolved to nearest git root",
        "Previous check reported missing .agents/system"
    ],
    "budgetMode": "lean",
    "maxRiskTier": 2,
    "authorizedCommandsOrPatterns": [
        "python ~/.agents/skills/bootstrap-orchestration/bootstrap_orchestration.py --root <target-root> --mode check",
        "python ~/.agents/skills/bootstrap-orchestration/bootstrap_orchestration.py --root <target-root> --mode apply"
    ],
    "sideEffectsAllowed": true,
    "userApprovalReference": "User approved apply in current turn",
    "knowledgePromotionAllowed": false,
    "requiredOutputSchema": "shared-response-envelope-v1"
}
```

## Field reference

- `taskId`: current task identifier.
- `parentTaskId`: parent task if this packet is part of a branch; otherwise `null`.
- `clusterId`: logical work cluster within the task.
- `mode`: one of `gather`, `fix`, `validate`, `clarify-support`, `maintenance`.
- `objective`: single-sentence desired outcome.
- `scope`: allowed target area plus explicit out-of-scope boundaries.
- `constraints`: non-negotiable rules for this packet.
- `acceptanceCriteria`: concrete pass conditions.
- `relevantContext`: minimal context slice needed for execution.
- `budgetMode`: one of `micro`, `lean`, `standard`, `deep`.
- `maxRiskTier`: highest allowed risk tier (`0` to `3`).
- `authorizedCommandsOrPatterns`: exact commands or narrow patterns allowed.
- `sideEffectsAllowed`: whether local side effects are allowed.
- `userApprovalReference`: proof of approval for repo-visible mutation, or `null`.
- `knowledgePromotionAllowed`: whether committed `.agents/knowledge/**` writes are allowed.
- `requiredOutputSchema`: required response envelope identifier.

## Authorization rules

If a required command or mutation is not explicitly covered by `maxRiskTier`, `authorizedCommandsOrPatterns`, `sideEffectsAllowed`, and `userApprovalReference`, the sub-agent must `checkpoint`.

Bootstrap rules:

- `check` can run as tier 0 when in scope.
- `apply` is tier 2 and requires explicit approval unless the user directly requested bootstrap/repair.

## Role extensions

Investigator packet extensions:

- `commandsOrSearchTargets`
- `evidenceQuestions`

Implementer packet extensions:

- `targetFilesOrSymbols`
- `changeConstraints`
- `validationPlan`

## Required sub-agent output envelope

All sub-agent responses should return:

```json
{
    "taskId": "tsk_042",
    "status": "completed",
    "confidence": "high",
    "summary": "Checked scaffold and prepared apply decision",
    "rolePayload": {},
    "memoryDelta": {},
    "blockers": [],
    "nextAction": "Ask for apply approval",
    "compressionNote": "No extra context required",
    "budgetStatus": "within-budget"
}
```

Allowed enums:

- `status`: `completed`, `checkpoint`, `blocked`, `failed`
- `confidence`: `low`, `medium`, `high`

`memoryDelta` may include `OperationalFacts` and promotion candidates.

## Budget guidance

- `micro`: trivial one-file/symbol work; usually no persistent task state.
- `lean`: small inspection, one bounded change or validation.
- `standard`: multi-step work requiring delegation and independent validation.
- `deep`: ambiguous or high-blast-radius work.

`deep` is not permission to pass full conversation history.

## Scope and checkpoint guidance

Good packets specify named targets, explicit constraints, concrete acceptance criteria, and clear out-of-scope boundaries.

Sub-agents should `checkpoint` when:

- true scope exceeds authorized scope
- required risk tier exceeds authorization
- packet is missing critical information
- contradictory evidence suggests wrong workflow
- blast radius is materially higher than expected

## Relationship to memory

Packets are scoped instructions derived from canonical memory; they are not canonical memory.

Include only the smallest relevant context slice, including current `OperationalFacts` when needed to avoid repeating failed command choices.
