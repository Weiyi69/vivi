from typing import Protocol


class AiUnavailableError(RuntimeError):
    pass


class AiProvider(Protocol):
    async def generate(self, prompt: str) -> str:
        """Generate text for a future learning feature."""


class UnavailableAiProvider:
    async def generate(self, prompt: str) -> str:
        raise AiUnavailableError("AI inference is not configured")
