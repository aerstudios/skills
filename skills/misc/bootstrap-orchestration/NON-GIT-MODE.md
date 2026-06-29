# Non-Git Mode

Non-git scaffolding is best-effort only in v1.

## Root rule

If no enclosing git root exists:

1. use the current working directory as the candidate root
2. explain that repo-scoped behavior will be weaker outside git
3. ask before creating `.agents/` in that directory

## Expectations

In non-git mode:

- local scaffold creation is still allowed with confirmation
- runtime state still belongs under `.agents/state/`
- committed-vs-ignored semantics are weaker because there is no repo index
- resume/fork lineage is still local to that directory

## Recommendation

Prefer using the orchestration system inside a git repo. Use non-git mode for experiments or one-off work only.
