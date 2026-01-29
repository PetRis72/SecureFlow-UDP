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
        
        # File receiving states
        self.file_buffer = {} 
        self.incoming_filename = "unknown_file"

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Socket Fix: Allow immediate port reuse after crash/close
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Performance: Increase OS buffer for high-speed UDP data
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024 * 1024)
        
        try:
            self.sock.bind(('0.0.0.0', self.my_port))
            self.log_signal.emit(f"Engine Online. Port: {self.my_port}")
        except Exception as e:
            self.log_signal.emit(f"BIND ERROR: {str(e)}")
            return

        # Start listener thread
        threading.Thread(target=self.listen_loop, daemon=True).start()

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
                
                if channel == 1: # Chat Channel
                    self.new_message.emit("1", content.decode())
                
                elif channel == 2: # High-Speed Data/File Channel
                    self.handle_incoming_file(seq, content)

            except Exception:
                # Ignore failed decryptions (blocks sniffers/corrupt data)
                pass

    def handle_incoming_file(self, seq, content):
        """Processes incoming data chunks and saves the file when EOF is reached."""
        
        # Check for Metadata markers
        if content.startswith(b"START:"):
            self.incoming_filename = content.decode().split(":")[1]
            self.file_buffer = {} # Reset buffer for new file
            self.log_signal.emit(f"INCOMING FILE: {self.incoming_filename}")
        
        elif content == b"EOF":
            self.save_file_to_disk()
        
        else:
            # Store the chunk using its sequence number
            self.file_buffer[seq] = content
            # Update progress bar (simulated loop)
            self.progress_signal.emit(len(self.file_buffer) % 101)

    def save_file_to_disk(self):
        """Assembles the buffer into a physical file."""
        try:
            if not self.file_buffer:
                return

            # Ensure downloads folder exists
            if not os.path.exists("downloads"):
                os.makedirs("downloads")

            save_path = os.path.join("downloads", self.incoming_filename)
            
            # Sort keys to ensure packets are written in the correct order
            sorted_seqs = sorted(self.file_buffer.keys())
            
            with open(save_path, "wb") as f:
                for s in sorted_seqs:
                    f.write(self.file_buffer[s])
            
            self.log_signal.emit(f"SUCCESS: Saved to /downloads/{self.incoming_filename}")
            self.new_message.emit("1", f"System: File '{self.incoming_filename}' received.")
            self.file_buffer = {} # Clear memory
            self.progress_signal.emit(100)
            
        except Exception as e:
            self.log_signal.emit(f"SAVE ERROR: {str(e)}")

    def send_secure(self, channel, payload_bytes):
        """Core encryption and transmission method."""
        nonce = os.urandom(12)
        header = struct.pack("!BI", channel, self.next_seq)
        encrypted = self.cipher.encrypt(nonce, header + payload_bytes, b"auth")
        
        self.sock.sendto(nonce + encrypted, self.target)
        self.next_seq += 1

    def send_file(self, file_path):
        """Splits file into chunks and sends with Metadata markers."""
        if not os.path.exists(file_path):
            self.log_signal.emit("FILE ERROR: Path does not exist.")
            return

        filename = os.path.basename(file_path)
        
        # 1. Send START marker
        self.send_secure(2, f"START:{filename}".encode())
        time.sleep(0.05) # Allow receiver to prepare
        
        # 2. Stream chunks
        with open(file_path, "rb") as f:
            while chunk := f.read(1024):
                self.send_secure(2, chunk)
                # High-speed pacing (Aspera-style)
                time.sleep(0.0005) 
        
        # 3. Send EOF marker
        time.sleep(0.05)
        self.send_secure(2, b"EOF")
        self.log_signal.emit(f"TRANSFER COMPLETE: {filename}")