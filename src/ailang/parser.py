"""
AILANG Parser - Converts AILANG syntax to AST.
"""

import re
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class AILangAST:
    """Abstract Syntax Tree for an AILANG command."""

    action: str
    subject: str = ""
    specifiers: list[str] = field(default_factory=list)
    must: list[str] = field(default_factory=list)  # ! modifiers
    maybe: list[str] = field(default_factory=list)  # ~ modifiers
    priority: list[str] = field(default_factory=list)  # ^ modifiers
    avoid: list[str] = field(default_factory=list)  # _ modifiers
    chain: Optional["AILangAST"] = None  # > chained command
    parallel: list[str] = field(default_factory=list)  # & parallel outputs
    persona: str | None = None  # @as context
    variables: dict[str, str] = field(default_factory=dict)  # {var} placeholders


class ParseError(Exception):
    """Raised when AILANG syntax is invalid."""

    pass


def parse(command: str) -> AILangAST:
    """
    Parse an AILANG command string into an AST.

    Args:
        command: AILANG command string

    Returns:
        AILangAST representing the parsed command

    Raises:
        ParseError: If the syntax is invalid

    Examples:
        >>> ast = parse('write "hello" !short')
        >>> ast.action
        'write'
        >>> ast.must
        ['short']

        >>> ast = parse('code "sort" [python] !typed ^fast')
        >>> ast.specifiers
        ['python']
        >>> ast.priority
        ['fast']
    """
    command = command.strip()

    # Handle @as persona blocks
    persona = None
    persona_match = re.match(r'@as\s+"([^"]+)"\s*\{(.+)\}', command, re.DOTALL)
    if persona_match:
        persona = persona_match.group(1)
        command = persona_match.group(2).strip()

    # Handle chains (split by >)
    chain_parts = _split_chain(command)

    if len(chain_parts) > 1:
        # Parse first part, then recursively parse the rest
        ast = _parse_single(chain_parts[0])
        ast.persona = persona
        ast.chain = parse(" > ".join(chain_parts[1:]))
        return ast

    ast = _parse_single(command)
    ast.persona = persona
    return ast


def _split_chain(command: str) -> list[str]:
    """Split command by > while respecting quotes and brackets."""
    parts = []
    current = ""
    depth = 0
    in_quotes = False

    i = 0
    while i < len(command):
        char = command[i]

        if char == '"' and (i == 0 or command[i - 1] != "\\"):
            in_quotes = not in_quotes
            current += char
        elif char in "[{(" and not in_quotes:
            depth += 1
            current += char
        elif char in "]})" and not in_quotes:
            depth -= 1
            current += char
        elif char == ">" and depth == 0 and not in_quotes:
            parts.append(current.strip())
            current = ""
        else:
            current += char
        i += 1

    if current.strip():
        parts.append(current.strip())

    return parts


def _parse_single(command: str) -> AILangAST:
    """Parse a single AILANG command (no chains)."""

    # Extract action (first word)
    action_match = re.match(r"^(\w+)", command)
    if not action_match:
        raise ParseError(f"Could not find action in: {command}")

    action = action_match.group(1)
    rest = command[len(action) :].strip()

    # Extract subject (quoted string or {variable})
    subject = ""
    subject_match = re.match(r'^"([^"]*)"', rest)
    if subject_match:
        subject = subject_match.group(1)
        rest = rest[len(subject_match.group(0)) :].strip()
    else:
        var_match = re.match(r"^\{(\w+)\}", rest)
        if var_match:
            subject = f"{{{var_match.group(1)}}}"
            rest = rest[len(var_match.group(0)) :].strip()

    # Extract specifiers [x] [y]
    specifiers = re.findall(r"\[([^\]]+)\]", rest)

    # Extract modifiers
    must = re.findall(r"!(\w+)", rest)
    maybe = re.findall(r"~(\w+)", rest)
    priority = re.findall(r"\^(\w+)", rest)
    avoid = re.findall(r"_(\w+)", rest)

    # Extract parallel outputs (& separated)
    parallel = []
    parallel_match = re.search(r"&\s*(\w+(?:\s*&\s*\w+)*)", rest)
    if parallel_match:
        parallel = [p.strip() for p in parallel_match.group(0).split("&") if p.strip()]

    # Extract variables {name}
    variables = {}
    for var in re.findall(r"\{(\w+)\}", command):
        variables[var] = ""

    return AILangAST(
        action=action,
        subject=subject,
        specifiers=specifiers,
        must=must,
        maybe=maybe,
        priority=priority,
        avoid=avoid,
        parallel=parallel,
        variables=variables,
    )


def validate(ast: AILangAST) -> list[str]:
    """
    Validate an AST and return any warnings.

    Args:
        ast: Parsed AILANG AST

    Returns:
        List of warning messages (empty if valid)
    """
    warnings = []

    valid_actions = {
        "write",
        "rewrite",
        "summarize",
        "expand",
        "translate",
        "explain",
        "list",
        "compare",
        "reply",
        "title",
        "img",
        "edit_img",
        "describe_img",
        "style",
        "logo",
        "icon",
        "diagram",
        "mockup",
        "code",
        "fix",
        "refactor",
        "test",
        "review",
        "convert",
        "api",
        "query",
        "regex",
        "docs",
        "analyze",
        "evaluate",
        "predict",
        "diagnose",
        "recommend",
        "rank",
        "verify",
        "extract",
        "classify",
        "sentiment",
        "brainstorm",
        "name",
        "story",
        "joke",
        "poem",
        "script",
        "pitch",
        "slogan",
        "recipe",
        "playlist",
        "format",
        "merge",
        "split",
        "filter",
        "sort",
        "dedupe",
        "validate",
        "map",
        "template",
        "parse",
        "research",
        "plan",
        "generate",
    }

    if ast.action not in valid_actions:
        sample = ", ".join(sorted(valid_actions)[:5])
        warnings.append(f"Unknown action '{ast.action}'. Did you mean one of: {sample}...?")

    if not ast.subject and ast.action not in {"list", "brainstorm"}:
        warnings.append(f"Action '{ast.action}' typically requires a subject.")

    return warnings
