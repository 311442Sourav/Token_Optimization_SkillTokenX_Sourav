from __future__ import annotations
import argparse, shutil
from pathlib import Path
from .discovery import find_files
from .reducer import SkillTokenXReducer
from .reports import write_reports

def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="SkillTokenX offline skill/instruction optimizer")
    p.add_argument("--root", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--target-reduction", type=float, default=0.30)
    p.add_argument("--mode", choices=["safe", "balanced", "aggressive"], default="safe")
    p.add_argument("--overwrite", action="store_true")
    return p

def main() -> None:
    args = parser().parse_args()
    root = Path(args.root).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    if out.exists() and args.overwrite:
        shutil.rmtree(out)
    opt_root = out / "optimized_files"
    opt_root.mkdir(parents=True, exist_ok=True)

    files = find_files(root)
    if not files:
        print(f"No skill/instruction files found under {root}")
        return

    reducer = SkillTokenXReducer(args.target_reduction, args.mode)
    rows = []

    for f in files:
        rel = f.relative_to(root)
        text = f.read_text(encoding="utf-8", errors="replace")
        result = reducer.reduce(text)

        target = opt_root / rel.parent / f"{f.stem}.optimized{f.suffix}"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(result.optimized_text, encoding="utf-8")

        row = {
            "source_file": str(f),
            "relative_file": str(rel),
            "output_file": str(target),
            "original_tokens": result.original_tokens,
            "optimized_tokens": result.optimized_tokens,
            "reduced_tokens": result.reduced_tokens,
            "reduction_pct": result.reduction_pct,
            "token_method": result.token_method,
            "nlp_method": result.nlp_method,
            "quality_score": result.quality_score,
            "quality_passed": result.quality_passed,
            "quality_issues": "; ".join(result.quality_issues),
            "total_blocks": result.total_blocks,
            "kept_blocks": result.kept_blocks,
            "mode": args.mode,
            "target_reduction": args.target_reduction,
        }
        rows.append(row)
        print(
            f"[OK] {rel}: {result.original_tokens} -> {result.optimized_tokens} "
            f"tokens, reduced {result.reduction_pct}%, quality={result.quality_score}"
        )

    write_reports(rows, out)
    print(f"\nOptimized files: {opt_root}")
    print(f"Logs: {out / 'logs'}")
    print(f"Research mapping: {out / 'research' / 'research_mapping.md'}")
    print(f"Patent draft: {out / 'patent' / 'invention_disclosure_draft.md'}")
