import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QProgressBar, QLabel, QFileDialog, QStatusBar)
from PyQt6.QtCore import Qt
from engine import SecureEngine # Ensure engine.py is in the same folder

class SecureFlowUI(QMainWindow):
    def __init__(self, my_port, target_ip, target_port):
        super().__init__()
        # 1. Configuration
        self.setWindowTitle(f"SecureFlow-UDP | Node {my_port}")
        self.setMinimumSize(900, 650)
        self.key = b"12345678901234567890123456789012" # Must match partner node

        # 2. Setup User Interface
        self.setup_ui()
        
        # 3. Initialize and Start Engine
        self.engine = SecureEngine(my_port, target_ip, target_port, self.key)
        
        # Connect Engine signals to UI slots
        self.engine.log_signal.connect(self.add_log)
        self.engine.new_message.connect(self.on_message_received)
        self.engine.progress_signal.connect(self.progress.setValue)
        
        self.engine.start()
        self.add_log(f"System initialized. Target set to {target_ip}:{target_port}")

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # --- LEFT PANEL: Chat and File Transfer ---
        left_panel = QVBoxLayout()
        
        # Chat Display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText("Encrypted Chat History...")
        self.chat_display.setStyleSheet("font-size: 13px; padding: 5px;")
        
        # Message Input
        input_row = QHBoxLayout()
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Enter secure message...")
        self.send_btn = QPushButton("Send Text")
        self.send_btn.setFixedWidth(100)
        input_row.addWidget(self.msg_input)
        input_row.addWidget(self.send_btn)
        
        # File Transfer Controls
        file_label = QLabel("High-Speed Data Channel (Video/Images)")
        file_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        self.progress = QProgressBar()
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.file_btn = QPushButton("Select & Send File via UDP")
        self.file_btn.setStyleSheet("background-color: #2c3e50; color: white; font-weight: bold; height: 30px;")

        left_panel.addWidget(QLabel("Encrypted Messaging:"))
        left_panel.addWidget(self.chat_display)
        left_panel.addLayout(input_row)
        left_panel.addWidget(file_label)
        left_panel.addWidget(self.progress)
        left_panel.addWidget(self.file_btn)
        
        # --- RIGHT PANEL: Technical Logs ---
        right_panel = QVBoxLayout()
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("""
            background-color: #121212; 
            color: #00FF41; 
            font-family: 'Consolas', 'Courier New'; 
            font-size: 11px;
        """)
        self.log_display.setFixedWidth(350)
        
        right_panel.addWidget(QLabel("Protocol & Security Logs (Metadata View):"))
        right_panel.addWidget(self.log_display)

        # Combine Panels
        main_layout.addLayout(left_panel, stretch=2)
        main_layout.addLayout(right_panel, stretch=1)

        # Status Bar
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage(f"Local Port: {self.engine_port_display(self)} | Security: AES-256-GCM Active")

        # UI Connections
        self.send_btn.clicked.connect(self.send_text_message)
        self.msg_input.returnPressed.connect(self.send_text_message)
        self.file_btn.clicked.connect(self.open_file_dialog)

    def engine_port_display(self, obj):
        # Helper for status bar since engine isn't fully started in __init__ UI call
        return sys.argv[1] if len(sys.argv) > 1 else "9999"

    def add_log(self, msg):
        timestamp = time.strftime("%H:%M:%S")
        self.log_display.append(f"[{timestamp}] {msg}")

    def on_message_received(self, channel, content):
        if channel == "1":
            self.chat_display.append(f"<b style='color: #2980b9;'>Partner:</b> {content}")
        elif channel == "2":
            # Engine handles the data, we just notify the chat
            self.chat_display.append(f"<i>Incoming high-speed data stream... Check logs.</i>")

    def send_text_message(self):
        text = self.msg_input.text().strip()
        if text:
            self.engine.send_secure(1, text.encode())
            self.chat_display.append(f"<b>Me:</b> {text}")
            self.msg_input.clear()

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Send", "", "All Files (*)")
        if file_path:
            # Start file sending in a background process via the engine
            self.add_log(f"Preparing to stream: {file_path}")
            # We wrap this in a thread so the UI doesn't lag during the disk read
            threading.Thread(target=self.engine.send_file, args=(file_path,), daemon=True).start()

if __name__ == "__main__":
    import threading # Required for the file dialog thread
    app = QApplication(sys.argv)
    
    # Usage: python main_node.py [local_port] [target_port]
    local_p = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
    target_p = int(sys.argv[2]) if len(sys.argv) > 2 else 9998
    
    window = SecureFlowUI(local_p, "127.0.0.1", target_p)
    window.show()
    sys.exit(app.exec())