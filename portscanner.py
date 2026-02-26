import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

print("Please provide which port to scan: ")

ports = []
ports = input().split(',')
ports = list(map(int, ports))


listofips = []

hostIP = socket.gethostbyname(socket.gethostname()).split('.')
hostIP[-1] = 0


for ipa in range(0, 256):
    hostIP[-1] = ipa
    listofips.append(hostIP.copy())

resulto = [".".join(str(octet) for octet in ip) for ip in listofips]

def check_ip(ip):
    open_ports = []

    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        sock_result = sock.connect_ex((ip, port))
        sock.close()

        if sock_result == 0:
            open_ports.append(port)

    if open_ports:
        return f"\033[32mOpen ports on {ip}: {', '.join(map(str, open_ports))}\033[0m"
    
with ThreadPoolExecutor(max_workers=255) as executor:
    futures = [executor.submit(check_ip, ip) for ip in resulto]
    for future in as_completed(futures):
        res = future.result()
        if res is not None:  # only print non-None results
            print(res)
