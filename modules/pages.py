"""
modules/pages.py
================
Page-level operations: rotate, extract specific pages, add watermark.
All processing is local — no files leave your machine.
"""

from pathlib import Path
from pypdf import PdfReader, PdfWriter
from rich.console import Console
from modules._helpers import (
    prompt_input_file,
    prompt_output_file,
    prompt_int,
    success, info, warn, divider,
)

console = Console()

VALID_ROTATIONS = [90, 180, 270]


# ── Rotate Pages ───────────────────────────────────────────────────────────────

def run_rotate() -> None:
    """Rotate all or specific pages of a PDF by 90, 180, or 270 degrees."""
    console.print("  [bold]Rotate Pages[/bold]\n")
    divider()

    input_path = prompt_input_file("Input PDF path")
    reader     = PdfReader(str(input_path))
    total      = len(reader.pages)
    info(f"Document has {total} page(s).")

    # Choose rotation angle
    divider()
    console.print("  [cyan]Rotation angle:[/cyan]")
    console.print("    [bold yellow]1[/bold yellow]  90°  clockwise")
    console.print("    [bold yellow]2[/bold yellow]  180° (upside-down)")
    console.print("    [bold yellow]3[/bold yellow]  270° clockwise (= 90° counter-clockwise)")
    angle_map = {"1": 90, "2": 180, "3": 270}
    raw = console.input("  [cyan]Choice [1/2/3]: [/cyan]").strip()
    if raw not in angle_map:
        warn("Invalid choice. Aborting.")
        return
    degrees = angle_map[raw]

    # Which pages?
    divider()
    console.print("  [cyan]Apply to:[/cyan]")
    console.print("    [bold yellow]A[/bold yellow]  All pages")
    console.print("    [bold yellow]R[/bold yellow]  Specific page range (e.g. 2-4)")
    scope = console.input("  [cyan]Choice [A/R]: [/cyan]").strip().upper()

    if scope == "R":
        console.print(f"  [dim]Pages 1–{total}[/dim]")
        raw_range = console.input(f"  [cyan]Range (e.g. 1-{total}): [/cyan]").strip()
        try:
            parts = raw_range.split("-")
            start = int(parts[0].strip()) - 1
            end   = int(parts[1].strip()) - 1 if len(parts) > 1 else start
        except (ValueError, IndexError):
            warn("Could not parse range. Aborting.")
            return
        page_indices = list(range(max(0, start), min(total - 1, end) + 1))
    else:
        page_indices = list(range(total))

    # Output path
    divider()
    default_out = f"{input_path.stem}_rotated{input_path.suffix}"
    output_path = prompt_output_file("Output PDF path", default=default_out)
    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    # Rotate and write
    writer = PdfWriter()
    for i, page in enumerate(reader.pages):
        if i in page_indices:
            page.rotate(degrees)
        writer.add_page(page)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        writer.write(f)

    divider()
    success(
        f"Rotated {len(page_indices)} page(s) by {degrees}° → [bold]{output_path}[/bold]"
    )


# ── Extract Specific Pages ─────────────────────────────────────────────────────

def run_extract() -> None:
    """Extract a subset of pages from a PDF into a new file."""
    console.print("  [bold]Extract Specific Pages[/bold]\n")
    divider()

    input_path = prompt_input_file("Input PDF path")
    reader     = PdfReader(str(input_path))
    total      = len(reader.pages)
    info(f"Document has {total} page(s).")

    divider()
    console.print(
        f"  [cyan]Pages to extract[/cyan] [dim](e.g. 1,3,5-8 · max={total}):[/dim]"
    )
    raw     = console.input("  [cyan]Pages: [/cyan]").strip()

    # Parse the range expression
    indices = set()
    for token in raw.split(","):
        token = token.strip()
        if "-" in token:
            try:
                a, b = token.split("-", 1)
                indices.update(range(int(a) - 1, int(b)))
            except ValueError:
                warn(f"Skipping invalid token: '{token}'")
        elif token.isdigit():
            indices.add(int(token) - 1)
        elif token:
            warn(f"Skipping invalid token: '{token}'")

    indices = sorted(i for i in indices if 0 <= i < total)
    if not indices:
        warn("No valid pages selected. Aborting.")
        return
    info(f"Extracting {len(indices)} page(s): {[i+1 for i in indices]}")

    divider()
    default_out = f"{input_path.stem}_extract.pdf"
    output_path = prompt_output_file("Output PDF path", default=default_out)
    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    writer = PdfWriter()
    for i in indices:
        writer.add_page(reader.pages[i])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        writer.write(f)

    divider()
    success(f"Extracted {len(indices)} page(s) → [bold]{output_path}[/bold]")


# ── Add Watermark ──────────────────────────────────────────────────────────────

def run_watermark() -> None:
    """
    Overlay a watermark PDF onto every page of an input PDF.
    The watermark PDF must be a single-page PDF (e.g. 'watermark.pdf').
    """
    console.print("  [bold]Add Watermark[/bold]\n")
    divider()
    console.print(
        "  [dim]You need a single-page PDF as the watermark overlay.\n"
        "  You can create one in any PDF editor or with reportlab.[/dim]\n"
    )

    input_path     = prompt_input_file("Input PDF path")
    watermark_path = prompt_input_file("Watermark PDF path (single page)")

    reader    = PdfReader(str(input_path))
    watermark = PdfReader(str(watermark_path)).pages[0]
    total     = len(reader.pages)
    info(f"Applying watermark to {total} page(s)…")

    divider()
    default_out = f"{input_path.stem}_watermarked.pdf"
    output_path = prompt_output_file("Output PDF path", default=default_out)
    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    writer = PdfWriter()
    for page in reader.pages:
        page.merge_page(watermark)
        writer.add_page(page)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        writer.write(f)

    divider()
    success(f"Watermarked {total} page(s) → [bold]{output_path}[/bold]")
