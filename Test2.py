from tkinter import *
from tkinter.filedialog import *
from tkinter.constants import *
dirtext='Select your pictures folder'
filetext= 'Select your watermark file'
def openFile():
    filename = askopenfilename(parent=root,initialdir='/home/',title=filetext , filetypes=[('image files', '.png')]) ## filename not filehandle
    filebut["text"]= str(filename) if filename else filetext
def openDirectory():
    dirname = askdirectory(parent=root, initialdir='/home/', title=dirtext)
    dirbut["text"] = str(dirname) if dirname else dirtext
root = Tk()
root.title('Watermark Image Processing 1.0b')
#Options for buttons
button_opt = {'fill': BOTH, 'padx': 5, 'pady': 5}
#Define asking directory button
dirbut= Button(root, text = dirtext, fg = 'black', command= openDirectory)
dirbut.pack(**button_opt) ## must pack separately to get the value to dirbut
#Define asking watermark file button
filebut = Button(root, text = filetext, fg = 'black', command= openFile)
filebut.pack(**button_opt)
root.mainloop()
