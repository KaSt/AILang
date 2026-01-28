# API Reference

## Python Library

### AILANG Class

The main interface for executing AILANG commands.

```python
from ailang import AILANG

# Standard OpenAI
ai = AILANG(
    provider="openai",      # Provider: openai, anthropic, ollama, google
    api_key="sk-...",       # API key (or use env var)
    model="gpt-5.2",        # Model name (optional)
    temperature=0.7,        # Temperature (optional)
    max_tokens=2000,        # Max tokens (optional)
)

# Custom OpenAI-compatible server (LM Studio, vLLM, LocalAI, text-generation-webui, etc.)
ai = AILANG(
    provider="openai",
    base_url="http://localhost:1234/v1",  # Your server's OpenAI-compatible endpoint
    api_key="not-needed",                  # Some servers don't require this
    model="local-model",
)

# Azure OpenAI
ai = AILANG(
    provider="openai",
    base_url="https://your-resource.openai.azure.com/openai/deployments/your-deployment",
    api_key="your-azure-api-key",
)

# Ollama (local)
ai = AILANG(
    provider="ollama",
    base_url="http://localhost:11434",  # Default Ollama URL
    model="llama2",
)
```

---

## Output Contracts API (Recommended)

### `ask(question, returns, voice=None, **context) -> ContractResult`

Ask a question in natural language with guaranteed output structure.

```python
from ailang import AILANG, str_, int_, code, list_, optional

ai = AILANG(provider="openai")

result = ai.ask(
    "explain how git rebase works",
    returns={
        "tldr": str_(max=50),
        "steps": list_(str_()),
        "example": code("bash"),
        "warning": optional(str_()),
    },
    voice="casual"  # optional: casual, formal, technical, simple, brief, detailed
)

# Dot access to fields
print(result.tldr)      # "Replays commits onto another branch"
print(result.steps)     # ["checkout target", "run rebase", ...]
print(result.example)   # "git rebase main"
print(result.warning)   # "Don't rebase public branches" or None

# Also supports dict access
print(result["tldr"])
print(result.to_dict())
```

### `ask_async(...)` 

Async version of `ask()`.

```python
result = await ai.ask_async("explain recursion", returns={"summary": str_()})
```

### `chain(*commands, returns=None, **variables) -> str | ContractResult`

Chain multiple AILANG commands, optionally with output contract.

```python
result = ai.chain(
    'analyze {code} ^security',
    'fix !all', 
    'test [pytest]',
    code=my_code,
    returns={
        "fixed_code": code("python"),
        "tests": code("python"),
        "issues_found": int_(),
    }
)
print(result.fixed_code)
print(result.issues_found)
```

---

## Output Contract Types

```python
from ailang import str_, int_, float_, bool_, code, list_, optional, enum
```

| Type | Description | Example |
|------|-------------|---------|
| `str_()` | String | `str_(max=100, min=10)` |
| `int_()` | Integer | `int_(min=0, max=10)` |
| `float_()` | Float | `float_(precision=2)` |
| `bool_()` | Boolean | `bool_()` |
| `code()` | Code block | `code("python")`, `code("javascript")` |
| `list_()` | List | `list_(str_())`, `list_(int_(), exactly=5)` |
| `optional()` | Nullable | `optional(str_())` |
| `enum()` | One of choices | `enum("small", "medium", "large")` |

---

## AILANG Syntax API

### `run(command, **variables) -> str`

Execute an AILANG command synchronously.

```python
result = ai.run('write "haiku about coding"')
result = ai.run('summarize {text} !brief', text="Long article...")
```

### `run_async(command, **variables) -> str`

Execute an AILANG command asynchronously.

```python
result = await ai.run_async('explain "recursion" [eli5]')
```

### `transpile_only(command, **variables) -> str`

Convert to natural language without executing.

```python
prompt = ai.transpile_only('code "sort" [python] !typed')
# Returns: "Write code for sort. Use python. Include type annotations."
```

### `parse_only(command) -> AILangAST`

Parse to AST without executing.

```python
ast = ai.parse_only('write "hello" !short')
print(ast.action)  # "write"
print(ast.must)    # ["short"]
```

---

## Standalone Functions

```python
from ailang import parse, transpile, to_ailang

# Parse to AST
ast = parse('code "sort" [python]')

# Transpile to natural language
prompt = transpile('img "sunset" !photo')

# Reverse: natural language to AILANG
cmd = to_ailang("Write a short professional email")
```

---

## REST API

Start the server:

```bash
ailang serve --port 8000
```

### Endpoints

#### `POST /run`

Execute an AILANG command.

**Request:**
```json
{
  "command": "write \"haiku\" !traditional",
  "variables": {},
  "provider": "openai",
  "model": "gpt-5.2",
  "api_key": "sk-..."
}
```

**Response:**
```json
{
  "result": "Code compiles clean\nBugs emerge from the shadows\nStack overflow saves",
  "prompt": "Write haiku. Must be traditional.",
  "provider": "openai"
}
```

---

#### `POST /transpile`

Convert AILANG to natural language.

**Request:**
```json
{
  "command": "code \"sort\" [python] !typed ^fast",
  "variables": {}
}
```

**Response:**
```json
{
  "prompt": "Write code for sort. Use python. Include type annotations. Optimize for speed.",
  "ast": {
    "action": "code",
    "subject": "sort",
    "specifiers": ["python"],
    "must": ["typed"],
    "priority": ["fast"],
    "avoid": []
  },
  "warnings": []
}
```

---

#### `POST /reverse`

Convert natural language to AILANG.

**Request:**
```json
{
  "prompt": "Write a short professional email about the meeting"
}
```

**Response:**
```json
{
  "command": "write \"email about the meeting\" !short !professional"
}
```

---

#### `GET /commands`

List all available commands.

**Response:**
```json
{
  "categories": {
    "text": ["write", "rewrite", "summarize", ...],
    "image": ["img", "logo", "icon", ...],
    "code": ["code", "fix", "refactor", ...],
    ...
  },
  "total": 50
}
```

---

#### `GET /modifiers`

List all available modifiers.

**Response:**
```json
{
  "must (!)": ["short", "detailed", "typed", ...],
  "priority (^)": ["fast", "quality", "security", ...],
  "avoid (_)": ["verbose", "jargon", "emoji", ...]
}
```

---

#### `GET /health`

Health check.

**Response:**
```json
{
  "status": "ok"
}
```

---

## CLI

```bash
# Execute AILANG command
ailang 'write "haiku"'

# Transpile only (see the prompt without executing)
ailang --transpile-only 'code "sort" [python] !typed'

# Parse only (see the AST)
ailang --parse-only 'write "hello" !short'

# Interactive mode
ailang --interactive

# Start API server
ailang serve --port 8000

# Reverse (human prompt to AILANG)
ailang reverse "Write a short professional email"

# Provider options
ailang --provider anthropic 'explain "AI"'
ailang --model gpt-5.2 'code "api" [python]'
```

### Interactive Mode Commands

```
ailang> write "hello" !short          # Execute AILANG
ailang> !transpile                     # Toggle transpile-only mode
ailang> !provider anthropic            # Switch provider
ailang> !to_ailang Write a short email # Convert human to AILANG
ailang> !help                          # Show help
ailang> !exit                          # Exit
```
