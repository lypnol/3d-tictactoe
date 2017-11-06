
def getNeighbor(grid, startx, starty, startz):
    neighbors= list()
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            for k in [-1,0,1]:
                if i == j == k == 0:
                    continue
                elif startx+i in [0,1,2] and starty+j in [0,1,2] and startz+k in [0,1,2]:
                    neighbors.append((grid[startx+i][starty+j][startz+k],[startx+i,starty+j,startz+k]))
    return neighbors

def getVector(firstPoint, secondPoint):
    return ([firstPoint[0]-secondPoint[0], firstPoint[1]-secondPoint[1], firstPoint[2]-secondPoint[2]])

def isParallel(firstVector, secondVector):
    coef = None
    verifier = True
    for i in [0,1,2]:
        if firstVector[i] == 0:
            if secondVector[i] != 0:
                verifier = False
                break
            continue
        elif coef is None:
            coef = secondVector[i]/firstVector[i]
        if coef==0:
            verifier = False
            break
        elif coef != secondVector[i]/firstVector[i]:
            verifier = False
            break
    return verifier
