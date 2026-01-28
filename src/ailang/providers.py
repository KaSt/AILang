"""
AILANG Providers - Adapters for various AI providers.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ProviderConfig:
    """Configuration for an AI provider."""

    api_key: str
    model: str = ""
    base_url: str | None = None
    temperature: float = 0.7
    max_tokens: int = 2000


class Provider(ABC):
    """Abstract base class for AI providers."""

    def __init__(self, config: ProviderConfig):
        self.config = config

    @abstractmethod
    async def complete(self, prompt: str) -> str:
        """Send a prompt and get a completion."""
        pass

    @abstractmethod
    async def complete_with_image(self, prompt: str) -> bytes:
        """Generate an image from a prompt."""
        pass


class OpenAIProvider(Provider):
    """OpenAI API provider (GPT-5.2, GPT-5.2-Codex, DALL-E)."""

    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        try:
            from openai import AsyncOpenAI

            self.client = AsyncOpenAI(
                api_key=config.api_key,
                base_url=config.base_url,
            )
        except ImportError:
            raise ImportError("OpenAI package required: pip install openai")

        self.model = config.model or "gpt-5.2"

    async def complete(self, prompt: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )
        return response.choices[0].message.content or ""

    async def complete_with_image(self, prompt: str) -> bytes:
        response = await self.client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # Download image
        import httpx

        async with httpx.AsyncClient() as client:
            url = response.data[0].url if response.data else None
            if not url:
                raise RuntimeError("No image URL returned")
            img_response = await client.get(url)
            return img_response.content


class AnthropicProvider(Provider):
    """Anthropic API provider (Claude)."""

    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        try:
            from anthropic import AsyncAnthropic

            self.client = AsyncAnthropic(api_key=config.api_key)
        except ImportError:
            raise ImportError("Anthropic package required: pip install anthropic")

        self.model = config.model or "claude-opus-4.5"

    async def complete(self, prompt: str) -> str:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=self.config.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        block = response.content[0]
        return block.text if hasattr(block, "text") else str(block)

    async def complete_with_image(self, prompt: str) -> bytes:
        raise NotImplementedError("Anthropic does not support image generation")


class OllamaProvider(Provider):
    """Ollama local provider."""

    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self.base_url = config.base_url or "http://localhost:11434"
        self.model = config.model or "llama2"

    async def complete(self, prompt: str) -> str:
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                },
                timeout=120.0,
            )
            return response.json()["response"]

    async def complete_with_image(self, prompt: str) -> bytes:
        raise NotImplementedError("Ollama does not support image generation")


class GoogleProvider(Provider):
    """Google Gemini provider."""

    def __init__(self, config: ProviderConfig):
        super().__init__(config)
        self.api_key = config.api_key
        self.model = config.model or "gemini-3-pro-preview"

    async def complete(self, prompt: str) -> str:
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent",
                params={"key": self.api_key},
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": self.config.temperature,
                        "maxOutputTokens": self.config.max_tokens,
                    },
                },
            )
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

    async def complete_with_image(self, prompt: str) -> bytes:
        raise NotImplementedError("Use Imagen API for Google image generation")


PROVIDERS = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "claude": AnthropicProvider,
    "ollama": OllamaProvider,
    "local": OllamaProvider,
    "google": GoogleProvider,
    "gemini": GoogleProvider,
}


def get_provider(name: str, config: ProviderConfig) -> Provider:
    """
    Get a provider instance by name.

    Args:
        name: Provider name (openai, anthropic, ollama, google)
        config: Provider configuration

    Returns:
        Provider instance

    Raises:
        ValueError: If provider is unknown
    """
    name = name.lower()
    if name not in PROVIDERS:
        raise ValueError(f"Unknown provider: {name}. Available: {list(PROVIDERS.keys())}")

    return PROVIDERS[name](config)
