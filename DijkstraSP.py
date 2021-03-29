from EdgeWeightedDigraph import EdgeWeightedDigraph

class DijkstraSP:
    distTo = []
    edgeTo = []
    marked = []
    pq = None

    def __init__(self, digraph, start):
        self.edgeTo = [[vertex, None] for vertex in digraph.adjList]