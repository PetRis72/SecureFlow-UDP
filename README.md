# SecureFlow-UDP (Aspera-Inspired Transport)

A high-speed, military-grade secure UDP protocol implemented in Python. This project demonstrates a custom transport layer that combines the speed of Aspera (FASP) with modern cryptographic security.

## Features
* **Dual-Channel Architecture:** Separate low-latency channel for text (control) and high-speed channel for data (video/images).
* **Full Metadata Encryption:** Not just the payload, but headers and sequence numbers are encrypted to prevent traffic analysis.
* **Congestion Control:** A delay-based algorithm that maximizes bandwidth usage while preventing network congestion.
* **Selective Repeat & Reset:** Efficient packet loss recovery and a "Security Valve" for automatic hard resets during persistent blockages.
* **MITM-Proof:** Verified against Man-in-the-Middle attacks using AES-256-GCM.

## Installation
Ensure you have Python 3.x installed, then run:
```bash
pip install PyQt6 cryptography

## How to Test
**1. Node 1 (Listener/Sender):** `python main_node.py 9999 9998`

**2. Node 2 (Listener/Sender):** `python main_node.py 9998 9999`

**3. Security Test (MITM):** Run `python mitm_sniffer.py` to observe that all intercepted traffic is unreadable noise.

## Technical Details
* **Encryption: AES-256-GCM** (Authenticated Encryption with Associated Data).

* **Transport:** UDP (User Datagram Protocol).

* **GUI:** PyQt6 for real-time monitoring and logging.