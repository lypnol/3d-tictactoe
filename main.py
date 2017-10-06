import itertools

from Scene.StartScene import StartScene
from Scene.GameScene import GameScene
from TicTacToe import TicTacToe


X_COLOR = 'e8c02c'
O_COLOR = '5fa0ba'
N = 3


def main():
    start_scene = StartScene()
    start_scene.show()
    start_scene.wait_for_start()
    start_scene.hide()

    game_scene = GameScene(N, X_COLOR, O_COLOR)
    tictactoe = TicTacToe(game_scene, N)
    game_scene.show()

if __name__ == '__main__':
    main()
