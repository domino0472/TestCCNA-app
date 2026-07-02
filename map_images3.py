import fitz
doc = fitz.open("CCNA.pdf")
img_list = []
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]
    img_idx = 0
    for b in blocks:
        if b["type"] == 1:
            if b.get("width", 0) >= 100 and b.get("height", 0) >= 40:
                print(f"page_{page_num}_img_{img_idx}.png ({b.get('width')}x{b.get('height')})")
                img_list.append(f"page_{page_num}_img_{img_idx}")
            img_idx += 1
print(f"Total valid images: {len(img_list)}")
