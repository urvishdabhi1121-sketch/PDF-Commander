"""
modules/converter.py
====================
Convert PDFs to Word, Word to PDF, and PDF to plain text.
All processing is local — no files leave your machine.
"""

from pathlib import Path
from rich.console import Console
from modules._helpers import (
    prompt_input_file,
    prompt_output_file,
    success, info, warn, divider,
)

console = Console()


# ── PDF → Word ─────────────────────────────────────────────────────────────────

def pdf_to_word() -> None:
    """Convert a PDF file to a Word (.docx) document using pdf2docx."""
    console.print("  [bold]PDF → Word (.docx)[/bold]\n")
    divider()

    try:
        from pdf2docx import Converter
    except ImportError:
        warn("pdf2docx is not installed. Run: pip install pdf2docx")
        return

    input_path  = prompt_input_file("Input PDF path")
    default_out = input_path.with_suffix(".docx").name
    output_path = prompt_output_file("Output .docx path", default=default_out)
    if output_path.suffix.lower() != ".docx":
        output_path = output_path.with_suffix(".docx")

    divider()
    info(f"Converting [bold]{input_path.name}[/bold] → [bold]{output_path.name}[/bold] …")

    cv = Converter(str(input_path))
    cv.convert(str(output_path), start=0, end=None)
    cv.close()

    divider()
    success(f"Saved Word document → [bold]{output_path}[/bold]")


# ── Word → PDF ─────────────────────────────────────────────────────────────────

def word_to_pdf() -> None:
    """
    Convert a Word (.docx) file to PDF.
    Uses docx2pdf, which calls LibreOffice (Linux/macOS) or Word (Windows).
    """
    console.print("  [bold]Word (.docx) → PDF[/bold]\n")
    divider()

    try:
        from docx2pdf import convert
    except ImportError:
        warn("docx2pdf is not installed. Run: pip install docx2pdf")
        return

    # Accept .docx input
    console.print("  [dim]Accepts .docx files. LibreOffice required on Linux/macOS.[/dim]\n")
    raw        = console.input("  [cyan]Input .docx path: [/cyan]").strip().strip('"').strip("'")
    input_path = Path(raw)
    if not input_path.is_file():
        warn(f"File not found: {input_path}")
        return

    default_out = input_path.with_suffix(".pdf").name
    output_path = prompt_output_file("Output PDF path", default=default_out)
    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    divider()
    info(f"Converting [bold]{input_path.name}[/bold] → [bold]{output_path.name}[/bold] …")
    info("(This may take a few seconds while LibreOffice/Word processes the file.)")

    try:
        convert(str(input_path), str(output_path))
    except Exception as exc:
        warn(f"Conversion failed: {exc}")
        warn("Ensure LibreOffice is installed: https://www.libreoffice.org/download/")
        return

    divider()
    success(f"Saved PDF → [bold]{output_path}[/bold]")


# ── PDF → Plain Text ───────────────────────────────────────────────────────────

def pdf_to_text() -> None:
    """Extract all text from a PDF and write it to a .txt file."""
    console.print("  [bold]PDF → Plain Text (.txt)[/bold]\n")
    divider()

    try:
        import pdfplumber
    except ImportError:
        warn("pdfplumber is not installed. Run: pip install pdfplumber")
        return

    input_path  = prompt_input_file("Input PDF path")
    default_out = input_path.with_suffix(".txt").name
    output_path = prompt_output_file("Output .txt path", default=default_out)
    if output_path.suffix.lower() != ".txt":
        output_path = output_path.with_suffix(".txt")

    divider()
    info(f"Extracting text from [bold]{input_path.name}[/bold] …")

    all_text = []
    with pdfplumber.open(str(input_path)) as pdf:
        total = len(pdf.pages)
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            all_text.append(f"{'='*60}\nPage {i} of {total}\n{'='*60}\n{text}\n")
            info(f"  Page {i:>{len(str(total))}}/{total} — {len(text)} chars")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(all_text), encoding="utf-8")

    divider()
    success(
        f"Extracted {total} page(s) of text → [bold]{output_path}[/bold]  "
        f"({output_path.stat().st_size:,} bytes)"
    )
