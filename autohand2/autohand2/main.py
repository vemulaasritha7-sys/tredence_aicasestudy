"""
AutoHand — CLI Interface
========================
Rich terminal UI that accepts user instructions, plans them via
the Planner agent, and executes them step-by-step with live logging.
"""

import sys
import json
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.rule import Rule
from rich import box

from agents.planner import plan, PlannerError
from agents.executor import execute

console = Console()

# ─── Banner ───────────────────────────────────────────────────────────────────
BANNER = r"""
 █████╗ ██╗   ██╗████████╗ ██████╗ ██╗  ██╗ █████╗ ███╗   ██╗██████╗ 
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██║  ██║██╔══██╗████╗  ██║██╔══██╗
███████║██║   ██║   ██║   ██║   ██║███████║███████║██╔██╗ ██║██║  ██║
██╔══██║██║   ██║   ██║   ██║   ██║██╔══██║██╔══██║██║╚██╗██║██║  ██║
██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║  ██║██║  ██║██║ ╚████║██████╔╝
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝
"""


def print_banner():
    console.print(
        Panel(
            Text(BANNER, style="bold magenta", justify="center"),
            subtitle="[dim cyan]AI Desktop Operator  •  Powered by Claude[/]",
            border_style="bright_magenta",
            padding=(0, 2),
        )
    )
    console.print()


def print_plan(plan_steps: list[dict]):
    table = Table(
        title="📋  Execution Plan",
        box=box.ROUNDED,
        border_style="bright_cyan",
        header_style="bold cyan",
        show_lines=True,
    )
    table.add_column("#",       style="dim",          width=4)
    table.add_column("Action",  style="bold yellow",  min_width=18)
    table.add_column("Value",   style="white",        min_width=30)

    for i, step in enumerate(plan_steps, 1):
        table.add_row(str(i), step["action"], step["value"] or "[dim]—[/]")

    console.print(table)
    console.print()


def print_logs(logs):
    table = Table(
        title="🖥️  Execution Log",
        box=box.ROUNDED,
        border_style="bright_green",
        header_style="bold green",
        show_lines=True,
    )
    table.add_column("Step",    style="dim",      width=5)
    table.add_column("Action",  style="yellow",   min_width=18)
    table.add_column("Status",  min_width=10)
    table.add_column("Message", min_width=30)
    table.add_column("ms",      style="dim",      width=7)

    for log in logs:
        if log.status == "success":
            status_str = "[bold green]✅ success[/]"
        elif log.status == "error":
            status_str = "[bold red]❌ error[/]"
        else:
            status_str = f"[dim]{log.status}[/]"

        table.add_row(
            str(log.step),
            log.action,
            status_str,
            log.message,
            str(log.elapsed_ms),
        )

    console.print(table)
    console.print()


def run_once(user_query: str):
    """Run a single query through the full pipeline."""
    console.print(Rule("[bold cyan]Planning[/]", style="cyan"))
    console.print(f"[dim]Query:[/] [bold white]{user_query}[/]\n")

    # ── Planning ──────────────────────────────────────────────────────────────
    with Progress(
        SpinnerColumn(spinner_name="dots", style="magenta"),
        TextColumn("[cyan]Thinking with Claude...[/]"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task("plan", total=None)
        try:
            action_plan = plan(user_query)
        except PlannerError as e:
            console.print(f"[bold red]Planner Error:[/] {e}")
            return

    console.print(f"[bold green]✓[/] Plan generated — [bold]{len(action_plan)}[/] steps\n")
    print_plan(action_plan)

    # ── Execution ─────────────────────────────────────────────────────────────
    console.print(Rule("[bold green]Executing[/]", style="green"))

    with Progress(
        SpinnerColumn(spinner_name="point", style="green"),
        TextColumn("[green]Executing actions...[/]"),
        transient=True,
        console=console,
    ) as progress:
        progress.add_task("exec", total=None)
        logs = execute(action_plan)

    successes = sum(1 for l in logs if l.status == "success")
    errors     = sum(1 for l in logs if l.status == "error")

    print_logs(logs)

    if errors == 0:
        console.print(Panel(
            f"[bold green]✨ All {successes} steps completed successfully![/]",
            border_style="green",
        ))
    else:
        console.print(Panel(
            f"[bold yellow]⚠  {successes} succeeded, [bold red]{errors} failed[/]",
            border_style="yellow",
        ))

    console.print()


def main():
    print_banner()
    console.print("[dim]Type your instruction below. Type [bold]exit[/] to quit.\n")

    while True:
        try:
            user_input = console.input("[bold magenta]AutoHand >[/] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Goodbye![/]")
            sys.exit(0)

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "q"}:
            console.print("[dim]Goodbye![/]")
            break

        run_once(user_input)


if __name__ == "__main__":
    main()
