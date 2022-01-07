import sys
import struct
import socket
import time

PORT = 12345
MAX_TTL = 256
TRIES = 3
TIMEOUT_SEC = 3
TIMEOUT_MS = 0

def trace(host):
    for ttl in range(1, MAX_TTL):
        dest_addr = socket.gethostbyname(host)
        
        timeout = struct.pack("ll", TIMEOUT_SEC, TIMEOUT_MS)
        receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        receiver_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, timeout)
        receiver_socket.bind(("", PORT))

        sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sender_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        
        
        curr_addr = None
        curr_name = None

        for _ in range(TRIES):
            sender_socket.sendto(bytes("", "utf-8"), (host, 1))
            try: 
                curr_addr = receiver_socket.recvfrom(65535)[1][0]
                try:
                    curr_name = socket.gethostbyaddr(curr_addr)[0]
                except socket.error:
                    curr_name = curr_addr
                break
            except socket.error:
                output = "no reply"
            
        sender_socket.close()
        receiver_socket.close()
        
        if curr_name:
            output = f"{curr_name} ({curr_addr})"
        elif curr_addr:
            output = curr_addr
        
        print(ttl, output)
        if curr_addr == dest_addr:
            break

if __name__ == "__main__":
    host = sys.argv[1]
    trace(host)