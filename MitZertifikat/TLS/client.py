import socket, ssl
HOST, PORT = "localhost", 8443

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.minimum_version = ssl.TLSVersion.TLSv1_2
context.load_verify_locations(cafile="ca.crt")

# For mTLS: provide client certificate and key
context.load_cert_chain(certfile="client.crt", keyfile="client.key")
with socket.create_connection((HOST, PORT)) as raw_sock:
    with context.wrap_socket(raw_sock, server_hostname="localhost") as conn:
        print("TLS connection established, protocol:", conn.version())
        conn.sendall(b"Hello, Dexter Morgan (TLS)")
        print("Response:", conn.recv(4096).decode("utf-8", errors="replace"))
