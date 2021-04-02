class DirectedEdge:
    vertex = None
    desVertex = None
    weight = None

    def __init__(self, vertex, desVertex, weight):

        self.vertex = None
        self.desVertex = None
        self.weight = None


        self.vertex = vertex
        self.desVertex = desVertex
        self.weight = weight

    def source(self):
        return self.vertex

    def dest(self):
        return self.desVertex

    # "<" operation between 2 vertices
    def __lt__(self, other):
        return self.weight < other.weight

    # ">" operation between 2 vertices
    def __gt__(self, other):
        return self.weight > other.weight

    # ">=" operation between 2 vertices
    def __ge__(self, other):
        return self.weight >= other.weight

    # "<=" operation between 2 vertices
    def __le__(self, other):
        return self.weight <= other.weight

    # "==" operation between 2 vertices
    def __eq__(self, other):
        return self.weight == other.weight

    def toString(self):
        return str(self.vertex) + " - " + \
               str(self.desVertex) + " : " + \
               str(self.weight)