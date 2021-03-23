class Graph:
    adjList = {}

    def __init__(self, fileInput):
        text_file = open(fileInput, "r")
        lines = text_file.readlines()
        for line in lines:
            element = line.split(":")
            vertice1 = element[0]
            paths = element[1]
            vertice2 = paths.split(", ")
            for vertice in vertice2:
                self.addEdge(vertice1, vertice2)

    def addEdge(self, vertice1, vertice2):
        if vertice1 in self.adjList:
            self.adjList[vertice1].append(vertice2)
        else:
            self.adjList[vertice1] = []
            self.adjList[vertice1].append(vertice2)

        if vertice2 in self.adjList:
            self.adjList[vertice2].append(vertice1)
        else:
            self.adjList[vertice2] = []
            self.adjList[vertice2].append(vertice1)