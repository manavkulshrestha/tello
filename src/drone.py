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
        self.local = ip in ['localhost', '127.0.0.1']


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.local:
            self.drone = Tello()
            self.drone.connect()
            # if verbose:
            print(self.drone.get_battery())
            self._setup_server(port)
        else:
            self._setup_client(ip, port)

        self.verbose = verbose
        # self._BUFFER_SIZE = 1024

    def _setup_server(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', port)) # listen on all ip's for convenience
        self.sock.listen()

        if self.verbose:
            print(f"Server listening on all IPs at port {port}...")

        conn, addr = self.sock.accept()
        if self.verbose:
            print(f"Connection established with {addr}")

        self._handle_client(conn) # blocking - it'll stay here until connection closed

    def _handle_client(self, conn):
        while True:
            data = self._recv(conn) # blocking
            if data:
                ret = getattr(self.drone, data['name'])(*data['args'], **data['kwargs'])
                # self._send(ret, conn=conn)
            else:
                if self.verbose:
                    print('Closing connection.')
                break
        conn.close()

    def _setup_client(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def _recv(self, conn):
        raw_msglen = conn.recv(4)
        if not raw_msglen:
            return None
        msglen = int.from_bytes(raw_msglen, byteorder='big')

        data = b''
        while len(data) < msglen:
            packet = conn.recv(min(1024, msglen - len(data)))
            if not packet:
                return None
            data += packet
        return pickle.loads(data)

    def _send(self, obj, conn=None):
        conn = self.sock if conn is None else conn
        data = pickle.dumps(obj)
        conn.sendall(len(data).to_bytes(4, byteorder='big'))
        conn.sendall(data)

    def __getattr__(self, name):
        def dummy_dronefunc(*args, **kwargs):
            getret = kwargs.get('return', False)
            if 'return' in kwargs:
                del kwargs['return']
            if self.local:
                # getattr(self.drone, name)(*args, **kwargs) # not really used since localhost drone will always be listening for commands
                raise NotImplementedError
            else:
                self._send({'name': name, 'args': args, 'kwargs': kwargs})
                if getret:
                    return self._recv(self.sock) # blocking
        return dummy_dronefunc
