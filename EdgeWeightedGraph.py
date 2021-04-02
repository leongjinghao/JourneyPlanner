from DirectedEdge import DirectedEdge

class EdgeWeightedGraph:
    adjList = {}
    allNodesIndex = {}

    def __init__(self, fileInput):

        self.adjList = {}
        self.allNodesIndex = {}

        text_file = open(fileInput, "r")
        lines = text_file.readlines()
        self.setAllNodesIndex()
        for line in lines:
            #remove line breaks, which is the last char
            line = line[:-1]
            vertex, desVertices = line.split(": ")
            desVerticesWithWeight = desVertices.split(", ")
            for vertexWithWeight in desVerticesWithWeight:
                desVertex, weight = vertexWithWeight.split(" - ")
                self.addEdge(self.allNodesIndex[vertex], self.allNodesIndex[desVertex], int(weight))
    
    def addEdge(self, vertex, desVertex, weight):
        edge = DirectedEdge(vertex, desVertex, weight)

        if vertex in self.adjList:
            self.adjList[vertex].append(edge)
        else:
            self.adjList[vertex] = []
            self.adjList[vertex].append(edge)
        
        oppEdge = DirectedEdge(desVertex, vertex, weight)

        if desVertex in self.adjList:
            self.adjList[desVertex].append(oppEdge)
        else:
            self.adjList[desVertex] = []
            self.adjList[desVertex].append(oppEdge)

    def getAdjacent(self, vertex):
        return self.adjList[vertex]

    def getAllVertices(self):
        return self.adjList.keys()

    def getAllEdges(self):
        allEdges = []
        
        for vertex in self.adjList:
            for edge in self.adjList[vertex]:
                allEdges.append(edge)

        return allEdges

    def setAllNodesIndex(self):
        text_file = open("all_unique_stations.csv", "r")
        lines = text_file.readlines()
        index = 0
        for line in lines:
            node = line[:-1]
            self.allNodesIndex[node] = index
            index += 1

    def getStationName(self, index):
        for key, value in self.allNodesIndex.items():
            if value == index:
                return key
        
        return "key does not exist"