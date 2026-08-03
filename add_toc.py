import argparse
import csv
from pathlib import Path
import pymupdf


def parse_csv_toc(csv_file_path: Path, page_offset: int = 0) -> list:
    """Parses a 1-indexed CSV TOC file into PyMuPDF TOC structure."""
    toc = []
    with open(csv_file_path, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not any(row):  # Skip empty lines
                continue

            level = int(row[0].strip())
            title = row[1].strip()
            # Convert 1-indexed printed page + offset to 0-indexed PyMuPDF page
            page = int(row[2].strip()) + page_offset - 1

            toc.append([level, title, page])
    return toc


def main():
    parser = argparse.ArgumentParser(
        prog="add_toc",
        description="Automatically insert a Table of Contents into a PDF using a CSV file."
    )

    # Positional Argument: Input PDF
    parser.add_argument("pdf_path", type=Path, help="Path to the PDF file")

    # Optional Positional Argument: CSV file path
    parser.add_argument(
        "csv_path",
        type=Path,
        nargs="?",  # Makes this positional argument optional
        default=None,
        help="Path to the CSV file (Defaults to same filename with .csv extension)",
    )

    # Flag Argument: Page Offset
    parser.add_argument(
        "-o",
        "--offset",
        type=int,
        default=0,
        metavar="INT",
        help="Page offset integer to adjust printed page numbers (Default: 0)",
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s 1.0.0",  # Note: %(prog)s automatically injects your prog variable
    )

    args = parser.parse_args()

    pdf_path = args.pdf_path.expanduser()

    # If CSV path is omitted, default to <pdf_filename>.csv in the same directory
    csv_path = (
        args.csv_path.expanduser()
        if args.csv_path
        else pdf_path.with_suffix(".csv")
    )

    # File Validation
    if not pdf_path.exists():
        print(f"Error: PDF file not found at '{pdf_path}'")
        return

    if not csv_path.exists():
        print(f"Error: CSV file not found at '{csv_path}'")
        return

    print(f"Processing PDF : {pdf_path.name}")
    print(f"Using CSV      : {csv_path.name}")
    print(f"Page Offset    : {args.offset}")

    # Process Document
    doc = pymupdf.open(pdf_path)
    toc = parse_csv_toc(csv_path, page_offset=args.offset)

    doc.set_toc(toc)

    # Save to a new file to prevent accidental overwrite
    output_path = pdf_path.parent / f"{pdf_path.stem}_with_toc.pdf"
    doc.save(output_path, garbage=4, deflate=True)
    doc.close()

    print(f"Done! Saved output to: {output_path}")


if __name__ == "__main__":
    main()