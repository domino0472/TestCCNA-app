import fitz
import re

doc = fitz.open("CCNA.pdf")
valid_images = 0
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    imgs = page.get_images(full=True)
    valid_imgs = [img for img in imgs if img[2] > 100 and img[3] > 100]
    valid_images += len(valid_imgs)
print(f"Valid images: {valid_images}")
