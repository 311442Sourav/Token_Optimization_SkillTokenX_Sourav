from __future__ import annotations
import math
import re
from collections import Counter, defaultdict
from .markdown_ast import Block
from .tokenizer import word_tokens

CRITICAL_TERMS = [
    "must", "never", "always", "required", "critical", "important", "preserve",
    "do not", "don't", "avoid", "error", "exception", "warning", "input", "output",
    "example", "command", "install", "run", "python", "pip", "git", "docker",
    "file", "path", "function", "class", "argument", "parameter", "return",
    "token", "quality", "validate", "test", "code generation", "offline",
]

CODE_PATTERNS = [
    r"`[^`]+`",
    r"\bdef\s+\w+\(",
    r"\bclass\s+\w+",
    r"\bimport\s+\w+",
    r"\bfrom\s+\w+\s+import\b",
    r"\w+\(",
    r"\.(py|md|json|yaml|yml|txt|csv|sh|sql)\b",
    r"\bpython\s+-m\b",
    r"\bpip\s+install\b",
    r"\bgit\s+",
    r"\/[\w\-\.\/]+",
]

BOILERPLATE = [
    r"this document is intended to",
    r"it is important to note that",
    r"please note that",
    r"in order to",
    r"the following are",
    r"below is",
    r"as mentioned above",
]

def structural_score(block: Block) -> float:
    if block.kind == "code_fence":
        return 100.0
    if block.kind == "heading":
        return 8.0 if block.heading_level <= 2 else 5.5
    if block.kind == "table":
        return 7.0
    if block.kind == "numbered":
        return 6.5
    if block.kind == "bullet":
        return 5.5
    if block.kind == "paragraph":
        return 3.0
    return 0.0

def rule_score(text: str) -> float:
    low = text.lower()
    score = 0.0
    for term in CRITICAL_TERMS:
        if term in low:
            score += 1.2
    for pattern in CODE_PATTERNS:
        if re.search(pattern, text, flags=re.I):
            score += 1.8
    for pattern in BOILERPLATE:
        if re.search(pattern, low, flags=re.I):
            score -= 1.3
    return min(14.0, score)

def pure_python_tfidf_scores(blocks: list[Block]) -> list[float]:
    docs = [word_tokens(b.text) for b in blocks]
    df = Counter()
    for doc in docs:
        df.update(set(doc))
    n = max(1, len(docs))
    idf = {t: math.log((1 + n) / (1 + c)) + 1.0 for t, c in df.items()}
    scores = []
    for doc in docs:
        if not doc:
            scores.append(0.0)
            continue
        tf = Counter(doc)
        total = len(doc)
        score = sum((c / total) * idf.get(t, 1.0) for t, c in tf.items())
        scores.append(score * 10.0)
    return scores

def sklearn_tfidf_scores(blocks: list[Block]) -> tuple[list[float], str]:
    texts = [b.text for b in blocks]
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer  # type: ignore
        import numpy as np  # type: ignore
        vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.92,
            token_pattern=r"(?u)\b[A-Za-z_][A-Za-z_0-9]{1,}\b",
        )
        matrix = vectorizer.fit_transform(texts)
        scores = matrix.sum(axis=1).A1.tolist()
        mx = max(scores) if scores else 1.0
        if mx > 0:
            scores = [(s / mx) * 10.0 for s in scores]
        return scores, "sklearn_tfidf"
    except Exception:
        return pure_python_tfidf_scores(blocks), "pure_python_tfidf"

def cosine_from_words(a: str, b: str) -> float:
    wa = Counter(word_tokens(a))
    wb = Counter(word_tokens(b))
    if not wa or not wb:
        return 0.0
    keys = set(wa) | set(wb)
    dot = sum(wa[k] * wb[k] for k in keys)
    na = math.sqrt(sum(v * v for v in wa.values()))
    nb = math.sqrt(sum(v * v for v in wb.values()))
    return dot / (na * nb) if na and nb else 0.0

def textrank_scores(blocks: list[Block], damping: float = 0.85, steps: int = 20) -> list[float]:
    n = len(blocks)
    if n == 0:
        return []
    weights = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            sim = cosine_from_words(blocks[i].text, blocks[j].text)
            if sim > 0:
                weights[i][j] = sim
                weights[j][i] = sim
    scores = [1.0 / n] * n
    for _ in range(steps):
        new = [(1 - damping) / n] * n
        for i in range(n):
            denom = sum(weights[i])
            if denom == 0:
                continue
            for j in range(n):
                if weights[i][j] > 0:
                    new[j] += damping * scores[i] * (weights[i][j] / denom)
        scores = new
    mx = max(scores) if scores else 1.0
    return [(s / mx) * 10.0 for s in scores]
