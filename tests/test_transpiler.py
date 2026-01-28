"""
AILANG Tests - Transpiler tests.
"""

from ailang.transpiler import to_ailang, transpile


class TestTranspile:
    """Test AILANG to natural language transpilation."""

    def test_simple_write(self):
        prompt = transpile('write "hello"')
        assert "Write" in prompt
        assert "hello" in prompt

    def test_with_must_modifier(self):
        prompt = transpile('write "email" !short')
        assert "concise" in prompt.lower() or "brief" in prompt.lower()

    def test_with_priority_modifier(self):
        prompt = transpile('code "sort" ^fast')
        assert "speed" in prompt.lower() or "performance" in prompt.lower()

    def test_with_avoid_modifier(self):
        prompt = transpile('write "doc" _verbose')
        assert "avoid" in prompt.lower() or "verbose" in prompt.lower()

    def test_with_specifier(self):
        prompt = transpile('code "sort" [python]')
        assert "python" in prompt.lower()

    def test_translate_specifier(self):
        prompt = transpile('translate "hello" [french]')
        assert "french" in prompt.lower()

    def test_chain(self):
        prompt = transpile('write "text" > translate[es]')
        assert "write" in prompt.lower()
        assert "then" in prompt.lower()
        assert "translate" in prompt.lower()

    def test_persona(self):
        prompt = transpile('@as "expert" { review {code} }')
        assert "you are" in prompt.lower() or "expert" in prompt.lower()

    def test_variables(self):
        prompt = transpile("summarize {article}", article="My long article text")
        assert "My long article text" in prompt


class TestReverseTranspile:
    """Test natural language to AILANG conversion."""

    def test_simple_write(self):
        cmd = to_ailang("Write a short email")
        assert "write" in cmd.lower()
        assert "!short" in cmd

    def test_detect_professional(self):
        cmd = to_ailang("Write a professional cover letter")
        assert "!professional" in cmd

    def test_detect_language(self):
        cmd = to_ailang("Create a Python function to sort numbers")
        assert "[python]" in cmd.lower()

    def test_detect_avoid(self):
        cmd = to_ailang("Write an explanation but don't use jargon")
        assert "_" in cmd  # Should have an avoid modifier

    def test_subject_extraction(self):
        cmd = to_ailang("Write a blog post about machine learning")
        assert "machine learning" in cmd.lower() or "blog" in cmd.lower()


class TestComplexExamples:
    """Test complex real-world examples."""

    def test_code_generation(self):
        prompt = transpile('code "merge sort" [rust] !typed !tested ^performance')
        assert "rust" in prompt.lower()
        assert "type" in prompt.lower()
        assert "test" in prompt.lower()
        assert "performance" in prompt.lower()

    def test_image_generation(self):
        prompt = transpile('img "sunset" !photo ^cinematic _text')
        assert "image" in prompt.lower() or "generate" in prompt.lower()
        assert "photorealistic" in prompt.lower()
        assert "cinematic" in prompt.lower()
        assert "text" in prompt.lower()  # "do not include text"

    def test_analysis_chain(self):
        prompt = transpile("analyze {code} > fix !all > test[unit]")
        assert "analyze" in prompt.lower()
        assert "then" in prompt.lower()
        assert "fix" in prompt.lower()
