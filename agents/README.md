# Runtime Agents

These agent prompts are the installed runtime surface for the orchestration system.

They exist alongside the reusable skills, but serve a different purpose:

- `orchestrator.agent.md` — public entry point for the full custom multi-agent runtime
- `controller.agent.md` — public entry point for the thinner harness-cooperative runtime
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

## Runtime modes

### `orchestrator.agent.md`
Use this when you want the full custom multi-agent runtime.

Characteristics:

- explicit runtime roles
- custom `investigator` and `implementer`
- portable across harnesses
- strongest fit for environments where custom sub-agents can be routed independently
- best when explicit role separation matters more than harness-native optimization

### `controller.agent.md`
Use this when you want a thinner harness-cooperative runtime.

Characteristics:

- one public controller
- same repo-owned task memory, bootstrap, workflow discipline, and operational learning
- bounded briefs instead of relying on explicit custom runtime `investigator` / `implementer` threads
- better fit for harnesses where native subthreads/subagents outperform custom agent routing

## Shared foundation

Both modes share the same core value layer:

- deterministic bootstrap
- repo-local task memory
- `OperationalFacts`
- workflow contracts
- bounded task shaping
- compaction discipline
- eval-oriented design

The difference is not in the memory or process model. The difference is in how much runtime work is delegated to the harness itself.

## Which one should I use?

Use:

- **`orchestrator`** for the fuller custom system
- **`controller`** for the thinner harness-cooperative system

If you are unsure, start with the mode that best matches the harness behavior you actually observe, not the one with the more elegant theory.

## Further reading

- [Orchestrator Agent](orchestrator.agent.md)
- [Controller Agent](controller.agent.md)
- [Investigator Agent](investigator.agent.md)
- [Implementer Agent](implementer.agent.md)
- [Anthropics Orchestration System](https://docs.anthropic.com/claude/docs/orchestration)
- [When you use MAS and when you don't](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)
