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
        #defining the 3x3x3 grid representing the cubes
        self.grid = [[[None for z in range(self.n)] for y in range(self.n)] for x in range(self.n)]
        self.game_type = game_type
        if self.game_type == 'remote' and self.game_scene and self.remote_socket:
            self.game_scene.searching_for_opponent()
            self.remote_socket.find_game()
        elif self.game_type == 'local' and self.game_scene:
            self.current_player = 'x'
            self.game_scene.start_new_game()
            self.game_scene.player_turn(self.current_player)

    def check_end_game(self):
        """returns the id of the winning cubes and their color"""
        g = self.grid
        n = len(g)
        for x in range(n):
            for y in range(n):
                for z in range(n):
                    if g[x][y][z] is None:
                        continue
                    #get the immediate neighbors of the cube(x,y,z)
                    neighbors = getNeighbor(g,x,y,z)
                    while neighbors:
                        #neighbors[0] is the first neighbor in the list
                        #neighbors[0][0] is the color of this cube
                        if neighbors[0][0] == g[x][y][z]:
                            #if the two cubes have the same color, we check the next neighbors in the list
                            for otherNeighbor in neighbors[1:]:
                                #if we find a 3rd cube, aligned with the 2 others with the same color, return the result
                                if otherNeighbor[0] == g[x][y][z] \
                                and isParallel(getVector(neighbors[0][1],(x,y,z)), getVector(otherNeighbor[1],(x,y,z))):
                                    return g[x][y][z], ([x,y,z], neighbors[0][1], otherNeighbor[1])
                        #if no such 3rd cube is found, remove the neighbor from the list and test the next
                        neighbors.pop(0)
        return None

        # Further explanations:
        # g[x][y][z] is either:
        #  * 'x': box containing X
        #  * 'o': box containing O
        #  * None: free box
        # check_end_game returns (result, boxes) where
        #  * result: either 'x', 'o', 'NULL' or None corresponding to (X won, O won, draw, unfinished game)
        #  * boxes: if result is 'X' or 'O', boxes contains a three element list ((x1, y1, z1), (x2, y2, z2), (x3, y3, z3))

    def switch_player(self):
        if self.current_player == 'x':
            self.current_player = 'o'
        else:
            self.current_player = 'x'

    def _apply_move(self, box_id):
        x, y, z = box_id
        self.grid[x][y][z] = self.current_player
        if self.game_scene:
            self.game_scene.select_box(box_id, self.current_player)
        match_ended = self.check_end_game()
        if match_ended is not None: return match_ended
        self.switch_player()
        return None

    def on_start_game(self, as_symbol):
        print("Started game as {}".format(as_symbol))
        self.current_player = 'x'
        if self.game_scene:
            self.game_scene.start_new_game()
            if as_symbol == 'o':
                self.game_scene.opponent_turn('x')
            else:
                self.game_scene.player_turn('x')

    def on_recv_move(self, box_id, debug=True):
        if debug: print("Player {} move {}".format(self.current_player, box_id))
        match_ended = self._apply_move(box_id)
        self.game_scene.player_turn(self.current_player)
        if match_ended and self.game_scene:
            if debug: print("Match ended {} {}".format(*match_ended))
            self.game_scene.game_over(match_ended)

    def on_select(self, box_id, debug=True):
        if debug: print("Player {} move {}".format(self.current_player, box_id))
        match_ended = self._apply_move(box_id)

        if self.game_scene and self.game_type == 'remote':
            self.game_scene.opponent_turn(self.current_player)
        elif self.game_scene:
            self.game_scene.player_turn(self.current_player)

        if self.game_type == 'remote' and self.remote_socket:
            self.remote_socket.send_move(box_id)

        if self.game_scene and match_ended:
            if debug: print("Match ended {} {}".format(*match_ended))
            self.game_scene.game_over(match_ended)
        return match_ended

    def on_opponent_left(self):
        if self.game_scene:
            self.game_scene.on_opponent_left()
