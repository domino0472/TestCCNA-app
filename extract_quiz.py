import fitz
import json
import re
import os

doc = fitz.open("CCNA.pdf")

os.makedirs("assets", exist_ok=True)

questions = []
current_question = None

COLOR_RED = 16711680

# To correctly order spans which might be broken
def process_pdf():
    global current_question
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Check images on this page
        images_on_page = page.get_images(full=True)
        
        # Check if previous question needs an exhibit from this new page
        if current_question and current_question.get("pending_exhibit") and images_on_page:
            current_question["has_exhibit"] = True
            current_question["pending_exhibit"] = False
            xref = images_on_page[0][0]
            base_image = doc.extract_image(xref)
            ext = base_image["ext"]
            image_bytes = base_image["image"]
            img_path = f"assets/q{current_question['id']}.{ext}"
            with open(img_path, "wb") as f:
                f.write(image_bytes)
            current_question["image"] = img_path

        blocks = page.get_text("dict")["blocks"]
        
        for b in blocks:
            if "lines" not in b:
                continue
                
            for l in b["lines"]:
                # To reconstruct the line
                line_text = ""
                is_bold = False
                is_red = False
                is_explanation = False
                
                # We'll just read spans
                for s in l["spans"]:
                    text = s["text"].strip()
                    if not text:
                        continue
                        
                    # Ignore header/footer/breadcrumbs (like "CCNA 1 v7.0 Final Exam Answers", dates, comments, etc)
                    if "CCNA 1 v7.0 Final Exam" in text or "Dec 20, 2019" in text or "Last Updated:" in text or "Course #1" in text or "Comments" in text or "Press “Ctrl + F”" in text or "IT Exam Items Repository" in text or "The exam consists of" in text:
                        continue
                    if text in ["video", "web", "file transfer", "voice", "peer to peer"]: 
                        pass # allow options

                    color = s["color"]
                    flags = s["flags"]
                    
                    if "Explanation:" in text:
                        is_explanation = True
                    
                    if re.match(r'^\d+\.\s+', text):
                        if current_question:
                            questions.append(current_question)
                        
                        current_question = {
                            "id": len(questions) + 1,
                            "question": text + " ",
                            "options": [],
                            "explanation": "",
                            "image": None,
                            "has_exhibit": False,
                            "section": "question"
                        }
                    elif current_question:
                        # Identify section based on style and text
                        if "Explanation:" in text or current_question["section"] == "explanation":
                            current_question["section"] = "explanation"
                            current_question["explanation"] += text + " "
                        elif color == COLOR_RED and (flags & 16):
                            # Correct option
                            current_question["section"] = "options"
                            current_question["options"].append({"text": text, "is_correct": True})
                            current_question.setdefault("raw_match_spans", []).append({"text": text, "bbox": s["bbox"]})
                        elif not (flags & 16) and color != COLOR_RED:
                            # Normal option (usually grey or black, non-bold)
                            # Let's avoid noise like breadcrumbs.
                            # Usually breadcrumbs have special characters or links, but we filter them.
                            # If it's a short text or just normal text in options section.
                            current_question["section"] = "options"
                            # If previous was also an option, maybe append? Let's just append as new option
                            current_question["options"].append({"text": text, "is_correct": False})
                            current_question.setdefault("raw_match_spans", []).append({"text": text, "bbox": s["bbox"]})
                        elif (flags & 16) and color != COLOR_RED:
                            # Question text continuation
                            if current_question["section"] == "question":
                                current_question["question"] += text + " "
                            else:
                                # Could be bold text in an option or explanation
                                pass
                                
        # Check for exhibit image after processing the page
        if current_question and "exhibit" in current_question["question"].lower() and not current_question.get("has_exhibit"):
            if images_on_page:
                current_question["has_exhibit"] = True
                current_question["pending_exhibit"] = False
                xref = images_on_page[0][0]
                base_image = doc.extract_image(xref)
                ext = base_image["ext"]
                image_bytes = base_image["image"]
                img_path = f"assets/q{current_question['id']}.{ext}"
                with open(img_path, "wb") as f:
                    f.write(image_bytes)
                current_question["image"] = img_path
            else:
                current_question["pending_exhibit"] = True

    if current_question:
        questions.append(current_question)

    # Clean up questions
    for q in questions:
        q["question"] = q["question"].strip()
        q["explanation"] = q["explanation"].replace("Explanation:", "").strip()
        
        q_lower = q["question"].lower()
        if q_lower.startswith("match ") or " match the " in q_lower or " match " in q_lower:
            q["type"] = "match"
            raw = q.get("raw_match_spans", [])
            left_spans = [s for s in raw if s["bbox"][0] < 200]
            right_spans = [s for s in raw if s["bbox"][0] >= 200]
            
            def group_spans(spans):
                if not spans: return []
                spans.sort(key=lambda s: s["bbox"][1])
                groups = []
                current_group = [spans[0]]
                for s in spans[1:]:
                    if s["bbox"][1] - current_group[-1]["bbox"][1] < 25:
                        current_group.append(s)
                    else:
                        groups.append(current_group)
                        current_group = [s]
                groups.append(current_group)
                items = []
                for g in groups:
                    g.sort(key=lambda x: (x["bbox"][1], x["bbox"][0]))
                    text = " ".join([x["text"] for x in g]).strip()
                    y0 = min([x["bbox"][1] for x in g])
                    items.append({"text": text, "y0": y0})
                return items
            
            left_items = group_spans(left_spans)
            right_items = group_spans(right_spans)
            
            q["left_items"] = [i["text"] for i in left_items]
            q["right_items"] = [i["text"] for i in right_items]
            
            mapping = {}
            for li in left_items:
                if not right_items: break
                closest = min(right_items, key=lambda ri: abs(ri["y0"] - li["y0"]))
                if abs(closest["y0"] - li["y0"]) < 20:
                    mapping[li["text"]] = closest["text"]
            
            q["correct_mapping"] = mapping
            if "options" in q: del q["options"]
            if "raw_match_spans" in q: del q["raw_match_spans"]
            if "correct" in q: del q["correct"]
            continue

        if "choose two" in q_lower:
            q["type"] = "multiple"
            q["maxSelections"] = 2
        elif "choose three" in q_lower:
            q["type"] = "multiple"
            q["maxSelections"] = 3
        else:
            q["type"] = "single"
            
        correct_answers = []
        for opt in q.get("options", []):
            if isinstance(opt, dict) and opt.get("is_correct"):
                correct_answers.append(opt.get("text"))
        q["correct"] = correct_answers
        if "raw_match_spans" in q: del q["raw_match_spans"]

process_pdf()

with open("baza_pytan.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=4)

print(f"Extracted {len(questions)} questions.")
