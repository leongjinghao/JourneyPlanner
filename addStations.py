from tkinter import *
from PIL import ImageTk, Image
import csv

class GUI:
    background = 'lightgrey'
    mainGUI = Tk(className=' Add Station App')  # Sets window name
    xyCoords = [] # store the coordinates of each point
    newStationName = StringVar() # input var for new station name
    newStationCode = StringVar() # input var for new station code
    nextStationCode = StringVar() # input var for next station code
    travelTime = IntVar() # input var for travel time
    altCol = ['white','grey25'] # alternating colours for "Existing" button
    newStations = [] # list of all new station inputs
    newStationCircle = [None] * 100 # display a max of 100 added point on gui
    newStationCircleCounter = 0 # counter to keep track on the number of points added
    isMrt = True # new station to be added is set to be a mrt by default
    existing = False # new station to be added is set to be not an existing station

    def __init__(self):
        self.guiInstance(self.mainGUI)
    
    # Function that instantiates the overall GUI
    def guiInstance(self, mainGUI):
        # Sets window size, background and its ability to be resized or not
        mainGUI.geometry("1500x750+10+0")  # Sets window size
        mainGUI.configure(bg=self.background)
        mainGUI.resizable(width=False, height=False)

        # Instantiates GUI map object
        map = Canvas(mainGUI, bg="white", height=750, width=1200)
        mapimage = ImageTk.PhotoImage(Image.open('mrtMap.png').resize((1200, 800)))
        self.initMap(map, mapimage)

        #-----------------------------------------Displays instructions for users-----------------------------------------------------
        instructions = Label(mainGUI,
                             text="INSTRUCTIONS\nLeft click to get coordinates.\nClose window after finished.")
        instructions.config(font=("Arial", 13))
        instructions.place(x=1230, y=50, height=60, width=250)
        # -------------------------------------------------------------------------------------------

        # Display a circle on the point user clicked, everytime the user clicks the circle reset to the new location
        tempCircle = map.create_oval(0, 0, 0, 0, fill='lime')
        # capture left clicks, upon clicking, onClick() method will be called
        map.bind('<Button-1>', lambda event: self.onClick(event, map, tempCircle))

        #-----------------------------------------Station Name Text Box-----------------------------------------------------
        Label(mainGUI, text="Station Name:", font=("Arial", 13)).place(x=1230, y=150)
        stnNameTextBox = Entry(mainGUI, textvariable=self.newStationName, font=("Arial", 15),width=20)
        stnNameTextBox.place(x=1230, y=170, height=35, width=250)
        # -------------------------------------------------------------------------------------------

        #-----------------------------------------Station Code Text Box-----------------------------------------------------
        Label(mainGUI, text="Station Code:", font=("Arial", 13)).place(x=1230, y=220)
        stnCodeTextBox = Entry(mainGUI, textvariable=self.newStationCode, font=("Arial", 15),width=20)
        stnCodeTextBox.place(x=1230, y=240, height=35, width=250)
        # -------------------------------------------------------------------------------------------

        #-----------------------------------------Station Code Text Box-----------------------------------------------------
        Label(mainGUI, text="Next Station Code:\n \"-\" if no next station", font=("Arial", 13)).place(x=1230, y=290)
        nextStnCodeTextBox = Entry(mainGUI, textvariable=self.nextStationCode, font=("Arial", 15),width=20)
        nextStnCodeTextBox.place(x=1230, y=330, height=35, width=250)
        # -------------------------------------------------------------------------------------------

        #-----------------------------------------Travel Time Text Box-----------------------------------------------------
        Label(mainGUI, text="Travel Time:", font=("Arial", 13)).place(x=1230, y=380)
        travelTimeTextBox = Entry(mainGUI, textvariable=self.travelTime, font=("Arial", 15),width=20)
        travelTimeTextBox.place(x=1230, y=400, height=35, width=250)
        # -------------------------------------------------------------------------------------------

        #-----------------------------------------MRT Station Check Box-----------------------------------------------------
        Label(mainGUI, text="Is it an MRT station?", bg=self.background, font=("Arial", 13)).place(x=1230, y=500)
        isMrt = BooleanVar()
        isMrtRadioButton = Radiobutton(mainGUI, text="Yes", variable=isMrt, value=True, bg=self.background)
        isMrtRadioButton.place(x=1230, y=550)

        isMrtRadioButton = Radiobutton(mainGUI, text="No", variable=isMrt, value=False, bg=self.background)
        isMrtRadioButton.place(x=1300, y=550)
        # -------------------------------------------------------------------------------------------

        #-----------------------------------------"Existing" Selection Box-----------------------------------------------------
        existingButton = Button(mainGUI, text="Existing", command=lambda: self.setExisting(existingButton))
        existingButton.config(font=("Arial", 13), bg='white')
        existingButton.place(x=1230, y=450, height=30, width=70)
        # -------------------------------------------------------------------------------------------

        #-----------------------------------------Confirmation Button-----------------------------------------------------
        confirmButton = Button(mainGUI, text="Add Station", 
                                command=lambda: self.storeCoords(map, self.xyCoords, self.newStationName, 
                                                                      self.newStationCode, self.nextStationCode, 
                                                                      self.travelTime, self.existing, isMrt.get()))
        confirmButton.config(font=("Arial", 30))
        confirmButton.place(x=1230, y=600, height=50, width=250)
        # -------------------------------------------------------------------------------------------

        #-----------------------------------------Abort Button-----------------------------------------------------
        abortButton = Button(mainGUI, text="Abort All Changes", command=lambda: self.abortAll())
        abortButton.config(font=("Arial", 20), fg = 'red')
        abortButton.place(x=1230, y=690, height=50, width=250)
        # -------------------------------------------------------------------------------------------

        # Run the GUI
        mainGUI.mainloop()

    # Method that places the Singapore MRT map onto the GUI
    def initMap(self, map, mapimage):
        map.place(x=10, y=10)
        map.create_image(600, 390, image=mapimage)

    # Run this method upon clicking on the map
    def onClick(self, event, map, LocationCircle):
        xyCoords = []
        xyCoords.append(event.x - 7)
        xyCoords.append(event.y - 7)
        xyCoords.append(event.x + 7)
        xyCoords.append(event.y + 7)

        LocationCircle = map.coords(LocationCircle, xyCoords[0], xyCoords[1], xyCoords[2], xyCoords[3])
        
        self.xyCoords = xyCoords

    # Method that stores all the new station inputs gathered, for each new station, inside the newStation[] list
    def storeCoords(self, map, xyCoords, stnName, stnCode, nextStnCode, travelTime, existing, isMrt):
        # show added station on gui
        self.newStationCircle[self.newStationCircleCounter] = \
            map.create_oval(xyCoords[0], xyCoords[1], xyCoords[2], xyCoords[3], fill='MAGENTA')
        
        # store the coordinates inside newStations list
        self.newStations.append([xyCoords[0], xyCoords[1], xyCoords[2], xyCoords[3], 
                                    stnName.get(), stnCode.get(), nextStnCode.get(), 
                                    travelTime.get(), existing, isMrt])

    # Method to invert the "Existing" value on click, alternate the colour of button to indicate the current value of "Existing"
    def setExisting(self, existingButton):
        # invert boolean value on click
        self.existing = not(self.existing)
        # swap alternate colour on every click
        self.altCol[0], self.altCol[1] = self.altCol[1], self.altCol[0]
        existingButton.config(bg=self.altCol[0])
    
    # Method to quit the Application
    def abortAll(self):
        quit()

# main() call the GUI for Add Station App
# open the GUI for Add Station Application
addStationApp = GUI()

# after the GUI window is closed, proceed with following operations
print(addStationApp.newStations)
# for each station's inputs on GUI
for station in addStationApp.newStations:
    # if it is a non existing station add them in the following csv files
    if (station[8] == False):
        with open('mapCoordinates.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list(station[0:6]))
    
        with open('all_unique_stations.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list([station[5]]))
    
    # if there is a new edge to add
    if (station[6] != "-"):
        # add the edge to the mrt_stations_weighted.csv regarless if it includes existing station
        with open('mrt_stations_weighted.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list(["{0}: {1} - {2}".format(station[5], station[6], station[7])]))

    # if the station input is not a mrt station, need to add the map coordinates inside bus_station.csv
    if (station[9] == False):
        with open('bus_stations.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([station[5], station[4], station[0], station[1], station[2], station[3]])

