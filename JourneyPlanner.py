from Graph import Graph

mrt = Graph("mrt_stations.txt")
print(mrt.shortest_path("EW28", "NE14"))