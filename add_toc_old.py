import pymupdf
import csv

def parse_csv_toc(csv_file_path, page_offset=0):
    toc = []
    with open(csv_file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # Skip empty lines
            if not row: 
                continue
            
            level = int(row[0].strip())
            title = row[1].strip()
            page = int(row[2].strip()) + page_offset - 1
            
            toc.append([level, title, page])
    return toc

# --- Usage ---
doc = pymupdf.open("input.pdf")

PAGE_OFFSET = 14
toc = parse_csv_toc("toc.csv", page_offset=PAGE_OFFSET)

doc.set_toc(toc)
doc.save("output_with_toc.pdf", garbage=4, deflate=True)
doc.close()