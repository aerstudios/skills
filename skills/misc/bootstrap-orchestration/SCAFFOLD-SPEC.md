# Bootstrap Orchestration Scaffold Spec

## 1. Root resolution

The bootstrap target root is determined in this order:

1. nearest enclosing git root from the current working directory
2. if no git root exists, use the current working directory as the candidate root
3. ask before creating repo-local orchestration artifacts in a non-git directory

Non-git scaffolding is best-effort only in v1.

## 2. Required directories

Bootstrap must ensure these directories exist:

- `.agents/`
- `.agents/system/`
- `.agents/system/schemas/`
- `.agents/system/workflows/`
- `.agents/system/policies/`
- `.agents/system/evals/`
- `.agents/state/`
- `.agents/state/tasks/`
- `.agents/knowledge/`
- `.agents/knowledge/entries/`

## 3. Required minimal files

Bootstrap must ensure these files exist:

- `.agents/system/manifest.json`
- `.agents/system/README.md`
- `.agents/knowledge/index.json`
- `.agents/state/index.json`

It may create missing parent directories automatically.

## 4. Gitignore requirements

Bootstrap must ensure runtime state is ignored via a managed block:

```gitignore
# BEGIN agents-orchestration
.agents/state/
# END agents-orchestration
```

Rules:

- if `.gitignore` does not exist, create it
- if the managed block exists, update it in place
- if an equivalent ignore already exists elsewhere, still add or maintain the managed block and report the redundancy as a warning
- do not disturb unrelated user-managed ignore rules

## 5. Minimal stub contents

## `.agents/system/manifest.json`

Minimum fields:

- `systemVersion`
- `sourceSkill`
- `generatedAt`
- `components`

Example shape:

```json
{
  "systemVersion": "0.1.0",
  "sourceSkill": "bootstrap-orchestration",
  "generatedAt": "2026-06-24T00:00:00Z",
  "components": ["system", "state", "knowledge"]
}
```

## `.agents/system/README.md`

Should briefly explain:

- what this scaffold is
- what lives in `.agents/system/`
- what lives in `.agents/state/`
- what lives in `.agents/knowledge/`
- which parts are committed vs ignored
- where canonical architecture docs live

Keep it short.

## `.agents/knowledge/index.json`

Minimum fields:

- `version`
- `entries`

Example shape:

```json
{
  "version": 1,
  "entries": []
}
```

## `.agents/state/index.json`

Minimum fields:

- `version`
- `nextTaskSequence`
- `tasksByStatus`
- `activeLocks`

Example shape:

```json
{
  "version": 1,
  "nextTaskSequence": 1,
  "tasksByStatus": {
    "active": [],
    "blocked": [],
    "paused": [],
    "completed": [],
    "abandoned": [],
    "superseded": []
  },
  "activeLocks": []
}
```

## 6. Non-goals

Bootstrap does not create:

- full workflow libraries
- sample task state
- knowledge entries
- task transcripts
- heavy templates
- product-code changes

Bootstrap should not attempt to infer repo-specific conventions beyond the scaffold contract.

## 7. Idempotence expectations

Rerunning bootstrap should be safe.

Expected behavior:

- do not duplicate directories or managed ignore blocks
- fill in missing required pieces
- preserve existing valid files
- preserve differing existing stub files and report warnings instead of overwriting them in v1
- report which pieces already existed
- ask before overwriting, renaming, or migrating existing curated content
