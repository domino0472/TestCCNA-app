import fitz
import re

doc = fitz.open("CCNA.pdf")
counts = {"q_text": 0, "q_not_bold": 0}

for page_num in range(1, 5):
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]
    
    current_q = False
    for b in blocks:
        if "lines" not in b: continue
        for l in b["lines"]:
            for s in l["spans"]:
                text = s["text"].strip()
                if not text: continue
                
                if re.match(r'^\d+\.\s+', text):
                    current_q = True
                    if s["flags"] & 16:
                        counts["q_text"] += 1
                    else:
                        counts["q_not_bold"] += 1
                        print(f"NOT BOLD Q: {text}")

print(f"Stats: {counts}")
