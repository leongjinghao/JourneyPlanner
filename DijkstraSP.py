from PriorityQueue import PriorityQueue

class DijkstraSP:
    timeTo = []
    edgeTo = []
    marked = []
    pq = None

    def __init__(self, digraph, start):
        self.edgeTo = [None for i in range(len(digraph.allNodesIndex))]
        self.marked = [False for i in range(len(digraph.allNodesIndex))]
        self.timeTo = [float('Inf') for i in range(len(digraph.allNodesIndex))]
        self.pq = PriorityQueue(start)
        self.timeTo[start] = 0
        while not self.pq.isEmpty():
            vertex = self.pq.delete_min()
            self.marked[vertex] = True
            print("Relaxing neighbours of vertex " + str(vertex) + ", " + str(self.timeTo[vertex]))
            for edge in digraph.adjList[vertex]:
                self.relax(edge)
                print("     - " + str(edge.desVertex) + ", " + str(self.timeTo[edge.desVertex]))

    def relax(self, edge):
        vertex = edge.vertex
        desVertex = edge.desVertex
        if self.timeTo[desVertex] > self.timeTo[vertex] + edge.weight:
            self.timeTo[desVertex] = self.timeTo[vertex] + edge.weight
            self.edgeTo[desVertex] = edge
            if self.pq.contains(desVertex):
                self.pq.change(desVertex, self.timeTo[desVertex])
            elif self.marked[desVertex] == False:
                self.pq.insert(desVertex, self.timeTo[desVertex])