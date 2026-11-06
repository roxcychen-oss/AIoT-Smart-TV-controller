import http.server
import socket
import json

TV_MAC = 'c0:f5:35:e0:8a:a9'
PORT = 3000

def send_wol():
    clean_mac = TV_MAC.replace(':', '').replace('-', '')
    data = bytes.fromhex('FF' * 6 + clean_mac * 16)
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.sendto(data, ('192.168.0.255', 9))
    print(f"[硬體喚醒] 已成功向電視 ({TV_MAC}) 發送 Magic Packet！")

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/wake-tv':
            send_wol()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
        else:
            super().do_GET()

if __name__ == '__main__':
    try:
        server = http.server.HTTPServer(('0.0.0.0', PORT), MyHandler)
        print(f"AIoT 本地中繼伺服器已啟動，監聽端口 {PORT}...")
        server.serve_forever()
    except Exception as e:
        print(f"❌ 伺服器啟動失敗，原因: {e}")