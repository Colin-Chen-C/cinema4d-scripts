"""
AR_ToggleTintedBorder

Author: Arttu Rautio (aturtur)
Website: http://aturtur.com/
Name-US: AR_ToggleTintedBorder
Description-US: Toggle opacity of tinted border in viewport, press shift to set custom value.
Note: Run the script from stored file location where you have writing permissions.
      The script creates a dat file for storing state of tinted border.
Written for Maxon Cinema 4D R20.057
"""
# Libraries
import c4d, os, re
from c4d import gui

# Functions
def main():
    doc = c4d.documents.GetActiveDocument() # Get active Cinema 4D document
    bd = doc.GetActiveBaseDraw() # Get active basedraw
    bc = c4d.BaseContainer() # Initialize base container
    path, fn = os.path.split(__file__) # Get path of the script
    data = os.path.join(path, 'AR_ToggleTintedBorder.dat') # data file path
    try: # Try to execute following script
        f = open(data.decode('utf-8')) # Open file for reading
        value = float(f.readline()) # Get value from data file
        f.close() # Close file
        if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,bc): # If button is pressed when script is executed
            if bc[c4d.BFM_INPUT_QUALIFIER] & c4d.QSHIFT: # If shift is pressed
                userValue = gui.InputDialog('Value') # Store user given value
                if userValue is not '':
                    userValue = userValue.replace(',','.') # Replace comma to dot, if found
                    numbers = re.compile('\d+(?:\.\d+)?') # Regular expression
                    userValue = float(numbers.findall(userValue)[0]) # Strip anything else but numbers
                    if userValue > 1: # If value is bigger than one
                        value = userValue / 100.0 # Divide value by 100
                    else: # If value is not bigger than one
                        value = userValue # Set value to userValue
                    f = open(data.decode('utf-8'), 'w') # Open file for writing
                    f.write(str(value)) # Write value to file
                    f.close() # Close file
                    bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = value # Set opacity to custom
            else: # If shift key is not pressed
                if bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] == 0: # If tinted border's opacity is 0
                    bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = value # Set opacity
                else: # If tinted border's opacity is not 0
                    f = open(data.decode('utf-8'), 'w') # Open file for writing
                    f.write(str(bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY])) # Write current value to file
                    f.close() # Close file
                    bd[c4d.BASEDRAW_DATA_TINTBORDER_OPACITY] = 0 # Set opacity to 0
    except: # If something went wrong
        pass # Do nothing
    c4d.EventAdd() # Refresh Cinema 4D

# Execute main()
if __name__=='__main__':
    main()