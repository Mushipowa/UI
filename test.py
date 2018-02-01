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
        self.dateFormat= None
        self.frame = tk.Frame(self.parent, bg='#E5EEF7', width=1200, height=600)
        self.frame.pack()
        self.frame.grid()
        self.frame.pack_propagate(0)

        self.menubar=tk.Menu(parent)
        self.parent.config(menu=self.menubar)
        self.menufichier=tk.Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="Fichier",menu=self.menufichier)
        self.menufichier.add_command(label="Ouvrir",command=self.load)
        self.menufichier.add_separator()
        self.menufichier.add_command(label="Enregistrer",command=self.save)
        self.menufichier.add_command(label="Enregistrer Sous",command=self.saveas)
        self.menufichier.add_separator()
        self.menufichier.add_command(label="Quitter",command=self.parent.destroy)


        self.cadre1 = tk.PanedWindow(self.frame, bg='#E5EEF7', width=350, height=600)
        self.cadre1.pack(side =tk.LEFT)
        self.cadre1.pack_propagate(0)
        self.cadre2 = tk.PanedWindow(self.frame, bg='#CCD6EB', width=900, height=600)
        self.cadre2.pack(side =tk.LEFT,padx =10)
        self.cadre2.pack_propagate(0)

        self.text = tk.Text(self.cadre2,bg='white')
        self.text.place(x=40,y=100, width =700, height=400)

        self.celluleVide =tk.Label(self.cadre1,text='Cellules Vides',bg='#E5EEF7')
        self.celluleVide.place(x=40, y=20)

        self.checkButtonCellule= tk.Checkbutton(self.cadre1,bg='#E5EEF7' )
        self.checkButtonCellule.place(x=15,y=20)

        self.formatNombre =tk.Label(self.cadre1,text='Format Nombre',bg='#E5EEF7')
        self.formatNombre.place(x=220, y=20)

        self.checkButtonNombre= tk.Checkbutton(self.cadre1,bg='#E5EEF7' )
        self.checkButtonNombre.place(x=200,y=20)

        self.formatEntree =tk.Label(self.cadre1,text='Format Entrée ',bg='#E5EEF7')
        self.formatEntree.place(x=220, y=80)

        self.listDate = tk.Listbox(self.cadre1)
        self.listDate.place(x=220, y=100, width=100, height=50)
        self.listDate.insert(tk.END,"Y/M/D")
        self.listDate.insert(tk.END,"Y/D/M")
        self.listDate.insert(tk.END,"M/D/Y")
        self.listDate.insert(tk.END,"M/Y/D")
        self.listDate.insert(tk.END,"D/M/Y")
        self.listDate.insert(tk.END,"D/Y/M")

        self.formatDate =tk.Label(self.cadre1,text='Format Date',bg='#E5EEF7')
        self.formatDate.place(x=40, y=100)

        self.checkButtonDate= tk.Checkbutton(self.cadre1,bg='#E5EEF7')
        self.checkButtonDate.place(x=15,y=100)

        self.anonymisation =tk.Label(self.cadre1,text='Anonymisation \n Données',bg='#E5EEF7')
        self.anonymisation.place(x=40, y=175)

        self.checkButtonAnonymisation= tk.Checkbutton(self.cadre1,bg='#E5EEF7' )
        self.checkButtonAnonymisation.place(x=15,y=175)

        self.entryAnonymisation = tk.Entry(self.cadre1)
        self.entryAnonymisation.place(x=220, y=180, width=100, height=25)

        self.colonneAnonymisation =tk.Label(self.cadre1,text='Colonne',bg='#E5EEF7')
        self.colonneAnonymisation.place(x=240, y=155)

        self.identificationDoublon =tk.Label(self.cadre1,text='Identification Doublon',bg='#E5EEF7')
        self.identificationDoublon.place(x=40, y=240)

        self.checkButtonDoublon= tk.Checkbutton(self.cadre1,bg='#E5EEF7' )
        self.checkButtonDoublon.place(x=15,y=240)


        self.compilationFichier =tk.Label(self.cadre1,text='Compilation Fichier',bg='#E5EEF7')
        self.compilationFichier.place(x=40, y=300)

        self.checkButtonCompilationFichier= tk.Checkbutton(self.cadre1,bg='#E5EEF7' )
        self.checkButtonCompilationFichier.place(x=15,y=300)

        self.button = tk.Button(self.cadre1, text='Chargement', command=self.load)
        self.button.place(x=40, y=350, width=100, height=25)

        self.liste = tk.Listbox(self.cadre1)
        self.liste.place(x=220, y=350, width=100, height=50)

        self.fichiers =tk.Label(self.cadre1,text='Fichiers',bg='#E5EEF7')
        self.fichiers.place(x=240, y=320)

        self.jointureFichier =tk.Label(self.cadre1,text='Jointure Fichier',bg='#E5EEF7')
        self.jointureFichier.place(x=40, y=400)

        self.checkButtonJointureFichier= tk.Checkbutton(self.cadre1,bg='#E5EEF7' )
        self.checkButtonJointureFichier.place(x=15,y=400)

        self.entryJointureFichier2 = tk.Entry(self.cadre1)
        self.entryJointureFichier2.place(x=220, y=450, width=100, height=25)

        self.jointureFichier1 =tk.Label(self.cadre1,text='Fichier 1',bg='#E5EEF7')
        self.jointureFichier1.place(x=40, y=425)

        self.jointureFichier2 =tk.Label(self.cadre1,text='Fichier 2',bg='#E5EEF7')
        self.jointureFichier2.place(x=240, y=425)

        self.entryJointureFichier1 = tk.Entry(self.cadre1)
        self.entryJointureFichier1.place(x=40, y=450, width=100, height=25)

        self.button = tk.Button(self.cadre1, text='Chargement', command=self.load)
        self.button.place(x=10, y=550, width=100, height=25)

        self.button = tk.Button(self.cadre2, text='Aperçu', command=self.display)
        self.button.place(x=270,y=550,width =100, height =25)

        self.button = tk.Button(self.cadre2,text='Effacer', command=self.clear)
        self.button.place(x=470, y=550, width=80, height=25)

        self.button = tk.Button(self.cadre1, text='Clean ', command=self.clean)
        self.button.place(x=120, y=550, width=100, height=25)

        self.button = tk.Button(self.cadre1, text='Save', command=self.save)
        self.button.place(x=230, y=550, width=100, height=25)

    def getParam(self):

        if self.listDate.curselection()[0]==0:
            self.dateFormat='%Y%m%d'
        if self.listDate.curselection()[0]==1:
            self.dateFormat='%Y%d%m'
        if self.listDate.curselection()[0]==2:
            self.dateFormat='%m%d%Y'
        if self.listDate.curselection()[0]==3:
            self.dateFormat='%m%Y%d'
        if self.listDate.curselection()[0]==4:
            self.dateFormat='%d%m%Y'
        if self.listDate.curselection()[0]==5:
            self.dateFormat='%d%Y%m'

    def save(self):
        self.cleaner.saveWB()

    def clean(self):


        self.getParam()
        self.cleaner = DC.Cleaner(self.filename, 0, 1, self.dateFormat, '/Users/Charles/Documents/Python/PFE/PFE_Data/Clean_Data/SampleCleanV5.XLSX')
        self.cleaner.openWB()
        self.cleaner.purify()
        self.cleaner.changeDate()
        self.cleaner.anonymize()



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
        else:
            self.text.delete('1.0',tk.END)
            self.text.insert('end', str(self.cleaner.getActiveSheet()) + '\n')

    def saveas(self):
        newName=tk.filedialog.asksaveasfile(title="Enregistrer sous.. un fichier", filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xlsx'))])
        print(newName.name)

    def clear(self):
        self.text.delete('1.0',tk.END)


# --- main ---

if __name__ == '__main__':
    parent = tk.Tk()
    parent.eval('lappend auto_path {' +TK_DND_PATH+ '}')
    top = MyWindow(parent)
    parent.mainloop()
