import json
from ShortestPath import shortest_path

stations = json.load(open('mrt_stations.json'))
route = shortest_path(stations,"ew28", "ne14")
print(route)