try:
    # Python 2
    import Tkinter as tk
    import ttk
    from tkFileDialog import askopenfilename
except ImportError:
    # Python 3
    import tkinter as tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename

import pandas as pd
import sys, os
from PFE_MondoClean.MondoClean.data_Cleaner_Module import data_Cleaner as DC
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath('_file_'))

TK_DND_PATH = os.path.join(application_path,'tkdnd2.8')


# --- classes ---
class MyWindow:

    def __init__(self, parent):

        self.parent = parent
        self.parent.title("MondoClean")
        #self.parent.rowconfigure(0, weight=1)
        #self.parent.columnconfigure(0, weight=1)
        self.filename = None
        self.df = None
        self.cleaner = None
        self.frame = tk.Frame(self.parent, bg='#C4CDD5', width=1200, height=600)
        self.frame.pack()
        self.frame.grid()
        self.frame.pack_propagate(0)

        self.cadre1 = tk.PanedWindow(self.frame, bg='#BEC8D0', width=400, height=600)
        self.cadre1.pack(side =tk.LEFT)
        self.cadre1.pack_propagate(0)
        self.cadre2 = tk.PanedWindow(self.frame, bg='#C4CDD5', width=800, height=500)
        self.cadre2.pack(side =tk.LEFT,padx =10)
        self.cadre2.pack_propagate(0)

        self.text = tk.Text(self.cadre2,bg='white', width=400, height=300)
        self.text.pack()

        self.button = tk.Button(self.cadre1, text='Chargement', command=self.load)
        self.button.place(x=10, y=550, width=100, height=25)

        self.button = tk.Button(self.cadre1, text='Aperçu', command=self.display)
        self.button.place(x=120, y=550, width=70, height=25)

        self.button = tk.Button(self.cadre1,text='Effacer', command=self.clear)
        self.button.place(x=200, y=550, width=80, height=25)

        self.button = tk.Button(self.cadre1, text='Clean ', command=self.clean)
        self.button.place(x=290, y=550, width=100, height=25)

        self.button = tk.Button(self.cadre1, text='Save', command=self.save)
        self.button.place(x=100, y=100, width=100, height=25)

    def save(self):
        self.cleaner.saveWB()

    def clean(self):
        cleaner = DC.Cleaner(self.filename, 0, 1, '%Y%m%d', '/Users/Charles/Documents/Python/PFE/PFE_Data/Clean_Data/SampleCleanV5.XLSX')
        cleaner.openWB()
        cleaner.purify()
        cleaner.changeDate()
        cleaner.anonymize()



    def load(self):

        name = askopenfilename(filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xlsx'))])


        if name:
            if name.endswith('.csv'):
                self.df = pd.read_csv(name)
            else:
                self.df = pd.read_excel(name)

            self.filename = name

        self.cleaner = DC.Cleaner(self.filename, 0, 1, '%Y%m%d', '/Users/Charles/Documents/Python/PFE/PFE_Data/Clean_Data/SampleCleanV5.XLSX')
            # display directly
            #self.text.insert('end', str(self.df.head()) + '\n')

    def display(self):
        # ask for file if not loaded yet
        if self.df is None:
            self.load()

        # display if loaded
        if self.df is not None:
            self.text.insert('end', self.filename + '\n')
            self.text.insert('end', str(self.df.head()) + '\n')

    def save_file():

        filename = askopenfilename(filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xlsx'))])
        if filename:
             print("User saved the filename with extension:", filename.split(".")[-1])


             button = tk.Button(self.parent, text='Save File', command=save_file)
             button.pack()

    def clear(self):
        self.text.delete('1.0',tk.END)


# --- main ---

if __name__ == '__main__':
    parent = tk.Tk()
    parent.eval('lappend auto_path {' +TK_DND_PATH+ '}')
    top = MyWindow(parent)
    parent.mainloop()
