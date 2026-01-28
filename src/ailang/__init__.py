"""
AILANG - A structured language for human-AI communication.

Example:
    from ailang import AILANG

    ai = AILANG(provider="openai", api_key="sk-...")

    # Natural language with output contracts
    result = ai.ask(
        "explain recursion",
        returns={
            "summary": str_(max=100),
            "example": code("python"),
        }
    )
    print(result.summary)

    # AILANG syntax for power users
    result = ai.run('summarize {text} !brief', text="Long article...")
"""

from ailang.contracts import (
    ContractError,
    ContractResult,
    OutputContract,
    bool_,
    code,
    enum,
    float_,
    int_,
    list_,
    optional,
    str_,
)
from ailang.core import AILANG
from ailang.parser import parse
from ailang.providers import get_provider
from ailang.transpiler import to_ailang, transpile

__version__ = "0.1.0"
__all__ = [
    # Main class
    "AILANG",
    # Parser & transpiler
    "parse",
    "transpile",
    "to_ailang",
    # Providers
    "get_provider",
    # Contract types
    "str_",
    "int_",
    "float_",
    "bool_",
    "code",
    "list_",
    "optional",
    "enum",
    # Contract classes
    "OutputContract",
    "ContractResult",
    "ContractError",
]
