import socket
import ssl

HOST, PORT = "127.0.0.1", 8443

# TLS-Client-Kontext erstellen
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.minimum_version = ssl.TLSVersion.TLSv1_2

# Server-Zertifikat prüfen
context.load_verify_locations(cafile="ca.crt")

# Client-Zertifikat und Schlüssel laden (für mTLS)
context.load_cert_chain(certfile="client.crt", keyfile="client.key")

# Verbindung aufbauen
with socket.create_connection((HOST, PORT)) as raw_sock:
    with context.wrap_socket(raw_sock, server_hostname="localhost") as conn:
        print("TLS connection established, protocol:", conn.version())
        conn.sendall(b"Hello, Dexter Morgan. (mTLS)")
        response = conn.recv(4096)
        print("Response:", response.decode(errors="replace"))
