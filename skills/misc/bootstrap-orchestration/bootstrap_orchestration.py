#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MANAGED_BLOCK_START = "# BEGIN agents-orchestration"
MANAGED_BLOCK_END = "# END agents-orchestration"
MANAGED_BLOCK_LINES = [
    MANAGED_BLOCK_START,
    ".agents/state/",
    MANAGED_BLOCK_END,
]

STRUCTURAL_DIRS = [
    ".agents",
    ".agents/system",
    ".agents/system/schemas",
    ".agents/system/workflows",
    ".agents/system/policies",
    ".agents/system/evals",
    ".agents/state",
    ".agents/state/tasks",
    ".agents/knowledge",
    ".agents/knowledge/entries",
]


@dataclass
class BootstrapResult:
    ok: bool
    root: str
    mode: str
    gitRootDetected: bool
    scaffoldStateBefore: str
    scaffoldStateAfter: str
    changed: dict[str, Any]
    preserved: dict[str, Any]
    warnings: list[str]
    errors: list[str]

    def to_json(self) -> str:
        return json.dumps(
            {
                "ok": self.ok,
                "root": self.root,
                "mode": self.mode,
                "gitRootDetected": self.gitRootDetected,
                "scaffoldStateBefore": self.scaffoldStateBefore,
                "scaffoldStateAfter": self.scaffoldStateAfter,
                "changed": self.changed,
                "preserved": self.preserved,
                "warnings": self.warnings,
                "errors": self.errors,
            },
            indent=2,
        )


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_manifest() -> dict[str, Any]:
    return {
        "systemVersion": "0.1.0",
        "sourceSkill": "bootstrap-orchestration",
        "generatedAt": utc_now(),
        "components": ["system", "state", "knowledge"],
    }


def build_system_readme() -> str:
    return """# Orchestration Scaffold\n\nThis repo uses the orchestration-system scaffold.\n\n- `.agents/system/` holds committed system artifacts and repo overrides\n- `.agents/state/` holds gitignored runtime task state\n- `.agents/knowledge/` holds committed curated repo knowledge\n\nCanonical design docs live in the source skills repo and the installed orchestration-system skill.\n"""


def build_knowledge_index() -> dict[str, Any]:
    return {
        "version": 1,
        "entries": [],
    }


def build_state_index() -> dict[str, Any]:
    return {
        "version": 1,
        "nextTaskSequence": 1,
        "tasksByStatus": {
            "active": [],
            "blocked": [],
            "paused": [],
            "completed": [],
            "abandoned": [],
            "superseded": [],
        },
        "activeLocks": [],
    }


def normalize_json(obj: Any) -> str:
    return json.dumps(obj, indent=2, sort_keys=False) + "\n"


def required_files() -> dict[str, str]:
    return {
        ".agents/system/manifest.json": normalize_json(build_manifest()),
        ".agents/system/README.md": build_system_readme(),
        ".agents/knowledge/index.json": normalize_json(build_knowledge_index()),
        ".agents/state/index.json": normalize_json(build_state_index()),
    }


def find_git_root(root: Path) -> Path | None:
    current = root.resolve()
    while True:
        if (current / ".git").exists():
            return current
        if current.parent == current:
            return None
        current = current.parent


def classify_scaffold(root: Path, warnings: list[str]) -> str:
    required_dirs = [root / rel for rel in STRUCTURAL_DIRS]
    required_file_map = {root / rel: content for rel, content in required_files().items()}

    dir_exists = [p.exists() and p.is_dir() for p in required_dirs]
    file_exists = [p.exists() and p.is_file() for p in required_file_map]

    has_any = any(dir_exists) or any(file_exists) or (root / ".agents").exists()
    if not has_any:
        return "missing"

    missing_any = not all(dir_exists) or not all(file_exists)
    mismatched = False

    for path, expected in required_file_map.items():
        if path.exists() and path.is_file():
            try:
                actual = path.read_text(encoding="utf-8")
            except Exception:
                warnings.append(f"Could not read existing file for comparison: {path.relative_to(root)}")
                mismatched = True
                continue
            if path.name == "manifest.json":
                try:
                    parsed = json.loads(actual)
                except Exception:
                    warnings.append(f"Existing manifest is not valid JSON: {path.relative_to(root)}")
                    mismatched = True
                    continue
                if not isinstance(parsed, dict) or parsed.get("sourceSkill") != "bootstrap-orchestration":
                    warnings.append(f"Existing manifest differs from managed stub: {path.relative_to(root)}")
                    mismatched = True
            elif actual != expected:
                warnings.append(f"Existing file differs from managed stub: {path.relative_to(root)}")
                mismatched = True

    gitignore_state = inspect_gitignore(root)
    if not gitignore_state["has_managed_block"]:
        warnings.append("Managed .gitignore block for .agents/state/ is missing")
        missing_any = True
    elif gitignore_state["has_duplicate_equivalent"]:
        warnings.append("Equivalent .agents/state/ ignore exists outside managed block")

    if missing_any or mismatched:
        return "partial"
    return "current"


def inspect_gitignore(root: Path) -> dict[str, bool]:
    path = root / ".gitignore"
    if not path.exists() or not path.is_file():
        return {
            "has_managed_block": False,
            "has_duplicate_equivalent": False,
        }

    try:
        content = path.read_text(encoding="utf-8")
    except Exception:
        return {
            "has_managed_block": False,
            "has_duplicate_equivalent": False,
        }

    lines = content.splitlines()
    has_start = MANAGED_BLOCK_START in lines
    has_end = MANAGED_BLOCK_END in lines
    has_block = has_start and has_end and lines.index(MANAGED_BLOCK_START) < lines.index(MANAGED_BLOCK_END)

    duplicate = False
    for idx, line in enumerate(lines):
        if line.strip() != ".agents/state/":
            continue
        if has_block:
            start = lines.index(MANAGED_BLOCK_START)
            end = lines.index(MANAGED_BLOCK_END)
            if not (start < idx < end):
                duplicate = True
                break
        else:
            duplicate = True
            break

    return {
        "has_managed_block": has_block,
        "has_duplicate_equivalent": duplicate,
    }


def ensure_directory(root: Path, rel: str, changed: dict[str, Any], preserved: dict[str, Any], apply: bool) -> None:
    path = root / rel
    if path.exists() and path.is_dir():
        preserved["existingDirectories"].append(rel)
        return
    if apply:
        path.mkdir(parents=True, exist_ok=True)
    changed["createdDirectories"].append(rel)


def ensure_file(root: Path, rel: str, content: str, changed: dict[str, Any], preserved: dict[str, Any], warnings: list[str], apply: bool) -> None:
    path = root / rel
    if path.exists():
        if not path.is_file():
            warnings.append(f"Existing path is not a file, preserved: {rel}")
            preserved["existingFiles"].append(rel)
            return
        try:
            actual = path.read_text(encoding="utf-8")
        except Exception:
            warnings.append(f"Could not read existing file, preserved: {rel}")
            preserved["existingFiles"].append(rel)
            return
        if rel.endswith("manifest.json"):
            try:
                parsed = json.loads(actual)
            except Exception:
                warnings.append(f"Existing manifest differs and was preserved: {rel}")
                preserved["existingFiles"].append(rel)
                return
            if isinstance(parsed, dict) and parsed.get("sourceSkill") == "bootstrap-orchestration":
                preserved["existingFiles"].append(rel)
                return
            warnings.append(f"Existing manifest differs and was preserved: {rel}")
            preserved["existingFiles"].append(rel)
            return
        if actual == content:
            preserved["existingFiles"].append(rel)
            return
        warnings.append(f"Existing file differs and was preserved: {rel}")
        preserved["existingFiles"].append(rel)
        return

    if apply:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    changed["createdFiles"].append(rel)


def update_gitignore(root: Path, changed: dict[str, Any], warnings: list[str], apply: bool) -> None:
    path = root / ".gitignore"
    content = ""
    if path.exists():
        try:
            content = path.read_text(encoding="utf-8")
        except Exception:
            warnings.append("Could not read existing .gitignore; managed block not updated")
            return

    lines = content.splitlines()
    has_duplicate_equivalent = False
    for idx, line in enumerate(lines):
        if line.strip() != ".agents/state/":
            continue
        if MANAGED_BLOCK_START in lines and MANAGED_BLOCK_END in lines:
            start = lines.index(MANAGED_BLOCK_START)
            end = lines.index(MANAGED_BLOCK_END)
            if not (start < idx < end):
                has_duplicate_equivalent = True
                break
        else:
            has_duplicate_equivalent = True
            break

    if has_duplicate_equivalent:
        warnings.append("Equivalent .agents/state/ ignore exists outside managed block")

    if MANAGED_BLOCK_START in lines and MANAGED_BLOCK_END in lines and lines.index(MANAGED_BLOCK_START) < lines.index(MANAGED_BLOCK_END):
        start = lines.index(MANAGED_BLOCK_START)
        end = lines.index(MANAGED_BLOCK_END)
        new_lines = lines[:start] + MANAGED_BLOCK_LINES + lines[end + 1 :]
    else:
        new_lines = lines[:]
        if new_lines and new_lines[-1].strip() != "":
            new_lines.append("")
        new_lines.extend(MANAGED_BLOCK_LINES)

    new_content = "\n".join(new_lines).rstrip() + "\n"
    if new_content == content:
        return

    if apply:
        path.write_text(new_content, encoding="utf-8")
    changed["updatedFiles"].append(".gitignore")
    changed["managedGitignoreBlock"] = True


def apply_scaffold(root: Path, apply: bool, git_root_detected: bool) -> BootstrapResult:
    warnings: list[str] = []
    errors: list[str] = []
    before_state = classify_scaffold(root, warnings=[])

    changed: dict[str, Any] = {
        "createdDirectories": [],
        "createdFiles": [],
        "updatedFiles": [],
        "managedGitignoreBlock": False,
    }
    preserved: dict[str, Any] = {
        "existingDirectories": [],
        "existingFiles": [],
    }

    for rel in STRUCTURAL_DIRS:
        ensure_directory(root, rel, changed, preserved, apply)

    for rel, content in required_files().items():
        ensure_file(root, rel, content, changed, preserved, warnings, apply)

    update_gitignore(root, changed, warnings, apply)

    after_state = classify_scaffold(root, warnings)
    ok = len(errors) == 0
    return BootstrapResult(
        ok=ok,
        root=str(root),
        mode="apply" if apply else "check",
        gitRootDetected=git_root_detected,
        scaffoldStateBefore=before_state,
        scaffoldStateAfter=after_state,
        changed=changed,
        preserved=preserved,
        warnings=warnings,
        errors=errors,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Bootstrap repo-local orchestration scaffold")
    parser.add_argument("--root", required=True, help="Target repo or working root")
    parser.add_argument("--mode", choices=["check", "apply"], default="check")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    root = Path(args.root).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        result = BootstrapResult(
            ok=False,
            root=str(root),
            mode=args.mode,
            gitRootDetected=False,
            scaffoldStateBefore="missing",
            scaffoldStateAfter="missing",
            changed={
                "createdDirectories": [],
                "createdFiles": [],
                "updatedFiles": [],
                "managedGitignoreBlock": False,
            },
            preserved={
                "existingDirectories": [],
                "existingFiles": [],
            },
            warnings=[],
            errors=[f"Root does not exist or is not a directory: {root}"],
        )
        print(result.to_json())
        return 1

    git_root_detected = find_git_root(root) is not None and find_git_root(root) == root
    result = apply_scaffold(root, apply=args.mode == "apply", git_root_detected=git_root_detected)
    print(result.to_json())
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
