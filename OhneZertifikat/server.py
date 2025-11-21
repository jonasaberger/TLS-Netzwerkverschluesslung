import socket

HOST, PORT = "127.0.0.1", 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"TCP-Server running at https://{HOST}:{PORT}")
    while True:
        conn, addr = sock.accept()
        try:
            with conn:
                print("TCP connection established with:", addr, "via", conn.version())
                data = conn.recv(4096)
                if data:
                    conn.sendall(b"echo: " + data)
        except Exception as e:
            print("Error:", e)
