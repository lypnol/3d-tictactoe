from vpython import vector

def hex_to_color_vector(h):
     return vector(*tuple(int(h[i:i+2], 16) / 256 for i in (0, 2 ,4)))

def getNeighbor(grid, startx, starty, startz):
    return([grid[startx+i][starty+j][startyz+k] for i in [-1,0,1] for j in [-1,0,1] for k in [-1,0,1]])
#ne pas oublier d'exclure les cas où le point sort du grid (hors de 0,1,2)

def getVector(firstPoint, secondPoint):
    return ([firstPoint[0]-secondPoint[0], firstPoint[1]-secondPoint[1], firstPoint[2]-secondPoint[2]])

def isParallel(firstVector, secondVector):
    quotient = []
    remainder = []
    for i in range(2):
        quotient[i] = firstVector[i] // secondVector[i]
        remainder[i] = firstVector[i] % secondVector[i]
    for item in remainder:
        if item != 0:
            return False
    return quotient[1:] == quotient[:-1]
