# Runtime Agents

These agent prompts are the installed runtime surface for the orchestration system.

They exist alongside the reusable skills, but serve a different purpose:

- `orchestrator.agent.md` — public entry point for repo-scoped orchestration
- `investigator.agent.md` — internal evidence and validation agent
- `implementer.agent.md` — internal bounded implementation agent

## Why this orchestration layer exists

Most coding harnesses already provide some mix of memory, workflows, tool use, and model switching. This system exists because those features are often harness-specific, opaque, and hard to govern at the repo level.

This orchestration layer makes the workflow **repo-owned**.

It provides:

- **explicit task memory** instead of hidden conversational residue
- **explicit workflow contracts** instead of ad hoc process
- **bounded roles** for orchestration, investigation, and implementation
- **deterministic bootstrap/setup** for repo-local state
- **inspectable artifacts** humans can review and evolve
- **portable process logic** that is less tied to one harness or provider

In short:

> This system is not mainly about doing more than the harness.  
> It is about **owning the orchestration logic ourselves**.

## Practical token usage

This system is designed to be **token-aware**, but not token-obsessed.

Priority order:

1. correctness
2. memory coherence
3. token efficiency

The biggest token savings come from:

- **bounded task packets** instead of passing full conversation history
- **active-view compaction** instead of replaying all prior context
- **role separation** between orchestration, evidence gathering, and implementation
- **operational learning** that avoids repeating failed command choices
- **workflow discipline** that reduces pointless retries and unnecessary clarification

This system does add some overhead through:

- packet generation
- memory updates
- workflow selection
- explicit validation loops

That overhead is intentional. The goal is not to make every task cheaper in raw tokens, especially trivial ones. The goal is to make token spend **more controlled, inspectable, and reusable** over multi-turn work and shareable with the team.

## Further reading

- [Orchestrator Agent](orchestrator.agent.md)
- [Investigator Agent](investigator.agent.md)
- [Implementer Agent](implementer.agent.md)
- [Anthropics Orchestration System](https://docs.anthropic.com/claude/docs/orchestration)
- [When you use MAS and when you don't](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)
