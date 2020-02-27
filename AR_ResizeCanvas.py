"""
AR_ResizeCanvas
Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ResizeCanvas
Description-US: Resizes canvas without changing the perspective.
Changes active render settings resolution and selected camera's sensor size (film gate) and possibly also film offsets.
Written for Maxon Cinema 4D R21.207
"""
# Libraries
import c4d
from c4d import gui
from c4d.gui import GeDialog

# Functions
def getSensorSize(old, new, sensor):
    return sensor * (new / old)

def getFilmAnchor(old, new, current):
    return current * (old/new)

def getFilmOffset(old, new, direction):
    filmOffset = ((1.0 - (old / new)) / 2.0)
    print old, new
    if (direction == "Up") or (direction == "Left"):
        filmOffset = filmOffset * -1.0
    return filmOffset

def resizeComposition(anchor, newWidth, newHeight):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    renderData = doc.GetActiveRenderData() # Get document render data

    if doc.GetActiveObject() == None:
        gui.MessageDialog("Select camera first!")
        return False
    camera = doc.GetActiveObject() # Get selected camera
    if camera.GetType() != 5103: # If not camera
        gui.MessageDialog("Select camera first!")
        return False

    focalLength = camera[c4d.CAMERA_FOCUS] # Get camera's focal length
    sensorSize = camera[c4d.CAMERAOBJECT_APERTURE] # Get camera's sensor size
    oldWidth = float(renderData[c4d.RDATA_XRES]) # Get render width resolution
    oldHeight = float(renderData[c4d.RDATA_YRES]) # Get render height resolution

    # Focal length method
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, camera) # Add undo step for camera changes
    doc.AddUndo(c4d.UNDOTYPE_CHANGE, renderData) # Add undo step for render data changes

    oldFilmOffsetY = float(camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y])
    oldFilmOffsetX = float(camera[c4d.CAMERAOBJECT_FILM_OFFSET_X])

    if anchor == "Mid Center":
        camera[c4d.CAMERAOBJECT_APERTURE] = getSensorSize(oldWidth, newWidth, sensorSize)
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY)
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX)

    elif anchor == "Top Center":
        camera[c4d.CAMERAOBJECT_APERTURE] = getSensorSize(oldWidth, newWidth, sensorSize)
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY) + getFilmOffset(oldHeight, newHeight, "Down")
    elif anchor == "Bot Center":
        camera[c4d.CAMERAOBJECT_APERTURE] = getSensorSize(oldWidth, newWidth, sensorSize)
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY) + getFilmOffset(oldHeight, newHeight, "Up")
    elif anchor == "Mid Left":
        camera[c4d.CAMERAOBJECT_APERTURE] = getSensorSize(oldWidth, newWidth, sensorSize)
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Right")
        print  getFilmOffset(oldWidth, newWidth, "Right")
    elif anchor == "Mid Right":
        camera[c4d.CAMERAOBJECT_APERTURE] = getSensorSize(oldWidth, newWidth, sensorSize)
        filmOffsetX = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Left")
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = filmOffsetX

    # Corners
    elif anchor == "Top Left":
        camera[c4d.CAMERAOBJECT_APERTURE] = getSensorSize(oldWidth, newWidth, sensorSize)
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Right")
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY) + getFilmOffset(oldHeight, newHeight, "Down")
    elif anchor == "Top Right":
        camera[c4d.CAMERAOBJECT_APERTURE] = getSensorSize(oldWidth, newWidth, sensorSize)
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Left")
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY) + getFilmOffset(oldHeight, newHeight, "Down")
    elif anchor == "Bot Left":
        camera[c4d.CAMERAOBJECT_APERTURE] = getSensorSize(oldWidth, newWidth, sensorSize)
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Right")
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY) + getFilmOffset(oldHeight, newHeight, "Up")
    elif anchor == "Bot Right":
        camera[c4d.CAMERAOBJECT_APERTURE] = getSensorSize(oldWidth, newWidth, sensorSize)
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_X] = getFilmAnchor(oldWidth, newWidth, oldFilmOffsetX) + getFilmOffset(oldWidth, newWidth, "Left")
        camera[c4d.CAMERAOBJECT_FILM_OFFSET_Y] = getFilmAnchor(oldHeight, newHeight, oldFilmOffsetY) + getFilmOffset(oldHeight, newHeight, "Up")


    renderData[c4d.RDATA_XRES] = newWidth
    renderData[c4d.RDATA_YRES] = newHeight
    doc.SetActiveRenderData(renderData)
    doc.EndUndo() # Stop recording undos
    return True

# Classes
class Dialog(GeDialog):
    def __init__(self):
        super(Dialog, self).__init__()

    # Create Dialog
    def CreateLayout(self):
        self.SetTitle("Resize composition") # Set dialog title
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(1000, c4d.BFH_CENTER, 2, 1) # Begin 'Mega1' group
        # ----------------------------------------------------------------------------------------
        # Radio checkboxes
        self.GroupBegin(1001, c4d.BFH_LEFT, 1, 2, "Anchor") # Begin 'Anchor' group
        self.GroupBorder(c4d.BORDER_ROUND)
        self.GroupBorderSpace(5, 5, 5, 5)

        self.AddRadioGroup(2000, c4d.BFH_CENTER, 3, 3)
        self.AddChild(2000, 2001, " ")
        self.AddChild(2000, 2002, " ")
        self.AddChild(2000, 2003, " ")
        self.AddChild(2000, 2004, " ")
        self.AddChild(2000, 2005, " ")
        self.AddChild(2000, 2006, " ")
        self.AddChild(2000, 2007, " ")
        self.AddChild(2000, 2008, " ")
        self.AddChild(2000, 2009, " ")
        self.SetBool(2005, 1) # Set default selection
        self.GroupEnd() # End 'Anchor' group
        # ----------------------------------------------------------------------------------------
        # Inputs
        self.GroupBegin(1002, c4d.BFH_RIGHT, 2, 2, "Resolution") # Begin 'Resolution' group
        self.GroupBorder(c4d.BORDER_ROUND)
        self.GroupBorderSpace(5, 5, 5, 5)
        self.AddStaticText(3000, c4d.BFH_LEFT, 0, 0, "Width", 0)
        #self.AddEditText(3001, c4d.BFH_LEFT, initw=80, inith=0)
        self.AddEditNumberArrows(3001, c4d.BFH_LEFT, initw=80, inith=0)
        self.AddStaticText(3002, c4d.BFH_LEFT, 0, 0, "Height", 0)
        #self.AddEditText(3003, c4d.BFH_LEFT, initw=80, inith=0)
        self.AddEditNumberArrows(3003, c4d.BFH_LEFT, initw=80, inith=0)
        self.SetFloat(3001, 0)
        self.SetFloat(3003, 0)
        self.GroupEnd() # End 'Resolution' group
        # ----------------------------------------------------------------------------------------
        self.GroupEnd() # End 'Mega1' group
        # ----------------------------------------------------------------------------------------
        self.GroupBegin(1005, c4d.BFH_CENTER, 0, 0, "Buttons") # Begin 'Buttons' group
        # Buttons
        self.AddButton(3004, c4d.BFH_LEFT, name="Accept") # Add button
        self.AddButton(3005, c4d.BFH_RIGHT, name="Cancel") # Add button

        self.GroupEnd() # End 'Buttons' group
        return True

    def Command(self, paramid, msg): # Handling commands (pressed button etc.)
        # Actions here
        if paramid == 3005: # If 'Cancel' button is pressed
            self.Close() # Close dialog
        if paramid == 3004: # If 'Accept' button is pressed
            width =  float(self.GetString(3001)) # Get width input
            height = float(self.GetString(3003)) # Get height input

            atl = self.GetBool(2001)      # Get 'Anchor' checkboxes
            atc = self.GetBool(2002)
            atr = self.GetBool(2003)
            aml = self.GetBool(2004)
            amc = self.GetBool(2005)
            amr = self.GetBool(2006)
            abl = self.GetBool(2007)
            abc = self.GetBool(2008)
            abr = self.GetBool(2009)

            if atl == True:
                anchor = "Top Left"
            elif atc == True:
                anchor = "Top Center"
            elif atr == True:
                anchor = "Top Right"
            elif aml == True:
                anchor = "Mid Left"
            elif amc == True:
                anchor = "Mid Center"
            elif amr == True:
                anchor = "Mid Right"
            elif abl == True:
                anchor = "Bot Left"
            elif abc == True:
                anchor = "Bot Center"
            else:
                anchor = "Bot Right"

            resizeComposition(anchor, width, height) # Run the main algorithm
            c4d.EventAdd() # Refresh Cinema 4D
            pass

        return True # Everything is fine

dlg = Dialog() # Create dialog object
dlg.Open(c4d.DLG_TYPE_ASYNC, 0, -2, -2, 5, 5) # Open dialog