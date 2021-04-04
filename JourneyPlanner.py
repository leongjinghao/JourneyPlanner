from EdgeWeightedGraph import EdgeWeightedGraph
from DijkstraSP import DijkstraSP

def computeRoute(currentLocation, destination):
    # initialise the edge weighted graph
    mrt = EdgeWeightedGraph("mrt_stations_weighted.csv")

    route = []
    routeReverse = []

    # search for the shortest path to all location from current location using dijkstra algo
    path = DijkstraSP(mrt, mrt.allNodesIndex[currentLocation])
    # retrieve the index for the destination location (station)
    dest_stn = mrt.allNodesIndex[destination]
    # station pointer used to traverse the path
    stn_ptr = dest_stn
    # retrieving the route by traversing the destination first and subsequently to current location
    # hence append destination (station) first
    routeReverse.append(mrt.getStationName(dest_stn))

    # while the station pointer is not at current lcation (station), continue traversing
    while (stn_ptr != mrt.allNodesIndex[currentLocation]):
        # set station pointer to the previous station
        stn_ptr = path.edgeTo[stn_ptr].vertex
        # append the station pointer to the reverse route list
        routeReverse.append(mrt.getStationName(stn_ptr))

    # while reverse route is not empty
    while len(routeReverse) != 0:
        # append to route in the reverse order using stack pop property
        route.append(routeReverse.pop())

    # retrieve the estimated time to the destination location (station)
    timeToDest = path.timeTo[dest_stn]
    # check
    # print("Time to {0}: {1} min".format(destination, path.timeTo[mrt.allNodesIndex[destination]]))
    return [route, timeToDest]