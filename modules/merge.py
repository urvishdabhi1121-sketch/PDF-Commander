"""
modules/merge.py
================
Merge two or more PDF files into a single output PDF.
All processing is local — no files leave your machine.
"""

from pypdf import PdfWriter, PdfReader
from rich.console import Console
from modules._helpers import (
    prompt_multiple_files,
    prompt_output_file,
    success, info, warn, divider,
)

console = Console()


def run() -> None:
    """Interactive merge: collect input PDFs, write combined output."""
    console.print("  [bold]Merge PDFs[/bold] — combine multiple PDFs into one.\n")
    divider()

    # ── Collect input files ────────────────────────────────────────────────────
    input_files = prompt_multiple_files("PDFs to merge (in order)")
    if len(input_files) < 2:
        warn("Merge requires at least two PDF files. Aborting.")
        return

    divider()
    info(f"Files queued for merge ({len(input_files)}):")
    for i, f in enumerate(input_files, 1):
        console.print(f"    [dim]{i}.[/dim] {f}")

    # ── Output path ────────────────────────────────────────────────────────────
    divider()
    output_path = prompt_output_file("Output file", default="merged_output.pdf")
    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    # ── Merge ──────────────────────────────────────────────────────────────────
    divider()
    writer = PdfWriter()
    total_pages = 0

    for pdf_path in input_files:
        try:
            reader = PdfReader(str(pdf_path))
            for page in reader.pages:
                writer.add_page(page)
            total_pages += len(reader.pages)
            info(f"Added {len(reader.pages):>3} page(s) from  {pdf_path.name}")
        except Exception as exc:
            warn(f"Skipping {pdf_path.name}: {exc}")

    if total_pages == 0:
        warn("No pages were collected. Nothing to write.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as out:
        writer.write(out)

    divider()
    success(f"Merged {total_pages} page(s) → [bold]{output_path}[/bold]")
