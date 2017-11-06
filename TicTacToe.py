import itertools
from geometry import getNeighbor, isParallel, getVector

class TicTacToe:
    def __init__(self, n, game_type='local', current_player='x', remote_socket=None, game_scene=None):
        self.n = n
        self.game_scene = game_scene
        self.current_player = current_player
        if self.game_scene:
            self.game_scene.on_select = self.on_select
            self.game_scene.on_restart = self.reset

        self.remote_socket = remote_socket
        if self.remote_socket:
            self.remote_socket.on_recv_move = self.on_recv_move
            self.remote_socket.on_start_game = self.on_start_game
            self.remote_socket.on_end_game = self.on_opponent_left

        self.reset(game_type)

    def reset(self, game_type):
        self.grid = [[[None for z in range(self.n)] for y in range(self.n)] for x in range(self.n)]
        self.game_type = game_type
        if self.game_type == 'remote' and self.game_scene and self.remote_socket:
            self.game_scene.wait_for_opponent()
            self.remote_socket.find_game()
        elif self.game_type == 'local' and self.game_scene:
            self.game_scene.component_is_ready()
            self.current_player = 'x'

    def check_end_game(self):
        g = self.grid
        n = len(g)
        for (x, y, z) in itertools.product(range(n), repeat=3):
            if g[x][y][z] is None:
                continue
            neighbors = getNeighbor(g,x,y,z)
            while neighbors:
                if neighbors[0][0] == g[x][y][z]:
                    for otherNeighbor in neighbors[1:]:
                        if otherNeighbor[0] == g[x][y][z] \
                        and isParallel(getVector(neighbors[0][1],(x,y,z)), getVector(otherNeighbor[1],(x,y,z))):
                            return g[x][y][z], ((x,y,z), tuple(neighbors[0][1]), tuple(otherNeighbor[1]))
                neighbors.pop(0)

        if all(g[x][y][z] is not None for (x, y, z) in itertools.product(range(n), repeat=3)):
            return 'NULL', []

        return None

    def switch_player(self):
        if self.current_player == 'x':
            self.current_player = 'o'
        else:
            self.current_player = 'x'
        if self.game_scene:
            self.game_scene.switch_colors()

    def _apply_move(self, box_id):
        x, y, z = box_id
        self.grid[x][y][z] = self.current_player
        match_ended = self.check_end_game()
        if match_ended is not None: return match_ended
        self.switch_player()
        return None

    def on_start_game(self, current_player):
        print("Started game as {}".format(current_player))
        self.current_player = current_player
        if self.game_scene:
            self.game_scene.component_is_ready()
            if self.current_player == 'o':
                self.game_scene.disable_actions = True
                self.game_scene.switch_colors()

    def on_recv_move(self, box_id, debug=True):
        if debug: print("Player {} move {}".format(self.current_player, box_id))
        if self.game_scene:
            self.game_scene.select_box(box_id)
            self.game_scene.disable_actions = False
        match_ended = self._apply_move(box_id)
        if match_ended and self.game_scene:
            if debug: print("Match ended {} {}".format(*match_ended))
            self.game_scene.game_over(match_ended)

    def on_select(self, box_id, debug=True):
        if debug: print("Player {} move {}".format(self.current_player, box_id))
        match_ended = self._apply_move(box_id)
        if self.game_type == 'remote' and self.game_scene and self.remote_socket:
            self.game_scene.disable_actions = True
            self.remote_socket.send_move(box_id)
        if self.game_scene and match_ended:
            if debug: print("Match ended {} {}".format(*match_ended))
            self.game_scene.game_over(match_ended)
        return match_ended

    def on_opponent_left(self):
        if self.game_scene:
            self.game_scene.on_opponent_left()
