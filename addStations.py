from tkinter import *
from PIL import ImageTk, Image
import csv

class GUI:
    background = 'lightgrey'
    mainGUI = Tk(className=' Add Station App')  # Sets window name
    xyCoords = []
    newStationName = StringVar()
    newStationCode = StringVar()
    nextStationCode = StringVar()
    travelTime = IntVar()
    existing = False
    altCol = ['white','grey25']
    newStations = []
    newStationCircle = [None] * 100 # display a max of 100 added point on gui
    newStationCircleCounter = 0

    def __init__(self):
        self.guiInstance(self.mainGUI)
    
    def guiInstance(self, mainGUI):
        mainGUI.geometry("1500x750+10+0")  # Sets window size
        mainGUI.configure(bg=self.background)
        mainGUI.resizable(width=False, height=False)

        map = Canvas(mainGUI, bg="white", height=750, width=1200)
        mapimage = ImageTk.PhotoImage(Image.open('mrtMap.png').resize((1200, 800)))
        self.initMap(map, mapimage)

        instructions = Label(mainGUI,
                             text="INSTRUCTIONS\nLeft click to get coordinates.\nClose window after finished.")
        instructions.config(font=("Arial", 13))
        instructions.place(x=1230, y=50, height=60, width=250)

        tempCircle = map.create_oval(0, 0, 0, 0, fill='lime')

        map.bind('<Button-1>', lambda event: self.onClick(event, map, tempCircle))

        Label(mainGUI, text="Station Name:", font=("Arial", 13)).place(x=1230, y=150)
        stnNameTextBox = Entry(mainGUI, textvariable=self.newStationName, font=("Arial", 15),width=20)
        stnNameTextBox.place(x=1230, y=170, height=35, width=250)

        Label(mainGUI, text="Station Code:", font=("Arial", 13)).place(x=1230, y=220)
        stnCodeTextBox = Entry(mainGUI, textvariable=self.newStationCode, font=("Arial", 15),width=20)
        stnCodeTextBox.place(x=1230, y=240, height=35, width=250)

        Label(mainGUI, text="Next Station Code:\n \"-\" if no next station", font=("Arial", 13)).place(x=1230, y=290)
        nextStnCodeTextBox = Entry(mainGUI, textvariable=self.nextStationCode, font=("Arial", 15),width=20)
        nextStnCodeTextBox.place(x=1230, y=330, height=35, width=250)

        Label(mainGUI, text="Travel Time:", font=("Arial", 13)).place(x=1230, y=380)
        travelTimeTextBox = Entry(mainGUI, textvariable=self.travelTime, font=("Arial", 15),width=20)
        travelTimeTextBox.place(x=1230, y=400, height=35, width=250)

        existingButton = Button(mainGUI, text="Existing", command=lambda: self.setExisting(existingButton))
        existingButton.config(font=("Arial", 13), bg='white')
        existingButton.place(x=1230, y=450, height=30, width=70)

        confirmButton = Button(mainGUI, text="Add Station", 
                                command=lambda: self.storeCoords(map, self.xyCoords, self.newStationName, 
                                                                      self.newStationCode, self.nextStationCode, 
                                                                      self.travelTime, self.existing))
        confirmButton.config(font=("Arial", 30))
        confirmButton.place(x=1230, y=500, height=50, width=250)

        abortButton = Button(mainGUI, text="Abort All Changes", command=lambda: self.abortAll())
        abortButton.config(font=("Arial", 20), fg = 'red')
        abortButton.place(x=1230, y=650, height=50, width=250)

        mainGUI.mainloop()  # Run the GUI

    def initMap(self, map, mapimage):
        map.place(x=10, y=10)
        map.create_image(600, 390, image=mapimage)

    def onClick(self, event, map, LocationCircle):
        xyCoords = []
        xyCoords.append(event.x - 7)
        xyCoords.append(event.y - 7)
        xyCoords.append(event.x + 7)
        xyCoords.append(event.y + 7)

        LocationCircle = map.coords(LocationCircle, xyCoords[0], xyCoords[1], xyCoords[2], xyCoords[3])
        
        self.xyCoords = xyCoords

    def storeCoords(self, map, xyCoords, stnName, stnCode, nextStnCode, travelTime, existing):
        # show added station on gui
        self.newStationCircle[self.newStationCircleCounter] = \
            map.create_oval(xyCoords[0], xyCoords[1], xyCoords[2], xyCoords[3], fill='MAGENTA')
        
        # store the coordinates inside newStations list
        self.newStations.append([xyCoords[0], xyCoords[1], xyCoords[2], xyCoords[3], 
                                    stnName.get(), stnCode.get(), nextStnCode.get(), 
                                    travelTime.get(), existing])

    def setExisting(self, existingButton):
        # invert boolean value on click
        self.existing = not(self.existing)
        # swap alternate colour on every click
        self.altCol[0], self.altCol[1] = self.altCol[1], self.altCol[0]
        existingButton.config(bg=self.altCol[0])
    
    def abortAll(self):
        quit()

# main() call the GUI for Add Station App
addStationApp = GUI()
print(addStationApp.newStations)
# for each station's inputs on GUI
for station in addStationApp.newStations:
    # if it is a non existing station add them in the following csv files
    if (station[8] == False):
        with open('mapCoordinates(test).csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list(station[0:6]))
    
        with open('all_unique_stations(test).csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list([station[5]]))
    
    # if there is a new edge to add
    if (station[6] != "-"):
        # add the edge to the mrt_stations_weighted.csv regarless if it includes existing station
        with open('mrt_stations_weighted(test).csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list(["{0}: {1} - {2}".format(station[5], station[6], station[7])]))