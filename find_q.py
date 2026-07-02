import fitz
import re

doc = fitz.open("CCNA.pdf")
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    text = page.get_text()
    for q in [13, 15, 35, 43, 113, 121, 127, 150]:
        if re.search(r'^' + str(q) + r'\.\s+', text, re.MULTILINE):
            print(f"Question {q} is on page {page_num}")
