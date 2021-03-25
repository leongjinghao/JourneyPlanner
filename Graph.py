class Graph:
    adjList = {}

    def __init__(self, fileInput):
        self.adjList = {}
        text_file = open(fileInput, "r")
        lines = text_file.readlines()
        for line in lines:
            #remove line breaks, which is the last char
            line = line[:-1]
            element = line.split(": ")
            vertice1 = element[0]
            paths = element[1]
            vertice2 = paths.split(", ")
            for vertice in vertice2:
                self.addEdge(vertice1, vertice)

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

    def shortest_path(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in list(self.adjList.keys()):
            return None
        shortest = None
        for node in self.adjList[start]:
            if node not in path:
                new_path = self.shortest_path(node, end, path)
                if new_path:
                    if not shortest or len(new_path) < len(shortest):
                        shortest = new_path
        return shortest