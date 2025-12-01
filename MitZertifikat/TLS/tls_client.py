import socket, ssl

HOST, PORT = "127.0.0.1", 8443

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.minimum_version = ssl.TLSVersion.TLSv1_2
context.load_verify_locations(cafile="ca.crt")  # prüft nur den Server

with socket.create_connection((HOST, PORT)) as raw_sock:
    with context.wrap_socket(raw_sock, server_hostname="localhost") as conn:
        conn.sendall(b"Hello, Dexter Morgan. (TLS)")
        print("Response:", conn.recv(4096).decode())
