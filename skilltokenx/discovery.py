from __future__ import annotations
from pathlib import Path

TARGETS = {
    "skill.md", "skills.md", "instruction.md", "instructions.md",
    "system_instruction.md", "system_instructions.md"
}

def find_files(root: Path) -> list[Path]:
    root = root.expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(root)
    return sorted([p for p in root.rglob("*") if p.is_file() and p.name.lower() in TARGETS])
