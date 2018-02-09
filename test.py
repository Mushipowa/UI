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
import PIL
from PIL import ImageTk, Image
import pandas as pd
import sys, os
from PFE_MondoClean.MondoClean.data_Cleaner_Module import data_Cleaner as DC
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app
    # path into variable _MEIPASS'.
    application_path = sys._MEIPASS
else:
    application_path = os.path.dirname(os.path.abspath('file'))

TK_DND_PATH = os.path.join(application_path,'tkdnd2.8')
# --- classes ---
class MyWindow:

    def __init__(self, parent):

        #Initialisation
        self.parent = parent
        self.parent.title("MondoClean")
        self.parent.resizable(width=False,height=False)
        #self.parent.rowconfigure(0, weight=1)
        #self.parent.columnconfigure(0, weight=1)
        self.filename = None
        self.df = None
        self.cleaner = None
        self.dateFormat= None
        self.colIndexDoublon= None
        self.colIndexAnonymisation= None
        self.banList= None
        self.listeCheminCompil= None
        self.cheminJointure = None
        self.colComp1 = None
        self.colComp2 = None
        self.colJoints = None
        self.frame = tk.Frame(self.parent, bg='#989292', width=1200, height=700)
        self.frame.grid()
        self.frame.grid_propagate(False)

        #Menu
        self.menubar=tk.Menu(parent)
        self.parent.config(menu=self.menubar)

        self.menufichier=tk.Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="Fichier",menu=self.menufichier)
        self.menufichier.add_command(label="Ouvrir",command=lambda: self.load(0, False))
        self.menufichier.add_separator()
        self.menufichier.add_command(label="Enregistrer",command=self.save)
        self.menufichier.add_command(label="Enregistrer Sous",command=self.saveas)
        self.menufichier.add_separator()
        self.menufichier.add_command(label="Quitter",command=self.parent.destroy)

        #Deux grands Panels
        self.cadre1 = tk.PanedWindow(self.frame, bg='#898283', width=500, height=700)
        self.cadre1.pack(side =tk.LEFT)
        self.cadre1.pack_propagate(0)
        self.cadre2 = tk.PanedWindow(self.frame, bg='#A7A1A2', width=800, height=700)
        self.cadre2.pack(side =tk.LEFT,padx =10)
        self.cadre2.pack_propagate(0)

        #Petits panels du Panel cadre1
        self.cadreFichier =tk.PanedWindow(self.cadre1,width= 475, height= 210, bd= 2, relief = 'sunken')
        self.cadreFichier.place(x=10,y=50)
        self.cadreFichier.pack_propagate(0)

        self.cadreDate =tk.PanedWindow(self.cadre1,width= 475, height= 160, bd= 2, relief = 'sunken')
        self.cadreDate.place(x=10,y=250)
        self.cadreDate.pack_propagate(0)

        self.cadreAnonymisation =tk.PanedWindow(self.cadre1,width= 475, height= 130, bd= 2, relief = 'sunken')
        self.cadreAnonymisation.place(x=10,y=420)
        self.cadreAnonymisation.pack_propagate(0)

        self.cadreCategorisation =tk.PanedWindow(self.cadre1,width= 475, height= 130, bd= 2, relief = 'sunken')
        self.cadreCategorisation.place(x=10,y=560)
        self.cadreCategorisation.pack_propagate(0)

        #Titre panel paramètres
        self.labelTitreCadre1 = tk.Label(self.cadre1,text='Paramètres',justify='center',width=55, bg='#5E5455',fg='white')
        self.labelTitreCadre1.place(x=0, y=0)

        #Image Doshas
        self.im=Image.open("/Users/charles/Documents/Python/PFE/PFE_UI/UI/images/Logo_Doshas_V7.JPG")
        self.photo=ImageTk.PhotoImage(self.im)
        self.labelDoshas=tk.Label(self.cadre2,image=self.photo, bg='#5A6932')
        self.labelDoshas.place(x=300, y=20, width=200 ,height=69)

        #Image run (Clean)
        self.play=Image.open("/Users/charles/Documents/Python/PFE/PFE_UI/UI/images/play_V2.JPG")
        self.photoPlay=ImageTk.PhotoImage(self.play)
        self.button = tk.Button(self.cadre2, bg='#5A6932',image=self.photoPlay,command=self.clean)
        self.button.place(x=400, y=620, width=64, height=64)


        #Zone d'affichage
        self.text = tk.Text(self.cadre2,bg='white')
        self.text.place(x=50,y=100, width =700, height=500)

        #cadreDate : Date,nombre,cellules vides
        self.banChar =tk.Label(self.cadreDate,text='Caractères Indésirables')
        self.banChar.place(x=50, y=30)

        self.varCell=tk.IntVar()
        self.checkButtonCellule= tk.Checkbutton(self.cadreDate,variable= self.varCell)
        self.checkButtonCellule.place(x=30,y=30)

        self.entryCaracteresIndesirables= tk.Entry(self.cadreDate)
        self.entryCaracteresIndesirables.place(x=260, y=30,  width=100, height=25)

        self.caracteresIndesirables= tk.Label(self.cadreDate, text='Valeurs')
        self.caracteresIndesirables.place(x=280, y=8)

        self.formatEntree =tk.Label(self.cadreDate,text='Format Entrée ')
        self.formatEntree.place(x=260, y=60)

        self.listDate = tk.Listbox(self.cadreDate)
        self.listDate.place(x=260, y=80, width=100, height=30)
        self.listDate.insert(tk.END,"Y/M/D")
        self.listDate.insert(tk.END,"Y/D/M")
        self.listDate.insert(tk.END,"M/D/Y")
        self.listDate.insert(tk.END,"M/Y/D")
        self.listDate.insert(tk.END,"D/M/Y")
        self.listDate.insert(tk.END,"D/Y/M")

        self.formatDate =tk.Label(self.cadreDate,text='Format Date')
        self.formatDate.place(x=50, y=80)

        self.varDate=tk.IntVar()
        self.checkButtonDate= tk.Checkbutton(self.cadreDate,variable= self.varDate)
        self.checkButtonDate.place(x=30,y=80)

        #cadreAnonymisation : Anonymisation et Doublon
        self.anonymisation =tk.Label(self.cadreAnonymisation,text='Anonymisation Données')
        self.anonymisation.place(x=50, y=30)

        self.varAnonymisation=tk.IntVar()
        self.checkButtonAnonymisation= tk.Checkbutton(self.cadreAnonymisation,variable= self.varAnonymisation )
        self.checkButtonAnonymisation.place(x=30,y=30)

        self.entryAnonymisation = tk.Entry(self.cadreAnonymisation)
        self.entryAnonymisation.place(x=260, y=30, width=100, height=25)

        self.colonneAnonymisation =tk.Label(self.cadreAnonymisation,text='Colonne')
        self.colonneAnonymisation.place(x=280, y=8)

        self.identificationDoublon =tk.Label(self.cadreAnonymisation,text='Identification Doublon')
        self.identificationDoublon.place(x=50, y=80)

        self.varDoublon=tk.IntVar()
        self.checkButtonDoublon= tk.Checkbutton(self.cadreAnonymisation,variable= self.varDoublon)
        self.checkButtonDoublon.place(x=30,y=80)

        self.entryDoublon= tk.Entry(self.cadreAnonymisation)
        self.entryDoublon.place(x=260, y=80, width=100, height=25)

        self.colonneDoublon =tk.Label(self.cadreAnonymisation,text='Colonne')
        self.colonneDoublon.place(x=280, y=58)


        #cadreFichier : Compilation et Jointure
        self.compilationFichier =tk.Label(self.cadreFichier,text='Compilation Fichier')
        self.compilationFichier.place(x=50, y=20)

        self.varCompilation=tk.IntVar()
        self.checkButtonCompilationFichier= tk.Checkbutton(self.cadreFichier,variable= self.varCompilation)
        self.checkButtonCompilationFichier.place(x=30,y=20)

        self.button = tk.Button(self.cadreFichier, text='Chargement',bd='4',relief='raised', command=lambda: self.load(1, False))
        self.button.place(x=200, y=20, width=100, height=25)

        self.listeCompilation = tk.Listbox(self.cadreFichier)
        self.listeCompilation.place(x=350, y=30, width=100, height=50)

        self.fichiers =tk.Label(self.cadreFichier,text='Fichiers')
        self.fichiers.place(x=370, y=5)

        self.jointureFichier =tk.Label(self.cadreFichier,text='Jointure Fichier')
        self.jointureFichier.place(x=50, y=90)

        self.listeJointure = tk.Listbox(self.cadreFichier)
        self.listeJointure.place(x=350, y=100, width=100, height=50)

        self.varJointure=tk.IntVar()
        self.checkButtonJointureFichier= tk.Checkbutton(self.cadreFichier,variable= self.varJointure)
        self.checkButtonJointureFichier.place(x=30,y=90)

        self.button = tk.Button(self.cadreFichier, text='Chargement',bd='4',relief='raised', command=lambda: self.load(2, False))
        self.button.place(x=200, y=90, width=100, height=25)

        self.jointureFichiersColonne=tk.Label(self.cadreFichier,text='Colonne')
        self.jointureFichiersColonne.place(x=10, y=150)

        self.jointureFichier1 =tk.Label(self.cadreFichier,text='Fichier 1')
        self.jointureFichier1.place(x=110, y=130)

        self.entryJointureFichier1 = tk.Entry(self.cadreFichier)
        self.entryJointureFichier1.place(x=90, y=150, width=100, height=25)

        self.jointureFichier2 =tk.Label(self.cadreFichier,text='Fichier 2')
        self.jointureFichier2.place(x=240, y=130)

        self.entryJointureFichier2 = tk.Entry(self.cadreFichier)
        self.entryJointureFichier2.place(x=220, y=150, width=100, height=25)

        self.jointureFichier3 =tk.Label(self.cadreFichier,text='Colonne à ajouter')
        self.jointureFichier3.place(x=340, y=130)

        self.entryJointureFichier3 = tk.Entry(self.cadreFichier)
        self.entryJointureFichier3.place(x=350, y=150, width=100, height=25)

        #cadreCategorisation : Categorisation
        self.categorisation =tk.Label(self.cadreCategorisation,text='Catégorisation')
        self.categorisation.place(x=50, y=20)

        self.varCategorisation=tk.IntVar()
        self.checkButtonCategorisation= tk.Checkbutton(self.cadreCategorisation,variable= self.varCategorisation)
        self.checkButtonCategorisation.place(x=30,y=20)

        self.entryColonneCategorisation = tk.Entry(self.cadreCategorisation)
        self.entryColonneCategorisation.place(x=260, y=30, width=100, height=25)

        self.colonneCategorisation =tk.Label(self.cadreCategorisation,text='Colonne')
        self.colonneCategorisation.place(x=280, y=8)

        self.entryEntreeCategorisation = tk.Entry(self.cadreCategorisation)
        self.entryEntreeCategorisation.place(x=50, y=80, width=100, height=25)

        self.colonneCategorisation =tk.Label(self.cadreCategorisation,text='Entrée')
        self.colonneCategorisation.place(x=70, y=58)

        self.entrySortieCategorisation = tk.Entry(self.cadreCategorisation)
        self.entrySortieCategorisation.place(x=260, y=80, width=100, height=25)

        self.colonneCategorisation =tk.Label(self.cadreCategorisation,text='Sortie')
        self.colonneCategorisation.place(x=280, y=58)

    #Parametres
    def getParam(self):
        if self.varDate.get():
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

        if self.varDoublon.get():
            entryDoublonString = self.entryDoublon.get().split(",")
            self.colIndexDoublon = [int(s) for s in entryDoublonString]

        if self.varAnonymisation.get():
            entryAnonymisationString= self.entryAnonymisation.get().split(",")
            self.colIndexAnonymisation= [int(s) for s in entryAnonymisationString]

        if self.varCell.get():
            self.banList= self.entryCaracteresIndesirables.get().split(",")

        if self.varCompilation.get():
            self.listeCheminCompil = []
            for i in range(self.listeCompilation.size()):
                self.listeCheminCompil.append(self.listeCompilation.get(i))

        if self.varJointure.get():
            self.cheminJointure = self.listeJointure.get(0)
            self.colComp1 = int(self.entryJointureFichier1.get())
            self.colComp2 = int(self.entryJointureFichier2.get())
            entryJoinFichier3 = self.entryJointureFichier3.get().split(",")
            self.colJoints = [int(s) for s in entryJoinFichier3]

    #Sauvegarder avec menu
    def save(self):
        self.cleaner.saveWB()

    #Nettoyer
    def clean(self):
        self.getParam()
        self.cleaner = DC.Cleaner(self.filename)
        self.cleaner.openWB(1, None)
        if self.banList is not None:
            self.cleaner.param(self.banList)
        self.cleaner.purify()
        if self.dateFormat is not None:
            self.cleaner.changeDate(self.dateFormat)
        if self.colIndexDoublon is not None:
            self.cleaner.doublons(self.colIndexDoublon)
        if self.colIndexAnonymisation is not None:
            self.cleaner.anonymize(self.colIndexAnonymisation)
        if self.listeCheminCompil is not None:
            self.cleaner.aggreg(self.listeCheminCompil)
        if self.cheminJointure is not None:
            self.cleaner.joint(self.cheminJointure, self.colComp1, self.colComp2, self.colJoints)
        self.cleaner.purify()
        self.saveas()
        self.resetParam()
        self.display()


    #Charger un fichier
    def load(self, keyLoad, update, *args):
        if update == False:
            name = askopenfilename(filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xlsx'))])
            if name:
                if keyLoad == 0:
                    if name.endswith('.csv'):
                        self.df = pd.read_csv(name)
                    else:
                        self.df = pd.read_excel(name)
                    self.filename = name
                    self.display()
                if keyLoad == 1:
                    self.listeCompilation.insert(tk.END, name)
                if keyLoad == 2:
                    self.listeJointure.insert(tk.END, name)
        else:
            if args[0].endswith('.csv'):
                self.df = pd.read_csv(args[0])
            else:
                self.df = pd.read_excel(args[0])
            self.display()

    #Reset Paramètres
    def resetParam(self):
        self.dateFormat= None
        self.colIndexDoublon= None
        self.colIndexAnonymisation= None
        self.banList= None
        self.listeCheminCompil= None
        self.cheminJointure = None
        self.colComp1 = None
        self.colComp2 = None
        self.colJoints = None

    #def resetUI(self):


    #Afficher sur la zone
    def display(self):
        # ask for file if not loaded yet
            self.text.delete('1.0',tk.END)
            self.text.insert('end', str(self.df.head()) + '\n')

    #Sauvegarder un fichier sous
    def saveas(self):
        newName=tk.filedialog.asksaveasfile(title="Enregistrer sous.. un fichier", filetypes=[('CSV', '*.csv',), ('Excel', ('*.xls', '*.xlsx'))])
        self.newPath = newName.name
        self.cleaner.saveWB(1, self.newPath)
        self.load(None, True, self.newPath)

    #Effacer l'affichage
    def clear(self):
        self.text.delete('1.0',tk.END)


# --- main ---

if __name__ == '__main__':
    parent = tk.Tk()
    parent.eval('lappend auto_path {' +TK_DND_PATH+ '}')
    top = MyWindow(parent)
    parent.mainloop()
