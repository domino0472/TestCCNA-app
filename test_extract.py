import fitz
import re

doc = fitz.open("CCNA.pdf")
page = doc.load_page(1)
blocks = page.get_text("dict")["blocks"]
blocks.sort(key=lambda b: b["bbox"][1])

for b in blocks:
    if b["type"] == 0:
        x0 = b["bbox"][0]
        if x0 > 300: # IGNORUJEMY SIDEBAR
            continue
        for l in b.get("lines", []):
            for s in l.get("spans", []):
                text = s["text"].strip()
                if not text: continue
                print(f"[{x0:.1f}] {text}")
