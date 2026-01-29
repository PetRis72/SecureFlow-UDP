import sys, socket, struct, time, os, threading
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QProgressBar, QLabel)
from PyQt6.QtCore import QThread, pyqtSignal
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# --- Network Engine ---
class NetworkWorker(QThread):
    new_message = pyqtSignal(str, str)
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, my_port, target_ip, target_port, key):
        super().__init__()
        self.my_port, self.target = my_port, (target_ip, target_port)
        self.cipher = AESGCM(key)
        self.running = True
        self.next_seq = 0

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.my_port))
        threading.Thread(target=self.listen_loop, daemon=True).start()
        self.log_signal.emit(f"System Online. Listening on port {self.my_port}")

    def listen_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                nonce, encrypted = data[:12], data[12:]
                decrypted = self.cipher.decrypt(nonce, encrypted, b"auth")
                chan, seq = struct.unpack("!BI", decrypted[:5])
                content = decrypted[5:]
                self.new_message.emit(str(chan), content.decode())
                self.log_signal.emit(f"Packet {seq} decrypted successfully from {addr[0]}")
            except: pass

    def send_secure(self, channel, payload):
        nonce = os.urandom(12)
        header = struct.pack("!BI", channel, self.next_seq)
        encrypted = self.cipher.encrypt(nonce, header + payload, b"auth")
        self.sock.sendto(nonce + encrypted, self.target)
        self.log_signal.emit(f"Sent encrypted packet {self.next_seq} on channel {channel}")
        self.next_seq += 1

# --- Main Interface ---
class SecureNodeUI(QMainWindow):
    def __init__(self, my_port, target_ip, target_port):
        super().__init__()
        self.setWindowTitle(f"SecureFlow Node | Port: {my_port}")
        self.setMinimumSize(850, 600)
        self.key = b"12345678901234567890123456789012" # 32-byte key

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # Left: Communication
        left = QVBoxLayout()
        self.chat = QTextEdit(); self.chat.setReadOnly(True)
        self.input = QLineEdit(); self.send_btn = QPushButton("Send Securely")
        self.prog = QProgressBar(); self.file_btn = QPushButton("High-Speed File Transfer")
        
        left.addWidget(QLabel(f"Target: {target_ip}:{target_port}"))
        left.addWidget(self.chat); left.addLayout(self._input_row()); left.addWidget(self.prog); left.addWidget(self.file_btn)

        # Right: Technical Logs
        self.logs = QTextEdit(); self.logs.setReadOnly(True)
        self.logs.setStyleSheet("background: #121212; color: #00FF41; font-family: 'Consolas'; font-size: 11px;")
        self.logs.setFixedWidth(320)
        
        main_layout.addLayout(left); main_layout.addWidget(self.logs)

        self.net = NetworkWorker(my_port, target_ip, target_port, self.key)
        self.net.log_signal.connect(self.add_log); self.net.new_message.connect(self.on_msg); self.net.start()
        self.send_btn.clicked.connect(self.send_txt)

    def _input_row(self):
        h = QHBoxLayout(); h.addWidget(self.input); h.addWidget(self.send_btn); return h

    def add_log(self, m): self.logs.append(f"[{time.strftime('%H:%M:%S')}] {m}")
    def on_msg(self, c, m): self.chat.append(f"<b>Received:</b> {m}")
    def send_txt(self):
        t = self.input.text()
        if t: self.net.send_secure(1, t.encode()); self.chat.append(f"<b>Me:</b> {t}"); self.input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    p, tp = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (9999, 9998)
    gui = SecureNodeUI(p, "127.0.0.1", tp)
    gui.show()
    sys.exit(app.exec())