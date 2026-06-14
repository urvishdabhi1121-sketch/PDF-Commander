"""
modules/security.py
===================
Security operations: AES encryption, password removal, metadata redaction.
Uses pikepdf for robust, standards-compliant PDF security.
All processing is local — no files leave your machine.
"""

from pathlib import Path
from rich.console import Console
from modules._helpers import (
    prompt_input_file,
    prompt_output_file,
    prompt_password,
    success, info, warn, divider,
)

console = Console()


# ── Encrypt (password protect) ─────────────────────────────────────────────────

def run_encrypt() -> None:
    """Add AES-256 password protection to a PDF (user + optional owner password)."""
    console.print("  [bold]Encrypt PDF[/bold] — add password protection\n")
    divider()

    try:
        import pikepdf
    except ImportError:
        warn("pikepdf is not installed. Run: pip install pikepdf")
        return

    input_path = prompt_input_file("Input PDF path")
    divider()

    console.print("  [dim]Set a user password (required to open the file).[/dim]")
    user_pw = prompt_password("User password")
    if not user_pw:
        warn("Password cannot be empty. Aborting.")
        return
    confirm = prompt_password("Confirm user password")
    if user_pw != confirm:
        warn("Passwords do not match. Aborting.")
        return

    console.print("\n  [dim]Optionally set an owner password (controls editing/printing).[/dim]")
    console.print("  [dim]Press Enter to use the same password as owner.[/dim]")
    owner_pw = prompt_password("Owner password (Enter to skip)")
    if not owner_pw:
        owner_pw = user_pw

    divider()
    default_out = f"{input_path.stem}_encrypted.pdf"
    output_path = prompt_output_file("Output PDF path", default=default_out)
    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    divider()
    info("Encrypting with AES-256…")

    with pikepdf.open(str(input_path)) as pdf:
        permissions = pikepdf.Permissions(
            extract=False,
            modify_annotation=False,
            modify_form=False,
            modify_other=False,
            print_lowres=True,
            print_highres=True,
        )
        encryption = pikepdf.Encryption(
            user=user_pw,
            owner=owner_pw,
            R=6,                   # PDF 2.0 / AES-256
            allow=permissions,
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        pdf.save(str(output_path), encryption=encryption)

    divider()
    success(f"Encrypted with AES-256 → [bold]{output_path}[/bold]")


# ── Decrypt (remove password) ──────────────────────────────────────────────────

def run_decrypt() -> None:
    """Remove password protection from a PDF you own (requires the password)."""
    console.print("  [bold]Decrypt PDF[/bold] — remove password protection\n")
    divider()

    try:
        import pikepdf
    except ImportError:
        warn("pikepdf is not installed. Run: pip install pikepdf")
        return

    input_path = prompt_input_file("Input (encrypted) PDF path")
    divider()
    password = prompt_password("Current PDF password")

    divider()
    default_out = f"{input_path.stem}_decrypted.pdf"
    output_path = prompt_output_file("Output PDF path", default=default_out)
    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    divider()
    info("Decrypting…")

    try:
        with pikepdf.open(str(input_path), password=password) as pdf:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            pdf.save(str(output_path))
    except pikepdf.PasswordError:
        warn("Incorrect password. Decryption failed.")
        return
    except Exception as exc:
        warn(f"Unexpected error: {exc}")
        return

    divider()
    success(f"Decrypted (no password) → [bold]{output_path}[/bold]")


# ── Redact Metadata ────────────────────────────────────────────────────────────

def run_redact_metadata() -> None:
    """
    Strip all identifying metadata from a PDF:
    Author, Creator, Producer, Title, Subject, Keywords,
    Creation/Modification dates, and any custom XMP data.
    """
    console.print("  [bold]Redact Metadata[/bold] — remove author, dates, and all hidden info\n")
    divider()

    try:
        import pikepdf
        from pikepdf import Dictionary, Name
    except ImportError:
        warn("pikepdf is not installed. Run: pip install pikepdf")
        return

    input_path = prompt_input_file("Input PDF path")
    divider()
    default_out = f"{input_path.stem}_clean.pdf"
    output_path = prompt_output_file("Output PDF path", default=default_out)
    if output_path.suffix.lower() != ".pdf":
        output_path = output_path.with_suffix(".pdf")

    divider()
    info("Reading existing metadata…")

    with pikepdf.open(str(input_path)) as pdf:
        # Show what we're about to remove
        if "/Info" in pdf.trailer:
            info_dict = pdf.trailer["/Info"]
            meta_keys = [str(k) for k in info_dict.keys()]
            if meta_keys:
                info(f"Found metadata keys: {', '.join(meta_keys)}")
            else:
                info("No /Info dictionary entries found.")
        else:
            info("No /Info dictionary found.")

        # Wipe standard Info dictionary
        pdf.trailer["/Info"] = Dictionary()

        # Remove XMP metadata stream if present
        if "/Root" in pdf.trailer:
            root = pdf.trailer["/Root"]
            if "/Metadata" in root:
                del root["/Metadata"]
                info("Removed embedded XMP metadata stream.")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        pdf.save(str(output_path))

    divider()
    success(f"Metadata redacted → [bold]{output_path}[/bold]")
    info("Author, Creator, Producer, Title, Subject, Dates, and XMP data removed.")
