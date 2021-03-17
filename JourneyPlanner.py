import json
from ShortestPath import shortest_path

stations = json.load(open('mrt_stations.json'))
route = shortest_path(stations,"ns10","ew15")
print(route)