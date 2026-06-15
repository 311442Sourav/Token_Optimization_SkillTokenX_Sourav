from __future__ import annotations
import csv, json
from pathlib import Path
from datetime import datetime

def write_reports(rows: list[dict], out: Path) -> None:
    logs = out / "logs"
#    research = out / "research"
#    patent = out / "patent"
    logs.mkdir(parents=True, exist_ok=True)
#    research.mkdir(parents=True, exist_ok=True)
#    patent.mkdir(parents=True, exist_ok=True)

    if rows:
        with (logs / "reduction_log.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    with (logs / "reduction_log.jsonl").open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    total_before = sum(r["original_tokens"] for r in rows)
    total_after = sum(r["optimized_tokens"] for r in rows)
    reduced = max(0, total_before - total_after)
    pct = round((reduced / total_before) * 100, 2) if total_before else 0.0

    report = [
        "# Reduction Report",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        f"- Files processed: {len(rows)}",
        f"- Total input tokens: {total_before}",
        f"- Total output tokens: {total_after}",
        f"- Total reduced tokens: {reduced}",
        f"- Overall reduction: {pct}%",
        "",
        "| File | Before | After | Reduced | % | Quality | NLP Method |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for r in rows:
        report.append(
            f"| `{r['relative_file']}` | {r['original_tokens']} | {r['optimized_tokens']} | "
            f"{r['reduced_tokens']} | {r['reduction_pct']} | {r['quality_score']} | {r['nlp_method']} |"
        )
    (logs / "reduction_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    qlines = ["# Quality Guardrail Report", ""]
    for r in rows:
        qlines.extend([
            f"## {r['relative_file']}",
            "",
            f"- Passed: {r['quality_passed']}",
            f"- Score: {r['quality_score']}",
            f"- Issues: {r['quality_issues']}",
            "",
        ])
    (logs / "quality_guardrail_report.md").write_text("\n".join(qlines), encoding="utf-8")

    #(research / "research_mapping.md").write_text(RESEARCH_MAPPING, encoding="utf-8")
    #(patent / "invention_disclosure_draft.md").write_text(INVENTION_DISCLOSURE, encoding="utf-8")

RESEARCH_MAPPING = """# Research Mapping

SkillTokenX is not a clone of one paper. It is an offline synthesis of established directions in prompt compression and extractive NLP.

## Mapped research principles

1. LLMLingua-style idea:
   - budget-controlled prompt compression
   - semantic integrity under compression
   - not directly implemented because it normally relies on language-model scoring

2. LongLLMLingua-style idea:
   - key information density
   - position-aware preservation
   - long-context cost and latency reduction

3. Selective Context-style idea:
   - remove redundant context
   - preserve informative content

4. Training-free prompt compression:
   - no fine-tuning
   - no LLM endpoint
   - no HuggingFace dependency

5. Classical NLP:
   - TF-IDF salience
   - TextRank graph centrality
   - Maximal Marginal Relevance for redundancy reduction
   - rule-based preservation of imperative and code-like instructions

## Differentiating enterprise angle

Most prompt-compression work focuses on generic QA, chat, or benchmark prompts.

SkillTokenX focuses on:
- skill files
- instruction files
- code-generation quality preservation
- offline corporate execution
- auditable before/after token logs
- deterministic compliance-friendly optimization
"""

INVENTION_DISCLOSURE = """# Invention Disclosure Draft

## Working title

Offline Code-Aware Skill and Instruction Token Optimization System Using Hybrid Salience, Structural Preservation, and Redundancy-Constrained Compression

## Problem

Enterprise AI teams maintain long skill and instruction files for code-generation assistants. These files consume large token budgets and increase latency/cost. Existing prompt compression methods often require LLMs, HuggingFace models, or remote APIs, which are blocked in many corporate environments.

## Proposed solution

A fully offline system that detects skill/instruction markdown files, parses them into structural blocks, preserves code-generation-critical elements, ranks remaining blocks using hybrid NLP salience, applies redundancy-aware selection, and generates optimized files with auditable token reduction logs.

## Core components

1. File discovery for SKILL.md and INSTRUCTION.md variants.
2. Markdown-AST segmentation.
3. Hard preservation of code fences, commands, function signatures, tables, and imperative rules.
4. TF-IDF salience scoring using scikit-learn when available.
5. Pure-Python TF-IDF fallback.
6. TextRank centrality scoring.
7. Maximal Marginal Relevance redundancy control.
8. Budget-controlled compression.
9. Quality guardrail validation.
10. CSV/JSONL/Markdown reduction audit.

## Potential novelty angle

The strongest novelty claim is not generic prompt compression. It is the combination of:
- offline execution without LLM or HuggingFace dependency,
- code-generation-instruction-specific preservation,
- markdown-structure-aware skill/instruction optimization,
- deterministic audit trail,
- quality guardrail checks tailored to code-generation prompts.

## Suggested independent claim draft

A computer-implemented method for optimizing code-generation skill and instruction documents, comprising:
1. recursively detecting markdown instruction files in a repository;
2. segmenting each file into structural markdown blocks;
3. classifying blocks into mandatory-preserve and compressible categories using code-aware and imperative-rule patterns;
4. computing hybrid salience scores using statistical term weighting, graph centrality, structural weighting, and rule-criticality;
5. selecting blocks under a target token budget using maximal marginal relevance to reduce semantic redundancy;
6. validating optimized output using code-generation quality guardrails;
7. generating optimized files and an auditable token-reduction log.

## Important legal note

This is a technical invention disclosure draft, not a legal patentability opinion. A patent attorney should perform prior-art search, claim drafting, and filing review.
"""
