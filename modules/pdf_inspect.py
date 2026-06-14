"""
modules/inspect.py
==================
Inspect a PDF: display metadata, page info, and extract text/tables.
All processing is local — no files leave your machine.
"""

from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich import box
from modules._helpers import (
    prompt_input_file,
    prompt_output_file,
    success, info, warn, divider,
)

console = Console()


# ── PDF Info & Metadata ────────────────────────────────────────────────────────

def run() -> None:
    """Display full metadata and page statistics for a PDF."""
    console.print("  [bold]Inspect PDF[/bold] — metadata, page count, file info\n")
    divider()

    try:
        from pypdf import PdfReader
    except ImportError:
        warn("pypdf is not installed. Run: pip install pypdf")
        return

    input_path = prompt_input_file("PDF path to inspect")
    divider()

    reader   = PdfReader(str(input_path))
    metadata = reader.metadata or {}
    total    = len(reader.pages)
    size_kb  = input_path.stat().st_size / 1024

    # ── File info table ────────────────────────────────────────────────────────
    file_table = Table(
        box=box.SIMPLE_HEAVY,
        show_header=True,
        header_style="bold magenta",
        border_style="dim",
        padding=(0, 2),
    )
    file_table.add_column("Property", style="cyan", width=20)
    file_table.add_column("Value",    style="white")

    file_table.add_row("File name",   input_path.name)
    file_table.add_row("File size",   f"{size_kb:,.1f} KB  ({input_path.stat().st_size:,} bytes)")
    file_table.add_row("Pages",       str(total))
    file_table.add_row("Encrypted",   "Yes" if reader.is_encrypted else "No")

    console.print("\n  [bold]── File Information ──[/bold]")
    console.print(file_table)

    # ── Metadata table ─────────────────────────────────────────────────────────
    meta_table = Table(
        box=box.SIMPLE_HEAVY,
        show_header=True,
        header_style="bold magenta",
        border_style="dim",
        padding=(0, 2),
    )
    meta_table.add_column("Metadata Field", style="cyan", width=20)
    meta_table.add_column("Value",          style="white")

    FIELDS = {
        "/Title":        "Title",
        "/Author":       "Author",
        "/Subject":      "Subject",
        "/Creator":      "Creator",
        "/Producer":     "Producer",
        "/Keywords":     "Keywords",
        "/CreationDate": "Created",
        "/ModDate":      "Modified",
    }
    found_any = False
    for key, label in FIELDS.items():
        val = metadata.get(key)
        if val:
            meta_table.add_row(label, str(val))
            found_any = True

    console.print("\n  [bold]── PDF Metadata ──[/bold]")
    if found_any:
        console.print(meta_table)
    else:
        console.print("  [dim]No metadata found (document may already be cleaned).[/dim]")

    # ── Per-page summary ───────────────────────────────────────────────────────
    console.print("\n  [bold]── Page Summary ──[/bold]")
    page_table = Table(
        box=box.SIMPLE,
        show_header=True,
        header_style="bold magenta",
        border_style="dim",
        padding=(0, 2),
    )
    page_table.add_column("Page",   style="yellow", justify="right")
    page_table.add_column("Width",  style="white",  justify="right")
    page_table.add_column("Height", style="white",  justify="right")
    page_table.add_column("Rotation", style="dim",  justify="right")

    for i, page in enumerate(reader.pages, 1):
        mb = page.mediabox
        w  = float(mb.width)
        h  = float(mb.height)
        rot = page.get("/Rotate", 0)
        page_table.add_row(str(i), f"{w:.0f} pt", f"{h:.0f} pt", f"{rot}°")
        if i >= 20 and total > 20:
            page_table.add_row("…", f"({total - 20} more pages)", "", "")
            break

    console.print(page_table)


# ── Extract Text & Tables ──────────────────────────────────────────────────────

def run_extract_text() -> None:
    """Extract all text and tables from a PDF; save to .txt file."""
    console.print("  [bold]Extract Text & Tables[/bold]\n")
    divider()

    try:
        import pdfplumber
    except ImportError:
        warn("pdfplumber is not installed. Run: pip install pdfplumber")
        return

    input_path  = prompt_input_file("Input PDF path")
    default_out = f"{input_path.stem}_extracted.txt"
    output_path = prompt_output_file("Output .txt path", default=default_out)
    if output_path.suffix.lower() != ".txt":
        output_path = output_path.with_suffix(".txt")

    divider()
    info(f"Extracting from [bold]{input_path.name}[/bold] …")

    sections = []
    with pdfplumber.open(str(input_path)) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages, 1):
            header = f"\n{'='*60}\nPAGE {i} of {total}\n{'='*60}\n"
            body   = page.extract_text() or "[No selectable text on this page]"
            tables = page.extract_tables()

            table_text = ""
            if tables:
                table_text = f"\n\n--- {len(tables)} TABLE(S) FOUND ---\n"
                for t_idx, table in enumerate(tables, 1):
                    table_text += f"\nTable {t_idx}:\n"
                    for row in table:
                        table_text += "  | " + " | ".join(
                            str(cell or "").strip() for cell in row
                        ) + " |\n"

            sections.append(header + body + table_text)
            info(
                f"  Page {i:>{len(str(total))}}/{total}  "
                f"{len(body):>6} chars  "
                f"{'[dim]' + str(len(tables)) + ' table(s)[/dim]' if tables else ''}"
            )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(sections), encoding="utf-8")

    divider()
    success(
        f"Extracted {total} page(s) → [bold]{output_path}[/bold]  "
        f"({output_path.stat().st_size:,} bytes)"
    )
