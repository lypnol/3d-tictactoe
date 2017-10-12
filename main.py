import itertools
import sys

from Scene.StartScene import StartScene
from Scene.GameScene import GameScene
from RemoteSocket import RemoteSocket
from TicTacToe import TicTacToe


X_COLOR = 'e8c02c'
O_COLOR = '5fa0ba'
N = 3

SERVER_ADDR = 'localhost' if len(sys.argv) < 2 else str(sys.argv[1])
SERVER_PORT = 8080 if len(sys.argv) < 3 else int(sys.argv[2])

def main():
    remote_socket = None
    try:
        remote_socket = RemoteSocket(SERVER_ADDR, SERVER_PORT)
        remote_socket.start()
    except ConnectionRefusedError:
        pass

    start_scene = StartScene(remote=(True if remote_socket is not None else False))
    start_scene.show()
    game_type = start_scene.wait_for_start()
    start_scene.hide()

    game_scene = GameScene(N, X_COLOR, O_COLOR)
    game_scene.show()
    tictactoe = TicTacToe(N, game_type=game_type, remote_socket=remote_socket, game_scene=game_scene)

if __name__ == '__main__':
    main()
