---
name: orchestration-system
description: Set up, inspect, or govern a repo-scoped multi-agent orchestration system with an orchestrator, internal sub-agents, bounded task packets, and repo-local task memory. Use when designing or upgrading orchestrated engineering workflows, repo scaffolding, task memory, or delegation contracts.
---

This skill defines a reusable orchestration system for repo-scoped engineering work. It governs the relationship between the public `orchestrator`, the internal `investigator` and `implementer`, and the repo-local `.agents/` artifacts they rely on.

Use this skill when:

- the user wants to set up the orchestration system in a repo
- the user wants to inspect or upgrade an existing orchestration scaffold
- the user wants to understand how task memory, delegation, and workflows are structured
- the user wants to align agent prompts with the orchestration architecture

Do not use this skill when:

- the task is ordinary coding work inside a repo that already has a working orchestration setup
- the user only wants a one-off implementation or bug fix with no orchestration-system changes

## Workflow

1. Identify the target repo root.
2. Inspect the existing orchestration scaffold and version markers.
3. If the scaffold is missing or partial, invoke the bootstrap workflow.
4. Consult the architecture and runtime contract docs before changing behavior.
5. Apply or explain repo-local conventions, overlays, and invariants.
6. Stop before mutating committed shared artifacts without confirmation.

## Source documents

- [ARCHITECTURE.md](./ARCHITECTURE.md)
- [RUNTIME-CONTRACT.md](./RUNTIME-CONTRACT.md)
- [WORKFLOWS.md](./WORKFLOWS.md)
- [PACKET-SCHEMA.md](./PACKET-SCHEMA.md)
- [TASK-STATE-SCHEMA.md](./TASK-STATE-SCHEMA.md)

## Invariants

- The `orchestrator` owns canonical task memory.
- `investigator` and `implementer` are internal sub-agents.
- Task state is repo-local and task-centric.
- `.agents/state/` is runtime-only and gitignored.
- Advisor skills refine work; they do not directly mutate canonical memory.
