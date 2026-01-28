"""
AILANG Tests - Output contracts tests.
"""

import pytest

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


class TestTypeConstraints:
    """Test individual type constraints."""

    def test_str_basic(self):
        t = str_()
        assert t.validate("hello")
        assert t.parse("hello") == "hello"

    def test_str_max_length(self):
        t = str_(max=10)
        assert t.validate("short")
        assert not t.validate("this is way too long")
        assert t.parse("this is way too long") == "this is..."

    def test_str_min_length(self):
        t = str_(min=5)
        assert t.validate("hello")
        assert not t.validate("hi")

    def test_int_basic(self):
        t = int_()
        assert t.validate(42)
        assert t.validate("42")
        assert t.parse("42") == 42

    def test_int_range(self):
        t = int_(min=0, max=100)
        assert t.validate(50)
        assert not t.validate(-1)
        assert not t.validate(101)

    def test_float_basic(self):
        t = float_()
        assert t.validate(3.14)
        assert t.validate("3.14")
        assert t.parse("3.14") == 3.14

    def test_float_precision(self):
        t = float_(precision=2)
        assert t.parse(3.14159) == 3.14

    def test_bool(self):
        t = bool_()
        assert t.validate(True)
        assert t.validate("true")
        assert t.validate("yes")
        assert t.parse("true")
        assert not t.parse("false")

    def test_code_basic(self):
        t = code("python")
        assert t.validate("def foo(): pass")
        assert "python" in t.to_prompt()

    def test_code_strips_fences(self):
        t = code("python")
        result = t.parse("```python\ndef foo(): pass\n```")
        assert result == "def foo(): pass"

    def test_list_basic(self):
        t = list_()
        assert t.validate([1, 2, 3])
        assert t.validate([])

    def test_list_with_count(self):
        t = list_(exactly=3)
        assert t.validate([1, 2, 3])
        assert not t.validate([1, 2])
        assert not t.validate([1, 2, 3, 4])

    def test_list_with_item_type(self):
        t = list_(str_())
        assert t.validate(["a", "b", "c"])
        assert not t.validate([1, 2, 3])

    def test_list_parse_from_string(self):
        t = list_()
        result = t.parse('["a", "b", "c"]')
        assert result == ["a", "b", "c"]

    def test_optional(self):
        t = optional(str_())
        assert t.validate("hello")
        assert t.validate(None)
        assert t.parse(None) is None
        assert t.parse("null") is None

    def test_enum(self):
        t = enum("small", "medium", "large")
        assert t.validate("small")
        assert not t.validate("xlarge")
        assert "small" in t.to_prompt()


class TestOutputContract:
    """Test output contract validation and parsing."""

    def test_simple_contract(self):
        contract = OutputContract(
            {
                "name": str_(),
                "age": int_(),
            }
        )

        response = '{"name": "Alice", "age": 30}'
        result = contract.parse_response(response)

        assert result["name"] == "Alice"
        assert result["age"] == 30

    def test_contract_with_constraints(self):
        contract = OutputContract(
            {
                "summary": str_(max=50),
                "score": int_(min=0, max=10),
            }
        )

        response = '{"summary": "Short summary", "score": 8}'
        result = contract.parse_response(response)

        assert len(result["summary"]) <= 50
        assert 0 <= result["score"] <= 10

    def test_contract_with_code(self):
        contract = OutputContract(
            {
                "code": code("python"),
            }
        )

        response = '{"code": "def hello():\\n    print(\\"Hello\\")"}'
        result = contract.parse_response(response)

        assert "def hello" in result["code"]

    def test_contract_with_list(self):
        contract = OutputContract(
            {
                "items": list_(str_(), exactly=3),
            }
        )

        response = '{"items": ["a", "b", "c"]}'
        result = contract.parse_response(response)

        assert len(result["items"]) == 3

    def test_contract_with_optional(self):
        contract = OutputContract(
            {
                "required": str_(),
                "optional": optional(str_()),
            }
        )

        # With optional present
        response1 = '{"required": "yes", "optional": "maybe"}'
        result1 = contract.parse_response(response1)
        assert result1["optional"] == "maybe"

        # With optional null
        response2 = '{"required": "yes", "optional": null}'
        result2 = contract.parse_response(response2)
        assert result2["optional"] is None

        # With optional missing
        response3 = '{"required": "yes"}'
        result3 = contract.parse_response(response3)
        assert result3["optional"] is None

    def test_contract_missing_required_field(self):
        contract = OutputContract(
            {
                "required": str_(),
            }
        )

        with pytest.raises(ContractError, match="Missing required field"):
            contract.parse_response("{}")

    def test_contract_invalid_json(self):
        contract = OutputContract({"name": str_()})

        with pytest.raises(ContractError, match="not valid JSON"):
            contract.parse_response("not json")

    def test_contract_strips_markdown(self):
        contract = OutputContract({"name": str_()})

        response = '```json\n{"name": "test"}\n```'
        result = contract.parse_response(response)

        assert result["name"] == "test"

    def test_to_prompt_instructions(self):
        contract = OutputContract(
            {
                "summary": str_(max=100),
                "steps": list_(str_()),
            }
        )

        prompt = contract.to_prompt_instructions()

        assert "JSON" in prompt
        assert "summary" in prompt
        assert "steps" in prompt
        assert "100" in prompt


class TestContractResult:
    """Test ContractResult access patterns."""

    def test_dot_access(self):
        result = ContractResult(_data={"name": "Alice", "age": 30})

        assert result.name == "Alice"
        assert result.age == 30

    def test_dict_access(self):
        result = ContractResult(_data={"name": "Alice"})

        assert result["name"] == "Alice"

    def test_to_dict(self):
        data = {"name": "Alice", "age": 30}
        result = ContractResult(_data=data)

        assert result.to_dict() == data

    def test_missing_attribute(self):
        result = ContractResult(_data={"name": "Alice"})

        with pytest.raises(AttributeError):
            _ = result.missing
