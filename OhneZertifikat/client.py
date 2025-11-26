import socket

HOST, PORT = "10.10.0.183", 9000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    print(f"Connected to TCP server at {HOST}:{PORT}")

    message = b"Hello, Dexter Morgan."
    sock.sendall(message)
    print(f"Sent: {message.decode()}")

    response = sock.recv(4096)
    print(f"Received: {response.decode()}")