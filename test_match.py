import fitz

doc = fitz.open("CCNA.pdf")

found = 0
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]
    for i, b in enumerate(blocks):
        if "lines" not in b: continue
        text = "".join(s["text"] for l in b["lines"] for s in l["spans"])
        if "12. " in text or "14. " in text or "30. " in text:
            print(f"=== Found on page {page_num} ===")
            for j in range(max(0, i), min(len(blocks), i+20)):
                blk = blocks[j]
                if "lines" not in blk: continue
                bbox = blk["bbox"]
                btext = "".join(s["text"] for l in blk["lines"] for s in l["spans"]).strip()
                if btext:
                    print(f"Bbox {bbox}: {btext}")
            found += 1
            break
    if found >= 3:
        break
