"""
AILANG CLI - Command line interface.
"""

import sys

import click
from rich.console import Console
from rich.panel import Panel

from ailang.core import AILANG
from ailang.parser import parse, validate
from ailang.transpiler import to_ailang, transpile

console = Console()


@click.group(invoke_without_command=True)
@click.argument("command", required=False)
@click.option("--provider", "-p", default="openai", help="AI provider (openai, anthropic, ollama)")
@click.option("--model", "-m", help="Model name")
@click.option("--api-key", "-k", help="API key")
@click.option("--transpile-only", "-t", is_flag=True, help="Show prompt without executing")
@click.option("--interactive", "-i", is_flag=True, help="Interactive mode")
@click.option("--parse-only", is_flag=True, help="Show parsed AST")
@click.pass_context
def main(
    ctx: click.Context,
    command: str | None,
    provider: str,
    model: str | None,
    api_key: str | None,
    transpile_only: bool,
    interactive: bool,
    parse_only: bool,
):
    """
    AILANG - A structured language for human-AI communication.

    Examples:

        ailang 'write "haiku about coding"'

        ailang 'code "fibonacci" [python] !typed' --transpile-only

        ailang --interactive

        ailang serve --port 8000
    """
    if ctx.invoked_subcommand is not None:
        return

    if interactive:
        _interactive_mode(provider, model, api_key)
        return

    if not command:
        console.print("[yellow]Usage: ailang 'command' or ailang --interactive[/yellow]")
        console.print("\nRun [cyan]ailang --help[/cyan] for more options.")
        return

    # Parse only mode
    if parse_only:
        try:
            ast = parse(command)
            console.print(Panel(str(ast), title="Parsed AST"))
            warnings = validate(ast)
            for w in warnings:
                console.print(f"[yellow]Warning: {w}[/yellow]")
        except Exception as e:
            console.print(f"[red]Parse error: {e}[/red]")
        return

    # Transpile only mode
    if transpile_only:
        try:
            prompt = transpile(command)
            console.print(Panel(prompt, title="Generated Prompt"))
        except Exception as e:
            console.print(f"[red]Transpile error: {e}[/red]")
        return

    # Execute command
    try:
        ai = AILANG(provider=provider, model=model, api_key=api_key)
        result = ai.run(command)
        console.print(result)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


def _interactive_mode(provider: str, model: str | None, api_key: str | None):
    """Run interactive REPL."""
    console.print(
        Panel.fit(
            "[bold cyan]AILANG Interactive Mode[/bold cyan]\n\n"
            "Commands:\n"
            "  [green]!help[/green]     - Show syntax help\n"
            "  [green]!transpile[/green] - Toggle transpile-only mode\n"
            "  [green]!provider[/green]  - Switch provider\n"
            "  [green]!exit[/green]     - Exit\n"
        )
    )

    ai = None
    transpile_mode = False
    current_provider = provider

    while True:
        try:
            cmd = console.input("[bold cyan]ailang>[/bold cyan] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye![/dim]")
            break

        if not cmd:
            continue

        # Meta commands
        if cmd == "!exit" or cmd == "exit":
            break
        elif cmd == "!help":
            _show_help()
            continue
        elif cmd == "!transpile":
            transpile_mode = not transpile_mode
            mode = "ON" if transpile_mode else "OFF"
            console.print(f"[dim]Transpile-only mode: {mode}[/dim]")
            continue
        elif cmd.startswith("!provider "):
            current_provider = cmd.split(" ", 1)[1]
            ai = None  # Reset
            console.print(f"[dim]Switched to: {current_provider}[/dim]")
            continue
        elif cmd.startswith("!to_ailang "):
            human_prompt = cmd.split(" ", 1)[1]
            result = to_ailang(human_prompt)
            console.print(f"[green]{result}[/green]")
            continue

        # Execute AILANG
        try:
            if transpile_mode:
                prompt = transpile(cmd)
                console.print(Panel(prompt, title="Generated Prompt", border_style="dim"))
            else:
                if ai is None:
                    ai = AILANG(provider=current_provider, model=model, api_key=api_key)
                result = ai.run(cmd)
                console.print(result)
                console.print()
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")


def _show_help():
    """Show syntax help."""
    help_text = """
[bold]AILANG Quick Reference[/bold]

[cyan]Structure:[/cyan]  action "subject" [specifier] modifiers

[cyan]Modifiers:[/cyan]
  !must      Required constraint     !short !typed !examples
  ~maybe     Optional hint           ~funny ~creative
  ^priority  Prioritize              ^speed ^quality ^security
  _avoid     Don't do this           _verbose _emoji _jargon

[cyan]Operators:[/cyan]
  >          Chain commands          write > translate[fr]
  &          Parallel outputs        title & summary & tags

[cyan]Common Actions:[/cyan]
  write  img  code  explain  summarize  translate
  fix  analyze  list  compare  recommend  convert

[cyan]Examples:[/cyan]
  write "birthday email" !warm ~funny
  img "sunset" !photo ^cinematic _text
  code "sort" [python] !typed ^fast
  analyze {data} > summarize !brief
"""
    console.print(Panel(help_text, title="AILANG Help"))


@main.command()
@click.option("--host", default="0.0.0.0", help="Host to bind")
@click.option("--port", default=8000, help="Port to bind")
@click.option("--provider", "-p", default="openai", help="Default provider")
def serve(host: str, port: int, provider: str):
    """Start AILANG API server."""
    try:
        import uvicorn

        from ailang.server import create_app
    except ImportError:
        console.print("[red]Server dependencies required: pip install ailang[server][/red]")
        sys.exit(1)

    console.print(f"[green]Starting AILANG server on {host}:{port}[/green]")
    app = create_app(default_provider=provider)
    uvicorn.run(app, host=host, port=port)


@main.command()
@click.argument("prompt")
def reverse(prompt: str):
    """Convert natural language prompt to AILANG."""
    result = to_ailang(prompt)
    console.print(f"[green]{result}[/green]")


if __name__ == "__main__":
    main()
