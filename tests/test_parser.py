"""
AILANG Tests - Parser tests.
"""

from ailang.parser import parse, validate


class TestParseBasic:
    """Test basic parsing functionality."""

    def test_simple_action(self):
        ast = parse('write "hello"')
        assert ast.action == "write"
        assert ast.subject == "hello"

    def test_action_only(self):
        ast = parse("list")
        assert ast.action == "list"
        assert ast.subject == ""

    def test_with_variable(self):
        ast = parse("summarize {article}")
        assert ast.action == "summarize"
        assert ast.subject == "{article}"
        assert "article" in ast.variables


class TestParseModifiers:
    """Test modifier parsing."""

    def test_must_modifier(self):
        ast = parse('write "email" !short')
        assert "short" in ast.must

    def test_multiple_must(self):
        ast = parse('code "sort" !typed !tested')
        assert "typed" in ast.must
        assert "tested" in ast.must

    def test_maybe_modifier(self):
        ast = parse('write "joke" ~funny')
        assert "funny" in ast.maybe

    def test_priority_modifier(self):
        ast = parse('code "algo" ^fast')
        assert "fast" in ast.priority

    def test_avoid_modifier(self):
        ast = parse('write "email" _verbose')
        assert "verbose" in ast.avoid

    def test_mixed_modifiers(self):
        ast = parse('code "sort" [python] !typed ^fast _verbose ~elegant')
        assert "typed" in ast.must
        assert "fast" in ast.priority
        assert "verbose" in ast.avoid
        assert "elegant" in ast.maybe


class TestParseSpecifiers:
    """Test specifier parsing."""

    def test_single_specifier(self):
        ast = parse('code "sort" [python]')
        assert "python" in ast.specifiers

    def test_multiple_specifiers(self):
        ast = parse('write "email" [formal] [short]')
        assert "formal" in ast.specifiers
        assert "short" in ast.specifiers

    def test_numeric_specifier(self):
        ast = parse('list "ideas" [10]')
        assert "10" in ast.specifiers


class TestParseChains:
    """Test chain parsing."""

    def test_simple_chain(self):
        ast = parse('write "text" > translate[fr]')
        assert ast.action == "write"
        assert ast.chain is not None
        assert ast.chain.action == "translate"

    def test_multiple_chains(self):
        ast = parse("summarize {doc} > translate[es] > format[json]")
        assert ast.action == "summarize"
        assert ast.chain.action == "translate"
        assert ast.chain.chain.action == "format"


class TestParsePersona:
    """Test persona parsing."""

    def test_persona(self):
        ast = parse('@as "expert" { review {code} }')
        assert ast.persona == "expert"
        assert ast.action == "review"

    def test_persona_with_modifiers(self):
        ast = parse('@as "senior developer" { review {code} !honest ^security }')
        assert ast.persona == "senior developer"
        assert "honest" in ast.must
        assert "security" in ast.priority


class TestValidation:
    """Test AST validation."""

    def test_valid_action(self):
        ast = parse('write "hello"')
        warnings = validate(ast)
        assert len(warnings) == 0

    def test_unknown_action(self):
        ast = parse('foobar "hello"')
        warnings = validate(ast)
        assert len(warnings) > 0
        assert "Unknown action" in warnings[0]

    def test_missing_subject_warning(self):
        ast = parse("write")
        warnings = validate(ast)
        assert any("subject" in w for w in warnings)
