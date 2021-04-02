from EdgeWeightedGraph import EdgeWeightedGraph
from DijkstraSP import DijkstraSP

def computeRoute(currentLocation, destination):
    mrt = EdgeWeightedGraph("mrt_stations_weighted.csv")

    route = []
    routeReverse = []
    path = DijkstraSP(mrt, mrt.allNodesIndex[currentLocation])
    dest_stn = mrt.allNodesIndex[destination]
    routeReverse.append(mrt.getStationName(dest_stn))

    while (dest_stn != mrt.allNodesIndex[currentLocation]):
        dest_stn = path.edgeTo[dest_stn].vertex
        routeReverse.append(mrt.getStationName(dest_stn))

    while len(routeReverse) != 0:
        # print route in the reverse order
        route.append(routeReverse.pop())

    return route