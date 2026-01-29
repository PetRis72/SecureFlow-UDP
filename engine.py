import socket
import struct
import time
import os
import threading
from PyQt6.QtCore import QThread, pyqtSignal
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class SecureEngine(QThread):
    new_message = pyqtSignal(str, str) # Channel, Content
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)

    def __init__(self, my_port, target_ip, target_port, key):
        super().__init__()
        self.my_port = my_port
        self.target = (target_ip, target_port)
        self.cipher = AESGCM(key)
        self.running = True
        self.next_seq = 0

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', self.my_port))
        
        # Start listener thread
        threading.Thread(target=self.listen_loop, daemon=True).start()
        self.log_signal.emit(f"Engine Online. Listening on port {self.my_port}")

    def listen_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                nonce = data[:12]
                encrypted = data[12:]
                
                # Decrypting payload and metadata
                decrypted = self.cipher.decrypt(nonce, encrypted, b"auth")
                channel, seq = struct.unpack("!BI", decrypted[:5])
                content = decrypted[5:]
                
                self.new_message.emit(str(channel), content.decode())
                self.log_signal.emit(f"Inbound: Packet {seq} on Channel {channel} decrypted.")
            except Exception as e:
                self.log_signal.emit(f"Decryption Error: {str(e)}")

    def send_secure(self, channel, payload_bytes):
        nonce = os.urandom(12)
        # Header is encrypted with the data for full metadata protection
        header = struct.pack("!BI", channel, self.next_seq)
        encrypted = self.cipher.encrypt(nonce, header + payload_bytes, b"auth")
        
        self.sock.sendto(nonce + encrypted, self.target)
        self.log_signal.emit(f"Outbound: Packet {self.next_seq} sent to {self.target}")
        self.next_seq += 1