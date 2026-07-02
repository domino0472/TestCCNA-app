import fitz
doc = fitz.open("CCNA.pdf")
for page_num in [23, 24, 27, 28, 67, 68, 76, 77, 89, 90]:
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]
    img_idx = 0
    for b in blocks:
        if b["type"] == 1:
            print(f"Page {page_num} Image {img_idx}: {b.get('width')}x{b.get('height')}")
            img_idx += 1
