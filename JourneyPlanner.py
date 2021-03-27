from Graph import Graph
from EdgeWeightedDigraph import EdgeWeightedDigraph

#mrt = Graph("mrt_stations.txt")
#print(mrt.shortest_path("EW28", "NE14"))

mrt = EdgeWeightedDigraph("mrt_stations_weighted.txt")
'''
allEdges = mrt.getAllEdges()
print(allEdges)
for edge in allEdges:
    print(edge.toString())
'''
arr = []
arr.insert("a", 0.0)
print(arr)