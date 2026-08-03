import pymupdf
from pathlib import Path

file_path = Path("~/Desktop/Schoppa, R. Keith - Blood Road_ The Mystery of Shen Dingyi in Revolutionary China (19\
95, University of California Press).pdf").expanduser()

# Start Code
doc = pymupdf.open(file_path)
toc = doc.get_toc()

toc.append([1, "New Concluding Chapter", 45])
toc.append([2, "New Sub-section under Conclusion", 47])
toc.append([1, "Chapter X", 55])

if toc:
    toc[0][1] = "Updated Introduction"
    toc[0][0] = 1


doc.set_toc(toc)

doc.save("output.pdf", garbage=4, deflate=True)
doc.close()

# if len(toc) > 1:
#     del toc[1]