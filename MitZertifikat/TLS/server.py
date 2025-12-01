import socket, ssl
HOST, PORT = "127.0.0.1", 8443

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.minimum_version = ssl.TLSVersion.TLSv1_2
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# For mTLS (mutual authentication)
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile="ca.crt")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"TLS Server running at https://{HOST}:{PORT}")
    while True:
        raw_conn, addr = sock.accept()
        try:
            with context.wrap_socket(raw_conn, server_side=True) as conn:
                print("TLS connection established with:", addr, "via", conn.version())
                data = conn.recv(4096)
                if not data:
                    continue
                conn.sendall(b"echo: " + data)
        except ssl.SSLError as e:
            print("TLS Error:", e)