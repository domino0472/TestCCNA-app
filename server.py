import http.server
import socketserver
import json
import os

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/remove_image':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data)
                question_id = data.get('id')
                
                if question_id:
                    with open('baza_pytan.json', 'r', encoding='utf-8') as f:
                        questions = json.load(f)
                    
                    for q in questions:
                        if q.get('id') == question_id:
                            q['image'] = None
                            q['has_exhibit'] = False
                            break
                            
                    with open('baza_pytan.json', 'w', encoding='utf-8') as f:
                        json.dump(questions, f, ensure_ascii=False, indent=4)
                        
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "success"}')
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_error(404, "Not Found")

print(f"Uruchamianie lokalnego serwera API + HTTP na porcie {PORT}...")
print("Aby zamknąć, naciśnij Ctrl+C")

with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nZamykanie serwera.")
