#from Graph import Graph
from EdgeWeightedDigraph import EdgeWeightedDigraph

#mrt = Graph("mrt_stations.txt")
#print(mrt.shortest_path("DT16/CE1", "NS4"))

mrt = EdgeWeightedDigraph("mrt_stations_weighted.txt")
'''
allEdges = mrt.getAllEdges()
#print(allEdges)
for edge in allEdges:
    print(edge.toString())
'''
mrt.setAllNodes()
edgeTo = {}
for node in mrt.allNodes:
    edgeTo[node] = None
print(edgeTo["CG2"])
#for line in edgeTo:
#    print(line)