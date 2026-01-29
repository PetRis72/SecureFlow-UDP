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
        
        # Buffer for incoming file chunks {seq: data}
        self.file_buffer = {} 

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Increase OS buffer size for high-speed video data
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
        self.sock.bind(('0.0.0.0', self.my_port))
        
        threading.Thread(target=self.listen_loop, daemon=True).start()
        self.log_signal.emit(f"Engine Online. Listening on port {self.my_port}")

    def listen_loop(self):
        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                nonce = data[:12]
                encrypted = data[12:]
                
                # Decrypting both Metadata (Header) and Payload
                decrypted = self.cipher.decrypt(nonce, encrypted, b"auth")
                channel, seq = struct.unpack("!BI", decrypted[:5])
                content = decrypted[5:]
                
                if channel == 1: # Chat Channel
                    self.new_message.emit("1", content.decode())
                
                elif channel == 2: # High-Speed Data/Video Channel
                    # In a full app, you would write this to a file
                    self.file_buffer[seq] = content
                    self.log_signal.emit(f"Data Stream: Received chunk {seq}")
                    # Update progress bar (simulated)
                    self.progress_signal.emit(len(self.file_buffer) % 101)

            except Exception as e:
                self.log_signal.emit(f"Security Alert: Blocked malformed packet.")

    def send_secure(self, channel, payload_bytes):
        """Sends a single encrypted packet."""
        nonce = os.urandom(12)
        header = struct.pack("!BI", channel, self.next_seq)
        encrypted = self.cipher.encrypt(nonce, header + payload_bytes, b"auth")
        
        self.sock.sendto(nonce + encrypted, self.target)
        self.next_seq += 1

    def send_file(self, file_path):
        """Chunks a file and streams it over Channel 2."""
        if not os.path.exists(file_path):
            self.log_signal.emit("Error: File not found.")
            return

        file_size = os.path.getsize(file_path)
        chunk_size = 1024 # 1KB chunks for stability
        total_chunks = (file_size // chunk_size) + 1
        
        self.log_signal.emit(f"Starting Stream: {os.path.basename(file_path)}")
        
        with open(file_path, "rb") as f:
            for i in range(total_chunks):
                chunk = f.read(chunk_size)
                if not chunk: break
                
                self.send_secure(2, chunk)
                
                # Progress calculation
                progress = int((i / total_chunks) * 100)
                self.progress_signal.emit(progress)
                
                # Aspera-style pacing: prevents flooding the router
                time.sleep(0.0005) 

        self.log_signal.emit("Stream Complete. All packets pushed to network.")