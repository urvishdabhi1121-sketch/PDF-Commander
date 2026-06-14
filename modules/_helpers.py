"""
modules/_helpers.py
===================
Shared utility functions used across all PDF-Commander modules.
"""

import os
from pathlib import Path
from rich.console import Console

console = Console()


# ── Path helpers ──────────────────────────────────────────────────────────────

def prompt_input_file(label: str = "Input PDF path") -> Path:
    """Prompt the user for an existing file path and validate it."""
    while True:
        raw = console.input(f"[cyan]  {label}: [/cyan]").strip().strip('"').strip("'")
        path = Path(raw)
        if path.is_file():
            return path
        console.print(f"[red]  ✗  File not found: {path}[/red]")


def prompt_output_file(label: str = "Output file path", default: str = "") -> Path:
    """Prompt for an output path; accepts Enter to use a default."""
    hint = f" [dim](default: {default})[/dim]" if default else ""
    raw = console.input(f"[cyan]  {label}{hint}: [/cyan]").strip().strip('"').strip("'")
    if not raw and default:
        raw = default
    return Path(raw)


def prompt_output_dir(label: str = "Output directory") -> Path:
    """Prompt for an output directory, creating it if needed."""
    while True:
        raw = console.input(f"[cyan]  {label}: [/cyan]").strip().strip('"').strip("'")
        path = Path(raw)
        try:
            path.mkdir(parents=True, exist_ok=True)
            return path
        except Exception as exc:
            console.print(f"[red]  ✗  Cannot create directory: {exc}[/red]")


def prompt_multiple_files(label: str = "PDF paths (comma-separated or one per line)") -> list[Path]:
    """
    Accept multiple file paths.
    The user can enter them comma-separated on one line, or one per line
    ending with an empty line.
    """
    console.print(f"[cyan]  {label}[/cyan]")
    console.print("  [dim](Enter paths one at a time, blank line when done)[/dim]")
    paths = []
    while True:
        raw = console.input("  [cyan]>[/cyan] ").strip().strip('"').strip("'")
        if not raw:
            if paths:
                break
            console.print("  [yellow]At least one file is required.[/yellow]")
            continue
        # Support comma-separated entry on a single line
        for part in raw.split(","):
            part = part.strip().strip('"').strip("'")
            if part:
                p = Path(part)
                if p.is_file():
                    paths.append(p)
                else:
                    console.print(f"  [red]  ✗  Not found, skipping: {p}[/red]")
    return paths


def prompt_password(label: str = "Password") -> str:
    """Prompt for a password (input is hidden via getpass)."""
    import getpass
    return getpass.getpass(f"  {label}: ")


def prompt_int(label: str, min_val: int = 1, max_val: int = 9999) -> int:
    """Prompt for an integer within [min_val, max_val]."""
    while True:
        raw = console.input(f"[cyan]  {label} ({min_val}–{max_val}): [/cyan]").strip()
        if raw.isdigit():
            val = int(raw)
            if min_val <= val <= max_val:
                return val
        console.print(f"  [red]Please enter a number between {min_val} and {max_val}.[/red]")


# ── Output helpers ─────────────────────────────────────────────────────────────

def success(msg: str) -> None:
    console.print(f"\n  [bold green]✓[/bold green]  {msg}")


def info(msg: str) -> None:
    console.print(f"  [cyan]ℹ[/cyan]  {msg}")


def warn(msg: str) -> None:
    console.print(f"  [yellow]⚠[/yellow]  {msg}")


def divider() -> None:
    console.print("  [dim]" + "─" * 50 + "[/dim]")
