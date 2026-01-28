"""
AILANG Core - Main interface for executing AILANG commands.
"""

import asyncio
import os
from pathlib import Path
from typing import Any

import yaml

from ailang.contracts import (
    ContractError,
    ContractResult,
    OutputContract,
    TypeConstraint,
)
from ailang.parser import AILangAST, parse
from ailang.providers import ProviderConfig, get_provider
from ailang.transpiler import transpile


class AILANG:
    """
    Main AILANG interface for executing commands.

    Examples:
        # AILANG syntax (power users)
        ai = AILANG(provider="openai", api_key="sk-...")
        result = ai.run('write "haiku about coding"')

        # Natural language + output contracts (everyone)
        result = ai.ask(
            "explain recursion",
            returns={
                "summary": str_(max=100),
                "example": code("python"),
                "analogy": str_(),
            }
        )
        print(result.summary)  # Dot access to fields

        # With variables
        result = ai.run('summarize {text} !brief', text="Long article...")

        # Async usage
        result = await ai.run_async('explain "recursion" [eli5]')
    """

    def __init__(
        self,
        provider: str = "openai",
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
        config_path: str | None = None,
        **kwargs: Any,
    ):
        """
        Initialize AILANG.

        Args:
            provider: AI provider name (openai, anthropic, ollama, google)
            api_key: API key (or set via env var)
            model: Model name (provider-specific)
            base_url: Custom API endpoint URL (for OpenAI-compatible servers)
            config_path: Path to config file
            **kwargs: Additional provider options (temperature, max_tokens)

        Examples:
            # Standard OpenAI
            ai = AILANG(provider="openai", api_key="sk-...")

            # Custom OpenAI-compatible server (LM Studio, vLLM, LocalAI, etc.)
            ai = AILANG(
                provider="openai",
                base_url="http://localhost:1234/v1",
                api_key="not-needed",  # Some servers don't require this
                model="local-model"
            )

            # Azure OpenAI
            ai = AILANG(
                provider="openai",
                base_url="https://your-resource.openai.azure.com/openai/deployments/your-deployment",
                api_key="your-azure-key",
            )
        """
        self.provider_name = provider

        # Load config
        config = self._load_config(config_path)

        # Merge with explicit args
        api_key = api_key or config.get("api_key") or self._get_env_key(provider)
        model = model or config.get("model")
        base_url = base_url or config.get("base_url")

        if not api_key and provider not in ("ollama", "local"):
            raise ValueError(f"API key required for {provider}. Set via argument or env var.")

        self.provider_config = ProviderConfig(
            api_key=api_key or "",
            model=model or "",
            temperature=kwargs.get("temperature", config.get("temperature", 0.7)),
            max_tokens=kwargs.get("max_tokens", config.get("max_tokens", 2000)),
            base_url=base_url,
        )

        self._provider = None

    def _load_config(self, config_path: str | None) -> dict[str, Any]:
        """Load configuration from file."""
        paths = [
            config_path,
            os.environ.get("AILANG_CONFIG"),
            Path.home() / ".ailang" / "config.yaml",
            Path.home() / ".ailang" / "config.yml",
            Path("ailang.yaml"),
            Path("ailang.yml"),
        ]

        for path in paths:
            if path and Path(path).exists():
                with open(path) as f:
                    data = yaml.safe_load(f) or {}
                    # Extract provider-specific config
                    providers = data.get("providers", {})
                    provider_config = providers.get(self.provider_name, {})
                    defaults = data.get("defaults", {})
                    return {**defaults, **provider_config}

        return {}

    def _get_env_key(self, provider: str) -> str | None:
        """Get API key from environment variable."""
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "claude": "ANTHROPIC_API_KEY",
            "google": "GOOGLE_API_KEY",
            "gemini": "GOOGLE_API_KEY",
        }
        var_name = env_vars.get(provider)
        return os.environ.get(var_name) if var_name else None

    @property
    def provider(self):
        """Lazy-load provider."""
        if self._provider is None:
            self._provider = get_provider(self.provider_name, self.provider_config)
        return self._provider

    def run(self, command: str, **variables: str) -> str:
        """
        Execute an AILANG command synchronously.

        Args:
            command: AILANG command string
            **variables: Values for {variable} placeholders

        Returns:
            AI response string
        """
        return asyncio.run(self.run_async(command, **variables))

    async def run_async(self, command: str, **variables: str) -> str:
        """
        Execute an AILANG command asynchronously.

        Args:
            command: AILANG command string
            **variables: Values for {variable} placeholders

        Returns:
            AI response string
        """
        # Parse and transpile
        prompt = transpile(command, **variables)

        # Detect if image generation
        ast = parse(command)
        if ast.action in ("img", "logo", "icon", "image"):
            # Return image as bytes or save path
            image_data = await self.provider.complete_with_image(prompt)
            # For now, save and return path
            output_path = Path("output.png")
            output_path.write_bytes(image_data)
            return f"Image saved to: {output_path}"

        # Text completion
        return await self.provider.complete(prompt)

    def transpile_only(self, command: str, **variables: str) -> str:
        """
        Transpile command to natural language without executing.

        Args:
            command: AILANG command string
            **variables: Values for {variable} placeholders

        Returns:
            Natural language prompt
        """
        return transpile(command, **variables)

    def parse_only(self, command: str) -> AILangAST:
        """
        Parse command to AST without executing.

        Args:
            command: AILANG command string

        Returns:
            Parsed AST
        """
        return parse(command)

    # =========================================================================
    # Output Contracts API - Natural language with structured output
    # =========================================================================

    def ask(
        self,
        question: str,
        returns: dict[str, TypeConstraint],
        voice: str | None = None,
        **context: str,
    ) -> ContractResult:
        """
        Ask a question in natural language with a guaranteed output structure.

        Args:
            question: Natural language question/request
            returns: Output contract defining expected fields and types
            voice: Optional tone/style (e.g., "casual", "technical", "brief")
            **context: Additional context variables

        Returns:
            ContractResult with dot access to fields

        Examples:
            result = ai.ask(
                "explain how git rebase works",
                returns={
                    "tldr": str_(max=50),
                    "steps": list_(str_()),
                    "warning": optional(str_()),
                }
            )
            print(result.tldr)
            print(result.steps)
        """
        return asyncio.run(self.ask_async(question, returns, voice, **context))

    async def ask_async(
        self,
        question: str,
        returns: dict[str, TypeConstraint],
        voice: str | None = None,
        **context: str,
    ) -> ContractResult:
        """Async version of ask()."""
        contract = OutputContract(returns)

        # Build prompt
        prompt_parts = []

        # Add voice/style
        if voice:
            voice_instructions = {
                "casual": "Use a casual, friendly tone.",
                "formal": "Use a formal, professional tone.",
                "technical": "Use technical language appropriate for experts.",
                "simple": "Use simple language a beginner would understand.",
                "brief": "Be as brief as possible.",
                "detailed": "Be thorough and detailed.",
            }
            if voice in voice_instructions:
                prompt_parts.append(voice_instructions[voice])
            else:
                prompt_parts.append(f"Tone: {voice}.")

        # Add context
        for key, value in context.items():
            prompt_parts.append(f"{key}: {value}")

        # Add the question
        prompt_parts.append(question)

        # Add output contract instructions
        prompt_parts.append("")
        prompt_parts.append(contract.to_prompt_instructions())

        full_prompt = "\n\n".join(prompt_parts)

        # Execute
        response = await self.provider.complete(full_prompt)

        # Parse and validate against contract
        try:
            data = contract.parse_response(response)
            return ContractResult(_data=data, _raw=response)
        except ContractError:
            # Retry once with stricter instructions
            retry_prompt = full_prompt + "\n\nIMPORTANT: Return ONLY valid JSON, no explanations."
            response = await self.provider.complete(retry_prompt)
            data = contract.parse_response(response)
            return ContractResult(_data=data, _raw=response)

    def chain(
        self,
        *commands: str,
        returns: dict[str, TypeConstraint] | None = None,
        **variables: str,
    ) -> str | ContractResult:
        """
        Chain multiple AILANG commands together.

        Args:
            *commands: AILANG commands to execute in sequence
            returns: Optional output contract for final result
            **variables: Variables for the first command

        Returns:
            Final result (str or ContractResult if returns specified)

        Example:
            result = ai.chain(
                'analyze {code} ^security',
                'fix !all',
                'test [pytest]',
                code=my_code,
                returns={"fixed": code("python"), "tests": code("python")}
            )
        """
        return asyncio.run(self.chain_async(*commands, returns=returns, **variables))

    async def chain_async(
        self,
        *commands: str,
        returns: dict[str, TypeConstraint] | None = None,
        **variables: str,
    ) -> str | ContractResult:
        """Async version of chain()."""
        # Execute commands in sequence, passing output as {input} to next
        result = ""
        current_vars = variables.copy()

        for i, command in enumerate(commands):
            if i > 0:
                current_vars["input"] = result
                current_vars["previous"] = result

            prompt = transpile(command, **current_vars)

            # For last command, add output contract if specified
            if i == len(commands) - 1 and returns:
                contract = OutputContract(returns)
                prompt += "\n\n" + contract.to_prompt_instructions()
                response = await self.provider.complete(prompt)
                data = contract.parse_response(response)
                return ContractResult(_data=data, _raw=response)

            result = await self.provider.complete(prompt)

        return result
