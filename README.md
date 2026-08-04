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

---

# PDF Page Labeler CLI

A Python utility that updates PDF metadata to display custom page numbers (such as **"Cover"**, lowercase/uppercase **Roman numerals**, or standard **Arabic numbers**) in PDF viewers like Adobe Acrobat, Preview, or Google Chrome.

---

## Overview

PDF readers distinguish between physical page indexes (0, 1, 2...) and display page labels. This tool uses [PyMuPDF](https://pymupdf.readthedocs.io/) to read human-readable label rules from a YAML configuration file and inject them directly into the PDF metadata without re-rendering or modifying the page contents.

---

## Prerequisites

Install the required Python packages:

```bash
pip install pymupdf pyyaml
```

---

## Configuration (`.yaml`) Format

Define page rules in a YAML file using zero-based page indexes (`startpage`).

```yaml
# Page index 0 (1st page) displays literally as "Cover"
- startpage: 0
  prefix: "Cover"

# Page index 1 (2nd page) starts lowercase Roman numerals (i, ii, iii...)
- startpage: 1
  style: "r"
  firstpagenum: 1

# Page index 4 (5th page) resets to standard Arabic numbers (1, 2, 3...)
- startpage: 4
  style: "D"
  firstpagenum: 1
```

### Configuration Options

| Key | Required | Type | Description |
| :--- | :--- | :--- | :--- |
| **`startpage`** | **Yes** | Integer | Zero-based index where the rule takes effect (`0` = 1st page of document). |
| **`style`** | No | String | Numbering style: `"r"` (i, ii), `"R"` (I, II), `"D"` (1, 2), `"a"` (a, b), `"A"` (A, B). Omit for static labels. |
| **`firstpagenum`**| No | Integer | Initial numeric value for the sequence (defaults to `1`). |
| **`prefix`** | No | String | Text prepended to the page label (e.g., `"Cover"` or `"App-"`). |

---

## Command Line Usage

The script accepts input arguments either **positionally** or via **flags** (`-i`, `-c`, `-o`). If no YAML file is specified, it automatically looks for a `.yaml` file matching the base name of the input PDF.

### Usage Syntax

```bash
python set_labels.py [INPUT_PDF] [YAML_CONFIG] [-i INPUT] [-c CONFIG] [-o OUTPUT]
```

### Examples

**1. Pure Positional Arguments**
```bash
python set_labels.py book.pdf rules.yaml
```

**2. Implicit Configuration File**
*(Automatically resolves to `book.yaml` and saves to `book_labeled.pdf`)*
```bash
python set_labels.py book.pdf
```

**3. Pure Flag Arguments**
```bash
python set_labels.py -i book.pdf -c rules.yaml
```

**4. Specifying a Custom Output File**
```bash
python set_labels.py book.pdf rules.yaml -o final_document.pdf
```

---

## CLI Options Reference

| Argument / Flag | Type | Description |
| :--- | :--- | :--- |
| **`pos_input`** | Positional | Optional path to the input PDF file. |
| **`pos_config`** | Positional | Optional path to the YAML rules file. |
| **`-i`, `--input`** | Flag | Optional path to the input PDF file (overrides positional input). |
| **`-c`, `--config`** | Flag | Optional path to the YAML rules file (overrides positional config). |
| **`-o`, `--output`** | Flag | Optional path for the generated PDF. Defaults to `<input_stem>_labeled.pdf`. |