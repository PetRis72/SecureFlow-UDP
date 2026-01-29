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

## How to Test (Local Simulation)

To see the protocol, the security valve, and the MITM protection in action, you need to open **three separate terminal windows**.

### Step 1: Start the Security Auditor (MITM)
In the first terminal, run the sniffer. This acts as the "hacker" watching your network traffic.
```bash
# Terminal 1
python mitm_sniffer.py
```

### Step 2: Start Node 1
In the second terminal, start the first user. It will listen on port 9999 and send data to 9998.
```bash
# Terminal 2
python main_node.py 9999 9998
```

### Step 3: Start Node 2
In the third terminal, start the second user. It will listen on port 9998 and send data to 9999.
```bash
# Terminal 3
python main_node.py 9998 9999
```

### What to Observe:
1. **Chat:** Type a message in Node 1. You will see it appear in Node 2 instantly.

2. **Security:** Look at **Terminal 1 (Sniffer)**. You will see encrypted hex-strings. You'll notice that you cannot read the messages, and you cannot tell if it's a chat message or a protocol reset command.

3. **Logs:** Check the green "Technical Log" in the GUI to see sequence numbers and encryption confirmations for every packet.


## Technical Details
* **Encryption: AES-256-GCM** (Authenticated Encryption with Associated Data).

* **Transport:** UDP (User Datagram Protocol).

* **GUI:** PyQt6 for real-time monitoring and logging.