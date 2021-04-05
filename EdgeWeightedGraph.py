from WeightedDirectedEdge import WeightedDirectedEdge

class EdgeWeightedGraph:
    adjList = {}
    allNodesIndex = {}

    def __init__(self, fileInput):
        # reset on every construct
        self.adjList = {}
        self.allNodesIndex = {}

        # read from a file input
        text_file = open(fileInput, "r")
        # list of each line on the file input
        lines = text_file.readlines()
        # method to index all vertices
        self.setAllNodesIndex()

        # for each line
        for line in lines:
            #remove line break, which is the last char
            line = line[:-1]
            # split vertex and destination vertex
            vertex, desVertices = line.split(": ")
            # might have multiple destination vertices, split by "," if so
            desVerticesWithWeight = desVertices.split(", ")
            # for each destination vertices, of a vertex
            for vertexWithWeight in desVerticesWithWeight:
                # split the destination vertex and weight
                desVertex, weight = vertexWithWeight.split(" - ")
                # add the edge (destination vertex and its weight) of the vertex into the adjList
                self.addEdge(self.allNodesIndex[vertex], self.allNodesIndex[desVertex], int(weight))
        
        # remove edges to brokendown stations, if there is any
        self.stnBreakdown()
    
    # method to add edge into the adjList
    def addEdge(self, vertex, desVertex, weight):
        # initialise a directed edge, with the given input
        edge = WeightedDirectedEdge(vertex, desVertex, weight)

        # if vertex is already inside the adjList, append edge into the list within the adjList of the vertex
        if vertex in self.adjList:
            self.adjList[vertex].append(edge)
        # else create a new entry for vertex in the adjList and insert a new list [], append the edge into list
        else:
            self.adjList[vertex] = []
            self.adjList[vertex].append(edge)
        
        # initialise edge for the other direction, from destination vertex to current vertex
        oppEdge = WeightedDirectedEdge(desVertex, vertex, weight)

        # if desVertex is already inside the adjList, append edge into the list within the adjList of desVertex
        if desVertex in self.adjList:
            self.adjList[desVertex].append(oppEdge)
        # else create a new entry for desVertex in the adjList and insert a new list [], append the edge into list
        else:
            self.adjList[desVertex] = []
            self.adjList[desVertex].append(oppEdge)

    # method to retrieve the adjacent edges (list) of a vertex
    def getAdjacent(self, vertex):
        return self.adjList[vertex]

    # method to retrieve all vertices
    def getAllVertices(self):
        return self.adjList.keys()

    # method to retrieve all edges
    def getAllEdges(self):
        allEdges = []
        
        for vertex in self.adjList:
            for edge in self.adjList[vertex]:
                allEdges.append(edge)

        return allEdges

    # method to index all the vertices (nodes)
    def setAllNodesIndex(self):
        # read from a input file which stores all the unique stations code
        text_file = open("all_unique_stations.csv", "r")
        lines = text_file.readlines()
        # index starts from 0
        index = 0
        # for each station stored in the input file, give it an index and store the value inside allNodeIndex (dict)
        for line in lines:
            # remove last char which is a line break
            node = line[:-1]
            # insert the index value for the vertex (node) inside allNodeIndex
            self.allNodesIndex[node] = index
            # increment index value for next index
            index += 1

    # method to retrieve the station name from a given index
    def getStationName(self, index):
        # traverse the allNodesIndex (dict) to find a match with the given index value
        for key, value in self.allNodesIndex.items():
            if value == index:
                return key
        
        # if no match found
        return "key does not exist"

    # remove edges from adj list, simulate station breakdown
    def stnBreakdown(self):
        # retrieve stations which have broken down
        stn_breakdown_file = open("stn_breakdown.csv", "r")
        stn_breakdown = stn_breakdown_file.read()
        
        # return out of function if there is no input for station breakdown
        if (stn_breakdown == ""): return
        
        stn_breakdown = stn_breakdown.split(", ")
        # for each station listed as brokendown
        for station in stn_breakdown:
            # retrieve the index of the brokendown station
            station_index = self.allNodesIndex[station]
            # retrieve adj edges of the brokendown stations, will need to remove edges 
            # of neighbour vertices to the brokendown station
            adj_edges = self.adjList[station_index]
            # remove the edge to the brokendown station from the neighbour vertices
            for adj_edge in adj_edges:
                # remove edge from adj vertex to brokendown station
                self.adjList[adj_edge.desVertex].remove(WeightedDirectedEdge(adj_edge.desVertex, adj_edge.vertex,adj_edge.weight))
            # lastly, remove all edges of the brokendown station by deleting the whole entry
            del self.adjList[station_index]