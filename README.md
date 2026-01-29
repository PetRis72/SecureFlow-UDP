# SecureFlow-UDP (Aspera-Inspired Transport)

A high-speed, military-grade secure UDP protocol implemented in Python. This project demonstrates a custom transport layer that combines the speed of Aspera (FASP) with modern cryptographic security.

## Features
* **Dual-Channel Architecture:** Separate low-latency channel for text (control) and high-speed channel for data (video/images).
* **Full Metadata Encryption:** Not just the payload, but headers and sequence numbers are encrypted to prevent traffic analysis.
* **Congestion Control:** A delay-based algorithm that maximizes bandwidth usage while preventing network congestion.
* **Selective Repeat & Reset:** Efficient packet loss recovery and a "Security Valve" for automatic hard resets during persistent blockages.
* **MITM-Proof:** Verified against Man-in-the-Middle attacks using AES-256-GCM.

## Installation / Setup
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/PetRis72/SecureFlow-UDP.git](https://github.com/PetRis72/SecureFlow-UDP.git)
   cd SecureFlow-UDP
   ```

2. **Set up a virtual environment:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Test
**1. Node 1 (Listener/Sender):** `python main_node.py 9999 9998`

**2. Node 2 (Listener/Sender):** `python main_node.py 9998 9999`

**3. Security Test (MITM):** Run `python mitm_sniffer.py` to observe that all intercepted traffic is unreadable noise.

## Technical Details
* **Encryption: AES-256-GCM** (Authenticated Encryption with Associated Data).

* **Transport:** UDP (User Datagram Protocol).

* **GUI:** PyQt6 for real-time monitoring and logging.