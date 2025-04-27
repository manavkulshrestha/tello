# server.py
import socket
import json
 
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 5000       # Arbitrary port above 1024
 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f'Server listening on port {PORT}...')
    conn, addr = s.accept()
    with conn:
        print(f'Connected by {addr}')
        data = conn.recv(1024)
        if data:
            received_dict = json.loads(data.decode())
            print('Received dict:', received_dict)