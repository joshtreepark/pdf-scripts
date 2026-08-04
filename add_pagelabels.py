import argparse
from pathlib import Path
import pymupdf
import yaml


def main():
    parser = argparse.ArgumentParser(
        description="Apply YAML-defined page labels (e.g., Cover, Roman, Arabic) to a PDF."
    )
    # Positional arguments (both optional via nargs="?")
    parser.add_argument("pos_input", nargs="?", help="Path to input PDF file (positional)")
    parser.add_argument("pos_config", nargs="?", help="Path to YAML config file (positional)")

    # Optional flag aliases
    parser.add_argument("-i", "--input", dest="flag_input", help="Path to input PDF file (flag)")
    parser.add_argument("-c", "--config", dest="flag_config", help="Path to YAML config file (flag)")
    parser.add_argument("-o", "--output", help="Path to output PDF file (optional)")

    args = parser.parse_args()

    # Collect positional arguments passed in order
    positionals = [p for p in (args.pos_input, args.pos_config) if p is not None]

    # Resolve PDF input path (flags take precedence over positionals)
    raw_input = args.flag_input or (positionals.pop(0) if positionals else None)
    if not raw_input:
        parser.error("You must provide an input PDF path (positionally or via -i/--input).")

    input_path = Path(raw_input)

    # Resolve YAML config path (if omitted entirely, defaults to <pdf_stem>.yaml)
    raw_config = args.flag_config or (positionals.pop(0) if positionals else None)
    config_path = Path(raw_config) if raw_config else input_path.with_suffix(".yaml")

    # Validate file paths
    if not input_path.exists():
        raise FileNotFoundError(f"PDF not found: {input_path}")
    if not config_path.exists():
        raise FileNotFoundError(f"YAML config not found: {config_path}")

    # Load label rules from YAML
    with open(config_path, "r", encoding="utf-8") as f:
        labels = yaml.safe_load(f)

    # Apply labels in PyMuPDF
    doc = pymupdf.open(input_path)
    doc.set_page_labels(labels)

    # Save output to specified path or auto-generate <pdf_stem>_labeled.pdf
    output_path = Path(args.output) if args.output else input_path.with_name(f"{input_path.stem}_labeled.pdf")
    doc.save(output_path)
    doc.close()

    print(f"Success! Processed '{input_path.name}' using '{config_path.name}' -> '{output_path.name}'")


if __name__ == "__main__":
    main()