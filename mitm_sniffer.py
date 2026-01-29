import socket
import threading

def forward_traffic(in_port, out_port, label):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', in_port))
    
    print(f"[*] Sniffer [{label}] active: Listening on {in_port} -> Forwarding to {out_port}")

    while True:
        data, addr = sock.recvfrom(4096)
        
        print(f"\n[!] INTERCEPTED [{label}] from {addr}")
        print(f"    DATA (HEX): {data.hex()[:60]}...")
        
        # Forsøk å dekode (vil feile/vise støy pga kryptering)
        readable = data.decode('utf-8', 'ignore').replace('\n', ' ')
        print(f"    READABLE: {readable[:40]}...")

        # Send videre til den faktiske mottakeren
        sock.sendto(data, ('127.0.0.1', out_port))

if __name__ == "__main__":
    print("=== FULL DUPLEX MITM SNIFFER ===")
    
    # Tråd 1: Fanger trafikk fra Node A og sender til Node B
    # Vi bruker port 8881 som "mellomstasjon" for Node B
    t1 = threading.Thread(target=forward_traffic, args=(8881, 9998, "A to B"), daemon=True)
    
    # Tråd 2: Fanger trafikk fra Node B og sender til Node A
    # Vi bruker port 8882 som "mellomstasjon" for Node A
    t2 = threading.Thread(target=forward_traffic, args=(8882, 9999, "B to A"), daemon=True)

    t1.start()
    t2.start()

    print("[*] Sniffer is running. Press Ctrl+C to stop.")
    t1.join()
    t2.join()