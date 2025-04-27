import pickle
from djitellopy.tello import Tello
import socket
import threading


class Drone:
    def __init__(self, ip, port=5000, verbose=True):
        '''
        Args:
            ip - should be either 'localhost'/'127.0.0.1' or an IP address 'X.X.X.X'. Denotes which machine the drone is connected to.
                If drone is connected to this machine (localhost), then commands can be executed on connected drone directly
                (or recieved from another machine and then executed)
                If drone is connected to different machine (at X.X.X.X), then command must first be sent to X.X.X.X, then executed on connected drone.
                (There must be a localhost drone instance listening on X.X.X.X)
        '''
        self.drone = Tello()
        self.drone.connect()
        self.local = ip in ['localhost', '127.0.0.1']


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.local:
            # Server mode (listen for commands to control the drone)
            self._setup_server(port)
        else:
            # Client mode (connect to remote drone server)
            self._setup_client(ip, port)

        self.verbose = verbose
        self._BUFFER_SIZE = 1024

    def _setup_server(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', port))
        self.sock.listen()

        if self.verbose:
            print(f"Server listening on all IPs at port {port}...")

        conn, addr = self.sock.accept()
        if self.verbose:
            print(f"Connection established with {addr}")

        self._handle_client(conn) # blocking

    def _handle_client(self, conn):
        while True:
            data = self._recv(conn)
            if data:
                getattr(self.drone, data['name'])(*data['args'], **data['kwargs'])
            else:
                if self.verbose:
                    print('Something went wrong. No data received. Closing connection.')
                break
        conn.close()

    def _setup_client(self, ip, port):
        # Set up client socket to connect to the remote server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def _recv(self):
        raw_msglen = self.sock.recv(4)
        if not raw_msglen:
            return None
        msglen = int.from_bytes(raw_msglen, byteorder='big')

        data = b''
        while len(data) < msglen:
            packet = self.sock.recv(min(self._BUFFER_SIZE, msglen - len(data)))
            if not packet:
                return None
            data += packet
        return pickle.loads(data)

    def _send(self, obj):
        data = pickle.dumps(obj)
        self.sock.sendall(len(data).to_bytes(4, byteorder='big'))
        self.sock.sendall(data)

    def __getattr__(self, name):
        def dummy_dronefunc(*args, **kwargs):
            if self.local:
                getattr(self.drone, name)(*args, **kwargs)
            else:
                self._send({'name': name, 'args': args, 'kwargs': kwargs})
        return dummy_dronefunc
