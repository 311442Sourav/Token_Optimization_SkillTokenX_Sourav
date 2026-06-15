from __future__ import annotations
import re
from dataclasses import dataclass

@dataclass
class Block:
    idx: int
    kind: str
    text: str
    start_line: int
    end_line: int
    heading_level: int = 0

FENCE_RE = re.compile(r"^\s*(```|~~~)")

def parse_markdown(text: str) -> list[Block]:
    lines = text.splitlines()
    blocks: list[Block] = []
    i = 0
    idx = 0

    def add(kind: str, buf: list[str], start: int, end: int, level: int = 0):
        nonlocal idx
        blocks.append(Block(idx, kind, "\n".join(buf).rstrip(), start, end, level))
        idx += 1

    while i < len(lines):
        line = lines[i]
        start = i + 1

        if FENCE_RE.match(line):
            fence = FENCE_RE.match(line).group(1)  # type: ignore
            buf = [line]
            i += 1
            while i < len(lines):
                buf.append(lines[i])
                if lines[i].strip().startswith(fence):
                    i += 1
                    break
                i += 1
            add("code_fence", buf, start, i)
            continue

        if not line.strip():
            add("blank", [line], start, start)
            i += 1
            continue

        if re.match(r"^\s{0,3}#{1,6}\s+", line):
            level = len(line.lstrip().split(" ", 1)[0])
            add("heading", [line], start, start, level)
            i += 1
            continue

        if _is_table_line(line):
            buf = [line]
            i += 1
            while i < len(lines) and _is_table_line(lines[i]):
                buf.append(lines[i])
                i += 1
            add("table", buf, start, i)
            continue

        if re.match(r"^\s*[-*+]\s+", line):
            buf = [line]
            i += 1
            while i < len(lines) and re.match(r"^\s*([-*+]|\s{2,}[-*+])\s+", lines[i]):
                buf.append(lines[i])
                i += 1
            add("bullet", buf, start, i)
            continue

        if re.match(r"^\s*\d+[\.)]\s+", line):
            buf = [line]
            i += 1
            while i < len(lines) and re.match(r"^\s*(\d+[\.)]|\s{2,}\d+[\.)])\s+", lines[i]):
                buf.append(lines[i])
                i += 1
            add("numbered", buf, start, i)
            continue

        buf = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if (
                not nxt.strip()
                or FENCE_RE.match(nxt)
                or re.match(r"^\s{0,3}#{1,6}\s+", nxt)
                or re.match(r"^\s*[-*+]\s+", nxt)
                or re.match(r"^\s*\d+[\.)]\s+", nxt)
                or _is_table_line(nxt)
            ):
                break
            buf.append(nxt)
            i += 1
        add("paragraph", buf, start, i)

    return blocks

def _is_table_line(line: str) -> bool:
    s = line.strip()
    return "|" in s and (s.startswith("|") or s.endswith("|") or s.count("|") >= 2)

def render_blocks(blocks: list[Block]) -> str:
    out = []
    prev_blank = False
    for b in blocks:
        text = b.text.strip()
        if not text:
            if not prev_blank:
                out.append("")
            prev_blank = True
        else:
            out.append(text)
            prev_blank = False
    result = "\n\n".join(out)
    result = re.sub(r"\n{4,}", "\n\n\n", result)
    return result.strip() + "\n"
