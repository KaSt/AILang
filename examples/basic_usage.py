"""
AILANG Examples - Basic usage patterns.
"""

from ailang import transpile, to_ailang, parse
from ailang import str_, int_, code, list_, optional, enum

# =============================================================================
# OUTPUT CONTRACTS - Type definitions demo (no API needed)
# =============================================================================

print("=== Output Contract Types ===\n")

# String with max length
summary_type = str_(max=100)
print(f"str_(max=100): {summary_type.to_prompt()}")

# Integer with range  
score_type = int_(min=0, max=10)
print(f"int_(min=0, max=10): {score_type.to_prompt()}")

# Code block
code_type = code("python")
print(f"code('python'): {code_type.to_prompt()}")

# List with item type
steps_type = list_(str_(), exactly=5)
print(f"list_(str_(), exactly=5): {steps_type.to_prompt()}")

# Optional field
warning_type = optional(str_())
print(f"optional(str_()): {warning_type.to_prompt()}")

# Enum
size_type = enum("small", "medium", "large")
print(f"enum(...): {size_type.to_prompt()}")

# =============================================================================
# OUTPUT CONTRACTS - Full contract demo
# =============================================================================

print("\n=== Output Contract Example ===\n")

from ailang.contracts import OutputContract

contract = OutputContract({
    "summary": str_(max=100),
    "steps": list_(str_()),
    "code_example": code("python"),
    "difficulty": enum("easy", "medium", "hard"),
    "prerequisites": optional(list_(str_())),
})

print("Contract prompt instructions:")
print(contract.to_prompt_instructions())

# =============================================================================
# AILANG SYNTAX - Transpile examples (no API needed)
# =============================================================================

print("\n=== AILANG Transpile Examples ===\n")

examples = [
    'write "birthday email for mom" !warm ~funny',
    'img "penguin drinking cola" !photo ^cinematic _text',
    'code "merge sort" [python] !typed !tested ^performance',
    'summarize {article} !brief ^key_points',
    'analyze {code} > fix !all > test[unit]',
    '@as "senior developer" { review {code} !honest ^security }',
]

for cmd in examples:
    print(f"AILANG:  {cmd}")
    print(f"PROMPT:  {transpile(cmd)}")
    print()

# =============================================================================
# REVERSE: Human prompt → AILANG
# =============================================================================

print("\n=== Reverse Examples ===\n")

prompts = [
    "Write a short professional email about the project update",
    "Generate a photorealistic image of a sunset, no text",
    "Create a Python function with type hints to sort a list",
]

for prompt in prompts:
    print(f"HUMAN:   {prompt}")
    print(f"AILANG:  {to_ailang(prompt)}")
    print()

# =============================================================================
# COMBINED USAGE (requires API key)
# =============================================================================

print("\n=== Combined Usage Example (requires API key) ===\n")

example_code = '''
from ailang import AILANG, str_, code, list_, optional

ai = AILANG(provider="openai")  # Uses OPENAI_API_KEY env var

# Natural language + output contract
result = ai.ask(
    "explain how async/await works in Python",
    returns={
        "summary": str_(max=100),
        "example": code("python"),
        "gotchas": list_(str_()),
        "see_also": optional(list_(str_())),
    },
    voice="casual"
)

print(result.summary)   # Guaranteed ≤100 chars
print(result.example)   # Clean Python code
print(result.gotchas)   # List of strings

# AILANG syntax for the same thing
result = ai.run('explain "async/await in Python" !example !gotchas ^practical')
'''
print(example_code)
