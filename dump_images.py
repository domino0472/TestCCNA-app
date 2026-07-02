import fitz
import os
import re

doc = fitz.open("CCNA.pdf")
os.makedirs("assets_tmp", exist_ok=True)

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]
    
    img_idx = 0
    text_preview = ""
    
    for b in blocks:
        if b["type"] == 0:
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    text = s["text"].strip()
                    if re.match(r'^\d+\.\s+', text):
                        text_preview += text + " "
        elif b["type"] == 1:
            if b.get("width", 0) >= 250 and b.get("height", 0) >= 150:
                print(f"Page {page_num}: Found image {img_idx}. Questions on page: {text_preview[:100]}")
                img_idx += 1
