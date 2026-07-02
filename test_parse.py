import fitz
import re

doc = fitz.open("CCNA.pdf")

valid_images = []
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    for img in page.get_image_info(xrefs=True):
        if img["width"] > 100 and img["height"] > 100:
            valid_images.append({
                "page": page_num,
                "y0": img["bbox"][1],
                "xref": img["xref"]
            })

print(f"Total valid images: {len(valid_images)}")

questions = []
current_question = None

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]
    for b in blocks:
        if "lines" not in b: continue
        for l in b["lines"]:
            for s in l["spans"]:
                text = s["text"].strip()
                if not text: continue
                if "CCNA 1 v7.0 Final Exam" in text or "Dec 20, 2019" in text or "Last Updated:" in text or "Course #1" in text or "Comments" in text or "Press “Ctrl + F”" in text or "IT Exam Items Repository" in text or "The exam consists of" in text:
                    continue
                if re.match(r'^\d+\.\s+', text):
                    if current_question: questions.append(current_question)
                    current_question = {"id": len(questions)+1, "text": text, "page": page_num, "y0": s["bbox"][1]}
                elif current_question:
                    current_question["text"] += " " + text

if current_question: questions.append(current_question)

exhibit_qs = [q for q in questions if "exhibit" in q["text"].lower()]
print(f"Questions with 'exhibit': {len(exhibit_qs)}")
