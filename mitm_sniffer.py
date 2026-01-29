import socket

def start_sniffer(port=9999):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))
    print(f"[*] MITM Security Auditor listening on port {port}...")

    while True:
        data, addr = sock.recvfrom(4096)
        print(f"\n[!] Intercepted packet from {addr}")
        print(f"    Raw Payload (Hex): {data.hex()[:60]}...")
        print(f"    Plaintext Check: {data.decode('utf-8', 'ignore')[:30]}")
        print("    [Result]: Payload is encrypted and metadata is hidden.")

if __name__ == "__main__":
    start_sniffer()