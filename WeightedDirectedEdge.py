class WeightedDirectedEdge:
    vertex = None
    desVertex = None
    weight = None

    def __init__(self, vertex, desVertex, weight):
        # reset on every construct
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

    # "<" operation between 2 edges' weight
    def __lt__(self, other):
        return self.weight < other.weight

    # ">" operation between 2 edges' weight
    def __gt__(self, other):
        return self.weight > other.weight

    # ">=" operation between 2 edges' weight
    def __ge__(self, other):
        return self.weight >= other.weight

    # "<=" operation between 2 edges' weight
    def __le__(self, other):
        return self.weight <= other.weight

    # "==" operation between 2 edges, test equality between 2 edges
    def __eq__(self, other):
        return self.vertex == other.vertex and self.desVertex == other.desVertex and self.weight == other.weight

    def toString(self):
        return str(self.vertex) + " - " + \
               str(self.desVertex) + " : " + \
               str(self.weight)