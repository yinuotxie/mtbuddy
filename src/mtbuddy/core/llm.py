"""LLM provider abstractions."""

from __future__ import annotations


class DeterministicLLMProvider:
    """Test-safe provider used until DeepSeek/OpenClaw is configured."""

    name = "deterministic"

    def complete(self, prompt: str) -> str:
        first_line = prompt.strip().splitlines()[0] if prompt.strip() else ""
        return f"Deterministic completion: {first_line}"
