import fitz
import json
import re
import os

import sys

doc = fitz.open("CCNA.pdf")
os.makedirs("assets", exist_ok=True)

IMAGE_DICTIONARY = {
    13: "q13.png",
    15: "q15.png",
    17: "q17.png",
    18: "q18.png",
    28:"q28.png",
    33: "q33.png",
    35: "q35.png",
    43: "q43.png",
    47: "q47.png",
    92: "q92.png",
    98: "q98.png",
    109: "q109.png",
    113: "q113.png",
    118: "q118.png",
    119: "q119.png",
    121: "q121.png",
    127: "q127.png",
    134: "q134.png",
    150: "q150.png"
    
}

HARDCODED_MATCHES = {
    152: [
        {"left": "location of a desktop PC in a classroom", "right": "physical topology diagram"},
        {"left": "path of cables that connect rooms to wiring closets", "right": "physical topology diagram"},
        {"left": "IP address of a server", "right": "logical topology diagram"}
    ],
    12: [
        {"left": "This network portion of the address is assigned by the provider.", "right": "global routing prefix"},
        {"left": "This part of the address is used by an organization to identify subnets.", "right": "subnet ID"},
        {"left": "This part of the address is the equivalent to the host portion of an IPv4 address.", "right": "interface ID"}
    ],
    14: [
        {"left": "low latency", "right": "cut-through"},
        {"left": "may forward runt frames", "right": "cut-through"},
        {"left": "begins forwarding when the destination address is received", "right": "cut-through"},
        {"left": "always stores the entire frame", "right": "store-and-forward"},
        {"left": "checks the CRC before forwarding", "right": "store-and-forward"},
        {"left": "checks the frame length before forwarding", "right": "store-and-forward"}
    ],
    17: [
        {"left": "Network A", "right": "192.168.0.128/25"},
        {"left": "Network B", "right": "192.168.0.0/26"},
        {"left": "Network C", "right": "192.168.0.96/27"},
        {"left": "Network D", "right": "192.168.0.80/30"}
    ],
    28: [
        {"left": "Network A", "right": "192.168.0.0/25"},
        {"left": "Network B", "right": "192.168.0.128/26"},
        {"left": "Network C", "right": "192.168.0.192/27"},
        {"left": "Network D", "right": "192.168.0.224/30"}
    ],
    30: [
        {"left": "FTP", "right": "TCP"},
        {"left": "HTTP", "right": "TCP"},
        {"left": "SMTP", "right": "TCP"},
        {"left": "DHCP", "right": "UDP"},
        {"left": "TFTP", "right": "UDP"}
    ],
    58: [
        {"left": "electrical threats", "right": "voltage spikes, insufficient supply voltage (brownouts), unconditioned power (noise), and total power loss"},
        {"left": "hardware threats", "right": "physical damage to servers, routers, switches, cabling plant, and workstations"},
        {"left": "environmental threats", "right": "temperature extremes (too hot or too cold) or humidity extremes (too wet or too dry)"},
        {"left": "maintenance threats", "right": "poor handling of key electrical components (electrostatic discharge), lack of critical spare parts, poor cabling, and poor labeling"}
    ],
    96: [
        {"left": "no dedicated server is required", "right": "peer-to-peer network"},
        {"left": "client and server roles are set on a per request basis", "right": "peer-to-peer network"},
        {"left": "requires a specific user interface", "right": "peer-to-peer application"},
        {"left": "a background service is required", "right": "peer-to-peer application"}
    ],
    99: [
        {"left": "This field checks if the frame has been damaged during the transfer.", "right": "error detection"},
        {"left": "This field helps to direct the frame toward its destination.", "right": "addressing"},
        {"left": "This field identifies the beginning of a frame.", "right": "frame start"},
        {"left": "This field is used by the LLC to identify the Layer 3 protocol.", "right": "type"}
    ],
    101: [
        {"left": "prevents access by port number", "right": "application filtering"},
        {"left": "prevents access based on IP or MAC address", "right": "packet filtering"},
        {"left": "prevents unsolicited incoming sessions", "right": "stateful packet inspection"},
        {"left": "prevents access to websites", "right": "URL filtering"}
    ],
    110: [
        {"left": "contained in the Layer 3 header", "right": "IP address"},
        {"left": "separated into a network portion and a unique identifier", "right": "IP address"},
        {"left": "32 or 128 bits", "right": "IP address"},
        {"left": "contained in the Layer 2 header", "right": "MAC address"},
        {"left": "separated into OUI and a unique identifier", "right": "MAC address"},
        {"left": "48 bits", "right": "MAC address"}
    ],
    120: [
        {"left": "no dedicated server is required", "right": "peer-to-peer network"},
        {"left": "client and server roles are set on a per request basis", "right": "peer-to-peer network"},
        {"left": "requires a specific user interface", "right": "peer-to-peer application"},
        {"left": "a background service is required", "right": "peer-to-peer application"}
    ],
    126: [
        {"left": "Destination MAC Address", "right": "Layer 2"},
        {"left": "FCS (Frame Check Sequence)", "right": "Layer 2"},
        {"left": "802.2 header", "right": "Layer 2"},
        {"left": "Source IP Address", "right": "Layer 3"},
        {"left": "TTL", "right": "Layer 3"},
        {"left": "Destination Port Number", "right": "Layer 4"},
        {"left": "Acknowledgment Number", "right": "Layer 4"}
    ],
    145: [
        {"left": "the process of placing one message format inside another message format", "right": "message encapsulation"},
        {"left": "the process of breaking up a long message into individual pieces before being sent over the network", "right": "message sizing"},
        {"left": "the process of converting information from one format into another acceptable for transmission", "right": "message encoding"}
    ],
    149: [
        {"left": "number of bytes a destination device can accept and process at one time", "right": "window size"},
        {"left": "used to identify missing segments of data", "right": "sequence numbers"},
        {"left": "method of managing segments of data loss", "right": "retransmission"},
        {"left": "received by a sender before transmitting more segments in a session", "right": "acknowledgment"}
    ],
    152: [
        {"left": "location of a desktop PC in a classroom", "right": "physical topology diagram"},
        {"left": "path of cables that connect rooms to wiring closets", "right": "physical topology diagram"},
        {"left": "IP address of a server", "right": "logical topology diagram"}
    ],
    157: [
        {"left": "an experimental address", "right": "240.2.6.255"},
        {"left": "a link-local address", "right": "169.254.1.5"},
        {"left": "a public address", "right": "198.133.219.2"},
        {"left": "a loopback address", "right": "127.0.0.1"}
    ]
}

COLOR_RED = 16711680
questions = []

# KROK 2: Parsowanie tekstu
print("Parsowanie pytań...")
active_question = None
capture_options = False

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    blocks = page.get_text("dict")["blocks"]
    
    # Sort blocks natively (y0)
    blocks.sort(key=lambda b: b["bbox"][1])
    
    for b in blocks:
        if b["type"] == 0: # Text block
            # CAŁKOWITE ODRZUCENIE SIDEBARU (Współrzędna X > 300)
            if b["bbox"][0] > 300:
                continue

            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    text = s["text"].strip()
                    if not text: continue
                    
                    color = s["color"]
                    flags = s["flags"]
                    
                    match = re.match(r'^(\d+)\.\s+', text)
                    if match:
                        q_id = int(match.group(1))
                        
                        # Fix for duplicate/mismatched questions if they happen
                        if active_question:
                            expected_id = active_question["id"] + 1
                        else:
                            expected_id = 1
                            
                        if q_id != expected_id:
                            print(f"[ERROR] Missing question ID in sequence! Expected {expected_id}, but found {q_id}. Sticking to PDF ID.")
                        
                        if active_question:
                            questions.append(active_question)
                        
                        if q_id in IMAGE_DICTIONARY:
                            image_path = f"assets/{IMAGE_DICTIONARY[q_id]}"
                        else:
                            image_path = None
                            
                        active_question = {
                            "id": q_id,
                            "question": text + " ",
                            "options": [],
                            "explanation": "",
                            "image": image_path,
                            "section": "question"
                        }
                        capture_options = True
                    elif active_question:
                        if "Explanation:" in text:
                            active_question["section"] = "explanation"
                            capture_options = False
                        
                        if active_question["section"] == "explanation":
                            active_question["explanation"] += text + " "
                            continue
                        
                        if capture_options:
                            # Zamiast szukać znaku '•' (którego nie ma w warstwie tekstowej PDF),
                            # polegamy na odcięciu sidebaru po X > 300 i sprawdzaniu kolorów/flag
                            if color == COLOR_RED and (flags & 16):
                                active_question["options"].append({"text": text, "is_correct": True})
                            elif not (flags & 16) and color != COLOR_RED:
                                active_question["options"].append({"text": text, "is_correct": False})
                            elif (flags & 16) and color != COLOR_RED:
                                if active_question["section"] == "question":
                                    active_question["question"] += text + " "

if active_question:
    questions.append(active_question)

# KROK 3: Mapowanie obrazków i weryfikacja
print("Weryfikacja obrazków i przypisywanie...")
for q in questions:
    if q["id"] in IMAGE_DICTIONARY:
        q["image"] = IMAGE_DICTIONARY[q["id"]]
        print(f"DEBUG: Przypisano obrazek {q['image']} do pytania {q['id']}")
    else:
        q["image"] = None

    if "section" in q: del q["section"]
    
    # HARDCODED MATCHES
    if q["id"] in HARDCODED_MATCHES:
        q["type"] = "matching"
        q["matches"] = HARDCODED_MATCHES[q["id"]]
        if "options" in q: del q["options"]
        if "correct" in q: del q["correct"]
        continue
    
    q_lower = q["question"].lower()
    
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

with open("baza_pytan.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=4)

print(f"Wyodrębniono {len(questions)} pytań i zaktualizowano JSON.")
