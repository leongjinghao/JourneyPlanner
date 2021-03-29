from EdgeWeightedGraph import EdgeWeightedGraph
from queue import PriorityQueue
from DijkstraSP import DijkstraSP

mrt = EdgeWeightedGraph("mrt_stations_weighted_1.csv")
'''
allEdges = mrt.getAllEdges()
#print(allEdges)
for edge in allEdges:
    print(edge.toString())

print(len(edgeTo))
'''
edges = mrt.adjList[80]
for edge in edges:
    print(edge.vertex, edge.desVertex, edge.weight)


route = []
path = DijkstraSP(mrt, mrt.allNodesIndex["EW5"])
dest_stn = mrt.allNodesIndex["NS25/EW13"]
route.append(mrt.getStationName(dest_stn))

while (dest_stn != mrt.allNodesIndex["EW5"]):
    dest_stn = path.edgeTo[dest_stn].vertex
    route.append(mrt.getStationName(dest_stn))

while len(route) != 0:
    print(route.pop())

#print(mrt.allNodesIndex)
#print(len(edgeTo))

#for line in edgeTo:
#    print(line)