import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

import argparse

def arguments():
    parser = argparse.ArgumentParser(description="Network port discovery tool")

    # flag that just shows info
    parser.add_argument(
        "--info",
        action="store_true",
        help="Show program information"
    )

    args = parser.parse_args()

    if args.info:
        print("Welcome to network port discovery.")
        print("This tool scans IP ports in your local network.\n")


if __name__ == "__main__":
    arguments()
    print(f"Please provide which port to scan:")

ports = []
ports = input().split(',')
ports = list(map(int, ports))
listofips = []
hostIP = socket.gethostbyname(socket.gethostname()).split('.')
hostIP[-1] = 0
hostIP[-2] = 0

for ipa in range(0, 256):
    for ipb in range(0, 256):
        hostIP[-2] = ipa
        hostIP[-1] = ipb
        listofips.append(hostIP.copy())

resulto = [".".join(str(octet) for octet in ip) for ip in listofips]

def check_ip(ip):
    open_ports = {}
    
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.2)
        sock_result = sock.connect_ex((ip, port))
        sock.close()

        if sock_result == 0:
            try:
                with socket.create_connection((ip, port), timeout=1) as s:
                    banner = s.recv(1024).decode(errors="ignore").strip()
            except Exception:
                banner = "Unknown service"

            open_ports[port] = banner

    if open_ports:
        results = []
        for port, banner in open_ports.items():
            results.append(f"{port} ({banner})")

        return f"\033[32mOpen ports on {ip}: {', '.join(results)}\033[0m"
    
with ThreadPoolExecutor(max_workers=65025) as executor:
    futures = [executor.submit(check_ip, ip) for ip in resulto]
    for future in as_completed(futures):
        res = future.result()
        if res is not None: 
            print(res)
