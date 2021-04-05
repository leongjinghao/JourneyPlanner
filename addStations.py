from tkinter import *
from PIL import ImageTk, Image
import csv

class GUI:
    background = 'lightgrey'
    mainGUI = Tk(className='Journey Planner')  # Sets window name
    xyCoords = []

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
        instructions.place(x=1230, y=100, height=60, width=250)

        newStationCircle = map.create_oval(0, 0, 0, 0, fill='lime')

        map.bind('<Button-1>', lambda event: self.onClick(event, map, newStationCircle))

        confirmButton = Button(mainGUI, text="Add Station", command=lambda: self.writeCoords(self.xyCoords))
        confirmButton.config(font=("Arial", 30))
        confirmButton.place(x=1230, y=350, height=50, width=250)

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
        #self.writeCoords(xyCoords)

    def writeCoords(self, xyCoords):
        with open('new_station.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(list(xyCoords))

GUI()
print("I can do more stuff after GUI")