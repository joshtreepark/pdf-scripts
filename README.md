# add_toc

A lightweight command-line tool built with [PyMuPDF](https://pymupdf.readthedocs.io/) to quickly parse and insert a Table of Contents (TOC) into any PDF document using a simple CSV file.

---

## Features

- **Human-Friendly CSV Input:** Easily define document structure without editing complex nested lists in code.
- **Automatic Page Offset:** Enter natural printed page numbers from the book; the script handles PDF 0-indexing and cover page offsets.
- **Smart Defaults:** Omit the CSV argument, and `add_toc` automatically checks for a `.csv` file matching your PDF's name.
- **Safe Output:** Generates a new file (`<filename>_with_toc.pdf`) so your original PDF is never overwritten.

---

## Prerequisites & Installation

### 1. Requirements
* Python 3.8+
* [PyMuPDF](https://pymupdf.readthedocs.io/)

### 2. Setup Virtual Environment

```bash
# Clone or navigate to your project directory
cd /path/to/project

# Create a virtual environment
python3 -m venv .venv

# Install required dependencies
./.venv/bin/pip install pymupdf

```

---

## CSV File Formatting

Create a CSV file containing three columns without headers: `Level`, `Title`, `Page Number`.

```csv
1, Introduction, 1
1, Chapter 1: Early Life, 15
2, 1.1 Family Background, 17
2, 1.2 Education, 25
1, Chapter 2: Revolutionary Movement, 45

```

### Columns Explanation:

1. **Level (`int`):** Hierarchy depth (`1` for main chapters/parts, `2` for sub-sections, `3` for sub-sub-sections).
2. **Title (`string`):** The exact text title to display in the PDF bookmark list.
3. **Page (`int`):** The **printed page number** as shown inside the book itself (1-indexed).

---

## Usage

You can run the script using your virtual environment's Python binary directly—no need to manage `activate`/`deactivate` shell states:

```bash
./.venv/bin/python add_toc.py [PDF_PATH] [CSV_PATH] [-o OFFSET]

```

### Examples

#### 1. Standard Execution (Auto-detect CSV)

If your PDF and CSV share the same base name (e.g., `book.pdf` and `book.csv` in the same directory):

```bash
./.venv/bin/python add_toc.py ~/Desktop/book.pdf -o 14

```

#### 2. Specifying a Custom CSV Path

```bash
./.venv/bin/python add_toc.py ~/Desktop/book.pdf ~/Documents/my_structure.csv -o 12

```

#### 3. No Page Offset

If physical PDF page 1 aligns directly with printed page 1:

```bash
./.venv/bin/python add_toc.py ~/Desktop/book.pdf

```

---

## How Page Offsets Work (`-o` / `--offset`)

Books frequently have front matter (covers, copyright, forewords) that push "Printed Page 1" several pages into the physical PDF file.

* **Example:** If Chapter 1 starts on **printed page 1**, but that page is the **15th physical page** of your PDF file, your page offset is `14`.

Passing `-o 14` automatically translates every page number in your CSV into the correct zero-indexed location required by PyMuPDF.

---

## Command-Line Arguments Reference

To view all supported flags and usage instructions from the terminal:

```bash
./.venv/bin/python add_toc.py --help

```

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `pdf_path` | Positional | *Required* | Path to the target PDF document. |
| `csv_path` | Positional | `None` | Path to the CSV file. Defaults to `<pdf_filename>.csv` if omitted. |
| `-o`, `--offset` | Flag | `0` | Integer adjustment for cover/front-matter pages. |
| `-h`, `--help` | Flag | — | Displays the help message and exits. |
