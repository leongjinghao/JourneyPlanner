#from Graph import Graph
from EdgeWeightedDigraph import EdgeWeightedDigraph
#mrt = Graph("mrt_stations.txt")
#print(mrt.shortest_path("DT16/CE1", "NS4"))
from queue import PriorityQueue
from DijkstraSP import DijkstraSP

mrt = EdgeWeightedDigraph("mrt_stations_weighted.csv")
'''
allEdges = mrt.getAllEdges()
#print(allEdges)
for edge in allEdges:
    print(edge.toString())


edgeTo = [None for i in range(len(mrt.allNodesIndex))]

print(len(edgeTo))

edges = mrt.adjList[mrt.allNodesIndex["NS24/NE6/CC1"]]
for edge in edges:
    print(edge.vertex, edge.desVertex, edge.weight)
'''
path = DijkstraSP(mrt, 5)
#print(len(edgeTo))

#for line in edgeTo:
#    print(line)