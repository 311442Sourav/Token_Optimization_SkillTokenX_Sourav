# Enterprise Instruction File for Offline Skill Token Optimization


## Objective


You are building and testing a local token optimization system for skill and instruction markdown files. The system must detect large markdown files, count tokens before optimization, apply an offline optimization algorithm, generate optimized output files, and produce logs showing reduction percentage and quality guardrail status.


The instruction file is intentionally large. It is designed to stress-test the optimizer. It contains important rules, examples, tables, repeated sections, and implementation guidance. The optimizer should reduce redundant explanatory text while preserving code examples, commands, numbered procedures, quality requirements, and critical constraints.


This instruction file repeats some ideas intentionally. This instruction file repeats some ideas intentionally. This instruction file repeats some ideas intentionally. The repetition exists so that the optimizer can prove it removes redundancy.


## Required behavior


1. Recursively scan the provided root folder. 2. Detect files named `SKILL.md`, `skills.md`, `INSTRUCTION.md`, `instructions.md`, `system_instruction.md`, and `system_instructions.md`. 3. Count tokens before optimization. 4. Parse markdown into structured blocks. 5. Preserve fenced code blocks. 6. Preserve shell commands. 7. Preserve function signatures. 8. Preserve class definitions. 9. Preserve tables. 10. Preserve headings. 11. Preserve imperative rules containing `must`, `never`, `always`, `required`, or `do not`. 12. Score compressible blocks using NLP salience. 13. Use scikit-learn TF-IDF when available. 14. Use pure-Python fallback when scikit-learn is not available. 15. Apply redundancy reduction using MMR or a similar method. 16. Respect the requested target reduction. 17. Write optimized files into a separate output folder. 18. Do not modify original files. 19. Generate CSV logs. 20. Generate JSONL logs. 21. Generate Markdown report. 22. Generate quality guardrail report. 23. Print concise terminal output. 24. Exit with clear error messages. 25. Support Windows PowerShell and Linux terminal usage.


## Demo command for Windows PowerShell


Use this single-line command in PowerShell:


```powershell
python -m skilltokenx --root examples/input --out runs/demo --target-reduction 0.30 --mode safe --overwrite
```


Do not use Linux-style line continuation in PowerShell.


## Demo command for Linux


Use this command in Linux:


```bash
python -m skilltokenx \
  --root examples/input \
  --out runs/demo \
  --target-reduction 0.30 \
  --mode safe \
  --overwrite
```


## Expected terminal output


The terminal output should look similar to this:


```text
[OK] enterprise_python_codegen/SKILL.md: 2600 -> 1800 tokens, reduced 30.77%, quality=100.0
[OK] enterprise_python_codegen/INSTRUCTION.md: 2100 -> 1500 tokens, reduced 28.57%, quality=100.0

Optimized files: runs/demo/optimized_files
Logs: runs/demo/logs
Research mapping: runs/demo/research/research_mapping.md
Patent draft: runs/demo/patent/invention_disclosure_draft.md
```


The exact token numbers may be different depending on whether `tiktoken` is installed.


## Expected output structure


```text
runs/demo/
  optimized_files/
    enterprise_python_codegen/
      SKILL.optimized.md
      INSTRUCTION.optimized.md
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


The optimizer must preserve the structure of input folders under `optimized_files`.


## Required CSV columns


The CSV log must include these columns:


| Column | Requirement | |---|---| | source_file | Full source path | | relative_file | Relative file path | | output_file | Optimized output path | | original_tokens | Token count before optimization | | optimized_tokens | Token count after optimization | | reduced_tokens | Token reduction | | reduction_pct | Percentage reduction | | token_method | Token counter used | | nlp_method | NLP scoring method used | | quality_score | Guardrail score | | quality_passed | Boolean quality status | | quality_issues | Issues found | | total_blocks | Total markdown blocks | | kept_blocks | Blocks retained | | mode | safe, balanced, or aggressive | | target_reduction | User requested reduction target |


Tables like this should not be removed because they define the reporting contract.


## Quality preservation contract


The optimizer must not remove content that changes code-generation behavior. The optimizer must not remove code examples. The optimizer must not remove setup commands. The optimizer must not remove rules about offline operation. The optimizer must not remove rules about HuggingFace restrictions. The optimizer must not remove rules about LLM endpoint restrictions. The optimizer must not remove rules about safe file handling. The optimizer must not remove examples that explain how to run the generated code.


The optimizer may remove repeated prose. The optimizer may compress verbose explanations. The optimizer may remove duplicated statements. The optimizer may remove low-information paragraphs that do not contain constraints, code, commands, inputs, outputs, or important implementation details.


## Example quality guardrail logic


```python
import re

def count_code_fences(text: str) -> int:
    return len(re.findall(r"^\s*(```|~~~)", text, flags=re.MULTILINE))

def quality_passed(original: str, optimized: str) -> bool:
    if count_code_fences(original) != count_code_fences(optimized):
        return False
    if "must" in original.lower() and "must" not in optimized.lower():
        return False
    if "python -m" in original and "python -m" not in optimized:
        return False
    return True
```


This example must be preserved because it defines an important guardrail strategy.


## Algorithm requirement


The algorithm should combine multiple signals:


1. Structural importance. 2. Rule criticality. 3. TF-IDF salience. 4. TextRank centrality. 5. Code-like pattern detection. 6. Position-aware preservation. 7. Redundancy penalty. 8. Token budget control. 9. Quality validation.


Do not rely on only one signal. A single score is usually fragile. A hybrid score is more robust for enterprise instruction files.


## Suggested hybrid scoring formula


```text
final_score =
  0.34 * structural_score
+ 0.30 * rule_criticality_score
+ 0.23 * tfidf_salience_score
+ 0.10 * textrank_score
+ 0.03 * position_bonus
```


The exact weights can be tuned. The optimizer should expose mode-level behavior: safe, balanced, and aggressive.


## Mode behavior


| Mode | Expected behavior | |---|---| | safe | Conservative; best for preserving code-generation quality | | balanced | Stronger reduction; still preserves critical material | | aggressive | Maximum reduction; requires human review |


The first demo should use safe mode. The second demo can use balanced mode to show stronger reduction.


## Test procedure


Use this procedure during a live demo:


1. Show original `SKILL.md` and `INSTRUCTION.md`. 2. Show that the files are large and contain repeated sections. 3. Run the optimizer in safe mode. 4. Show terminal reduction output. 5. Open `reduction_report.md`. 6. Open `quality_guardrail_report.md`. 7. Open the optimized `SKILL.optimized.md`. 8. Confirm code blocks remain. 9. Confirm commands remain. 10. Confirm critical rules remain. 11. Compare before and after token counts. 12. Explain that no HuggingFace or LLM endpoint was used.


## Smoke test command


```powershell
python tests_smoke.py
```


The smoke test should verify that at least one file is found, token count decreases, and quality score remains acceptable.


## Reviewer talking points


Use these talking points when explaining the demo:


- This is not simple summarization. - This is not generic text shortening. - This is a code-aware skill and instruction optimizer. - It preserves code-generation-critical material. - It applies offline NLP using scikit-learn when available. - It uses deterministic fallback when scikit-learn is not available. - It generates audit logs. - It supports enterprise review. - It avoids HuggingFace and external LLM endpoints. - It is suitable for restricted corporate machines. - It can be extended later with local embeddings if approved. - It can be extended later with downstream code-generation evaluation if an internal LLM endpoint becomes available.


## Repeated enterprise explanation


Enterprise AI teams often suffer from long prompt files, long skill files, long instruction files, and repeated policy blocks. Enterprise AI teams often suffer from long prompt files, long skill files, long instruction files, and repeated policy blocks. Enterprise AI teams often suffer from long prompt files, long skill files, long instruction files, and repeated policy blocks.


Token reduction can reduce cost and latency, but careless reduction can damage quality. Token reduction can reduce cost and latency, but careless reduction can damage quality. Token reduction can reduce cost and latency, but careless reduction can damage quality.


A useful optimizer must keep code examples, constraints, setup commands, and quality rules intact. A useful optimizer must keep code examples, constraints, setup commands, and quality rules intact. A useful optimizer must keep code examples, constraints, setup commands, and quality rules intact.


## Future extension ideas


The project may later add:


- Local embedding model support if approved. - Sentence-transformer support if HuggingFace becomes available. - Internal LLM endpoint validation if UST provides one. - Downstream code-generation evaluation. - AST-based validation for generated Python code. - Prompt variant A/B testing. - Token budget recommendation. - Per-section reduction reports. - Configurable preserve patterns. - Configurable ignored directories. - HTML dashboard. - Streamlit interface. - Git pre-commit integration. - CI/CD report generation. - Repository-wide token optimization trend tracking.


These future ideas are useful but should not be required for the offline demo.


## Final instruction


The optimized files must be shorter, but they must remain useful for code generation. Do not chase maximum compression at the cost of correctness. For the first demo, prioritize quality and auditability.


## Demo Validation Section 1


During demo validation, the reviewer should confirm that important instructions are still present after optimization. The reviewer should compare original and optimized files. The reviewer should check whether the optimized output keeps code blocks, commands, tables, and critical constraints. This paragraph is intentionally repeated for optimization testing. The reviewer should compare original and optimized files. The reviewer should check whether the optimized output keeps code blocks, commands, tables, and critical constraints.


Required checks:


1. Must confirm token count decreased. 2. Must confirm quality score is acceptable. 3. Must confirm code fence count did not change. 4. Must confirm `python -m skilltokenx` command is preserved. 5. Must confirm HuggingFace restriction is preserved. 6. Must confirm LLM endpoint restriction is preserved. 7. Must confirm source files are not overwritten. 8. Must confirm logs are generated.


Validation command:


```powershell
python -m skilltokenx --root examples/input --out runs/demo_section_1 --target-reduction 0.30 --mode safe --overwrite
```


This validation section is deliberately verbose. This validation section is deliberately verbose. This validation section is deliberately verbose.


## Demo Validation Section 2


```powershell
python -m skilltokenx --root examples/input --out runs/demo_section_2 --target-reduction 0.30 --mode safe --overwrite
```


## Demo Validation Section 3


```powershell
python -m skilltokenx --root examples/input --out runs/demo_section_3 --target-reduction 0.30 --mode safe --overwrite
```


## Demo Validation Section 4


```powershell
python -m skilltokenx --root examples/input --out runs/demo_section_4 --target-reduction 0.30 --mode safe --overwrite
```


## Demo Validation Section 5


```powershell
python -m skilltokenx --root examples/input --out runs/demo_section_5 --target-reduction 0.30 --mode safe --overwrite
```


## Demo Validation Section 6


```powershell
python -m skilltokenx --root examples/input --out runs/demo_section_6 --target-reduction 0.30 --mode safe --overwrite
```


## Demo Validation Section 7

```powershell
python -m skilltokenx --root examples/input --out runs/demo_section_7 --target-reduction 0.30 --mode safe --overwrite
```

## Demo Validation Section 8

```powershell
python -m skilltokenx --root examples/input --out runs/demo_section_8 --target-reduction 0.30 --mode safe --overwrite
```

## Demo Validation Section 9

```powershell
python -m skilltokenx --root examples/input --out runs/demo_section_9 --target-reduction 0.30 --mode safe --overwrite
```

## Demo Validation Section 10

```powershell
python -m skilltokenx --root examples/input --out runs/demo_section_10 --target-reduction 0.30 --mode safe --overwrite
```

## Demo Validation Section 11

```powershell
python -m skilltokenx --root examples/input --out runs/demo_section_11 --target-reduction 0.30 --mode safe --overwrite
```

## Demo Validation Section 12


```powershell
python -m skilltokenx --root examples/input --out runs/demo_section_12 --target-reduction 0.30 --mode safe --overwrite
```
