"""
AR_CreateControlNullsForJoints

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_CreateControlNullsForJoints
Description-US: Create control null object(s) from selected joint(s). Joints' transformation needs to be unfrozen.
Written for Maxon Cinema 4D R21.057
"""
# Libraries
import c4d
from c4d import utils as u

# Global variables
prevNull = None

# Functions
def GetGlobalPosition(obj): # Get object's global position
    return obj.GetMg().off

def GetGlobalRotation(obj): # Get object's global rotation
    return u.MatrixToHPB(obj.GetMg())

def GetGlobalScale(obj): # Get object's global scale
    m = obj.GetMg()
    return c4d.Vector(m.v1.GetLength(),
                      m.v2.GetLength(),
                      m.v3.GetLength())

def SetGlobalPosition(obj, pos): # Set object's global position
    m = obj.GetMg()
    m.off = pos
    obj.SetMg(m)

def SetGlobalRotation(obj, rot): # Set object's global rotation
    m = obj.GetMg()
    pos = m.off
    scale = c4d.Vector(m.v1.GetLength(),
                       m.v2.GetLength(),
                       m.v3.GetLength())
    m = u.HPBToMatrix(rot)
    m.off = pos
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def SetGlobalScale(obj, scale): # Set object's global scale
    m = obj.GetMg()
    m.v1 = m.v1.GetNormalized() * scale.x
    m.v2 = m.v2.GetNormalized() * scale.y
    m.v3 = m.v3.GetNormalized() * scale.z
    obj.SetMg(m)

def FreezePSR(obj):
    obj.SetFrozenPos(obj.GetAbsPos()) # Freeze position
    obj.SetFrozenRot(obj.GetAbsRot()) # Freeze rotation
    obj.SetFrozenScale(obj.GetAbsScale()) # Freeze scale
    obj.SetRelPos(c4d.Vector(0,0,0)) # Reset relative position
    obj.SetRelRot(c4d.Vector(0,0,0)) # Reset relative rotation
    obj.SetRelScale(c4d.Vector(1,1,1)) # Reset relative scale

def ResetPSR(obj):
    obj.SetRelPos(c4d.Vector(0,0,0)) # Reset relative position
    obj.SetRelRot(c4d.Vector(0,0,0)) # Reset relative rotation
    obj.SetRelScale(c4d.Vector(1,1,1)) # Reset relative scale

def CreateNulls(obj):
    global prevNull
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    try: # Try to execute following script
        objectNull = c4d.BaseObject(c4d.Onull) # Initialize null object
        objectNull.SetName(str(obj.GetName()) + " Points") # Set parent null's name
        objectNull[c4d.NULLOBJECT_DISPLAY] = 14 # Set null's display mode to none
        SetGlobalPosition(objectNull,GetGlobalPosition(obj)) # Set global position, rotation and scale
        SetGlobalRotation(objectNull,GetGlobalRotation(obj))
        SetGlobalScale(objectNull,GetGlobalScale(obj))
        objectNull.SetName(obj.GetName()+"_Null") # Set null's name
        objectNull[c4d.NULLOBJECT_DISPLAY] = 2 # Set null's display mode circle
        objectNull.SetAbsPos(obj.GetAbsPos()) # Set null's position
        obj.InsertTag(c4d.BaseTag(1019364)) # Insert constraint tag to obj
        tag = obj.GetFirstTag() # Select constraint tag
        tag[c4d.ID_CA_CONSTRAINT_TAG_PARENT] = 1 # Activate parent constraint
        tag[30001] = objectNull # Set Target
        doc.AddUndo(c4d.UNDOTYPE_NEW, objectNull) # Add undo command for adding new object
        if prevNull == None:
            prevNull = objectNull
            doc.InsertObject(objectNull) # Insert null to document
        else:
            objectNull.InsertUnder(prevNull) # Insert null under to parent
        FreezePSR(objectNull) # Freeze PSR
        prevNull = objectNull
        ResetPSR(obj)
    except: # If something went wrong
        pass # Do nothing

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_CHILDREN) # Get active selection
    for obj in selection: # Loop through selected items
        if obj.GetType() == 1019362: # If joint object
            CreateNulls(obj) # Run CreateNulls function
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()