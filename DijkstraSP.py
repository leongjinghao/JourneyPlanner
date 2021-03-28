from EdgeWeightedDigraph import EdgeWeightedDigraph

class DijkstraSP:
    distTo = []
    edgeTo = []
    marked = []
    pq = None

    def __init__(self, graph, start):
        