import fitz
import re

doc = fitz.open("CCNA.pdf")
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]
    
    img_idx = 0
    questions_on_page = []
    
    for b in blocks:
        if b["type"] == 0:
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    text = s["text"].strip()
                    m = re.match(r'^(\d+)\.\s+(.*)', text)
                    if m:
                        questions_on_page.append(m.group(1))
        elif b["type"] == 1:
            if b.get("width", 0) >= 250 and b.get("height", 0) >= 150:
                print(f"Image page_{page_num}_img_{img_idx}.png -> Questions on page: {questions_on_page}")
                img_idx += 1
