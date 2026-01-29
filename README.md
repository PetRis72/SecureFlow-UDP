# SecureFlow-UDP (Aspera-Inspired Transport)

A high-speed, military-grade secure UDP protocol implemented in Python. This project demonstrates a custom transport layer that combines the speed of Aspera (FASP) with modern cryptographic security.

## Features
* **Dual-Channel Architecture:** Separate low-latency channel for text (control) and high-speed channel for data (video/images).
* **Full Metadata Encryption:** Not just the payload, but headers and sequence numbers are encrypted to prevent traffic analysis.
* **Congestion Control:** A delay-based algorithm that maximizes bandwidth usage while preventing network congestion.
* **Selective Repeat & Reset:** Efficient packet loss recovery and a "Security Valve" for automatic hard resets during persistent blockages.
* **MITM-Proof:** Verified against Man-in-the-Middle attacks using AES-256-GCM.

## Project Structure
* **`main_node.py`**: The Graphical User Interface (GUI) built with PyQt6.
* **`engine.py`**: The core protocol logic (Encryption, Sockets, and Threading).
* **`mitm_sniffer.py`**: Security auditing tool to verify encryption.
* **`requirements.txt`**: Project dependencies.

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

## Usage Modes

### **1. Normal Mode (Direct Secure Communication)**
Use this for standard peer-to-peer communication. The nodes connect directly to each other.

* **Terminal 1 (Node A):**
```bash
python main_node.py 9999 9998
```

* **Terminal 2 (Node B):**
```bash
python main_node.py 9998 9999
```

### **2. Demo Mode (With MITM Sniffer/Proxy)**
Use this to verify that the encryption works. All traffic is routed through the sniffer, which attempts to "read" the data in the middle.

* **Terminal 1 (The Sniffer):**
```bash
python mitm_sniffer.py
```

* **Terminal 2 (Node A):**
```bash
python mitm_sniffer.py
```

* **Terminal 3 (Node B):**
```bash
python mitm_sniffer.py
```

Observe the Sniffer terminal to see the intercepted, encrypted Hex data.

## Technical Details
* **Full Metadata Encryption:** Unlike standard protocols, SecureFlow encrypts the entire packet, including headers and sequence numbers.

* **AES-256-GCM:** Authenticated encryption ensures that data cannot be modified in transit.

* **Aspera-Style Pacing:** Controlled UDP streaming to maximize bandwidth without causing network congestion.

* **Auto-Save:** Received files are automatically reassembled and saved to the /downloads folder.

## License
This project is licensed under the MIT License.

## Attribution
This project is the original work of [Peter Risberg/PetRis72]. 

If you choose to fork, copy, or use this base code in your own projects, you are **required** to:
1. Provide a clear link back to this original GitHub repository. 
```bash
https://github.com/PetRis72/SecureFlow-UDP
```

2. Mention the original author in your documentation or "About" section.
```bash
Original work of Peter Risberg/PetRis72
```


## MIT License

Copyright (c) 2024 Peter Risberg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.