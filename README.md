# SkillTokenX v2: Offline Patent-Oriented Skill / Instruction Token Optimizer

SkillTokenX is an offline, enterprise-machine-friendly optimizer for `SKILL.md` and `INSTRUCTION.md` files used in code-generation systems.



## What is new in v2

This version adds an advanced research-backed offline NLP layer:

1. **Markdown-AST aware segmentation**
2. **Code block and command preservation**
3. **TF-IDF salience scoring using scikit-learn when available**
4. **Fallback pure-Python TF-IDF when scikit-learn is unavailable**
5. **MMR redundancy reduction**
6. **Graph TextRank scoring**
7. **Constraint and imperative rule preservation**
8. **Budget-controlled compression**
9. **Quality guardrail scoring**
10. **Audit logs for before/after tokens and reduction percentage**
11. **Invention disclosure template for patent discussion**

## Approach

LLMLingua and LongLLMLingua are LLM-assisted prompt compression methods. They usually rely on small language models, token-level probability, or LLM-related components.



So SkillTokenX implements a **training-free, offline, deterministic compression algorithm** that borrows the research principles:
- keep dense information
- remove redundancy
- preserve task-critical instructions
- use budget-controlled compression
- preserve positional and structural key information

## Giving a name of Algorithm tried to build

**CAPS-MMR**

Code-aware
Action-preserving  
Prompt/skill  
Salience optimizer with  
Maximal  
Marginal  
Redundancy control

## Install

No mandatory dependency:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Recommended if allowed in UST machine:

```bash
python -m pip install scikit-learn numpy
```

Optional for closer OpenAI-style token counting:

```bash
python -m pip install tiktoken
```

If these are blocked, the project still runs with pure Python fallback.

## Run demo

```bash
python -m skilltokenx \
  --root examples/input \
  --out runs/demo \
  --target-reduction 0.35 \
  --mode safe \
  --overwrite
```

## Run on your repository

```bash
python -m skilltokenx \
  --root /path/to/your/repo \
  --out /path/to/optimized_output \
  --target-reduction 0.30 \
  --mode safe \
  --overwrite
```

## Outputs

```text
optimized_files/
logs/
  reduction_log.csv
  reduction_log.jsonl
  reduction_report.md
  quality_guardrail_report.md
research/
  research_mapping.md
patent/
  invention_disclosure_draft.md
```

## Modes

- `safe`: best for code generation quality
- `balanced`: stronger reduction
- `aggressive`: use only after review

## Smoke test

```bash
python tests_smoke.py
```
