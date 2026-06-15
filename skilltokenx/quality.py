from __future__ import annotations
import re
from dataclasses import dataclass

@dataclass
class QualityGuardrail:
    passed: bool
    score: float
    issues: list[str]

def count_fences(text: str) -> int:
    return len(re.findall(r"^\s*(```|~~~)", text, flags=re.M))

def important_markers(text: str) -> set[str]:
    markers = set()
    for m in re.findall(r"\b(must|never|always|required|do not|don't|error|exception|input|output|example|python|pip|git)\b", text.lower()):
        markers.add(m)
    for m in re.findall(r"`([^`]+)`", text):
        markers.add("code:" + m.lower())
    for m in re.findall(r"\b[\w\-/\.]+\.(py|md|json|yaml|yml|csv|txt|sh)\b", text.lower()):
        markers.add("ext:" + m)
    return markers

def validate_quality(original: str, optimized: str) -> QualityGuardrail:
    issues = []
    score = 100.0

    if count_fences(original) != count_fences(optimized):
        issues.append("Fenced code block count changed.")
        score -= 35

    orig_markers = important_markers(original)
    opt_markers = important_markers(optimized)
    lost = sorted(orig_markers - opt_markers)
    if lost:
        issues.append(f"Lost important markers: {lost[:20]}")
        score -= min(35, len(lost) * 2)

    if "```" in original and "```" not in optimized:
        issues.append("All code fences disappeared.")
        score -= 40

    passed = score >= 70 and not any("Fenced code" in i or "All code" in i for i in issues)
    return QualityGuardrail(passed=passed, score=max(0.0, score), issues=issues)
