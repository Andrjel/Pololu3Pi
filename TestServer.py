# Test server for exchanging data
import socket

# Create TCP socket
HOST = "127.0.0.1"
PORT = 8000
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        print(f"conn is {conn}, addr is {addr}")
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data.decode())
                conn.send(b"[0112c000300230005001840203]")
            conn.close()
