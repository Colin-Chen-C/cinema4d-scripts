"""
AR_ReplaceWithCloneOfFirst

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ReplaceWithCloneOfFirst
Description-US: Replace other objects with clone of first selected object
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d

# Functions
def deleteWithoutChildren(s):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    children = s.GetChildren() # Get selected object's children
    for child in reversed(children): # Loop through children
        globalMatrix = child.GetMg() # Get current global matrix
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, child) # Add undo command for moving item
        child.InsertAfter(s) # Move child
        child.SetMg(globalMatrix) # Set old global matrix
    doc.AddUndo(c4d.UNDOTYPE_DELETE, s) # Add undo command for deleting selected object
    s.Remove() # Remove selected object

def replaceWithCloneOfFirst(inherit = False):
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    selection = doc.GetActiveObjects(c4d.GETACTIVEOBJECTFLAGS_SELECTIONORDER) # Get selection
    cloneList = [] # Initialize list for clone objects
    childrenList = [] # Initialize list for list of children
    # Create clone objects and place those
    for i, s in enumerate(selection): # Loop through selected objects
        doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
        s.DelBit(c4d.BIT_ACTIVE) # Deselect first selected object
        if i != 0: # If not first loop round
            childrenList.append(selection[i].GetChildren()) # Get children objects
            cloneObj = selection[0].GetClone() # Get clone object
            cloneObj[c4d.ID_BASELIST_NAME] = selection[0].GetName()+"_Clone_"+str(i) # Change name
            cloneObj.InsertUnder(s) # Put instance under the selected object
            doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
            s.DelBit(c4d.BIT_ACTIVE) # Deselect object
            doc.AddUndo(c4d.UNDOTYPE_NEW, cloneObj) # Add undo command for inserting a new object
            cloneList.append(cloneObj) # Add current instance to list
    # Reset PSR and remove original object
    for i, s in enumerate(cloneList): # Loop through instances
        doc.AddUndo(c4d.UNDOTYPE_BITS, s) # Add undo command for changing bits
        s.SetBit(c4d.BIT_ACTIVE) # Select object
        # Reset position
        s[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_X] = 0
        s[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Y] = 0
        s[c4d.ID_BASEOBJECT_REL_POSITION,c4d.VECTOR_Z] = 0
        # Reset scale
        s[c4d.ID_BASEOBJECT_REL_SCALE,c4d.VECTOR_X] = 1
        s[c4d.ID_BASEOBJECT_REL_SCALE,c4d.VECTOR_Y] = 1
        s[c4d.ID_BASEOBJECT_REL_SCALE,c4d.VECTOR_Z] = 1
        # Reset rotation
        s[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_X] = 0
        s[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Y] = 0
        s[c4d.ID_BASEOBJECT_REL_ROTATION,c4d.VECTOR_Z] = 0
        deleteWithoutChildren(s.GetUp()) # Delete Without Children
        # Move old children (inherit)
        if inherit == True:
            for child in childrenList[i]:
                childMg = child.GetMg()
                doc.AddUndo(c4d.UNDOTYPE_CHANGE, child)
                child.InsertUnderLast(s)
                child.SetMg(childMg)
    # Select objects again
    doc.AddUndo(c4d.UNDOTYPE_BITS, selection[0]) # Add undo command for changing bits
    selection[0].SetBit(c4d.BIT_ACTIVE) # Select first object
    for i in cloneList: # Loop through instances
            doc.AddUndo(c4d.UNDOTYPE_BITS, i) # Add undo command for changing bits
            i.SetBit(c4d.BIT_ACTIVE) # Select object

def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    doc.StartUndo() # Start recording undos
    replaceWithCloneOfFirst(True) # Run the script
    doc.EndUndo() # Stop recording undos
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()