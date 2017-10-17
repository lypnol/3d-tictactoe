import itertools
from Scene.utils import getNeighbor, isParallel, getVector

class TicTacToe:
    def __init__(self, game_scene, n, current_player='x'):
        self.grid = [[[None for z in range(n)] for y in range(n)] for x in range(n)]
        self.game_scene = game_scene
        self.game_scene.on_select = self.on_select
        self.current_player = current_player

    def check_end_game(self):
        g = self.grid
        n = len(g)
        for x in range(n):
            for y in range(n):
                for z in range(n):
                    neighbors = getNeighbor(g,x,y,z)
                    #for item in neighbors:
                    #neighbors[0] est le 1er voisin de la liste
                    #neighbors[0][0] est la couleur
                    while neighbors:
                        if neighbors[0][0] == g[x][y][z]:
                            for otherNeighbor in neighbors[1:]:
                                if otherNeighbor[0] == g[x][y][z] \
                                and isParallel(getVector(neighbors[0][1],(x,y,z)), getVector(otherNeighbor[1],(x,y,z))):
                                    return ("It's a win", [x,y,z], neighbors[0][1], otherNeighbor[1])
                            neighbors.pop(0)
        return None


        # TODO Logic du jeu 3d
        # On doit utiliser l'état du jeu stocké dans la matrice 3x3x3 g
        # g[x][y][z] est un des éléments suivants:
        #  * 'x': case occupée par le joueur X
        #  * 'o': case occupée par le joueur O
        #  * None: case libre
        # Il faut retourner le couple (resultat, cases) où
        #  * resultat: soit 'x', 'o', 'NULL' ou None pour (X a gagné, O a gagné, match nul, match non terminé)
        #  * cases: si resultat est 'X' ou 'O', cases doit contenir un tableau des 3 points gagnants ((x1, y1, z1), (x2, y2, z2), (x3, y3, z3))

    def switch_player(self):
        if self.current_player == 'x':
            self.current_player = 'o'
        else:
            self.current_player = 'x'
        self.game_scene.switch_colors()

    def on_select(self, box_id):
        x, y, z = box_id
        print('Player', self.current_player, ':', box_id)
        self.grid[x][y][z] = self.current_player
        result, points = self.check_end_game()
        if result is not None:
            print('Match ended: ', result, points)
            self.game_scene.game_over((result, points), self.restart)
        else:
            self.switch_player()
