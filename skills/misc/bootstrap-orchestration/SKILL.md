---
name: bootstrap-orchestration
description: Install, repair, or conservatively update the minimal repo-local .agents scaffold required by the orchestration system. Use when a repo needs orchestration folders, gitignore rules, manifest/index stubs, or scaffold repair.
---

This skill installs or repairs the minimal repo-local scaffold required by the orchestration system.

The deterministic implementation lives in `bootstrap_orchestration.py` beside this skill. The agent should use that script for scaffold checks and mutations instead of reimplementing file creation ad hoc.

Use this skill when:

- a repo lacks the required `.agents/` layout
- the scaffold is partial or outdated
- `.gitignore` is missing the runtime-state ignore rule
- the user wants to initialize orchestration support in a repo

Do not use this skill when:

- normal runtime task orchestration is already proceeding in a healthy scaffolded repo
- the user wants to redesign the orchestration architecture rather than scaffold it

## Bootstrap contract

- Create the minimal scaffold only.
- Repair conservatively in place.
- Do not overwrite curated files without confirmation.
- If no git root exists, use the invocation directory as the candidate root and ask before writing.
- Runtime state must remain gitignored.

## Workflow

1. Find the target root.
2. Run the deterministic script in check mode:
   - `python ~/.agents/skills/bootstrap-orchestration/bootstrap_orchestration.py --root <target-root> --mode check`
3. Classify the result as missing, partial, current, or outdated.
4. Ask when repo-visible mutation is needed.
5. If mutation is approved, run the deterministic script in apply mode:
   - `python ~/.agents/skills/bootstrap-orchestration/bootstrap_orchestration.py --root <target-root> --mode apply`
6. Report exactly what changed and what did not from the JSON result.

Do not hand-write scaffold files when the script can perform the operation.

## Supporting docs

- [SCAFFOLD-SPEC.md](./SCAFFOLD-SPEC.md)
- [UPDATE-POLICY.md](./UPDATE-POLICY.md)
- [NON-GIT-MODE.md](./NON-GIT-MODE.md)

## Script contract

- JSON is the default and only output mode in v1.
- `--mode check` must not mutate the target root.
- `--mode apply` creates or repairs the scaffold conservatively.
- Existing differing stub files are preserved and reported as warnings.
- The managed `.gitignore` block for `.agents/state/` is always maintained by the script.
