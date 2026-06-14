#!/usr/bin/env python3
"""
PDF-Commander — main.py
=======================
Privacy-first, local-only PDF operations toolkit.
No cloud. No telemetry. No data leaves your machine.

Run with:  python main.py
"""

import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box

console = Console()

# ── ASCII banner ───────────────────────────────────────────────────────────────
BANNER = """
 ██████╗ ██████╗ ███████╗      ██████╗ ███╗   ███╗██████╗ 
 ██╔══██╗██╔══██╗██╔════╝     ██╔════╝ ████╗ ████║██╔══██╗
 ██████╔╝██║  ██║█████╗       ██║      ██╔████╔██║██║  ██║
 ██╔═══╝ ██║  ██║██╔══╝       ██║      ██║╚██╔╝██║██║  ██║
 ██║     ██████╔╝██║          ╚██████╗ ██║ ╚═╝ ██║██████╔╝
 ╚═╝     ╚═════╝ ╚═╝           ╚═════╝ ╚═╝     ╚═╝╚═════╝ 
"""

# ── Menu definition ────────────────────────────────────────────────────────────
# Each entry: (display_label, module_path, function_name)
MENU_ITEMS = {
    # ── Merge & Split ──────────────────────────────────────────────────────────
    "1": ("Merge PDFs",               "modules.merge",     "run"),
    "2": ("Split PDF (by page)",      "modules.split",     "run_by_page"),
    "3": ("Split PDF (by range)",     "modules.split",     "run_by_range"),

    # ── Conversion ─────────────────────────────────────────────────────────────
    "4": ("PDF → Word (.docx)",       "modules.converter", "pdf_to_word"),
    "5": ("Word (.docx) → PDF",       "modules.converter", "word_to_pdf"),
    "6": ("PDF → Plain Text (.txt)",  "modules.converter", "pdf_to_text"),

    # ── Pages & Layout ─────────────────────────────────────────────────────────
    "7": ("Rotate Pages",             "modules.pages",     "run_rotate"),
    "8": ("Extract Specific Pages",   "modules.pages",     "run_extract"),
    "9": ("Add Watermark",            "modules.pages",     "run_watermark"),

    # ── Security ───────────────────────────────────────────────────────────────
    "10": ("Encrypt PDF (add password)",    "modules.security", "run_encrypt"),
    "11": ("Decrypt PDF (remove password)", "modules.security", "run_decrypt"),
    "12": ("Redact Metadata",               "modules.security", "run_redact_metadata"),

    # ── Inspection ─────────────────────────────────────────────────────────────
    "13": ("Inspect PDF (info + metadata)", "modules.pdf_inspect",  "run"),
    "14": ("Extract Text & Tables",         "modules.pdf_inspect",  "run_extract_text"),

    # ── Quit ───────────────────────────────────────────────────────────────────
    "0": ("Exit PDF-Commander", None, None),
}

# Category headers for display grouping
CATEGORY_HEADERS = {
    "1":  "── MERGE & SPLIT ──────────────────────────────",
    "4":  "── CONVERSION ─────────────────────────────────",
    "7":  "── PAGES & LAYOUT ─────────────────────────────",
    "10": "── SECURITY ────────────────────────────────────",
    "13": "── INSPECTION ──────────────────────────────────",
    "0":  "────────────────────────────────────────────────",
}


def print_banner() -> None:
    """Render the startup banner."""
    console.print(Text(BANNER, style="bold cyan"))
    console.print(
        Panel(
            "[bold white]Privacy-First · Local-Only · No Cloud · No Telemetry[/bold white]\n"
            "[dim]All processing happens 100% on your machine.[/dim]",
            style="cyan",
            box=box.ROUNDED,
        )
    )


def build_menu_table() -> Table:
    """Build a Rich table showing all available operations."""
    table = Table(
        box=box.SIMPLE_HEAVY,
        show_header=True,
        header_style="bold magenta",
        border_style="dim",
        expand=False,
        padding=(0, 2),
    )
    table.add_column("#", style="bold yellow", justify="right", width=4)
    table.add_column("Operation", style="white", min_width=40)

    for key, (label, _, _) in MENU_ITEMS.items():
        if key in CATEGORY_HEADERS:
            table.add_row("", f"[dim]{CATEGORY_HEADERS[key]}[/dim]")
        if key == "0":
            table.add_row(key, f"[bold red]{label}[/bold red]")
        else:
            table.add_row(key, label)

    return table


def dispatch(choice: str) -> None:
    """Dynamically import and call the selected module function."""
    if choice not in MENU_ITEMS:
        console.print("[bold red]  ✗  Invalid choice. Please try again.[/bold red]\n")
        return

    label, module_path, func_name = MENU_ITEMS[choice]

    if choice == "0":
        console.print(
            Panel(
                "[bold cyan]Thank you for using PDF-Commander.\n"
                "Your files stayed local — as they should.[/bold cyan]",
                box=box.ROUNDED,
                style="cyan",
            )
        )
        sys.exit(0)

    console.print(f"\n[bold cyan]▶  {label}[/bold cyan]\n")

    try:
        # Lazy import — only load the module when needed
        import importlib
        module = importlib.import_module(module_path)
        func   = getattr(module, func_name)
        func()
    except ImportError as exc:
        console.print(
            f"[bold red]  ✗  Could not load module '{module_path}'.[/bold red]\n"
            f"  [dim]{exc}[/dim]\n"
            f"  [yellow]Tip: Did you run [bold]pip install -r requirements.txt[/bold]?[/yellow]\n"
        )
    except AttributeError:
        console.print(
            f"[bold red]  ✗  Function '{func_name}' not found in '{module_path}'.[/bold red]\n"
        )
    except KeyboardInterrupt:
        console.print("\n[yellow]  ↩  Operation cancelled. Returning to menu.[/yellow]\n")
    except Exception as exc:   # noqa: BLE001
        console.print(f"[bold red]  ✗  Operation failed:[/bold red] {exc}\n")


def main() -> None:
    """Main application loop."""
    os.system("cls" if os.name == "nt" else "clear")
    print_banner()

    while True:
        console.print(build_menu_table())
        try:
            choice = console.input(
                "[bold yellow]Select an operation [0–14]: [/bold yellow]"
            ).strip()
        except (KeyboardInterrupt, EOFError):
            # Ctrl-C at the main prompt = graceful exit
            console.print("\n[yellow]Interrupted. Goodbye.[/yellow]")
            sys.exit(0)

        dispatch(choice)

        if choice != "0":
            console.input(
                "\n[dim]Press Enter to return to the main menu…[/dim]"
            )
            os.system("cls" if os.name == "nt" else "clear")
            print_banner()


if __name__ == "__main__":
    main()
