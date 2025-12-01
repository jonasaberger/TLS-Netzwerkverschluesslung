import socket
import ssl

HOST, PORT = "127.0.0.1", 8443

# TLS-Server-Kontext erstellen
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.minimum_version = ssl.TLSVersion.TLSv1_2

# Server-Zertifikat und Schlüssel laden
context.load_cert_chain(certfile="server.crt", keyfile="server.key")

# Client-Zertifikat zwingend erforderlich
context.verify_mode = ssl.CERT_REQUIRED
context.load_verify_locations(cafile="ca.crt")  # CA für Client-Zertifikat

# Socket erstellen und binden
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print(f"mTLS Server running at https://{HOST}:{PORT}")

    while True:
        raw_conn, addr = sock.accept()
        try:
            with context.wrap_socket(raw_conn, server_side=True) as conn:
                print("TLS connection established with:", addr, "via", conn.version())
                data = conn.recv(4096)
                if data:
                    print("Received:", data.decode(errors="replace"))
                    conn.sendall(b"echo: " + data)
        except ssl.SSLError as e:
            print("TLS Error:", e)
