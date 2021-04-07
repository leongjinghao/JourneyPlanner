from tkinter import *
from PIL import ImageTk, Image
from JourneyPlanner import computeRoute
import csv
import ctypes


# GUI class
class GUI:
    background = 'lightgrey'
    coordinatesXY = []
    station_name = []
    destination = ""
    currentLocation = ""
    route = []
    routeCircle = []  # Stores GUI circle objects that represents the routes
    breakdownCircle = []  # Stores GUI circle objects that represents unavailable stations
    busCircle = []  # Stores GUI circle objects that represents bus stations
    mainGUI = Tk(className='Journey Planner')  # Sets window name
    brokedownstations = []
    bus_stations = []

    def __init__(self):
        self.readCsvCoordinates()
        self.routeCircle = [None] * len(self.coordinatesXY)
        self.breakdownCircle = [None] * len(self.brokedownstations)
        self.busCircle = [None] * len(self.bus_stations)
        self.guiInstance(self.mainGUI)

    # Method to read data from csv files
    def readCsvCoordinates(self):
        # Reads mapCoordinates.csv file (must be same directory as this program) and store station details into coordinatesXY (list)
        with open('mapCoordinates.csv', 'r+', newline='',
                  encoding='utf-8') as savedItemsIO:
            for row in savedItemsIO:
                self.coordinatesXY.append(row.split(","))

        # Store station name in coordinatesXY[i][4] into station_name(list)
        for i in range(len(self.coordinatesXY)):
            self.station_name.append(self.coordinatesXY[i][4].replace('\r\n', ""))

        # Reads stn_breakdown.csv file (must be same directory as this program) and store unavailable stations into brokedownstations (list)
        with open('stn_breakdown.csv', 'r+', newline='',
                  encoding='utf-8') as savedItemsIO:
            for row in savedItemsIO:
                self.brokedownstations = row.split(",")

        # Reads bus_stations.csv file (must be same directory as this program) and store bus stations into bus_stations (list)
        with open('bus_stations.csv', 'r+', newline='',
                  encoding='utf-8') as savedItemsIO:
            for row in savedItemsIO:
                self.bus_stations.append(row.split(","))

    # Function that instantiates the overall GUI
    def guiInstance(self, mainGUI):
        # Sets window size, background and its ability to be resized or not
        mainGUI.geometry("1500x750+10+0")
        mainGUI.configure(bg=self.background)
        mainGUI.resizable(width=False, height=False)

        # Instantiates GUI map object
        map = Canvas(mainGUI, bg="white", height=750, width=1200)
        mapimage = ImageTk.PhotoImage(Image.open('mrtMap.png').resize((1200, 800)))
        self.initMap(map, mapimage)

        self.displayBusStations(map)

        map2 = Canvas(mainGUI, bg="white", height=130, width=250)
        map2.place(x=1230, y=550)

        # ------------------------Displays Legend--------------------------------
        legendLabel = Label(map2, text="Legend", bg="white")
        legendLabel.config(font=("MS Sans Serif", 15))
        legendLabel.place(x=0, y=0, height=50, width=250)

        map2.create_oval(30, 50, 40, 60, fill="Black")
        map2.create_oval(30, 70, 40, 80, fill="lime")
        map2.create_oval(30, 90, 40, 100, fill="red")
        map2.create_oval(30, 110, 40, 120, fill="magenta")

        legendLabel = Label(map2, text="Unavailable Stations", bg="white")
        legendLabel.config(font=("MS Sans Serif", 10))
        legendLabel.place(x=50, y=45, height=20, width=150)

        legendLabel = Label(map2, text="Current Location", bg="white")
        legendLabel.config(font=("MS Sans Serif", 10))
        legendLabel.place(x=50, y=65, height=20, width=150)

        legendLabel = Label(map2, text="Destination", bg="white")
        legendLabel.config(font=("MS Sans Serif", 10))
        legendLabel.place(x=50, y=85, height=20, width=150)

        legendLabel = Label(map2, text="Route", bg="white")
        legendLabel.config(font=("MS Sans Serif", 10))
        legendLabel.place(x=50, y=105, height=20, width=150)
        # -------------------------------------------------------------

        # ------------------------Displays Current Location Interface--------------------------------
        currentLocationTitle = Label(mainGUI, text="Current Location")
        currentLocationTitle.config(font=("MS Sans Serif", 20))
        currentLocationTitle.place(x=1230, y=10, height=50, width=250)

        currentLocation = Label(mainGUI, text="", fg='darkgreen')
        currentLocation.config(font=("Courier", 20))
        currentLocation.place(x=1230, y=60, height=50, width=250)
        # -------------------------------------------------------------------------------------------

        #Instantiates tkinter object that shows user's current location in a form of a green circle
        currentLocationCircle = map.create_oval(0, 0, 0, 0, fill='lime')

        # ------------------------Displays Destination Interface--------------------------------
        destinationTitle = Label(mainGUI, text="Destination")
        destinationTitle.config(font=("MS Sans Serif", 20))
        destinationTitle.place(x=1230, y=150, height=50, width=250)

        destination = Label(mainGUI, text="", fg="darkred")
        destination.config(font=("Courier", 20))
        destination.place(x=1230, y=200, height=50, width=250)
        # -------------------------------------------------------------------------------------------

        # Instantiates tkinter object that shows user's destination in a form of a green circle
        destinationLocationCircle = map.create_oval(0, 0, 0, 0, fill='red')

        # ------------------------Time Taken Interface--------------------------------
        timeTitle = Label(mainGUI, text="Estimated Time")
        timeTitle.config(font=("Arial", 20))
        timeTitle.place(x=1230, y=350, height=50, width=250)

        time_taken_display = Label(mainGUI, text="")
        time_taken_display.config(font=("Courier", 20))
        time_taken_display.place(x=1230, y=400, height=50, width=250)
        # -------------------------------------------------------------------------------------------

        #-----------------------------------------Displays instructions for users-----------------------------------------------------
        instructions = Label(mainGUI,
                             text="INSTRUCTIONS\nLeft click to select current location\n Right click to select destination")
        instructions.config(font=("Arial", 13))
        instructions.place(x=1230, y=480, height=60, width=250)
        # -------------------------------------------------------------------------------------------

        #Displays start button. Upon clicking it, displayCircles() method will be called
        startButton = Button(mainGUI, text="START", command=lambda: [map.coords(destinationLocationCircle, 0, 0, 0, 0),
                                                                     map.coords(currentLocationCircle, 0, 0, 0, 0),
                                                                     self.displayCircles(map, time_taken_display)])
        startButton.config(font=("Arial", 30))
        startButton.place(x=1230, y=270, height=50, width=250)

        #If user clicks left mouse button on a station, set it as the current location
        map.bind('<Button-1>', lambda event: self.onClick(event, currentLocation, currentLocationCircle, map, 1))
        # If user clicks right mouse button on a station, set it as the destination
        map.bind('<Button-3>', lambda event: self.onClick(event, destination, destinationLocationCircle, map, 2))

        self.displayBreakdown(map)

        # Run the GUI
        mainGUI.mainloop()

    # Method that places the Singapore MRT map onto the GUI
    def initMap(self, map, mapimage):
        map.place(x=10, y=10)
        map.create_image(600, 390, image=mapimage)

    # Run this method upon clicking on the map
    def onClick(self, event, Location, LocationCircle, map, mode):
        xyCoords = []
        xyCoords.append(event.x - 7)
        xyCoords.append(event.y - 7)
        xyCoords.append(event.x + 7)
        xyCoords.append(event.y + 7)

        # If coordinates of user's click location on the map matches the coordinates stored in coordinatesXY (list), display current location or destination
        for i in range(len(self.coordinatesXY)):
            if ((event.x >= int(self.coordinatesXY[i][0]))) and (event.x <= int(self.coordinatesXY[i][2])):
                if (int(event.y) >= int(self.coordinatesXY[i][1])) and (
                        int(event.y) <= int(self.coordinatesXY[i][3])):

                    for j in range(len(
                            self.brokedownstations)):  # Check if station selected by user is a broken down station
                        if self.brokedownstations[j].replace(" ", "") == self.coordinatesXY[i][5].replace("\r\n",
                                                                                                          ""):
                            mode = 3

                    if mode == 1:
                        self.currentLocation = self.coordinatesXY[i][5].replace("\r\n", "")
                        map.coords(LocationCircle, self.coordinatesXY[i][0], self.coordinatesXY[i][1],
                                   self.coordinatesXY[i][2], self.coordinatesXY[i][3])
                        Location.config(text=self.station_name[i])
                    elif mode == 2:
                        self.destination = self.coordinatesXY[i][5].replace("\r\n", "")
                        map.coords(LocationCircle, self.coordinatesXY[i][0], self.coordinatesXY[i][1],
                                   self.coordinatesXY[i][2], self.coordinatesXY[i][3])
                        Location.config(text=self.station_name[i])
                    else:
                        pass
                    break

    # Method that displays the route from user's current location to destination on the map
    def displayCircles(self, map, time_taken_display):
        route = []
        timeToDest = 0
        if self.currentLocation != "" and self.destination != "":
            try:
                # computeRoute returns 2 items, route[] (list) and timeToDest (int)
                returnBag = computeRoute(str(self.currentLocation), str(self.destination))
                route = returnBag[0]
                timeToDest = returnBag[1]
            except:
                # If no route from user's current location to destination, an error will occur. This error will be caught and a message will display to users, telling them that there is no route to their destination.
                ctypes.windll.user32.MessageBoxW(0, "No route to your destination.", "Error", 1)

            print(route)

            # Displays route in a form of pink circles
            for i in range(len(self.coordinatesXY)):
                map.delete(self.routeCircle[i])
                for x in range(len(route)):
                    if route[x] == self.coordinatesXY[i][5].replace("\r\n", ""):
                        self.routeCircle[i] = map.create_oval(int(self.coordinatesXY[i][0]),
                                                              int(self.coordinatesXY[i][1]),
                                                              int(self.coordinatesXY[i][2]),
                                                              int(self.coordinatesXY[i][3]),
                                                              fill='MAGENTA')

            time_taken_display.config(text=str(timeToDest) + " mins")

    # Method to display unavailable stations
    def displayBreakdown(self, map):
        for i in range(len(self.brokedownstations)):
            map.delete(self.breakdownCircle[i])
            for j in range(len(self.coordinatesXY)):
                if self.brokedownstations[i].replace(" ", "") == self.coordinatesXY[j][5].replace("\r\n", ""):
                    self.breakdownCircle[i] = map.create_oval(int(self.coordinatesXY[j][0]) - 5,
                                                              int(self.coordinatesXY[j][1]) - 5,
                                                              int(self.coordinatesXY[j][2]) + 5,
                                                              int(self.coordinatesXY[j][3]) + 5,
                                                              fill='BLACK')

    # Method to display bus stations
    def displayBusStations(self, map):
        for i in range(len(self.bus_stations)):
            map.delete(self.busCircle[i])
            for j in range(len(self.coordinatesXY)):
                if self.bus_stations[i][0] == self.coordinatesXY[j][5].replace("\r\n", ""):
                    self.busCircle[i] = map.create_oval(int(self.coordinatesXY[j][0]) + 2,
                                                        int(self.coordinatesXY[j][1]) + 2,
                                                        int(self.coordinatesXY[j][2]) - 2,
                                                        int(self.coordinatesXY[j][3]) - 2,
                                                        fill='ORANGE')

            legendLabel = Label(map, text=self.bus_stations[i][1], bg="white")
            legendLabel.config(font=("Arial", 5, 'bold'))
            legendLabel.place(x=int(self.bus_stations[i][2]) + 15, y=int(self.bus_stations[i][3]), height=15,
                              width=len(self.bus_stations[i][1]) * 4)
