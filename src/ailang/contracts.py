"""
AILANG Output Contracts - Define what you want back from AI.

Example:
    from ailang import ai
    from ailang.contracts import str, code, list

    result = ai.ask(
        "explain recursion",
        returns={
            "summary": str(max=100),
            "example": code("python"),
            "steps": list[str],
        }
    )
    print(result.summary)  # Guaranteed to be ≤100 chars
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

# =============================================================================
# Type Definitions
# =============================================================================


@dataclass
class TypeConstraint:
    """Base class for output type constraints."""

    _type_name: str = ""

    def to_prompt(self) -> str:
        """Convert to natural language for the prompt."""
        raise NotImplementedError

    def validate(self, value: Any) -> bool:
        """Validate a value against this constraint."""
        raise NotImplementedError

    def parse(self, value: Any) -> Any:
        """Parse/coerce a value to this type."""
        return value


@dataclass
class Str(TypeConstraint):
    """String output with optional constraints."""

    max: int | None = None
    min: int | None = None
    pattern: str | None = None  # regex

    _type_name: str = "str"

    def to_prompt(self) -> str:
        parts = ["text"]
        if self.max:
            parts.append(f"(maximum {self.max} characters)")
        if self.min:
            parts.append(f"(minimum {self.min} characters)")
        return " ".join(parts)

    def validate(self, value: Any) -> bool:
        if not isinstance(value, str):
            return False
        if self.max and len(value) > self.max:
            return False
        if self.min and len(value) < self.min:
            return False
        if self.pattern and not re.match(self.pattern, value):
            return False
        return True

    def parse(self, value: Any) -> str:
        s = str(value)
        if self.max and len(s) > self.max:
            s = s[: self.max - 3] + "..."
        return s


@dataclass
class Int(TypeConstraint):
    """Integer output with optional constraints."""

    min: int | None = None
    max: int | None = None

    _type_name: str = "int"

    def to_prompt(self) -> str:
        parts = ["integer number"]
        if self.min is not None and self.max is not None:
            parts.append(f"(between {self.min} and {self.max})")
        elif self.min is not None:
            parts.append(f"(minimum {self.min})")
        elif self.max is not None:
            parts.append(f"(maximum {self.max})")
        return " ".join(parts)

    def validate(self, value: Any) -> bool:
        try:
            v = int(value)
            if self.min is not None and v < self.min:
                return False
            if self.max is not None and v > self.max:
                return False
            return True
        except (ValueError, TypeError):
            return False

    def parse(self, value: Any) -> int:
        return int(value)


@dataclass
class Float(TypeConstraint):
    """Float output with optional constraints."""

    min: float | None = None
    max: float | None = None
    precision: int | None = None

    _type_name: str = "float"

    def to_prompt(self) -> str:
        parts = ["decimal number"]
        if self.precision:
            parts.append(f"(to {self.precision} decimal places)")
        return " ".join(parts)

    def validate(self, value: Any) -> bool:
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False

    def parse(self, value: Any) -> float:
        v = float(value)
        if self.precision:
            v = round(v, self.precision)
        return v


@dataclass
class Bool(TypeConstraint):
    """Boolean output."""

    _type_name: str = "bool"

    def to_prompt(self) -> str:
        return "boolean (true/false)"

    def validate(self, value: Any) -> bool:
        if isinstance(value, bool):
            return True
        if isinstance(value, str):
            return value.lower() in ("true", "false", "yes", "no", "1", "0")
        return False

    def parse(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ("true", "yes", "1")
        return bool(value)


@dataclass
class Code(TypeConstraint):
    """Code output in a specific language."""

    language: str = "python"

    _type_name: str = "code"

    def to_prompt(self) -> str:
        return f"code in {self.language} (just the code, no markdown fences)"

    def validate(self, value: Any) -> bool:
        return isinstance(value, str)

    def parse(self, value: Any) -> str:
        s = str(value)
        # Strip markdown code fences if present
        s = re.sub(r"^```\w*\n?", "", s)
        s = re.sub(r"\n?```$", "", s)
        return s.strip()


@dataclass
class List_(TypeConstraint):
    """List output with optional item type and count."""

    item_type: TypeConstraint | None = None
    min_items: int | None = None
    max_items: int | None = None
    exact_items: int | None = None

    _type_name: str = "list"

    def to_prompt(self) -> str:
        parts = ["list"]
        if self.exact_items:
            parts.append(f"of exactly {self.exact_items} items")
        elif self.min_items and self.max_items:
            parts.append(f"of {self.min_items}-{self.max_items} items")
        elif self.min_items:
            parts.append(f"of at least {self.min_items} items")
        elif self.max_items:
            parts.append(f"of at most {self.max_items} items")

        if self.item_type:
            parts.append(f"where each item is {self.item_type.to_prompt()}")

        return " ".join(parts)

    def validate(self, value: Any) -> bool:
        if not isinstance(value, list):
            return False
        if self.exact_items and len(value) != self.exact_items:
            return False
        if self.min_items and len(value) < self.min_items:
            return False
        if self.max_items and len(value) > self.max_items:
            return False
        if self.item_type:
            return all(self.item_type.validate(item) for item in value)
        return True

    def parse(self, value: Any) -> list:
        if isinstance(value, str):
            # Try to parse as JSON
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                # Split by newlines or commas
                value = [v.strip() for v in re.split(r"[\n,]", value) if v.strip()]

        if self.item_type:
            return [self.item_type.parse(item) for item in value]
        return list(value)


@dataclass
class Optional_(TypeConstraint):
    """Optional output (can be null/None)."""

    inner_type: TypeConstraint = field(default_factory=lambda: Str())

    _type_name: str = "optional"

    def to_prompt(self) -> str:
        return f"{self.inner_type.to_prompt()} (or null if not applicable)"

    def validate(self, value: Any) -> bool:
        if value is None:
            return True
        return self.inner_type.validate(value)

    def parse(self, value: Any) -> Any:
        if value is None or value == "null" or value == "":
            return None
        return self.inner_type.parse(value)


@dataclass
class Enum_(TypeConstraint):
    """Enum output - one of specific values."""

    choices: list[str] = field(default_factory=list)

    _type_name: str = "enum"

    def to_prompt(self) -> str:
        return f"one of: {', '.join(self.choices)}"

    def validate(self, value: Any) -> bool:
        return str(value) in self.choices

    def parse(self, value: Any) -> str:
        return str(value)


# =============================================================================
# Convenience constructors (lowercase, like typing module)
# =============================================================================


def str_(max: int | None = None, min: int | None = None, pattern: str | None = None) -> Str:
    """String type with constraints."""
    return Str(max=max, min=min, pattern=pattern)


def int_(min: int | None = None, max: int | None = None) -> Int:
    """Integer type with constraints."""
    return Int(min=min, max=max)


def float_(
    min: float | None = None,
    max: float | None = None,
    precision: int | None = None,
) -> Float:
    """Float type with constraints."""
    return Float(min=min, max=max, precision=precision)


def bool_() -> Bool:
    """Boolean type."""
    return Bool()


def code(language: str = "python") -> Code:
    """Code type in a specific language."""
    return Code(language=language)


def list_(
    item_type: TypeConstraint | None = None,
    min: int | None = None,
    max: int | None = None,
    exactly: int | None = None,
) -> List_:
    """List type with constraints."""
    return List_(item_type=item_type, min_items=min, max_items=max, exact_items=exactly)


def optional(inner_type: TypeConstraint) -> Optional_:
    """Optional (nullable) type."""
    return Optional_(inner_type=inner_type)


def enum(*choices: str) -> Enum_:
    """Enum type - one of the given choices."""
    return Enum_(choices=list(choices))


# =============================================================================
# Output Contract
# =============================================================================


@dataclass
class OutputContract:
    """
    Defines the expected structure of an AI response.

    Example:
        contract = OutputContract({
            "summary": str_(max=100),
            "steps": list_(str_()),
            "code": code("python"),
        })
    """

    schema: dict[str, TypeConstraint]

    def to_prompt_instructions(self) -> str:
        """Generate prompt instructions for the output format."""
        lines = ["Respond with a JSON object containing exactly these fields:", ""]
        for name, type_constraint in self.schema.items():
            lines.append(f'- "{name}": {type_constraint.to_prompt()}')

        lines.extend(["", "Return ONLY the JSON object, no other text or markdown."])
        return "\n".join(lines)

    def parse_response(self, response: str) -> dict[str, Any]:
        """Parse and validate an AI response against the contract."""
        # Try to extract JSON from response
        response = response.strip()

        # Handle markdown code blocks
        if response.startswith("```"):
            response = re.sub(r"^```\w*\n?", "", response)
            response = re.sub(r"\n?```$", "", response)

        try:
            data = json.loads(response)
        except json.JSONDecodeError as e:
            raise ContractError(f"Response is not valid JSON: {e}")

        if not isinstance(data, dict):
            raise ContractError(f"Response must be a JSON object, got {type(data).__name__}")

        # Validate and parse each field
        result = {}
        for name, type_constraint in self.schema.items():
            if name not in data:
                if isinstance(type_constraint, Optional_):
                    result[name] = None
                    continue
                raise ContractError(f"Missing required field: {name}")

            value = data[name]
            if not type_constraint.validate(value):
                raise ContractError(
                    f"Field '{name}' failed validation: "
                    f"expected {type_constraint.to_prompt()}, got {value!r}"
                )
            result[name] = type_constraint.parse(value)

        return result


class ContractError(Exception):
    """Raised when a response doesn't match its contract."""

    pass


@dataclass
class ContractResult:
    """Result of an AI call with a contract - provides dot access to fields."""

    _data: dict[str, Any]
    _raw: str = ""

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            return super().__getattribute__(name)
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"No field '{name}' in result")

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def to_dict(self) -> dict[str, Any]:
        return self._data.copy()

    def __repr__(self) -> str:
        return f"ContractResult({self._data})"


# =============================================================================
# Exports
# =============================================================================

__all__ = [
    # Type constructors
    "str_",
    "int_",
    "float_",
    "bool_",
    "code",
    "list_",
    "optional",
    "enum",
    # Classes
    "TypeConstraint",
    "OutputContract",
    "ContractResult",
    "ContractError",
    # Type classes (for isinstance checks)
    "Str",
    "Int",
    "Float",
    "Bool",
    "Code",
    "List_",
    "Optional_",
    "Enum_",
]
