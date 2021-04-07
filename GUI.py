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
    station_code = []
    destination = ""
    currentLocation = ""
    route = []
    routeCircle = []  # Stores GUI circle objects that represents the routes
    breakdownCircle = []  # Stores GUI circle objects that represents a broken down station
    mainGUI = Tk(className='Journey Planner')  # Sets window name
    brokedownstations = []

    def __init__(self):
        self.readCsvCoordinates()
        self.routeCircle = [None] * len(self.coordinatesXY)
        self.breakdownCircle = [None] * len(self.brokedownstations[0])
        self.guiInstance(self.mainGUI)

    # Function to read data from csv files
    def readCsvCoordinates(self):
        with open('mapCoordinates.csv', 'r', newline='',
                  encoding='utf-8') as savedItemsIO:  # Open savedItems.csv file (must be same directory as this program)
            for row in savedItemsIO:
                self.coordinatesXY.append(row.split(","))

        for i in range(len(self.coordinatesXY)):
            self.station_name.append(self.coordinatesXY[i][4].replace('\r\n', ""))

        with open('stn_breakdown.csv', 'r', newline='',
                  encoding='utf-8') as savedItemsIO:  # Open savedItems.csv file (must be same directory as this program)
            for row in savedItemsIO:
                self.brokedownstations.append(row.split(","))

    # Function that instantiates the overall GUI
    def guiInstance(self, mainGUI):
        mainGUI.geometry("1500x750+10+0")  # Sets window size
        mainGUI.configure(bg=self.background)
        mainGUI.resizable(width=False, height=False)

        map = Canvas(mainGUI, bg="white", height=750, width=1200)
        mapimage = ImageTk.PhotoImage(Image.open('mrtMap.png').resize((1200, 800)))
        self.initMap(map, mapimage)

        map2 = Canvas(mainGUI, bg="white", height=130, width=250)
        map2.place(x=1230, y=550)

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

        currentLocationTitle = Label(mainGUI, text="Current Location")
        currentLocationTitle.config(font=("MS Sans Serif", 20))
        currentLocationTitle.place(x=1230, y=10, height=50, width=250)

        currentLocation = Label(mainGUI, text="", fg='darkgreen')
        currentLocation.config(font=("Courier", 20))
        currentLocation.place(x=1230, y=60, height=50, width=250)

        currentLocationCircle = map.create_oval(0, 0, 0, 0, fill='lime')

        destinationTitle = Label(mainGUI, text="Destination")
        destinationTitle.config(font=("MS Sans Serif", 20))
        destinationTitle.place(x=1230, y=150, height=50, width=250)

        timeTitle = Label(mainGUI, text="Estimated Time")
        timeTitle.config(font=("Arial", 20))
        timeTitle.place(x=1230, y=350, height=50, width=250)

        time_taken_display = Label(mainGUI, text="")
        time_taken_display.config(font=("Courier", 20))
        time_taken_display.place(x=1230, y=400, height=50, width=250)

        destination = Label(mainGUI, text="", fg="darkred")
        destination.config(font=("Courier", 20))
        destination.place(x=1230, y=200, height=50, width=250)

        destinationLocationCircle = map.create_oval(0, 0, 0, 0, fill='red')

        instructions = Label(mainGUI,
                             text="INSTRUCTIONS\nLeft click to select current location\n Right click to select destination")
        instructions.config(font=("Arial", 13))
        instructions.place(x=1230, y=480, height=60, width=250)

        startButton = Button(mainGUI, text="START", command=lambda: [map.coords(destinationLocationCircle, 0, 0, 0, 0),
                                                                     map.coords(currentLocationCircle, 0, 0, 0, 0),
                                                                     self.displayCircles(map, time_taken_display)])
        startButton.config(font=("Arial", 30))
        startButton.place(x=1230, y=270, height=50, width=250)

        map.bind('<Button-1>', lambda event: self.onClick(event, currentLocation, currentLocationCircle, map, 1))
        map.bind('<Button-3>', lambda event: self.onClick(event, destination, destinationLocationCircle, map, 2))

        self.displayBreakdown(map)

        mainGUI.mainloop()  # Run the GUI

    # Function that places the Singapore MRT map onto the GUI
    def initMap(self, map, mapimage):
        map.place(x=10, y=10)
        map.create_image(600, 390, image=mapimage)

    # Run this function upon clicking on the map
    def onClick(self, event, Location, LocationCircle, map, mode):
        xyCoords = []
        xyCoords.append(event.x - 7)
        xyCoords.append(event.y - 7)
        xyCoords.append(event.x + 7)
        xyCoords.append(event.y + 7)

        for i in range(len(self.coordinatesXY)):
            if ((event.x >= int(self.coordinatesXY[i][0]))) and (event.x <= int(self.coordinatesXY[i][2])):
                if (int(event.y) >= int(self.coordinatesXY[i][1])) and (
                        int(event.y) <= int(self.coordinatesXY[i][3])):

                    for j in range(len(
                            self.brokedownstations[0])):  # Check if station selected by user is a broken down station
                        if self.brokedownstations[0][j].replace(" ", "") == self.coordinatesXY[i][5].replace("\r\n",
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


    def writeCoords(self, xyCoords):
        with open('mapCoordinates.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list(xyCoords))

    # Function that displays the route from user's current location to destination on the map
    def displayCircles(self, map, time_taken_display):
        route = []
        timeToDest = 0
        if self.currentLocation != "" and self.destination != "":
            try:
                returnBag = computeRoute(str(self.currentLocation), str(self.destination))
                route = returnBag[0]
                timeToDest = returnBag[1]
            except:
                ctypes.windll.user32.MessageBoxW(0, "No route to your destination.", "Error", 1)

            print(route)

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

    # Function to display unavailable stations
    def displayBreakdown(self, map):
        for i in range(len(self.brokedownstations[0])):
            map.delete(self.breakdownCircle[i])
            for j in range(len(self.coordinatesXY)):
                if self.brokedownstations[0][i].replace(" ", "") == self.coordinatesXY[j][5].replace("\r\n", ""):
                    self.breakdownCircle[i] = map.create_oval(int(self.coordinatesXY[j][0]) - 5,
                                                              int(self.coordinatesXY[j][1]) - 5,
                                                              int(self.coordinatesXY[j][2]) + 5,
                                                              int(self.coordinatesXY[j][3]) + 5,
                                                              fill='BLACK')
