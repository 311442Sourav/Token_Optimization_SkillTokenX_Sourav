from __future__ import annotations
from .markdown_ast import Block
from .features import cosine_from_words

def select_with_mmr(
    candidate_indices: list[int],
    blocks: list[Block],
    salience: list[float],
    budget_count: int,
    must_keep: set[int],
    lambda_salience: float = 0.72,
) -> set[int]:
    """
    Maximal Marginal Relevance selection.

    Keeps high-salience blocks while penalizing redundancy against already selected blocks.
    """
    selected = set(must_keep)
    remaining = [i for i in candidate_indices if i not in selected]

    while remaining and len(selected) < budget_count:
        best_i = None
        best_score = float("-inf")

        for i in remaining:
            redundancy = 0.0
            if selected:
                redundancy = max(cosine_from_words(blocks[i].text, blocks[j].text) for j in selected)
            score = lambda_salience * salience[i] - (1.0 - lambda_salience) * redundancy * 10.0
            if score > best_score:
                best_score = score
                best_i = i

        if best_i is None:
            break
        selected.add(best_i)
        remaining.remove(best_i)

    return selected
