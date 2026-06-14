"""
modules/split.py
================
Split a PDF into individual pages or custom page ranges.
All processing is local — no files leave your machine.
"""

from pathlib import Path
from pypdf import PdfReader, PdfWriter
from rich.console import Console
from modules._helpers import (
    prompt_input_file,
    prompt_output_dir,
    success, info, warn, divider,
)

console = Console()


# ── Helper ─────────────────────────────────────────────────────────────────────

def _parse_ranges(raw: str, max_page: int) -> list[list[int]]:
    """
    Parse a range string like "1-3,5,7-9" into lists of 0-based page indices.
    Returns a list of groups, each group = list of 0-based indices.
    """
    groups = []
    for token in raw.split(","):
        token = token.strip()
        if not token:
            continue
        if "-" in token:
            parts = token.split("-", 1)
            try:
                start = int(parts[0].strip())
                end   = int(parts[1].strip())
            except ValueError:
                warn(f"Ignoring invalid range: '{token}'")
                continue
            if not (1 <= start <= end <= max_page):
                warn(f"Range {token} out of bounds (1–{max_page}), skipping.")
                continue
            groups.append(list(range(start - 1, end)))
        else:
            try:
                page_num = int(token)
            except ValueError:
                warn(f"Ignoring invalid page: '{token}'")
                continue
            if not (1 <= page_num <= max_page):
                warn(f"Page {page_num} out of bounds (1–{max_page}), skipping.")
                continue
            groups.append([page_num - 1])
    return groups


def _write_subset(reader: PdfReader, indices: list[int], out_path: Path) -> None:
    writer = PdfWriter()
    for idx in indices:
        writer.add_page(reader.pages[idx])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        writer.write(f)


# ── Public functions ───────────────────────────────────────────────────────────

def run_by_page() -> None:
    """Split every page of a PDF into a separate file."""
    console.print("  [bold]Split PDF — one file per page[/bold]\n")
    divider()

    input_path = prompt_input_file("Input PDF path")
    reader     = PdfReader(str(input_path))
    total      = len(reader.pages)
    info(f"Document has {total} page(s).")
    divider()

    output_dir = prompt_output_dir("Output directory for page files")
    stem       = input_path.stem
    divider()

    for i in range(total):
        out_path = output_dir / f"{stem}_page_{i + 1:04d}.pdf"
        _write_subset(reader, [i], out_path)
        info(f"Wrote page {i + 1:>{len(str(total))}} → {out_path.name}")

    divider()
    success(f"Split into {total} file(s) in [bold]{output_dir}[/bold]")


def run_by_range() -> None:
    """Split a PDF into one file per user-defined page range."""
    console.print("  [bold]Split PDF — by page range[/bold]\n")
    divider()

    input_path = prompt_input_file("Input PDF path")
    reader     = PdfReader(str(input_path))
    total      = len(reader.pages)
    info(f"Document has {total} page(s).")
    divider()

    console.print(
        f"  [cyan]Enter page ranges[/cyan] [dim](e.g. 1-3,5,7-9 · max page = {total}):[/dim]"
    )
    raw    = console.input("  [cyan]Ranges: [/cyan]").strip()
    groups = _parse_ranges(raw, total)

    if not groups:
        warn("No valid ranges parsed. Aborting.")
        return

    divider()
    output_dir = prompt_output_dir("Output directory")
    stem       = input_path.stem
    divider()

    for i, indices in enumerate(groups, 1):
        label    = f"pages_{indices[0]+1}-{indices[-1]+1}"
        out_path = output_dir / f"{stem}_{label}.pdf"
        _write_subset(reader, indices, out_path)
        info(f"Range {i}: pages {indices[0]+1}–{indices[-1]+1} → {out_path.name}")

    divider()
    success(f"Created {len(groups)} file(s) in [bold]{output_dir}[/bold]")
