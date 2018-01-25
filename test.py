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

        self.filename = None
        self.df = None

        self.text = tk.Text(self.parent)
        self.text.pack()

        self.button = tk.Button(self.parent, text='chargement', command=self.load)
        self.button.pack()

        self.button = tk.Button(self.parent, text='Aperçu', command=self.display)
        self.button.pack()

        self.button = tk.Button(self.parent, text='save', command=self.save_file)
        self.button.pack()

        self.button = tk.Button(self.parent, text='clear', command=self.clear)
        self.button.pack()

    def load(self):

        name = askopenfilename(filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xlsx'))])

        if name:
            if name.endswith('.csv'):
                self.df = pd.read_csv(name)
            else:
                self.df = pd.read_excel(name)

            self.filename = name

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


             button = tk.Button(root, text='Save File', command=save_file)
             button.pack()

    def clear(self):
        self.text.delete('1.0',tk.END)


# --- main ---

if __name__ == '__main__':
    root = tk.Tk()
    root.eval('lappend auto_path {' +TK_DND_PATH+ '}')
    top = MyWindow(root)
    root.mainloop()
