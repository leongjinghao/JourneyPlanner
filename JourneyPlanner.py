from EdgeWeightedGraph import EdgeWeightedGraph
from DijkstraSP import DijkstraSP

mrt = EdgeWeightedGraph("mrt_stations_weighted_1.csv")

route = []
path = DijkstraSP(mrt, mrt.allNodesIndex["NS13"])
dest_stn = mrt.allNodesIndex["CC6"]
route.append(mrt.getStationName(dest_stn))

while (dest_stn != mrt.allNodesIndex["NS13"]):
    dest_stn = path.edgeTo[dest_stn].vertex
    route.append(mrt.getStationName(dest_stn))

while len(route) != 0:
    # print route in the reverse order
    print(route.pop())