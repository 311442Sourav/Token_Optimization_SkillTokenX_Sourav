from __future__ import annotations
import re
from dataclasses import dataclass

@dataclass
class TokenStats:
    count: int
    method: str

class TokenCounter:
    def __init__(self, encoding_name: str = "cl100k_base") -> None:
        self.method = "regex"
        self.encoding = None
        try:
            import tiktoken  # type: ignore
            self.encoding = tiktoken.get_encoding(encoding_name)
            self.method = f"tiktoken:{encoding_name}"
        except Exception:
            self.encoding = None

    def count(self, text: str) -> TokenStats:
        if self.encoding is not None:
            return TokenStats(len(self.encoding.encode(text)), self.method)
        tokens = re.findall(r"[A-Za-z_][A-Za-z_0-9]*|\d+\.\d+|\d+|[^\sA-Za-z_0-9]", text)
        return TokenStats(len(tokens), self.method)

def word_tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z_][a-zA-Z_0-9]{1,}", text.lower())
