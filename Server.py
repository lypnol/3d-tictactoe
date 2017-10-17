import socket
import struct
from collections import deque
from threading import Thread, RLock

from RemoteSocket import DATA_FORMAT, DEFAULT_PORT
from TicTacToe import TicTacToe


MAX_CONNECTIONS = 100
PORT = DEFAULT_PORT
HOST = '0.0.0.0'
N = 3

concurrent_print_lock = RLock()
def concurrent_print(*args, **kargs):
    global concurrent_print_lock
    with concurrent_print_lock:
        print(*args, **kargs)

class ConnectionHandler(Thread):
    def __init__(self, identifier, server, conn, addr):
        Thread.__init__(self)

        self.identifier = identifier
        self.conn = conn
        self.addr = addr
        self.server = server
        self._closed = False

        self.opponent = None
        self.game = None
        self.player_symbol = None

    def __str__(self):
        return "%d (%s:%d)" % (self.identifier, *self.addr)

    def read_bytes(self, n):
        l = 0
        data = b''
        while not self._closed and l < n:
            part = self.conn.recv(n-l)
            if not part:
                continue
            l += len(part)
            data += part
        return data

    def start_game(self, player_symbol, opponent, game):
        self.game = game
        self.player_symbol = player_symbol
        self.opponent = opponent
        self.conn.send(struct.pack(DATA_FORMAT, b's', 0 if player_symbol == 'o' else 1, 0, 0))

    def send_move(self, data):
        self.conn.send(struct.pack(DATA_FORMAT, b'm', *data))

    def end_game(self, data):
        self.game = None
        self.opponent = None

    def run(self):
        try:
            while not self._closed:
                data = self.read_bytes(struct.calcsize(DATA_FORMAT))
                parts = struct.unpack(DATA_FORMAT, data)
                cmd, data = parts[0], parts[1:]
                if cmd == b's':
                    self.server.game_request(self)
                elif cmd == b'm' and self.opponent and self.game.current_player == self.player_symbol:
                    concurrent_print("Player %s move %s" % (self, data))
                    match_ended = self.game.on_select(data, debug=False)
                    self.opponent.send_move(data)
                    if match_ended:
                        self.end_game()
        except:
            self.close()

    def in_game(self):
        return not self._closed and self.game is not None and self.opponent is not None

    def close(self):
        self._closed = True
        if self.conn:
            self.conn.close()
        if self.in_game():
            self.opponent.end_game()
            self.opponent.conn.send(struct.pack(DATA_FORMAT, b'e', 0, 0, 0))
        if self.server:
            self.server.disconnect(self)

class Queue:
    def __init__(self):
        self.queue = deque()
        self.lock = RLock()

    def pushpop2(self, e):
        with self.lock:
            self.queue.appendleft(e)
            if len(self.queue) >= 2:
                return (self.queue.pop(), self.queue.pop())
            return None, None

    def remove(self, e):
        with self.lock:
            try:
                self.queue.remove(e)
            except ValueError: pass

class Server:
    def __init__(self, host=HOST, port=PORT, max_connections=MAX_CONNECTIONS):
        self.port = port
        self.host = host
        self.max_connections = max_connections
        self.conn_identifier = 0
        self.id_lock = RLock()
        self.game_requests = Queue()

    def game_request(self, player):
        concurrent_print("Received game request from %s" % (player))
        player1, player2 = self.game_requests.pushpop2(player)
        if player1 and player2 and not player1.in_game() and not player2.in_game():
            game = TicTacToe(N)
            player2.start_game('o', player1, game)
            player1.start_game('x', player2, game)
            concurrent_print("Started game between %s and %s" % (player1, player2))

    def disconnect(self, player):
        self.game_requests.remove(player)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
            socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            socket_server.bind((self.host, self.port))
            socket_server.listen(self.max_connections)
            concurrent_print("Started server on %s:%d" % (self.host, self.port))
            while True:
                conn, addr = socket_server.accept()
                with self.id_lock:
                    self.conn_identifier += 1
                    identifier = self.conn_identifier
                    connection_handler = ConnectionHandler(identifier, self, conn, addr)
                    concurrent_print("Connection from %s" % connection_handler)
                    connection_handler.start()

def main():
    server = Server()
    server.start()

if __name__ == '__main__':
    main()
