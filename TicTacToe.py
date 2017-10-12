import itertools


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
                    winnerList = [g[x][y][z]]
                    #contient l'éventuel triplet gagnant
                    if g[x][y][z] == 'x':
                        for item in getNeighbor(g,x,y,z):
                            if item == 'x':
                                winnerList.append(item)
                            #on remplit la liste de tous les voisins immédiats de g de meme couleur
                        if len(winnerList)>1:
                            for item2 in winnerList[1:]:
                                lastNeighbors = getNeighbor(item2, item2[0], item2[1], item2[2])
                                #on regarde les voisins immédiats de chaque voisin trouvé précédemment
                                for i in range(lastNeighbors):
                                    if lastNeighbors[i] == 'x':
                                        if isParallel(getVector(item2,g), getVector(item2,lastNeighbors[i])):
                                            return('x', [g, item2, lastNeighbors[i]])
                                     #ici, on détermine si le vecteur formé par item2 (voisins immédiats de g
                                     #de meme couleur) et g est proportionnel
                                     # à celui formé par item2 et l'un de ses voisins immédiat
                                     #si c'est le cas, c'est gagné
                        else:
                            continue
                    elif g[x][y][z] == 'o':
                        for item in getNeighbor(g,x,y,z):
                            if item == 'o':
                                winnerList.append(item)
                        if len(winnerList)>1:
                            for item2 in winnerList[1:]:
                                lastNeighbors = getNeighbor(item2, item2[0], item2[1], item2[2])
                                for i in range(lastNeighbors):
                                    if lastNeighbors[i] == 'o':
                                        if isParallel(getVector(item2,g), getVector(item2,lastNeighbors[i])):
                                            return('o', [g, item2, lastNeighbors[i]])
                        else:
                            continue
                    elif g[x][y][z] == None:
                        return None, None
                    else:
                        return 'NULL'

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
