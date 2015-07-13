from atd.entities import Graph, ColoredMixin, Vertex, DFS_Graph

__author__ = 'alesha'


def genLegalMoves(x, y, bdSize):
    newMoves = []
    moveOffsets = [(-1, -2), (-1, 2), (-2, -1), (-2, 1),
                   (1, -2), (1, 2), (2, -1), (2, 1)]
    for i in moveOffsets:
        newX = x + i[0]
        newY = y + i[1]
        if legalCoord(newX, bdSize) and \
                legalCoord(newY, bdSize):
            newMoves.append((newX, newY))
    return newMoves


def legalCoord(x, bdSize):
    if x >= 0 and x < bdSize:
        return True
    return False

def posToNodeId(r, c, bdSize):
    nodeId = (bdSize * r) + c
    return nodeId


def knightGraph(bdSize):
    ktGraph = DFS_Graph()
    for row in range(bdSize):
        for col in range(bdSize):
            nodeId = posToNodeId(row, col, bdSize)
            newPositions = genLegalMoves(row, col, bdSize)
            for e in newPositions:
                nid = posToNodeId(e[0], e[1], bdSize)
                ktGraph.add_edge(nodeId, nid)
    return ktGraph


if __name__ == '__main__':
    g = DFS_Graph()
    g.add_edge('a', 'b')
    g.add_edge('a', 'd')

    g.add_edge('b', 'c')
    g.add_edge('b', 'd')

    g.add_edge('d', 'e')

    g.add_edge('e', 'b')
    g.add_edge('e', 'f')

    g.add_edge('f', 'c')

    path = g.compile('a')
    print('\n'.join([str(el) for el in path]))


