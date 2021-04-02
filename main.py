from Graph import Graph
from tkinter import *
from GUI import GUI
from EdgeWeightedDigraph import EdgeWeightedDigraph

#mrt = Graph("mrt_stations.txt")
#print(mrt.shortest_path("EW33", "EW30"))


mainGUI = Tk(className='Journey Planner')  # Sets window name
GUI(mainGUI)



#mrt = EdgeWeightedDigraph("mrt_stations_weighted.txt")
#allEdges = mrt.getAllEdges()
#print(allEdges)
#for edge in allEdges:
    #print(edge.toString())