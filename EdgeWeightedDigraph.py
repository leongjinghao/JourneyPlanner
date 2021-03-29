from DirectedEdge import DirectedEdge

class EdgeWeightedDigraph:
    adjList = {}
    allNodesIndex = {}

    def __init__(self, fileInput):
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

        if edge.vertex in self.adjList:
            self.adjList[edge.vertex].append(edge)
        else:
            self.adjList[edge.vertex] = []
            self.adjList[edge.vertex].append(edge)

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