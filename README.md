# AILANG

> **The language between humans and AI. Write less. Mean more.**

Two ways to get exactly what you want from AI:

```python
from ailang import AILANG, str_, code, list_

ai = AILANG(provider="openai")

# 🎯 Natural language + Output contracts (recommended)
result = ai.ask(
    "explain how git rebase works",
    returns={
        "tldr": str_(max=50),
        "steps": list_(str_()),
        "warning": str_(),
    }
)
print(result.tldr)    # "Replays your commits onto another branch tip"
print(result.steps)   # ["checkout target", "run rebase", "resolve conflicts"]

# ⚡ AILANG syntax (power users & automation)
result = ai.run('explain "git rebase" !brief !steps ^practical')
```

## Why AILANG?

| Problem | Solution |
|---------|----------|
| "AI gives unpredictable output formats" | **Output contracts** guarantee structure |
| "My prompts are verbose and inconsistent" | **AILANG syntax** is terse and reproducible |
| "I don't know what I'll get back" | **Type constraints** validate responses |
| "Prompt engineering is a dark art" | **Both approaches** are learnable in minutes |

## Quick Start

### Installation

```bash
pip install ailang
```

### Natural Language + Output Contracts

The easiest way — speak naturally, get structured data:

```python
from ailang import AILANG, str_, int_, code, list_, optional

ai = AILANG(provider="openai")  # Uses OPENAI_API_KEY env var

# Simple ask
result = ai.ask(
    "what's the capital of France?",
    returns={"answer": str_(), "population": int_()}
)
print(result.answer)      # "Paris"
print(result.population)  # 2161000

# With constraints
result = ai.ask(
    "write a function to check if a number is prime",
    returns={
        "code": code("python"),
        "explanation": str_(max=100),
        "time_complexity": str_(),
    }
)
print(result.code)  # Clean Python code, guaranteed

# With tone/style
result = ai.ask(
    "explain quantum entanglement",
    returns={"explanation": str_(), "analogy": str_()},
    voice="casual"  # or "technical", "brief", "formal"
)
```

### AILANG Syntax (Power Users)

Terse commands for automation and power users:

```python
# Direct execution
result = ai.run('write "haiku about coding" !traditional')

# With variables
result = ai.run('summarize {text} !brief ^key_points', text=long_article)

# Chained operations
result = ai.chain(
    'analyze {code} ^security',
    'fix !all',
    'test [pytest]',
    code=my_code,
    returns={"fixed": code("python"), "tests": code("python")}
)
```

### CLI

```bash
# Execute AILANG
ailang 'write "hello world" !short'

# See the generated prompt
ailang --transpile-only 'code "sort" [python] !typed'

# Interactive mode
ailang --interactive

# Start API server
ailang serve --port 8000
```

## Output Contract Types

| Type | Description | Example |
|------|-------------|---------|
| `str_()` | String | `str_(max=100)` |
| `int_()` | Integer | `int_(min=0, max=10)` |
| `float_()` | Float | `float_(precision=2)` |
| `bool_()` | Boolean | `bool_()` |
| `code()` | Code block | `code("python")` |
| `list_()` | List | `list_(str_(), exactly=5)` |
| `optional()` | Nullable | `optional(str_())` |
| `enum()` | One of | `enum("small", "medium", "large")` |

## AILANG Syntax

```
ACTION "subject" [specifier] modifiers
```

| Symbol | Meaning | Example |
|--------|---------|---------|
| `!` | must have | `!short` `!typed` `!photo` |
| `~` | nice to have | `~funny` `~examples` |
| `^` | prioritize | `^speed` `^quality` |
| `_` | avoid | `_verbose` `_emoji` |
| `>` | then do | `write > translate[fr]` |
| `&` | and also | `title & summary` |
| `[x]` | specify | `[python]` `[formal]` |

### Common Commands

| Category | Commands |
|----------|----------|
| **Text** | `write` `rewrite` `summarize` `expand` `translate` `explain` |
| **Image** | `img` `logo` `icon` `diagram` `mockup` |
| **Code** | `code` `fix` `refactor` `test` `review` `convert` |
| **Analysis** | `analyze` `compare` `evaluate` `recommend` `extract` |
| **Creative** | `brainstorm` `name` `story` `pitch` `slogan` |

## Examples

```ailang
# Write code with tests
code "merge sort" [rust] !typed !tested ^performance

# Generate and refine an image
img "cyberpunk city" !art [neon] ^detailed _people

# Analyze then act
analyze {code} > fix !all > test[unit]

# Multi-output
write "product launch" > title & summary & tweet

# With persona
@as "senior developer" { review {code} !honest ^security }
```

## Configuration

Create `~/.ailang/config.yaml`:

```yaml
default_provider: openai
providers:
  openai:
    api_key: ${OPENAI_API_KEY}
    model: gpt-5.2
  anthropic:
    api_key: ${ANTHROPIC_API_KEY}
    model: claude-opus-4.5
  
  # Custom OpenAI-compatible server (LM Studio, vLLM, LocalAI, etc.)
  local:
    base_url: http://localhost:1234/v1
    api_key: not-needed
    model: local-model
  
  # Azure OpenAI
  azure:
    base_url: https://your-resource.openai.azure.com/openai/deployments/your-deployment
    api_key: ${AZURE_OPENAI_KEY}
  
defaults:
  temperature: 0.7
  max_tokens: 2000
```

Or use environment variables:

```bash
export AILANG_PROVIDER=openai
export OPENAI_API_KEY=sk-...
```

## Supported Providers

- ✅ OpenAI (GPT-5.2, GPT-5.2-Codex)
- ✅ Anthropic (Claude Opus 4.5)
- ✅ Google (Gemini 3 Pro)
- ✅ Local (Ollama, LM Studio)
- ✅ Azure OpenAI
- 🔜 Mistral
- 🔜 Cohere

## Documentation

- [Full Specification](docs/SPECIFICATION.md) - Complete syntax reference
- [Command Dictionary](docs/COMMANDS.md) - All commands with examples
- [API Reference](docs/API.md) - Library and REST API docs
- [Examples](examples/) - Real-world usage patterns

## How It Works

1. **Parse**: AILANG syntax is parsed into an AST
2. **Transpile**: AST is converted to optimized natural language prompt
3. **Execute**: Prompt is sent to your chosen AI provider
4. **Return**: Response is returned (optionally post-processed)

```python
# What happens under the hood
"code 'sort' [python] !typed ^fast"
        ↓ parse
{action: "code", subject: "sort", spec: "python", 
 must: ["typed"], priority: ["fast"]}
        ↓ transpile  
"Write a Python function to sort. Include type hints. 
 Optimize for performance. Return only the code."
        ↓ execute
# Sent to OpenAI/Anthropic/etc.
```

## Contributing

```bash
git clone https://github.com/yourusername/ailang
cd ailang
pip install -e ".[dev]"
pytest
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE)

---

**AILANG** - Stop prompting. Start commanding.
