from tkinter import *
from PIL import ImageTk, Image
from EdgeWeightedGraph import EdgeWeightedGraph
from DijkstraSP import DijkstraSP
import csv
import time


class GUI:
    background = 'lightgrey'
    coordinatesXY = []
    station_name = []
    station_code = []
    destination = ""
    currentLocation = ""
    route = []
    routeCircle = [None] * 122
    mainGUI = Tk(className='Journey Planner')  # Sets window name
    weighted_data = []
    timevalue = 0

    def __init__(self):
        self.readCsvCoordinates()
        self.guiInstance(self.mainGUI)

    def readCsvCoordinates(self):
        with open('mapCoordinates.csv', 'r', newline='',
                  encoding='utf-8') as savedItemsIO:  # Open savedItems.csv file (must be same directory as this program)
            for row in savedItemsIO:
                self.coordinatesXY.append(row.split(","))

        for i in range(len(self.coordinatesXY)):
            self.station_name.append(self.coordinatesXY[i][4].replace('\r\n', ""))

        with open('mrt_stations_weighted.csv', 'r', newline='',
                  encoding='utf-8') as savedItemsIO:  # Open savedItems.csv file (must be same directory as this program)
            for row in savedItemsIO:
                self.weighted_data.append(row)

    def guiInstance(self, mainGUI):
        mainGUI.geometry("1500x750+10+0")  # Sets window size
        mainGUI.configure(bg=self.background)
        mainGUI.resizable(width=False, height=False)

        map = Canvas(mainGUI, bg="white", height=750, width=1200)
        mapimage = ImageTk.PhotoImage(Image.open('mrtMap.png').resize((1200, 800)))
        self.initMap(map, mapimage)

        currentLocationTitle = Label(mainGUI, text="Current Location")
        currentLocationTitle.config(font=("MS Sans Serif", 20))
        currentLocationTitle.place(x=1230, y=10, height=50, width=250)

        currentLocation = Label(mainGUI, text="", fg='darkgreen')
        currentLocation.config(font=("Courier", 20))
        currentLocation.place(x=1230, y=60, height=50, width=250)

        currentLocationCircle = map.create_oval(0, 0, 0, 0, fill='lime')

        destinationTitle = Label(mainGUI, text="Destination")
        destinationTitle.config(font=("MS Sans Serif", 20))
        destinationTitle.place(x=1230, y=200, height=50, width=250)

        timeTitle = Label(mainGUI, text="Estimated Time")
        timeTitle.config(font=("Arial", 20))
        timeTitle.place(x=1230, y=450, height=50, width=250)

        time_taken_display = Label(mainGUI, text="")
        time_taken_display.config(font=("Courier", 20))
        time_taken_display.place(x=1230, y=500, height=50, width=250)

        destination = Label(mainGUI, text="", fg="darkred")
        destination.config(font=("Courier", 20))
        destination.place(x=1230, y=250, height=50, width=250)

        destinationLocationCircle = map.create_oval(0, 0, 0, 0, fill='red')

        instructions = Label(mainGUI,
                             text="INSTRUCTIONS\nLeft click to select current location\n Right click to select destination")
        instructions.config(font=("Arial", 13))
        instructions.place(x=1230, y=600, height=60, width=250)

        startButton = Button(mainGUI, text="START", command=lambda: [map.coords(destinationLocationCircle, 0, 0, 0, 0),
                                                                     map.coords(currentLocationCircle, 0, 0, 0, 0),
                                                                     self.displayCircles(map, time_taken_display)])
        startButton.config(font=("Arial", 30))
        startButton.place(x=1230, y=350, height=50, width=250)

        map.bind('<Button-1>', lambda event: self.onClick(event, currentLocation, currentLocationCircle, map, 1))
        map.bind('<Button-3>', lambda event: self.onClick(event, destination, destinationLocationCircle, map, 2))

        mainGUI.mainloop()  # Run the GUI

    def initMap(self, map, mapimage):
        map.place(x=10, y=10)
        map.create_image(600, 390, image=mapimage)

    def onClick(self, event, Location, LocationCircle, map, mode):
        # currentLocation.place_forget()
        xyCoords = []
        xyCoords.append(event.x - 7)
        xyCoords.append(event.y - 7)
        xyCoords.append(event.x + 7)
        xyCoords.append(event.y + 7)

        for i in range(len(self.coordinatesXY)):
            if ((event.x >= int(self.coordinatesXY[i][0]))) and (event.x <= int(self.coordinatesXY[i][2])):
                if (int(event.y) >= int(self.coordinatesXY[i][1])) and (int(event.y) <= int(self.coordinatesXY[i][3])):
                    Location.config(text=self.station_name[i])
                    if mode == 1:
                        self.currentLocation = self.coordinatesXY[i][5].replace("\r\n", "")
                    else:
                        self.destination = self.coordinatesXY[i][5].replace("\r\n", "")
                    map.coords(LocationCircle, self.coordinatesXY[i][0], self.coordinatesXY[i][1],
                               self.coordinatesXY[i][2], self.coordinatesXY[i][3])
                    break

        # self.writeCoords(xyCoords)

    def writeCoords(self, xyCoords):
        with open('mapCoordinates.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list(xyCoords))

    def displayCircles(self, map, time_taken_display):
        if self.currentLocation != "" and self.destination != "":
            mrt = EdgeWeightedGraph("mrt_stations_weighted.csv")

            route = []
            routeReverse = []
            path = DijkstraSP(mrt, mrt.allNodesIndex[str(self.currentLocation)])
            dest_stn = mrt.allNodesIndex[str(self.destination)]
            routeReverse.append(mrt.getStationName(dest_stn))

            while (dest_stn != mrt.allNodesIndex[str(self.currentLocation)]):
                dest_stn = path.edgeTo[dest_stn].vertex
                routeReverse.append(mrt.getStationName(dest_stn))

            while len(routeReverse) != 0:
                # print route in the reverse order
                route.append(routeReverse.pop())

            print(route)

            for i in range(122):
                map.delete(self.routeCircle[i])
                for x in range(len(route)):
                    if route[x] == self.coordinatesXY[i][5].replace("\r\n", ""):
                        self.routeCircle[i] = map.create_oval(int(self.coordinatesXY[i][0]),
                                                              int(self.coordinatesXY[i][1]),
                                                              int(self.coordinatesXY[i][2]),
                                                              int(self.coordinatesXY[i][3]),
                                                              fill='MAGENTA')

            self.timevalue = 0
            for i in range(len(route)):
                for j in range(len(self.weighted_data)):
                    try:
                        if route[i] in self.weighted_data[j] and route[i + 1] in self.weighted_data[j]:
                            self.timevalue = self.timevalue + int(self.weighted_data[j].split("-")[1].replace("\n", ""))
                    except:
                        pass

            time_taken_display.config(text=str(self.timevalue)+" mins")
