from PriorityQueue import PriorityQueue

class DijkstraSP:
    timeTo = []
    edgeTo = []
    marked = []
    pq = None

    def __init__(self, graph, start):
        # reset on every construct
        self.timeTo = []
        self.edgeTo = []
        self.marked = []
        self.pq = None

        self.edgeTo = [None for i in range(len(graph.allNodesIndex))]
        self.marked = [False for i in range(len(graph.allNodesIndex))]
        self.timeTo = [float('Inf') for i in range(len(graph.allNodesIndex))]
        # initialise priority queue with starting node
        self.pq = PriorityQueue(start)
        # set the time to starting node as 0
        self.timeTo[start] = 0

        # while the priority queue is not empty (yet to finished relaxing all node)
        while not self.pq.isEmpty():
            # retrieve the vertex (node) with the least weight (time)
            vertex = self.pq.delete_min()
            # set the vertex as marked (visited)
            self.marked[vertex] = True
            # checking
            print("Relaxing neighbours of vertex " + str(vertex) + ", W: " + str(self.timeTo[vertex]))
            # for all edges of current vertex
            for edge in graph.adjList[vertex]:
                # relax all the edges from vertex
                self.relax(edge)

    # method for relaxing edges of a vertex
    def relax(self, edge):
        # current vertex
        vertex = edge.vertex
        # adjacent vertices
        desVertex = edge.desVertex
        # if the existing cumulative weight (timeTo) to the adjacent vertice is more than
        # the cumulative weight of the new route found, update the value in timeTo and edgeTo
        if self.timeTo[desVertex] > self.timeTo[vertex] + edge.weight:
            self.timeTo[desVertex] = self.timeTo[vertex] + edge.weight
            self.edgeTo[desVertex] = edge
            # checking relaxed edge
            print("     - " + str(edge.desVertex) + ", W: " + str(self.timeTo[edge.desVertex]))
            # update the values stored in the priority queue as well
            if self.pq.contains(desVertex):
                self.pq.change(desVertex, self.timeTo[desVertex])
            # if value not stored inside the priority queue yet, insert it inside the priority queue
            elif self.marked[desVertex] == False:
                self.pq.insert(desVertex, self.timeTo[desVertex])