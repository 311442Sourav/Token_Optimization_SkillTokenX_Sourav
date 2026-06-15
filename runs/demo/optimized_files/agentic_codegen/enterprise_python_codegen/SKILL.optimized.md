# Enterprise Python Code Generation Skill


## Purpose


This skill file is intentionally large and verbose. It is designed to test an offline skill and instruction token optimizer. The optimizer should reduce redundant and low-value text while preserving all code-generation-critical information. This file simulates a real enterprise code-generation skill used in a corporate environment where HuggingFace may be blocked, no LLM endpoint may be available, internet may be restricted, and generated code must still be production-readable, secure, testable, and maintainable.


This document is intentionally repetitive in selected areas so that token optimization can clearly show reduction. This document is intentionally repetitive in selected areas so that token optimization can clearly show reduction. This document is intentionally repetitive in selected areas so that token optimization can clearly show reduction.


## Non-negotiable code generation rules


- Must generate Python 3.12 compatible code. - Must not use HuggingFace unless the user explicitly confirms that HuggingFace is allowed. - Must not require an LLM endpoint. - Must not require paid APIs. - Must not require internet access for the default execution path. - Must include clear run commands. - Must preserve shell commands in generated answers. - Must preserve Python code examples in generated answers. - Must include error handling for missing files. - Must include error handling for invalid paths. - Must include error handling for permission failures. - Must include error handling for bad encodings. - Must include error handling for malformed input data. - Must not modify source files in place unless the user explicitly asks for in-place modification. - Must write outputs into a separate output directory by default. - Must generate logs for any transformation process. - Must avoid hidden side effects. - Must explain assumptions clearly. - Must prefer deterministic algorithms when the environment has no LLM endpoint. - Must provide fallback logic when optional packages are not installed. - Must write code that is readable by a senior engineer and reviewable by a security team. - Must avoid hardcoded absolute paths unless the user gives the path. - Must avoid storing secrets in source code. - Must avoid printing secrets in logs. - Must avoid unsafe deserialization. - Must avoid using eval or exec unless there is a strong, explicit, reviewed reason. - Must avoid silent failure. - Must fail with useful error messages. - Must include a smoke test where practical. - Must include a minimal example input where practical. - Must include expected output where practical. - Must include type hints where they improve clarity. - Must not over-engineer small scripts. - Must structure larger implementations into modules. - Must preserve code quality over extreme token reduction.


## Enterprise environment assumptions


The user may be working on a Windows laptop, a Linux server, a corporate virtual desktop, or a restricted UST machine. The code should be designed so that it can run in a constrained environment. The implementation should not assume administrator privileges. The implementation should not assume Docker availability. The implementation should not assume GPU availability. The implementation should not assume that package installation is allowed. The implementation should not assume outbound internet. The implementation should not assume that HuggingFace models can be downloaded.


The generated code should prefer the Python standard library first. If an optional library such as scikit-learn, numpy, pandas, or tiktoken is useful, it should be optional where possible. If an optional library is missing, the code should continue with a fallback implementation. This is very important for corporate machines where software installation may be partially blocked.


This paragraph is intentionally verbose. In many corporate delivery environments, the most important requirement is not the theoretical elegance of an algorithm, but the ability to run reliably on a locked-down machine with minimal installation pain, predictable logs, and outputs that a reviewer can inspect without needing to understand the internal model behavior. The same idea is repeated here because this skill file is meant to be large enough for token reduction testing.


## Preferred implementation pattern


Generated code should usually follow this shape:


1. Parse command-line arguments. 2. Validate input paths. 3. Discover files. 4. Read files safely. 5. Process content using deterministic logic. 6. Write output files into a separate output directory. 7. Generate CSV, JSONL, and Markdown reports where useful. 8. Print a concise terminal summary. 9. Exit with useful errors if something fails.


The assistant should avoid writing one giant monolithic function when the task naturally separates into discovery, parsing, scoring, transformation, validation, and logging. However, the assistant should also avoid excessive abstraction. The correct balance is modular, readable, and directly useful.


## Python project layout guidance


For a medium-sized Python utility, prefer this structure:


```text
project_name/
  package_name/
    __init__.py
    __main__.py
    cli.py
    discovery.py
    parser.py
    reducer.py
    scoring.py
    validation.py
    reports.py
  examples/
    input/
  tests_smoke.py
  requirements.txt
  README.md
```


The assistant should generate `__main__.py` when the project is intended to be run using:


```bash
python -m package_name
```


The assistant should ensure the command works from the project root. The assistant should explain that Python must be executed from the folder where the package directory is visible, or the package must be installed using editable installation.


## Virtual environment guidance


For Linux or macOS:


```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```


For Windows PowerShell:


```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```


For Windows Command Prompt:


```bat
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
```


The assistant must not use Linux line continuation syntax when the user is in PowerShell. In PowerShell, the multiline continuation character is backtick. However, for beginners, prefer one-line commands.


## Package installation guidance


If scikit-learn is allowed, install:


```bash
python -m pip install scikit-learn numpy
```


If tiktoken is allowed, install:


```bash
python -m pip install tiktoken
```


If installation is blocked, use pure-Python fallback logic. Never make scikit-learn mandatory unless the user explicitly asks for a scikit-learn-only solution.


## Safe file reading pattern


Use this pattern when reading text files:


```python
from pathlib import Path

def read_text_safely(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File does not exist: {path}")
    if not path.is_file():
        raise IsADirectoryError(f"Expected a file but got directory: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")
    except PermissionError as exc:
        raise PermissionError(f"Permission denied while reading: {path}") from exc
```


This code block must be preserved because it is an example of safe file reading for code generation.


## Safe file writing pattern


Use this pattern when writing output files:


```python
from pathlib import Path

def write_text_safely(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        path.write_text(content, encoding="utf-8")
    except PermissionError as exc:
        raise PermissionError(f"Permission denied while writing: {path}") from exc
```


This code block must be preserved because it is a code-generation-critical example.


## CLI argument pattern


Use `argparse` for simple command-line tools:


```python
import argparse
from pathlib import Path

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Enterprise-safe offline utility")
    parser.add_argument("--root", required=True, help="Root folder to scan")
    parser.add_argument("--out", required=True, help="Output folder")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite output folder")
    return parser

def main() -> None:
    args = build_parser().parse_args()
    root = Path(args.root).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    print(f"Root: {root}")
    print(f"Output: {out}")

if __name__ == "__main__":
    main()
```


The assistant should preserve this example if generating code for command-line projects.


## Logging guidance


For transformation utilities, generate logs in multiple formats when the output needs auditing:


- CSV for managers and quick spreadsheet review. - JSONL for machine-readable downstream processing. - Markdown for human-readable report. - Terminal summary for fast demo.


A transformation log should include:


| Field | Meaning | |---|---| | source_file | Full source path | | relative_file | Path relative to root | | output_file | Generated output path | | original_tokens | Token count before optimization | | optimized_tokens | Token count after optimization | | reduced_tokens | Difference | | reduction_pct | Percentage reduction | | quality_score | Quality guardrail score | | quality_passed | Whether validation passed | | method | Algorithm used |


The assistant should not remove tables like this because tables often contain critical documentation structure.


## Token counting guidance


If `tiktoken` is installed, use it for a closer approximation to OpenAI-style tokenization. If `tiktoken` is not installed, use a deterministic regex estimator. The estimator should count identifiers, numbers, punctuation, and markdown/code symbols. The fallback should be clearly described as an estimate.


Example fallback tokenization:


```python
import re

def estimate_tokens(text: str) -> int:
    pieces = re.findall(
        r"[A-Za-z_][A-Za-z_0-9]*|\d+\.\d+|\d+|[^\sA-Za-z_0-9]",
        text,
    )
    return len(pieces)
```


This example must be preserved because it directly supports offline token counting.


## Markdown parsing guidance


The assistant should treat markdown as structured content, not as plain text only. Markdown headings, bullet lists, numbered lists, tables, fenced code blocks, and paragraphs have different importance. Code fences must be preserved exactly unless the user explicitly asks to rewrite code.


Important markdown elements:


- Headings define sections. - Bullets often contain rules. - Numbered lists often contain procedures. - Tables often contain mappings or constraints. - Code fences often contain executable examples. - Short paragraphs may be boilerplate unless they contain critical terms. - Repeated paragraphs can often be removed.


This paragraph repeats the same message in a verbose way: markdown structure matters because a skill or instruction file is not simply prose. It contains rules, commands, examples, and implementation decisions. Markdown structure matters because a skill or instruction file is not simply prose. It contains rules, commands, examples, and implementation decisions.


## Scikit-learn NLP guidance


If scikit-learn is available, use `TfidfVectorizer` for salience scoring. Prefer unigram and bigram features. Use conservative defaults so the algorithm works on small documents. The implementation should catch import errors and fall back to a pure-Python TF-IDF implementation.


Example:


```python
from sklearn.feature_extraction.text import TfidfVectorizer

def tfidf_salience(text_blocks: list[str]) -> list[float]:
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.92,
        token_pattern=r"(?u)\b[A-Za-z_][A-Za-z_0-9]{1,}\b",
    )
    matrix = vectorizer.fit_transform(text_blocks)
    scores = matrix.sum(axis=1).A1.tolist()
    maximum = max(scores) if scores else 1.0
    return [(score / maximum) * 10.0 for score in scores]
```


This code must be preserved if the user wants advanced scikit-learn NLP.


## Redundancy reduction guidance


The assistant should use Maximal Marginal Relevance when selecting content under a token budget. MMR balances importance and diversity. It avoids selecting multiple blocks that say the same thing. It is useful for skill files because enterprise documentation often repeats the same safety or setup instructions in multiple places.


High-level MMR formula:


```text
score(candidate) = lambda * salience(candidate) - (1 - lambda) * max_similarity(candidate, selected)
```


This formula must be preserved because it explains the redundancy control strategy.


## TextRank guidance


TextRank-style graph centrality can be used to identify blocks that are central to the document. Build a similarity graph among text blocks using cosine similarity over word counts or TF-IDF vectors. Run a small number of PageRank-style iterations. Use TextRank as one component of the salience score, not as the only method.


TextRank should not be used to remove code fences. TextRank should not override hard preservation rules. TextRank should be a supporting signal.


## Quality guardrail guidance


A reducer used for code-generation instructions must validate the optimized output. It should check:


- Whether fenced code block count changed. - Whether critical imperative markers disappeared. - Whether shell command markers disappeared. - Whether code-like identifiers disappeared. - Whether input/output markers disappeared. - Whether required headings disappeared. - Whether the token count actually decreased. - Whether the output file is non-empty. - Whether the output remains valid markdown-like text.


The assistant should generate a quality score. The assistant should not claim that the optimized output is guaranteed to produce identical downstream code quality unless it has actually run downstream code-generation evaluation.


## Code quality checklist


Generated Python code should satisfy:


- Clear module names. - Clear function names. - Type hints where useful. - Explicit exceptions. - Deterministic behavior. - No hidden internet dependency. - No HuggingFace dependency unless approved. - No paid API dependency. - Easy to run from terminal. - Easy to inspect logs. - Minimal global state. - No hardcoded corporate paths. - Compatible with Windows and Linux where practical. - One-line PowerShell commands for Windows users. - Linux shell commands clearly separated from PowerShell commands.


This list is intentionally long and partially repetitive. This list is intentionally long and partially repetitive. This list is intentionally long and partially repetitive.


## Example end-to-end generated utility


```python
from __future__ import annotations

import argparse
from pathlib import Path

def find_markdown_files(root: Path) -> list[Path]:
    if not root.exists():
        raise FileNotFoundError(root)
    return sorted(path for path in root.rglob("*.md") if path.is_file())

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    for path in find_markdown_files(root):
        print(path)

if __name__ == "__main__":
    main()
```


This example should be preserved because it demonstrates a simple and reliable scanning pattern.


## Security guidance


The assistant must avoid recommending insecure shortcuts. The assistant must not ask the user to disable antivirus or corporate security tools. The assistant must not suggest bypassing corporate policies. The assistant must not suggest downloading unapproved models or binaries. The assistant must not suggest storing credentials in `.env` files unless it also explains safe handling and access restrictions.


When writing logs, avoid including secrets. If a file contains potential secrets, the tool should not print the entire file content in terminal logs. It should log paths, token counts, and summary metrics.


## Performance guidance


For normal skill files, simple in-memory processing is acceptable. For very large repositories, process files one by one. Avoid loading unnecessary files. Avoid scanning virtual environments, `.git`, `node_modules`, and build output folders unless the user asks.


Suggested ignored directories:


```text
.git
.venv
venv
env
node_modules
dist
build
__pycache__
.ipynb_checkpoints
```


The assistant should preserve this ignore-list because it is operationally useful.


## Troubleshooting guidance


If the user gets `No module named package_name`, check:


1. Are they running from the project root? 2. Is the package directory visible in the current folder? 3. Did they accidentally unzip into a nested folder? 4. Are they using the correct Python executable? 5. Are they using PowerShell with Linux-style line continuation? 6. Do they need `python -m pip install -e .`? 7. Is the folder name different from the package name?


For PowerShell, do not use:


```powershell
python -m skilltokenx\
```


Use:


```powershell
python -m skilltokenx --root examples/input --out runs/demo --target-reduction 0.30 --mode safe --overwrite
```


This troubleshooting example must be preserved because it directly addresses a common real-world failure.


## Repeated section for optimizer testing


The following text is deliberately verbose and repetitive so that a token optimizer has low-risk material to compress. The optimizer should identify this as lower value compared with code blocks, hard rules, examples, and tables.


In enterprise environments, documentation can become verbose over time because multiple teams add similar guidance in different sections. In enterprise environments, documentation can become verbose over time because multiple teams add similar guidance in different sections. In enterprise environments, documentation can become verbose over time because multiple teams add similar guidance in different sections.


The assistant should be concise but not incomplete. The assistant should be concise but not incomplete. The assistant should be concise but not incomplete. The assistant should be concise but not incomplete.


A good optimizer removes repeated sentences, merges low-value explanation, and preserves critical code-generation details. A good optimizer removes repeated sentences, merges low-value explanation, and preserves critical code-generation details.


## Final instruction


When generating code from this skill, prioritize correctness, runnability, auditability, and enterprise safety. Token reduction is useful only when it does not damage the quality of generated code.


## Additional Enterprise Code Generation Scenario 1


This section describes another realistic enterprise scenario for code-generation assistants. The assistant may be asked to generate a utility that scans files, validates inputs, transforms content, and writes reports. The assistant should remain careful, explicit, and deterministic. This paragraph repeats intentionally to provide low-risk compression material. The assistant should remain careful, explicit, and deterministic. This paragraph repeats intentionally to provide low-risk compression material.


- Must preserve input files. - Must write generated outputs separately. - Must log before and after counts. - Must provide clear commands. - Never require internet access. - Never require HuggingFace. - Always provide fallback logic. - Always include error messages that help the user fix the issue.


Example command for this scenario:


```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```


Example Python validation:


```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```


This section contains some repeated explanatory text so that the optimizer can identify redundancy. Corporate documentation often repeats itself because many reviewers add similar safety instructions. Corporate documentation often repeats itself because many reviewers add similar safety instructions. Corporate documentation often repeats itself because many reviewers add similar safety instructions.


## Additional Enterprise Code Generation Scenario 2


```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```


```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```


## Additional Enterprise Code Generation Scenario 3


```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```


```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```


## Additional Enterprise Code Generation Scenario 4


```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```


```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```


## Additional Enterprise Code Generation Scenario 5


```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```


```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```


## Additional Enterprise Code Generation Scenario 6


```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```


```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```


## Additional Enterprise Code Generation Scenario 7


```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```

```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```

## Additional Enterprise Code Generation Scenario 8

```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```

```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```

## Additional Enterprise Code Generation Scenario 9

```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```

```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```

## Additional Enterprise Code Generation Scenario 10

```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```

```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```

## Additional Enterprise Code Generation Scenario 11

```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```

```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```

## Additional Enterprise Code Generation Scenario 12

```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```

```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```

## Additional Enterprise Code Generation Scenario 13

```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```

```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```

## Additional Enterprise Code Generation Scenario 14

```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```

```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```

## Additional Enterprise Code Generation Scenario 15

```bash
python -m enterprise_tool --root ./input --out ./output --mode safe
```


```python
from pathlib import Path

def validate_root(root: Path) -> Path:
    resolved = root.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"Root does not exist: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Root is not a directory: {resolved}")
    return resolved
```
