import turtle
import tkinter
import tkinter.colorchooser
import tkinter.filedialog
import xml.dom.minidom

class GoToCommand:
    def __init__(self, x, y, width=1, color="black"):
        self.x = x
        self.y = y
        self.width = width
        self.color = color
    def draw (self, turtle) :
        turtle.width(self.width)
        turtle.pencolor(self.color)
        turtle.goto(self.x, self.y)

    def __str__(self):
        return '<Command_x="'+ str(self.x) + '"_y="'+ str(self.y) + \
               '" width="' + str(self.width) \
               + '" color ="' + self.color + '">GoTo</Command>'

class CircleCommand:
    def __init__ (self ,radius ,width =1 ,color="black"):
        self.radius = radius
        self.width = width
        self.color = color

    def draw (self, turtle) :
         turtle.width(self.width)
         turtle.pencolor(self.color)
         turtle.circle(self.radius)

    def __str__ (self) :
        return '<Command_radius ="' + str(self.radius) + '"_width="' + \
               str(self.width) + '"_color ="' + self.color + '">Circle</Command>'

class BeginFillCommand:
    def __init__ (self , color):
        self.color = color

    def draw (self, turtle):
        turtle.fillcolor(self.color)
        turtle.begin_fill()

    def __str__ (self):
         return '<Command_color ="' + self.color + '">BeginFill</Command>'

class EndFillCommand :
   def __init__ (self):
       pass

   def draw(self, turtle) :
       turtle.end_fill()

   def __str__(self) :
        return "<Command>EndFill</Command>"

class PenUpCommand:
   def __init__(self):
        pass

   def draw (self, turtle):
        turtle.penup( )

   def __str__(self):
         return "<Command>PenUp</Command>"

class PenDownCommand:
   def __init__ (self):
        pass
   def draw (self, turtle):
        turtle.pendown( )

   def __str__ (self):
        return "<Command>PenDown</Command>"

class PyList:
   def __init__(self):
       self.gcList = []

   def append(self, item):
       self.gcList = self.gcList + [item]

   def removeLast(self):
       self.gcList = self.gcList[:-1]

   def __iter__(self):
       for c in self.gcList:
            yield c
   def __len__(self) :
       return len(self.gcList)

#drawingapp. class inherits from frame class
class DrawingApplication(tkinter.Frame):
    def __init__ (self, master=None):
        super().__init__(master)
        self.pack()
        self.buildWindow()
        self.graphicsCommands = PyList()

    #this method is called to create all widgets, place them in GUI and defines event handlers
    def buildWindow(self):
        #master is root window
        self.master.title("Draw")
        bar = tkinter.Menu(self.master) #creating menu bar
        fileMenu = tkinter.Menu(bar, tearoff = 0) #tearoff=0 means menu can't be separated from the window

        def newWindow():
            theTurtle.clear()
            theTurtle.penup()
            theTurtle.goto()
            theTurtle.pendown()
            screen.update()
            screen.listen()
            self.graphicsCommands = PyList()

        fileMenu.add_command(label="New", command=newWindow)

        #the parse fun. add content of xml file to the sequence.
        def parse(filename):
            xmldoc = xml.dom.minidom.parse(filename)
            graphicsCommandsElement = xmldoc.getElementsByTagName("GraphicsCommands")[0]
            graphicsCommands = graphicsCommandsElement.getElementsByTagname("Command")
            for commandElement in graphicsCommands:
                print(type(commandElement))
                command = commandElement.firstChild.data.strip()
                attr = commandElement.attributes
                if command == "GoTo":
                    x = float(attr["x"].value)
                    y = float(attr["y"].value)
                    width = float(attr["width"].value)
                    color = attr["color"].value.strip()
                    cmd = GoToCommand(x, y, width, color)

                elif command == "Circle":
                    radius = float(attr["radius"].value)
                    width = float(attr["width"].value)
                    color = attr["color"].value.strip()
                    cmd = CircleCommand(radius,width,color)

                elif command == "BeginFill":
                    color = attr["color"].value.strip()
                    cmd = BeginFillCommand(color)

                elif command == "EndFill":
                    cmd = EndFillCommand()

                elif command == "PenUp":
                    cmd = PenUpCommand()

                elif command == "PenDown":
                    cmd = PenDownCommand()

                else:
                    raise RuntimeError("Unknown_Command:_ " + command)

                self.graphicsCommands.append(cmd)

        def loadFile():
             filename = tkinter.filedialog.askopenfilename(title = "Select_a_Graphics_File")
             newWindow()
             self.graphicsCommands = PyList()

             #calling parse will read comm. from file
             parse(filename)

             for cmd in self.graphicsCommands:
                 cmd.draw(theTurtle)

             screen.update()

        fileMenu.add_command(label="Load...", command=loadFile)

        def addToFile():
             filename = tkinter.filedialog.askopenfilename(title = "Select_a_Graphics_File")
             theTurtle.penup()
             theTurtle.goto(0,0)
             theTurtle.pendown()
             theTurtle.pencolor('#000')
             theTurtle.fillcolor('#000')
             cmd = PenUpCommand()
             self.graphicsCommands.append(cmd)
             cmd = GoToCommand(0,0,1,"#000")
             self.graphicsCommands.append(cmd)
             cmd = PenDownCommand()
             self.graphicsCommands.append(cmd)
             screen.update()
             parse(filename)

             for cmd in self.graphicsCommands:
                 cmd.draw(theTurtle)
             
             screen.update()
             
        fileMenu.add_command(label="Load_Into...", command=addToFile)

        def write(filename):
             file = open(filename, "w")
             file.write('<?xml_version="1.0"_encoding="UTF-8"_standalone="no"_?>\n')
             file.write('<GraphicsCommands>\n')
             for cmd in self.graphicsCommands:
                 file.write('___'+str(cmd)+"\n")
             file.write('</GraphicsCommands>\n')
             file.close()
        def saveFile():
             filename = tkinter.filedialog.asksaveasfilename(title = "Save_picture_as..")    
             write(filename)
        fileMenu.add_command(label="Save_As...", command=saveFile)
        fileMenu.add_command(label="Exit",command=self.master.quit)
        bar.add_cascade(label="File",menu=fileMenu)
        # This tells the root window to display the newly created menu bar.
        self.master.config(menu=bar)

         # Here several widgets are created. The canvas is the drawing area on
         # the left side of the window.
        canvas = tkinter.Canvas(self,width=600,height=600)
        canvas.pack(side=tkinter.LEFT)

        theTurtle = turtle.RawTurtle(canvas)
    
        theTurtle.shape("circle")
        screen = theTurtle.getscreen()

        screen.tracer(0)
        sideBar = tkinter.Frame(self,padx=5,pady=5)
        sideBar.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)

         # This is a label widget. Packing it puts it at the top of the sidebar.
        pointLabel = tkinter.Label(sideBar,text="Width")
        pointLabel.pack()

        widthSize = tkinter.StringVar()
        widthEntry = tkinter.Entry(sideBar,textvariable=widthSize)
        widthEntry.pack()
        widthSize.set(str(1))
        radiusLabel = tkinter.Label(sideBar,text="Radius")
        radiusLabel.pack()
        radiusSize = tkinter.StringVar()
        radiusEntry = tkinter.Entry(sideBar,textvariable=radiusSize)
        radiusSize.set(str(10))
        radiusEntry.pack()

        # function below is the event handler when the Draw Circle button is pressed.
        def circleHandler():
             # When drawing, a command is created and then the command is drawn by calling
             # the draw method. Adding the command to the graphicsCommands sequence means the
             # application will remember the picture.
            cmd = CircleCommand(float(radiusSize.get()), float(widthSize.get()), penColor.get())
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)

            # These two lines are needed to update the screen and to put the focus back
            # in the drawing canvas. This is necessary because when pressing "u" to undo,
            # the screen must have focus to receive the key press.
            screen.update()
            screen.listen()    

        # This creates the button widget in the sideBar. The fill=tkinter.BOTH causes the button
        # to expand to fill the entire width of the sideBar.
        circleButton = tkinter.Button(sideBar, text = "Draw Circle", command=circleHandler)
        circleButton.pack(fill=tkinter.BOTH)

        # The color mode 255 below allows colors to be specified in RGB form (i.e. Red/
        # Green/Blue). The mode allows the Red value to be set by a two digit hexadecimal
        # number ranging from 00-FF. The same applies for Blue and Green values. The
        # color choosers below return a string representing the selected color and a slice
        # is taken to extract the #RRGGBB hexadecimal string that the color choosers return.
        screen.colormode(255)
        penLabel = tkinter.Label(sideBar,text="Pen Color")
        penLabel.pack()
        penColor = tkinter.StringVar()
        penEntry = tkinter.Entry(sideBar,textvariable=penColor)
        penEntry.pack()
        penColor.set("#000000")

        def getPenColor():
            color = tkinter.colorchooser.askcolor()
            if color != None:
                penColor.set(str(color)[-9:-2])

            penColorButton = tkinter.Button(sideBar, text = "Pick Pen Color", command=getPenColor)
            penColorButton.pack(fill=tkinter.BOTH)

            fillLabel = tkinter.Label(sideBar,text="Fill Color")
            fillLabel.pack()
            fillColor = tkinter.StringVar()
            fillEntry = tkinter.Entry(sideBar,textvariable=fillColor)
            fillEntry.pack()
            fillColor.set("#000000")

        def getFillColor():
            color = tkinter.colorchooser.askcolor()
            if color != None:
                fillColor.set(str(color)[-9:-2])
        fillColorButton = \
            tkinter.Button(sideBar, text = "Pick Fill Color", command=getFillColor)
        fillColorButton.pack(fill=tkinter.BOTH)

        def beginFillHandler():
             cmd = BeginFillCommand(fillColor.get())
             cmd.draw(theTurtle)
             self.graphicsCommands.append(cmd)
        beginFillButton = tkinter.Button(sideBar, text = "Begin Fill", command=beginFillHandler)
        beginFillButton.pack(fill=tkinter.BOTH)

        def endFillHandler():
            cmd = EndFillCommand()
            cmd.draw(theTurtle)
            self.graphicsCommands.append(cmd)

        endFillButton = tkinter.Button(sideBar, text = "End Fill", command=endFillHandler)
        endFillButton.pack(fill=tkinter.BOTH)
        penLabel = tkinter.Label(sideBar,text="Pen Is Down")
        penLabel.pack()

        def penUpHandler():
            cmd = PenUpCommand()
            cmd.draw(theTurtle)
            penLabel.configure(text="Pen Is Up")
            self.graphicsCommands.append(cmd)
        penUpButton = tkinter.Button(sideBar, text = "Pen Up", command=penUpHandler)
        penUpButton.pack(fill=tkinter.BOTH)

        def penDownHandler():
            cmd = PenDownCommand()
            cmd.draw(theTurtle)
            penLabel.configure(text="Pen Is Down")
            self.graphicsCommands.append(cmd)
        penDownButton = tkinter.Button(sideBar, text = "Pen Down", command=penDownHandler)
        penDownButton.pack(fill=tkinter.BOTH)
         # Here is another event handler. This one handles mouse clicks on the screen.
        def clickHandler(x,y):
            # When a mouse click occurs, get the widthSize entry value and set the width of the
             # pen to the widthSize value. The float(widthSize.get()) is needed because
             # the width is a float, but the entry widget stores it as a string.
             cmd = GoToCommand(x,y,float(widthSize.get()),penColor.get())
             cmd.draw(theTurtle)
             self.graphicsCommands.append(cmd)
             screen.update()
             screen.listen()

        # Here is how we tie the clickHandler to mouse clicks.
             screen.onclick(clickHandler)

        def dragHandler(x,y):
             cmd = GoToCommand(x,y,float(widthSize.get()),penColor.get())
             cmd.draw(theTurtle)
             self.graphicsCommands.append(cmd)
             screen.update()
             screen.listen()
        theTurtle.ondrag(dragHandler)

        def undoHandler():
            if len(self.graphicsCommands) > 0:
                 self.graphicsCommands.removeLast()
                 theTurtle.clear()
                 theTurtle.penup()
                 theTurtle.goto(0,0)
                 theTurtle.pendown()
            for cmd in self.graphicsCommands:
                 cmd.draw(theTurtle)
                 screen.update()
                 screen.listen()

        screen.onkeypress(undoHandler, "u")
        screen.listen()

def main():
     root = tkinter.Tk()
     drawingApp = DrawingApplication(root)

     drawingApp.mainloop()
     print("Program Execution Completed.")

if __name__ == "__main__":
     main()               
        
