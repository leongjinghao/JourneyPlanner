#from Graph import Graph
from EdgeWeightedGraph import EdgeWeightedGraph
#mrt = Graph("mrt_stations.txt")
#print(mrt.shortest_path("DT16/CE1", "NS4"))
from queue import PriorityQueue
from DijkstraSP import DijkstraSP

mrt = EdgeWeightedGraph("mrt_stations_weighted.csv")
'''
allEdges = mrt.getAllEdges()
#print(allEdges)
for edge in allEdges:
    print(edge.toString())


print(len(edgeTo))
'''
edges = mrt.adjList[mrt.allNodesIndex["NS24/NE6/CC1"]]
for edge in edges:
    print(edge.vertex, edge.desVertex, edge.weight)


path = DijkstraSP(mrt, 5)
current_stn = 63
print(mrt.getStationName(current_stn))
while (current_stn != 5):
    current_stn = path.edgeTo[current_stn].vertex
    print(mrt.getStationName(current_stn))
#print(mrt.allNodesIndex)
#print(len(edgeTo))

#for line in edgeTo:
#    print(line)