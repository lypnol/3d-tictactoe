import sys

from Scene.StartScene import StartScene
from Scene.GameScene import GameScene
from RemoteSocket import RemoteSocket
from TicTacToe import TicTacToe

#Here we define the box colors by their hex code
X_COLOR = 'e8c02c' #yellow for the player
O_COLOR = '5fa0ba' #blue for the opponent

N = 3 #cube dimension

#If no IP is mentioned, launched on localhost
SERVER_ADDR = 'localhost' if len(sys.argv) < 2 else str(sys.argv[1])
SERVER_PORT = 8080 if len(sys.argv) < 3 else int(sys.argv[2])

def main():
    remote_socket = None
    try:
        remote_socket = RemoteSocket(SERVER_ADDR, SERVER_PORT)
        remote_socket.start()
    except ConnectionRefusedError:
        pass

    remote_enabled = True if remote_socket is not None else False

    start_scene = StartScene(remote_enabled=remote_enabled)
    start_scene.show()

    #Wait for player's click, then hide welcome screen
    game_type = start_scene.wait_for_start()
    start_scene.hide()

    game_scene = GameScene(N, X_COLOR, O_COLOR, remote_enabled=remote_enabled)
    game_scene.show()
    tictactoe = TicTacToe(N, game_type=game_type, remote_socket=remote_socket, game_scene=game_scene)

if __name__ == '__main__':
    main()
