@ -0,0 +1,207 @@
# PDF-Commander

> **Privacy-First · Local-Only · No Cloud · No Telemetry**

A professional-grade, modular command-line toolkit for every PDF operation you'll ever need. Every byte of processing happens on your machine. No files are uploaded. No accounts required. No analytics phoning home.

---

## Philosophy

Most PDF tools are SaaS products that ask you to upload sensitive documents to a stranger's server. PDF-Commander is the opposite. It is a local Python application that runs entirely on your hardware. Your payslips, contracts, medical records, and confidential reports never leave your disk.

The codebase is deliberately modular — each operation lives in its own file under `modules/`. You can read, audit, or modify any single feature without touching the rest.

---

## Features

### Merge & Split
| Operation | Description |
|---|---|
| **Merge PDFs** | Combine any number of PDFs into one, in any order |
| **Split (by page)** | Burst a PDF into individual single-page files |
| **Split (by range)** | Extract custom ranges (e.g. `1-3,5,8-10`) into separate files |

### Conversion
| Operation | Description |
|---|---|
| **PDF → Word** | Convert a PDF to an editable `.docx` file |
| **Word → PDF** | Convert a `.docx` file to PDF via LibreOffice/Microsoft Word |
| **PDF → Text** | Extract all selectable text to a clean `.txt` file |

### Pages & Layout
| Operation | Description |
|---|---|
| **Rotate Pages** | Rotate all or specific pages by 90°, 180°, or 270° |
| **Extract Pages** | Pull out specific pages into a new PDF |
| **Add Watermark** | Overlay a watermark PDF onto every page |

### Security
| Operation | Description |
|---|---|
| **Encrypt PDF** | Add AES-256 password protection (user + owner passwords) |
| **Decrypt PDF** | Remove password protection from a PDF you own |
| **Redact Metadata** | Strip author, creation dates, XMP data, and all hidden info |

### Inspection
| Operation | Description |
|---|---|
| **Inspect PDF** | View metadata, page count, dimensions, encryption status |
| **Extract Text & Tables** | Export all text and structured tables to a `.txt` file |

---

## Project Structure

```
PDF-Commander/
│
├── main.py                  # Entry point — interactive CLI menu
├── requirements.txt         # All Python dependencies
├── README.md                # This file
│
└── modules/                 # One file per feature area
    ├── __init__.py
    ├── _helpers.py          # Shared prompt/output utilities
    ├── merge.py             # Merge operation
    ├── split.py             # Split operations
    ├── converter.py         # Format conversion
    ├── pages.py             # Rotate, extract, watermark
    ├── security.py          # Encrypt, decrypt, metadata redaction
    └── inspect.py           # PDF info and text/table extraction
```

---

## Installation

### 1. Prerequisites

- **Python 3.10+** — [python.org](https://www.python.org/downloads/)
- **LibreOffice** *(only required for Word → PDF conversion on Linux/macOS)*
  - Ubuntu/Debian: `sudo apt install libreoffice`
  - macOS: [libreoffice.org](https://www.libreoffice.org/download/)
  - Windows: not required (uses Microsoft Word automatically)
- **Tesseract** *(only required for OCR on scanned PDFs)*
  - Ubuntu/Debian: `sudo apt install tesseract-ocr`
  - macOS: `brew install tesseract`

### 2. Clone & install

```bash
# Clone the repository
git clone https://github.com/your-username/pdf-commander.git
cd pdf-commander

# Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

# Install all dependencies
pip install -r requirements.txt
```

---

## How to Run

```bash
python main.py
```

You will see the main menu:

```
 ██████╗ ██████╗ ███████╗      ██████╗ ███╗   ███╗██████╗ 
...

╭─────────────────────────────────────────────────────────╮
│  Privacy-First · Local-Only · No Cloud · No Telemetry   │
│  All processing happens 100% on your machine.           │
╰─────────────────────────────────────────────────────────╯

  #    Operation
 ───  ─────────────────────────────────────────
       ── MERGE & SPLIT ──────────────────────
   1   Merge PDFs
   2   Split PDF (by page)
   3   Split PDF (by range)
       ── CONVERSION ─────────────────────────
   4   PDF → Word (.docx)
  ...

Select an operation [0–14]:
```

- Enter a number and press **Enter** to select an operation.
- Each operation will guide you through the required inputs with clear prompts.
- Press **Enter** after any operation completes to return to the main menu.
- Enter **0** to exit cleanly.

### Tip — keyboard shortcuts

| Key | Action |
|---|---|
| `Ctrl+C` at a prompt | Cancel the current operation and return to menu |
| `Ctrl+C` at the main menu | Exit the program |

---

## Dependencies

| Library | Version | Purpose |
|---|---|---|
| `pypdf` | ≥ 4.0 | Core PDF manipulation (merge, split, rotate, encrypt) |
| `pikepdf` | ≥ 8.0 | AES-256 encryption, decryption, metadata redaction |
| `pdfplumber` | ≥ 0.10 | Text and table extraction with layout awareness |
| `pdf2docx` | ≥ 0.5 | PDF → Word conversion |
| `docx2pdf` | ≥ 0.1 | Word → PDF conversion |
| `reportlab` | ≥ 4.0 | Programmatic PDF creation (watermark support) |
| `pdf2image` | ≥ 1.16 | PDF → image conversion for OCR |
| `pytesseract` | ≥ 0.3 | OCR wrapper (requires Tesseract binary) |
| `rich` | ≥ 13.0 | Terminal UI — menus, tables, colours |
| `click` | ≥ 8.1 | CLI argument parsing used internally |

---

## Privacy Guarantee

PDF-Commander makes **zero network requests** during normal operation. It contains no analytics, no update checks, no crash reporters, and no licensing calls. You can verify this yourself — every network-capable call would require an import of `requests`, `httpx`, `urllib`, or similar, none of which appear in the source outside of `requirements.txt`.

To run in a fully air-gapped environment, simply install dependencies once while online, then disconnect.

---

## Extending PDF-Commander

Adding a new operation takes three steps:

1. Create (or add a function to) a file in `modules/`:

```python
# modules/my_feature.py
from modules._helpers import prompt_input_file, success

def run():
    path = prompt_input_file("Input PDF")
    # ... your logic ...
    success("Done!")
```

2. Register it in `main.py`'s `MENU_ITEMS` dict:

```python
"15": ("My New Feature", "modules.my_feature", "run"),
```

3. Add a `CATEGORY_HEADERS` entry if you're starting a new section (optional).

That's it. No framework wiring, no decorators, no config files.

---

## License

MIT — free to use, modify, and distribute.
