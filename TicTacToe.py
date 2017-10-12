import itertools


class TicTacToe:
    def __init__(self, n, game_type='local', current_player='x', remote_socket=None, game_scene=None):
        self.grid = [[[None for z in range(n)] for y in range(n)] for x in range(n)]
        self.game_type = game_type

        self.game_scene = game_scene
        if self.game_scene:
            self.game_scene.on_select = self.on_select

        self.remote_socket = remote_socket
        if self.remote_socket and game_type == 'remote':
            self.remote_socket.on_recv_move = self.on_recv_move
            self.remote_socket.on_start_game = self.on_start_game

        if self.game_type == 'remote' and self.game_scene and self.remote_socket:
            self.game_scene.wait_for_opponent()
            self.remote_socket.find_game()
        elif self.game_type == 'local' and self.game_scene:
            self.game_scene.component_is_ready()

        self.current_player = current_player

    def check_end_game(self):
        g = self.grid
        n = len(g)

        # TODO Logic du jeu 3d
        # On doit utiliser l'état du jeu stocké dans la matrice 3x3x3 g
        # g[x][y][z] est un des éléments suivants:
        #  * 'x': case occupée par le joueur X
        #  * 'o': case occupée par le joueur O
        #  * None: case libre
        # Il faut retourner le couple (resultat, cases) où
        #  * resultat: soit 'x', 'o', 'NULL' ou None pour (X a gagné, O a gagné, match nul, match non terminé)
        #  * cases: si resultat est 'X' ou 'O', cases doit contenir un tableau des 3 points gagnants ((x1, y1, z1), (x2, y2, z2), (x3, y3, z3))

        return None, None

    def switch_player(self):
        if self.current_player == 'x':
            self.current_player = 'o'
        else:
            self.current_player = 'x'
        if self.game_scene:
            self.game_scene.switch_colors()

    def on_start_game(self, current_player):
        print("Started game as {}".format(current_player))
        self.current_player = current_player
        if self.game_scene:
            self.game_scene.component_is_ready()
            if self.current_player == 'o':
                self.game_scene.disable_actions = True
                self.game_scene.switch_colors()

    def on_recv_move(self, box_id, change_color=True):
        if change_color:
            print("Received move {}".format(box_id))
        else:
            print("Selected move {}".format(box_id))
        x, y, z = box_id
        self.grid[x][y][z] = self.current_player
        result, points = self.check_end_game()
        if self.game_scene and change_color:
            self.game_scene.select_box(box_id)
            self.game_scene.disable_actions = False
        if result is not None:
            if self.game_scene:
                self.game_scene.game_over((result, points), self.restart)
            return result, points
        else:
            self.switch_player()

    def on_select(self, box_id):
        res = self.on_recv_move(box_id, change_color=False)
        if self.game_scene and self.game_type == 'remote':
            self.game_scene.disable_actions = True
        if self.remote_socket:
            self.remote_socket.send_move(box_id)
            # TODO wait for other player
        return res
