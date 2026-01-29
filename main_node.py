import sys
import time
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTextEdit, QLineEdit, QPushButton, 
                             QProgressBar, QLabel)
from engine import SecureEngine # Importing your logic

class SecureNodeUI(QMainWindow):
    def __init__(self, my_port, target_ip, target_port):
        super().__init__()
        self.setWindowTitle(f"SecureFlow-UDP | Node {my_port}")
        self.setMinimumSize(850, 600)
        
        # Hardcoded 32-byte key for testing
        self.key = b"12345678901234567890123456789012"

        self.setup_ui()
        
        # Initialize and connect the engine
        self.engine = SecureEngine(my_port, target_ip, target_port, self.key)
        self.engine.log_signal.connect(self.add_log)
        self.engine.new_message.connect(self.on_message_received)
        self.engine.start()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)

        # Communication Panel
        left_panel = QVBoxLayout()
        self.chat_display = QTextEdit(); self.chat_display.setReadOnly(True)
        self.msg_input = QLineEdit(); self.send_btn = QPushButton("Send Secure Message")
        self.progress = QProgressBar()
        
        left_panel.addWidget(QLabel("Encrypted Chat History:"))
        left_panel.addWidget(self.chat_display)
        
        input_row = QHBoxLayout()
        input_row.addWidget(self.msg_input); input_row.addWidget(self.send_btn)
        left_panel.addLayout(input_row)
        
        left_panel.addWidget(QLabel("High-Speed Data Channel:"))
        left_panel.addWidget(self.progress)
        
        main_layout.addLayout(left_panel)

        # Technical Log Panel
        self.log_display = QTextEdit(); self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet("background: #000; color: #0f0; font-family: Consolas;")
        self.log_display.setFixedWidth(350)
        
        right_panel = QVBoxLayout()
        right_panel.addWidget(QLabel("Protocol & Security Logs:"))
        right_panel.addWidget(self.log_display)
        
        main_layout.addLayout(right_panel)

        # Connect UI signals
        self.send_btn.clicked.connect(self.send_message)
        self.msg_input.returnPressed.connect(self.send_message)

    def add_log(self, msg):
        self.log_display.append(f"[{time.strftime('%H:%M:%S')}] {msg}")

    def on_message_received(self, channel, content):
        self.chat_display.append(f"<b>Partner:</b> {content}")

    def send_message(self):
        text = self.msg_input.text()
        if text:
            self.engine.send_secure(1, text.encode())
            self.chat_display.append(f"<b>Me:</b> {text}")
            self.msg_input.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Defaulting to ports if no args provided
    p, tp = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (9999, 9998)
    window = SecureNodeUI(p, "127.0.0.1", tp)
    window.show()
    sys.exit(app.exec())