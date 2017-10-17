import socket
import struct
from threading import Thread


DATA_FORMAT = 'ciii'
DEFAULT_PORT = 8080

class RemoteSocket(Thread):
    def __init__(self, host, port=DEFAULT_PORT):
        Thread.__init__(self)
        self._on_recv_move = None
        self._on_start_game = None
        self._on_end_game = None

        self.socket = socket.socket()
        self.socket.connect((host,port))
        self._closed = False

    def send_move(self, box_id):
        data = struct.pack(DATA_FORMAT, b'm', *box_id)
        self.socket.send(data)

    def find_game(self):
        data = struct.pack(DATA_FORMAT, b's', 0, 0, 0)
        self.socket.send(data)

    def run(self):
        while not self._closed:
            parts = struct.unpack(DATA_FORMAT, self.socket.recv(struct.calcsize(DATA_FORMAT)))
            cmd, data = parts[0], parts[1:]
            if cmd == b'm' and self.on_recv_move:
                self.on_recv_move(data)
            if cmd == b's' and self.on_start_game:
                self.on_start_game('x' if data[0] == 1 else 'o')
            if cmd == b'e' and self.on_end_game:
                self.on_end_game(data[0])

    def close(self):
        self._closed = True
        self.socket.close()

    def _get_on_recv_move(self):
        return self._on_recv_move
    def _set_on_recv_move(self, on_recv_move):
        self._on_recv_move = on_recv_move

    def _get_on_start_game(self):
        return self._on_start_game
    def _set_on_start_game(self, on_start_game):
        self._on_start_game = on_start_game

    def _get_on_end_game(self):
        return self._on_end_game
    def _set_on_end_game(self, on_end_game):
        self._on_end_game = on_end_game

    on_recv_move = property(_get_on_recv_move, _set_on_recv_move)
    on_start_game = property(_get_on_start_game, _set_on_start_game)
    on_end_game = property(_get_on_end_game, _set_on_end_game)
