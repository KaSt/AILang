"""
AILANG Examples - Working with different providers.
"""

import asyncio
from ailang import AILANG

# =============================================================================
# OpenAI
# =============================================================================

async def openai_example():
    """Using OpenAI (GPT-5.2)."""
    ai = AILANG(
        provider="openai",
        # api_key="sk-...",  # Or set OPENAI_API_KEY env var
        model="gpt-5.2",
    )
    
    # Simple write
    result = await ai.run_async('write "startup pitch" [elevator] !60sec ^problem_solution')
    print("OpenAI result:", result[:200], "...")

# =============================================================================
# Anthropic (Claude)
# =============================================================================

async def anthropic_example():
    """Using Anthropic (Claude Opus 4.5)."""
    ai = AILANG(
        provider="anthropic",
        # api_key="sk-ant-...",  # Or set ANTHROPIC_API_KEY env var
        model="claude-opus-4.5",
    )
    
    result = await ai.run_async('explain "quantum entanglement" [eli5] !analogies')
    print("Claude result:", result[:200], "...")

# =============================================================================
# Ollama (Local)
# =============================================================================

async def ollama_example():
    """Using Ollama for local inference."""
    ai = AILANG(
        provider="ollama",
        model="llama2",
        base_url="http://localhost:11434",  # Default Ollama URL
    )
    
    result = await ai.run_async('code "hello world" [python]')
    print("Ollama result:", result)

# =============================================================================
# Custom OpenAI-Compatible Server (LM Studio, vLLM, LocalAI, etc.)
# =============================================================================

async def custom_openai_server_example():
    """Using any OpenAI-compatible API server."""
    ai = AILANG(
        provider="openai",  # Use openai provider with custom base_url
        base_url="http://localhost:1234/v1",  # LM Studio, vLLM, LocalAI, etc.
        api_key="not-needed",  # Many local servers don't require API key
        model="local-model",   # Model name as configured in your server
    )
    
    result = await ai.run_async('explain "recursion" !brief')
    print("Local server result:", result)

# =============================================================================
# Azure OpenAI
# =============================================================================

async def azure_openai_example():
    """Using Azure OpenAI."""
    ai = AILANG(
        provider="openai",
        base_url="https://your-resource.openai.azure.com/openai/deployments/your-deployment",
        api_key="your-azure-api-key",  # Or set AZURE_OPENAI_KEY env var
    )
    
    result = await ai.run_async('write "hello" !short')
    print("Azure OpenAI result:", result)

# =============================================================================
# Google Gemini
# =============================================================================

async def google_example():
    """Using Google Gemini 3."""
    ai = AILANG(
        provider="google",
        # api_key="...",  # Or set GOOGLE_API_KEY env var
        model="gemini-3-pro-preview",
    )
    
    result = await ai.run_async('list "creative date ideas" [10] !unique ^budget_friendly')
    print("Gemini result:", result[:200], "...")

# =============================================================================
# Configuration File
# =============================================================================

# Create ~/.ailang/config.yaml:
"""
default_provider: openai

providers:
  openai:
    api_key: ${OPENAI_API_KEY}
    model: gpt-5.2
    
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    model: claude-opus-4.5
    
  ollama:
    base_url: http://localhost:11434
    model: llama2

defaults:
  temperature: 0.7
  max_tokens: 2000
"""

# Then just:
# ai = AILANG()  # Uses config file
# ai = AILANG(provider="anthropic")  # Override provider


if __name__ == "__main__":
    # Uncomment to run examples (requires API keys):
    # asyncio.run(openai_example())
    # asyncio.run(anthropic_example())
    # asyncio.run(ollama_example())
    # asyncio.run(google_example())
    
    print("Provider examples ready. Set API keys and uncomment to run.")
