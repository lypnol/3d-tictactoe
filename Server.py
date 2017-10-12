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
        self.conn.send(struct.pack(DATA_FORMAT, b's', 0 if player_symbol == 'o' else 1, 0, 0))
        self.player_symbol = player_symbol
        self.opponent = opponent
        self.game = game

    def send_move(self, data):
        self.conn.send(struct.pack(DATA_FORMAT, b'm', *data))

    def end_game(self, data):
        self.conn.send(struct.pack(DATA_FORMAT, b'e', *data))

    def run(self):
        while not self._closed:
            data = self.read_bytes(struct.calcsize(DATA_FORMAT))
            parts = struct.unpack(DATA_FORMAT, data)
            cmd, data = parts[0], parts[1:]
            if cmd == b's':
                self.server.game_request(self)
            elif cmd == b'm' and self.opponent and self.game.current_player == self.player_symbol:
                self.game.on_select(data)
                concurrent_print("Player %s move %s" % (self, data))
                self.opponent.send_move(data)

    def close(self):
        self._closed = True
        self.conn.close()

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

class Server:
    def __init__(self, host=HOST, port=PORT, max_connections=MAX_CONNECTIONS):
        self.port = port
        self.host = host
        self.max_connections = max_connections
        self.conn_identifier = 0
        self.id_lock = RLock()
        self.game_requests = Queue()
        self.games = {}
        self.games_lock = RLock()

    def game_request(self, player):
        concurrent_print("Received game request from %s" % (player))
        player1, player2 = self.game_requests.pushpop2(player)
        if player1 and player2:
            with self.games_lock:
                games = self.games
                if player1 not in games and player2 not in games:
                    game = TicTacToe(N)
                    self.games[player1] = game
                    self.games[player2] = game
                    player2.start_game('o', player1, game)
                    player1.start_game('x', player2, game)
                    concurrent_print("Started game between %s and %s" % (player1, player2))

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
