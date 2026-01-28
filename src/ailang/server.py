"""
AILANG API Server - FastAPI-based REST API.
"""

from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ailang.core import AILANG
from ailang.parser import parse, validate
from ailang.transpiler import to_ailang, transpile


class RunRequest(BaseModel):
    """Request to execute an AILANG command."""

    command: str
    variables: dict[str, str] = {}
    provider: str | None = None
    model: str | None = None
    api_key: str | None = None


class RunResponse(BaseModel):
    """Response from executing an AILANG command."""

    result: str
    prompt: str
    provider: str


class TranspileRequest(BaseModel):
    """Request to transpile AILANG to natural language."""

    command: str
    variables: dict[str, str] = {}


class TranspileResponse(BaseModel):
    """Response with transpiled prompt."""

    prompt: str
    ast: dict[str, Any]
    warnings: list[str]


class ReverseRequest(BaseModel):
    """Request to convert natural language to AILANG."""

    prompt: str


class ReverseResponse(BaseModel):
    """Response with AILANG command."""

    command: str


def create_app(default_provider: str = "openai") -> FastAPI:
    """
    Create the FastAPI application.

    Args:
        default_provider: Default AI provider

    Returns:
        FastAPI application
    """
    app = FastAPI(
        title="AILANG API",
        description="A structured language for human-AI communication",
        version="0.1.0",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        """API info."""
        return {
            "name": "AILANG API",
            "version": "0.1.0",
            "docs": "/docs",
        }

    @app.get("/health")
    async def health():
        """Health check."""
        return {"status": "ok"}

    @app.post("/run", response_model=RunResponse)
    async def run(request: RunRequest):
        """
        Execute an AILANG command.

        Example:
            POST /run
            {
                "command": "write \"haiku about coding\" !traditional",
                "provider": "openai"
            }
        """
        provider = request.provider or default_provider

        try:
            ai = AILANG(
                provider=provider,
                model=request.model,
                api_key=request.api_key,
            )
            prompt = ai.transpile_only(request.command, **request.variables)
            result = await ai.run_async(request.command, **request.variables)

            return RunResponse(
                result=result,
                prompt=prompt,
                provider=provider,
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/transpile", response_model=TranspileResponse)
    async def transpile_endpoint(request: TranspileRequest):
        """
        Transpile AILANG to natural language prompt without executing.

        Example:
            POST /transpile
            {
                "command": "code \"sort\" [python] !typed ^fast"
            }
        """
        try:
            ast = parse(request.command)
            warnings = validate(ast)
            prompt = transpile(request.command, **request.variables)

            return TranspileResponse(
                prompt=prompt,
                ast={
                    "action": ast.action,
                    "subject": ast.subject,
                    "specifiers": ast.specifiers,
                    "must": ast.must,
                    "maybe": ast.maybe,
                    "priority": ast.priority,
                    "avoid": ast.avoid,
                },
                warnings=warnings,
            )
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.post("/reverse", response_model=ReverseResponse)
    async def reverse(request: ReverseRequest):
        """
        Convert natural language prompt to AILANG.

        Example:
            POST /reverse
            {
                "prompt": "Write a short professional email about the meeting"
            }
        """
        try:
            command = to_ailang(request.prompt)
            return ReverseResponse(command=command)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.get("/commands")
    async def list_commands():
        """List all available AILANG commands."""
        from ailang.transpiler import ACTION_TEMPLATES

        categories = {
            "text": [
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
            ],
            "image": ["img", "logo", "icon", "diagram", "mockup"],
            "code": [
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
            ],
            "analysis": [
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
            ],
            "creative": [
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
            ],
            "data": ["format", "merge", "split", "filter", "sort", "dedupe", "validate", "parse"],
        }

        return {
            "categories": categories,
            "total": len(ACTION_TEMPLATES),
        }

    @app.get("/modifiers")
    async def list_modifiers():
        """List all available modifiers."""
        from ailang.transpiler import AVOID_EXPANSIONS, MUST_EXPANSIONS, PRIORITY_EXPANSIONS

        return {
            "must (!)": list(MUST_EXPANSIONS.keys()),
            "priority (^)": list(PRIORITY_EXPANSIONS.keys()),
            "avoid (_)": list(AVOID_EXPANSIONS.keys()),
        }

    return app


# For running directly
app = create_app()
