from __future__ import annotations
import re
from dataclasses import dataclass
from .markdown_ast import Block, parse_markdown, render_blocks
from .features import structural_score, rule_score, sklearn_tfidf_scores, textrank_scores
from .mmr import select_with_mmr
from .quality import validate_quality
from .tokenizer import TokenCounter

MODE_KEEP = {
    "safe": 0.74,
    "balanced": 0.60,
    "aggressive": 0.48,
}

@dataclass
class Result:
    optimized_text: str
    original_tokens: int
    optimized_tokens: int
    reduced_tokens: int
    reduction_pct: float
    token_method: str
    nlp_method: str
    quality_score: float
    quality_passed: bool
    quality_issues: list[str]
    total_blocks: int
    kept_blocks: int

class SkillTokenXReducer:
    def __init__(self, target_reduction: float = 0.30, mode: str = "safe") -> None:
        if mode not in MODE_KEEP:
            raise ValueError(f"Invalid mode {mode}")
        if not 0 <= target_reduction <= 0.80:
            raise ValueError("target_reduction must be between 0 and 0.80")
        self.target_reduction = target_reduction
        self.mode = mode
        self.counter = TokenCounter()

    def reduce(self, text: str) -> Result:
        original_tokens = self.counter.count(text)
        blocks = parse_markdown(text)
        blocks = self._normalize_blocks(blocks)

        tfidf, tfidf_method = sklearn_tfidf_scores(blocks)
        graph = textrank_scores(blocks)

        salience = []
        for i, b in enumerate(blocks):
            position_bonus = 1.0 if i < 3 or i >= len(blocks) - 3 else 0.0
            combined = (
                0.34 * structural_score(b)
                + 0.30 * rule_score(b.text)
                + 0.23 * tfidf[i]
                + 0.10 * graph[i]
                + 0.03 * position_bonus
            )
            salience.append(combined)

        must_keep = self._must_keep_indices(blocks)
        target_token_count = int(original_tokens.count * (1 - self.target_reduction))

        min_keep_by_mode = max(1, int(len(blocks) * MODE_KEEP[self.mode]))
        candidate_budget = max(min_keep_by_mode, len(must_keep))

        # First select by MMR block budget.
        candidates = [i for i, b in enumerate(blocks) if b.kind != "blank"]
        selected = select_with_mmr(
            candidates,
            blocks,
            salience,
            budget_count=candidate_budget,
            must_keep=must_keep,
            lambda_salience=0.76 if self.mode == "safe" else 0.68,
        )

        # Then gradually remove lowest selected optional blocks until token target is approached.
        optional_selected = sorted([i for i in selected if i not in must_keep], key=lambda i: salience[i])
        for i in optional_selected:
            candidate_selected = selected - {i}
            candidate_text = render_blocks([b for j, b in enumerate(blocks) if j in candidate_selected])
            if self.counter.count(candidate_text).count <= target_token_count:
                selected = candidate_selected
                break
            # In balanced/aggressive continue removing carefully.
            if self.mode != "safe":
                selected = candidate_selected

        selected_blocks = [b for i, b in enumerate(blocks) if i in selected]
        optimized = render_blocks(selected_blocks)

        q = validate_quality(text, optimized)

        # Safety fallback: if guardrail fails, keep all must-keep + top salience 80%.
        if not q.passed and self.mode == "safe":
            budget = max(len(must_keep), int(len(blocks) * 0.82))
            ranked = sorted(range(len(blocks)), key=lambda i: salience[i], reverse=True)
            selected = set(ranked[:budget]) | must_keep
            selected_blocks = [b for i, b in enumerate(blocks) if i in selected]
            optimized = render_blocks(selected_blocks)
            q = validate_quality(text, optimized)

        optimized_tokens = self.counter.count(optimized)
        reduced = max(0, original_tokens.count - optimized_tokens.count)
        pct = round((reduced / original_tokens.count) * 100, 2) if original_tokens.count else 0.0

        return Result(
            optimized_text=optimized,
            original_tokens=original_tokens.count,
            optimized_tokens=optimized_tokens.count,
            reduced_tokens=reduced,
            reduction_pct=pct,
            token_method=optimized_tokens.method,
            nlp_method=f"{tfidf_method}+textrank+mmr",
            quality_score=q.score,
            quality_passed=q.passed,
            quality_issues=q.issues,
            total_blocks=len(blocks),
            kept_blocks=len(selected_blocks),
        )

    def _must_keep_indices(self, blocks: list[Block]) -> set[int]:
        keep = set()
        patterns = [
            r"\bmust\b", r"\bnever\b", r"\balways\b", r"\brequired\b",
            r"\bdo not\b", r"\bdon't\b", r"\berror\b", r"\bexception\b",
            r"\binput\b", r"\boutput\b", r"\bexample\b",
            r"\bpython\s+-m\b", r"\bpip\s+install\b", r"\bgit\s+",
            r"\bdef\s+\w+\(", r"\bclass\s+\w+",
        ]
        for i, b in enumerate(blocks):
            low = b.text.lower()
            if b.kind in {"heading", "code_fence", "table"}:
                keep.add(i)
            elif any(re.search(p, low, flags=re.I) for p in patterns):
                keep.add(i)
        return keep

    def _normalize_blocks(self, blocks: list[Block]) -> list[Block]:
        seen = set()
        out = []
        for b in blocks:
            if b.kind == "code_fence":
                out.append(b)
                continue
            text = b.text
            text = re.sub(r"\bplease make sure that\b", "ensure", text, flags=re.I)
            text = re.sub(r"\bin order to\b", "to", text, flags=re.I)
            text = re.sub(r"\bit is important to note that\b", "note", text, flags=re.I)
            text = re.sub(r"\s+", " ", text).strip()
            key = re.sub(r"[^a-z0-9 ]", "", text.lower())
            if b.kind not in {"heading", "blank"} and key in seen:
                continue
            seen.add(key)
            b.text = text
            out.append(b)
        return out
