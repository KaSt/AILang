"""
AILANG Transpiler - Converts between AILANG and natural language prompts.
"""

import re

from ailang.parser import AILangAST, parse

# Action to natural language templates
ACTION_TEMPLATES = {
    # Text
    "write": "Write {subject}",
    "rewrite": "Rewrite the following: {subject}",
    "summarize": "Summarize {subject}",
    "expand": "Expand on {subject} with more detail",
    "translate": "Translate {subject}",
    "explain": "Explain {subject}",
    "list": "List {subject}",
    "compare": "Compare {subject}",
    "reply": "Write a reply to {subject}",
    "title": "Generate a title for {subject}",
    # Image
    "img": "Generate an image of {subject}",
    "logo": "Design a logo for {subject}",
    "icon": "Create an icon for {subject}",
    "diagram": "Create a diagram showing {subject}",
    "mockup": "Create a UI mockup for {subject}",
    # Code
    "code": "Write code for {subject}",
    "fix": "Fix the following code: {subject}",
    "refactor": "Refactor the following code: {subject}",
    "test": "Write tests for {subject}",
    "review": "Review this code: {subject}",
    "convert": "Convert this code: {subject}",
    "api": "Design an API for {subject}",
    "query": "Write a database query for {subject}",
    "regex": "Create a regex pattern for {subject}",
    "docs": "Write documentation for {subject}",
    # Analysis
    "analyze": "Analyze {subject}",
    "evaluate": "Evaluate {subject}",
    "predict": "Predict {subject}",
    "diagnose": "Diagnose issues in {subject}",
    "recommend": "Recommend {subject}",
    "rank": "Rank {subject}",
    "verify": "Verify {subject}",
    "extract": "Extract {subject}",
    "classify": "Classify {subject}",
    "sentiment": "Analyze the sentiment of {subject}",
    # Creative
    "brainstorm": "Brainstorm ideas for {subject}",
    "name": "Generate names for {subject}",
    "story": "Write a story about {subject}",
    "joke": "Write a joke about {subject}",
    "poem": "Write a poem about {subject}",
    "script": "Write a script for {subject}",
    "pitch": "Create a pitch for {subject}",
    "slogan": "Create a slogan for {subject}",
    "recipe": "Create a recipe for {subject}",
    "playlist": "Create a playlist for {subject}",
    # Data
    "format": "Format {subject}",
    "merge": "Merge {subject}",
    "split": "Split {subject}",
    "filter": "Filter {subject}",
    "sort": "Sort {subject}",
    "dedupe": "Remove duplicates from {subject}",
    "validate": "Validate {subject}",
    "parse": "Parse {subject}",
}

# Modifier expansions
MUST_EXPANSIONS = {
    "short": "Keep it concise and brief.",
    "brief": "Keep it brief.",
    "concise": "Be concise.",
    "detailed": "Include thorough details.",
    "long": "Make it comprehensive and detailed.",
    "simple": "Use simple, easy-to-understand language.",
    "technical": "Use technical terminology.",
    "formal": "Use a formal tone.",
    "casual": "Use a casual, conversational tone.",
    "professional": "Maintain a professional tone.",
    "friendly": "Use a friendly, approachable tone.",
    "examples": "Include examples.",
    "typed": "Include type annotations.",
    "tested": "Include unit tests.",
    "commented": "Include code comments.",
    "explained": "Explain your reasoning.",
    "photo": "Make it photorealistic.",
    "art": "Make it artistic/illustrated.",
    "minimal": "Use a minimalist style.",
    "honest": "Be honest and direct.",
    "creative": "Be creative and original.",
    "accurate": "Ensure accuracy.",
    "structured": "Use a clear structure with sections.",
    "bullets": "Format as bullet points.",
    "numbered": "Format as a numbered list.",
    "bare": "Return only the result, no explanations.",
}

PRIORITY_EXPANSIONS = {
    "speed": "Optimize for speed/performance.",
    "fast": "Optimize for speed.",
    "performance": "Prioritize performance.",
    "quality": "Prioritize quality over speed.",
    "readable": "Prioritize readability.",
    "clarity": "Prioritize clarity.",
    "security": "Focus on security.",
    "memory": "Optimize for memory efficiency.",
    "creative": "Prioritize creativity.",
    "accuracy": "Prioritize accuracy.",
    "seo": "Optimize for SEO.",
    "engagement": "Optimize for engagement.",
    "conversion": "Optimize for conversion.",
    "cinematic": "Use cinematic composition and lighting.",
    "detailed": "Include rich details.",
    "vibrant": "Use vibrant colors.",
}

AVOID_EXPANSIONS = {
    "verbose": "Avoid being verbose.",
    "technical": "Avoid technical jargon.",
    "jargon": "Avoid jargon.",
    "emoji": "Do not use emojis.",
    "text": "Do not include text in the image.",
    "generic": "Avoid generic or cliché approaches.",
    "boring": "Don't be boring.",
    "repetitive": "Avoid repetition.",
    "complex": "Avoid unnecessary complexity.",
    "deps": "Avoid external dependencies.",
    "offensive": "Avoid offensive content.",
}


def transpile(command: str, **variables: str) -> str:
    """
    Convert an AILANG command to a natural language prompt.

    Args:
        command: AILANG command string
        **variables: Values for {variable} placeholders

    Returns:
        Natural language prompt string

    Examples:
        >>> transpile('write "email" !professional !short')
        'Write email. Maintain a professional tone. Keep it concise and brief.'

        >>> transpile('img "cat" !photo ^cinematic _text')  # doctest: +SKIP
        'Generate an image of cat. Make it photorealistic. ...'
    """
    ast = parse(command)
    return _transpile_ast(ast, variables)


def _transpile_ast(ast: AILangAST, variables: dict[str, str]) -> str:
    """Convert an AST to natural language."""
    parts = []

    # Handle persona
    if ast.persona:
        parts.append(f"You are {ast.persona}.")

    # Base action
    template = ACTION_TEMPLATES.get(ast.action, f"{ast.action.capitalize()} {{subject}}")
    subject = ast.subject

    # Replace variables
    for var_name, var_value in variables.items():
        subject = subject.replace(f"{{{var_name}}}", var_value)

    base = template.format(subject=subject) if subject else template.replace(" {subject}", "")
    parts.append(base)

    # Add specifiers
    for spec in ast.specifiers:
        if ast.action in ("code", "convert", "query"):
            parts.append(f"Use {spec}.")
        elif ast.action == "translate":
            parts.append(f"Translate to {spec}.")
        elif ast.action == "img":
            parts.append(f"Style: {spec}.")
        elif spec.isdigit():
            parts.append(f"Provide {spec} items.")
        else:
            parts.append(f"Format: {spec}.")

    # Add must modifiers
    for mod in ast.must:
        if mod in MUST_EXPANSIONS:
            parts.append(MUST_EXPANSIONS[mod])
        elif mod.startswith("under_"):
            limit = mod.replace("under_", "")
            parts.append(f"Keep it under {limit} characters.")
        else:
            parts.append(f"Must be {mod}.")

    # Add maybe modifiers
    for mod in ast.maybe:
        if mod in MUST_EXPANSIONS:
            parts.append(f"If possible, {MUST_EXPANSIONS[mod].lower()}")
        else:
            parts.append(f"Optionally, make it {mod}.")

    # Add priority modifiers
    for mod in ast.priority:
        if mod in PRIORITY_EXPANSIONS:
            parts.append(PRIORITY_EXPANSIONS[mod])
        else:
            parts.append(f"Prioritize {mod}.")

    # Add avoid modifiers
    for mod in ast.avoid:
        if mod in AVOID_EXPANSIONS:
            parts.append(AVOID_EXPANSIONS[mod])
        else:
            parts.append(f"Avoid {mod}.")

    # Handle parallel outputs
    if ast.parallel:
        parts.append(f"Also provide: {', '.join(ast.parallel)}.")

    # Handle chain
    if ast.chain:
        chain_prompt = _transpile_ast(ast.chain, variables)
        parts.append(f"Then, {chain_prompt[0].lower()}{chain_prompt[1:]}")

    return " ".join(parts)


def to_ailang(prompt: str) -> str:
    """
    Convert a natural language prompt to AILANG (best effort).

    Args:
        prompt: Natural language prompt

    Returns:
        AILANG command string

    Examples:
        >>> to_ailang("Write a short professional email about the meeting")
        'write "email about the meeting" !short !professional'
    """
    prompt_lower = prompt.lower()

    # Detect action
    action = "write"  # default
    for act in ACTION_TEMPLATES.keys():
        if act in prompt_lower or f"{act}e" in prompt_lower or f"{act}ing" in prompt_lower:
            action = act
            break

    # Extract subject (look for quoted strings or key phrases)
    subject_match = re.search(r'"([^"]+)"', prompt)
    if subject_match:
        subject = subject_match.group(1)
    else:
        # Try to extract subject from common patterns
        patterns = [
            r"(?:about|for|of|on)\s+(?:a\s+)?(.+?)(?:\.|,|$)",
            r"(?:write|create|generate|make)\s+(?:a\s+)?(.+?)(?:\.|,|$)",
        ]
        subject = ""
        for pattern in patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                subject = match.group(1).strip()
                break

    # Detect modifiers
    modifiers = []

    # Must modifiers
    must_keywords = {
        "short": ["short", "brief", "concise"],
        "detailed": ["detailed", "comprehensive", "thorough"],
        "professional": ["professional"],
        "formal": ["formal"],
        "casual": ["casual", "informal"],
        "simple": ["simple", "easy to understand", "eli5"],
        "examples": ["example", "examples"],
        "typed": ["type hint", "typed", "type annotation"],
    }
    for mod, keywords in must_keywords.items():
        if any(kw in prompt_lower for kw in keywords):
            modifiers.append(f"!{mod}")

    # Priority modifiers
    if "focus on" in prompt_lower or "prioritize" in prompt_lower:
        focus_match = re.search(r"(?:focus on|prioritize)\s+(\w+)", prompt_lower)
        if focus_match:
            modifiers.append(f"^{focus_match.group(1)}")

    # Avoid modifiers
    avoid_patterns = ["don't", "do not", "avoid", "no "]
    for pattern in avoid_patterns:
        if pattern in prompt_lower:
            avoid_match = re.search(rf"{pattern}\s+(\w+)", prompt_lower)
            if avoid_match:
                modifiers.append(f"_{avoid_match.group(1)}")

    # Detect language/format specifiers
    specs = []
    languages = ["python", "javascript", "typescript", "rust", "go", "java", "ruby", "c++", "c#"]
    for lang in languages:
        if lang in prompt_lower:
            specs.append(f"[{lang}]")
            break

    formats = ["json", "csv", "xml", "yaml", "markdown", "html"]
    for fmt in formats:
        if fmt in prompt_lower:
            specs.append(f"[{fmt}]")
            break

    # Build command
    parts = [action]
    if subject:
        parts.append(f'"{subject}"')
    parts.extend(specs)
    parts.extend(modifiers)

    return " ".join(parts)
