import socket, ssl

HOST, PORT = "localhost", 8443

context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
context.minimum_version = ssl.TLSVersion.TLSv1_2
context.load_verify_locations(cafile="ca.crt")

# For mTLS: provide client certificate & key
context.load_cert_chain("client.crt", "client.key")

with socket.create_connection((HOST, PORT)) as raw_sock:
    with context.wrap_socket(raw_sock, server_hostname="localhost") as conn:
        print("TLS connection established, protocol:", conn.version())
        conn.sendall(b"Hello, tls.")
        print("Response:", conn.recv(1024).decode("utf-8", errors="replace"))