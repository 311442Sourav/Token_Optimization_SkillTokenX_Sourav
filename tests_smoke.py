from pathlib import Path
from skilltokenx.discovery import find_files
from skilltokenx.reducer import SkillTokenXReducer

files = find_files(Path("examples/input"))
assert files
text = files[0].read_text(encoding="utf-8")
result = SkillTokenXReducer(target_reduction=0.25, mode="safe").reduce(text)
assert result.optimized_tokens <= result.original_tokens
assert result.quality_score >= 70
print("Smoke test passed")
