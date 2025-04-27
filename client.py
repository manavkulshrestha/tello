# client.py
import socket
import json

HOST = "10.164.8.210"  # ideas10
HOST = "10.164.8.203"  # ideas3
PORT = 5000

my_dict = {"name": "Alice", "age": 30}

data = json.dumps(my_dict).encode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(data)
    print("Dict sent!")