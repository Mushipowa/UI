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
import threading
import pandas as pd
import PFE_UI.UI.filePathGenerator.file as pg
import sys, os
import time
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
        self.colIndexC = None
        self.modeCateg = None
        self.changes = {}
        self.bytes=0
        self.maxbytes = 100

        self.frame = tk.Frame(self.parent, bg='#989292', width=1200, height=700)
        self.frame.grid()
        self.frame.grid_propagate(False)
        self.dirPath = pg.getFilePath().replace('filePathGenerator','')

        #Menu
        self.menubar=tk.Menu(parent)
        self.parent.config(menu=self.menubar)

        self.menufichier=tk.Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="Fichier",menu=self.menufichier)
        self.menufichier.add_command(label="Nouveau Fichier",command=lambda: self.load(0, False))
        self.menufichier.add_separator()
        self.menufichier.add_command(label="Enregistrer",command=self.save)
        self.menufichier.add_command(label="reset ",command=self.resetUI)
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
        self.cadreFichier =tk.PanedWindow(self.cadre1,width= 475, height= 220, bd= 2, relief = 'sunken')
        self.cadreFichier.place(x=10,y=45)
        self.cadreFichier.pack_propagate(0)

        self.cadreDate =tk.PanedWindow(self.cadre1,width= 475, height= 130, bd= 2, relief = 'sunken')
        self.cadreDate.place(x=10,y=275)
        self.cadreDate.pack_propagate(0)

        self.cadreAnonymisation =tk.PanedWindow(self.cadre1,width= 475, height= 130, bd= 2, relief = 'sunken')
        self.cadreAnonymisation.place(x=10,y=415)
        self.cadreAnonymisation.pack_propagate(0)

        self.cadreCategorisation =tk.PanedWindow(self.cadre1,width= 475, height= 120, bd= 2, relief = 'sunken')
        self.cadreCategorisation.place(x=10,y=555)
        self.cadreCategorisation.pack_propagate(0)

        #Titre panel paramètres
        self.labelTitreCadre1 = tk.Label(self.cadre1,text='Paramètres',justify='center',width=55, bg='#5E5455',fg='white')
        self.labelTitreCadre1.place(x=0, y=0)


        #Image Doshas
        self.im=Image.open(self.dirPath+"/filePathGenerator/images/Logo_Doshas_V7.JPG")
        self.photo=ImageTk.PhotoImage(self.im)
        self.labelDoshas=tk.Label(self.cadre2,image=self.photo, bg='#5A6932')
        self.labelDoshas.place(x=300, y=20, width=200 ,height=69)

        #Control panel (Clean/Reset/PullBack)
        self.play=Image.open(self.dirPath+"/filePathGenerator/images/play_V4.JPG")
        self.photoPlay=ImageTk.PhotoImage(self.play)
        self.button = tk.Button(self.cadre2,image=self.photoPlay,command=self.clean)
        self.button.place(x=380, y=620, width=64, height=64)

        self.pullBack=Image.open(self.dirPath+"/filePathGenerator/images/retour_V3.JPG")
        self.photoPullBack=ImageTk.PhotoImage(self.pullBack)
        self.buttonPullBack = tk.Button(self.cadre2,image=self.photoPullBack,command=self.undo)
        self.buttonPullBack.place(x=100, y=630, width=50, height=50)

        self.reset=Image.open(self.dirPath+"/filePathGenerator/images/reset.JPG")
        self.photoReset=ImageTk.PhotoImage(self.reset)
        self.buttonReset = tk.Button(self.cadre2, bg='#5A6932',image=self.photoReset,command=self.resetCleaner)
        self.buttonReset.place(x=640, y=630, width=50, height=50)


        #Zone d'affichage
        self.text = tk.Text(self.cadre2,bg='white')
        self.text.place(x=50,y=100, width =700, height=500)

        #bouton Chargement
        self.buttonChargement = tk.Button(self.text, text='Importer un Fichier',bd='4',relief='raised',highlightcolor='black', command=lambda: self.load(0, False))
        self.buttonChargement.place(x=250, y=225, width=200, height=50)


        #cadreDate : Date,nombre,cellules vides
        self.banChar =tk.Label(self.cadreDate,text='Caractères Indésirables')
        self.banChar.place(x=50, y=30)

        self.varCell=tk.IntVar()
        self.checkButtonCellule= tk.Checkbutton(self.cadreDate,variable= self.varCell,command=self.unlockCaracteres)
        self.checkButtonCellule.place(x=30,y=30)

        self.entryCaracteresIndesirables= tk.Entry(self.cadreDate,state='normal')
        self.entryCaracteresIndesirables.place(x=260, y=30,  width=100, height=25)
        self.entryCaracteresIndesirables.configure(state='disabled',disabledbackground='#E8E8E8')

        self.caracteresIndesirables= tk.Label(self.cadreDate, text='Valeurs')
        self.caracteresIndesirables.place(x=280, y=18, width=50, height=12)

        self.formatEntree =tk.Label(self.cadreDate,text='Format Entrée ')
        self.formatEntree.place(x=260, y=60)

        self.listDate = tk.Listbox(self.cadreDate, state='normal')
        self.listDate.place(x=260, y=80, width=100, height=30)
        self.listDate.insert(tk.END,"AAAA/MM/JJ")
        self.listDate.insert(tk.END,"AAAA/JJ/MM")
        self.listDate.insert(tk.END,"MM/JJ/AAAA")
        self.listDate.insert(tk.END,"MM/AAAA/JJ")
        self.listDate.insert(tk.END,"JJ/MM/AAAA")
        self.listDate.insert(tk.END,"JJ/AAAA/MM")
        self.listDate.configure(state='disabled')

        self.formatDate =tk.Label(self.cadreDate,text='Format Date')
        self.formatDate.place(x=50, y=80)

        self.varDate=tk.IntVar()
        self.checkButtonDate= tk.Checkbutton(self.cadreDate,variable= self.varDate,command=self.unlockDate)
        self.checkButtonDate.place(x=30,y=80)

        #cadreAnonymisation : Anonymisation et Doublon
        self.anonymisation =tk.Label(self.cadreAnonymisation,text='Anonymisation Données')
        self.anonymisation.place(x=50, y=30)

        self.varAnonymisation=tk.IntVar()
        self.checkButtonAnonymisation= tk.Checkbutton(self.cadreAnonymisation,variable= self.varAnonymisation, command=self.unlockAnonymisation )
        self.checkButtonAnonymisation.place(x=30,y=30)

        self.entryAnonymisation = tk.Entry(self.cadreAnonymisation,state='normal')
        self.entryAnonymisation.place(x=260, y=30, width=100, height=25)
        self.entryAnonymisation.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneAnonymisation =tk.Label(self.cadreAnonymisation,text='Colonne')
        self.colonneAnonymisation.place(x=270, y=18, width=70, height=12)

        self.identificationDoublon =tk.Label(self.cadreAnonymisation,text='Identification Doublon')
        self.identificationDoublon.place(x=50, y=80)

        self.varDoublon=tk.IntVar()
        self.checkButtonDoublon= tk.Checkbutton(self.cadreAnonymisation,variable= self.varDoublon,command= self.unlockDoublon)
        self.checkButtonDoublon.place(x=30,y=80)

        self.entryDoublon= tk.Entry(self.cadreAnonymisation, state='normal')
        self.entryDoublon.place(x=260, y=80, width=100, height=25)
        self.entryDoublon.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneDoublon =tk.Label(self.cadreAnonymisation,text='Colonne')
        self.colonneDoublon.place(x=270, y=68, width=70, height=12)


        #cadreFichier : Compilation et Jointure
        self.compilationFichier =tk.Label(self.cadreFichier,text='Compilation Fichier')
        self.compilationFichier.place(x=50, y=20)

        self.varCompilation=tk.IntVar()
        self.checkButtonCompilationFichier= tk.Checkbutton(self.cadreFichier,variable= self.varCompilation, command = self.unlockCompilation)
        self.checkButtonCompilationFichier.place(x=30,y=20)

        self.buttonCompil = tk.Button(self.cadreFichier,state='normal',text='Chargement',bd='4',relief='raised', command=lambda: self.load(1, False))
        self.buttonCompil.place(x=200, y=20, width=100, height=25)
        self.buttonCompil.configure(state='disabled')

        self.listeCompilation = tk.Listbox(self.cadreFichier,state='normal')
        self.listeCompilation.place(x=350, y=30, width=100, height=30)
        self.listeCompilation.configure(state='disabled')

        self.fichiers =tk.Label(self.cadreFichier,text='Fichiers')
        self.fichiers.place(x=370, y=16, width=50, height=12)

        self.jointureFichier =tk.Label(self.cadreFichier,text='Jointure Fichier')
        self.jointureFichier.place(x=50, y=120)

        self.fichiersJointure =tk.Label(self.cadreFichier,text='Fichiers')
        self.fichiersJointure.place(x=370, y=106, width=50, height=12)

        self.listeJointure = tk.Listbox(self.cadreFichier,state='normal')
        self.listeJointure.place(x=350, y=120, width=100, height=30)
        self.listeJointure.configure(state='disabled')

        self.varJointure=tk.IntVar()
        self.checkButtonJointureFichier= tk.Checkbutton(self.cadreFichier,variable= self.varJointure, command=self.unlockJointure)
        self.checkButtonJointureFichier.place(x=30,y=120)

        self.buttonJointure = tk.Button(self.cadreFichier, text='Chargement',bd='4',relief='raised', command=lambda: self.load(2, False))
        self.buttonJointure.place(x=200, y=120, width=100, height=25)
        self.buttonJointure.configure(state='disabled')

        self.jointureFichiersColonne=tk.Label(self.cadreFichier,text='Colonne')
        self.jointureFichiersColonne.place(x=10, y=180)

        self.jointureFichier1 =tk.Label(self.cadreFichier,text='Fichier 1')
        self.jointureFichier1.place(x=110, y=160)

        self.entryJointureFichier1 = tk.Entry(self.cadreFichier, state='normal')
        self.entryJointureFichier1.place(x=90, y=180, width=100, height=25)
        self.entryJointureFichier1.configure(state='disabled',disabledbackground='#E8E8E8')

        self.jointureFichier2 =tk.Label(self.cadreFichier,text='Fichier 2')
        self.jointureFichier2.place(x=240, y=160)

        self.entryJointureFichier2 = tk.Entry(self.cadreFichier,state='normal')
        self.entryJointureFichier2.place(x=220, y=180, width=100, height=25)
        self.entryJointureFichier2.configure(state='disabled',disabledbackground='#E8E8E8')

        self.jointureFichier3 =tk.Label(self.cadreFichier,text='Colonne à ajouter')
        self.jointureFichier3.place(x=340, y=160)

        self.entryJointureFichier3 = tk.Entry(self.cadreFichier,state='normal')
        self.entryJointureFichier3.place(x=350, y=180, width=100, height=25)
        self.entryJointureFichier3.configure(state='disabled',disabledbackground='#E8E8E8')

        #cadreCategorisation : Categorisation
        self.categorisation =tk.Label(self.cadreCategorisation,text='Catégorisation')
        self.categorisation.place(x=50, y=20)

        self.varCategorisation=tk.IntVar()
        self.checkButtonCategorisation= tk.Checkbutton(self.cadreCategorisation,variable= self.varCategorisation, command=self.unlockCategorisation)
        self.checkButtonCategorisation.place(x=30,y=20)

        self.entryColonneCategorisation = tk.Entry(self.cadreCategorisation,state='normal')
        self.entryColonneCategorisation.place(x=50, y=80, width=100, height=25)
        self.entryColonneCategorisation.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneCategorisation =tk.Label(self.cadreCategorisation,text='Colonne')
        self.colonneCategorisation.place(x=60, y=68, width=70, height=12)

        self.entryEntreeCategorisation = tk.Entry(self.cadreCategorisation,state='normal')
        self.entryEntreeCategorisation.place(x=200, y=80, width=100, height=25)
        self.entryEntreeCategorisation.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneCategorisation =tk.Label(self.cadreCategorisation,text='Entrée')
        self.colonneCategorisation.place(x=225, y=68, width=40, height=12)

        self.entrySortieCategorisation = tk.Entry(self.cadreCategorisation,state='normal')
        self.entrySortieCategorisation.place(x=350, y=80, width=100, height=25)
        self.entrySortieCategorisation.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneCategorisation =tk.Label(self.cadreCategorisation,text='Sortie')
        self.colonneCategorisation.place(x=375, y=68, width=40, height=12)

        self.listModeCategorisation = tk.Listbox(self.cadreCategorisation, state='normal')
        self.listModeCategorisation.place(x=250, y=15, width=140, height=40)
        self.listModeCategorisation.insert(tk.END,"Numérique")
        self.listModeCategorisation.insert(tk.END,"Chaine de caractères")
        self.listModeCategorisation.configure(state='disabled')

    #Progressbar
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure("green.Horizontal.TProgressbar",
            foreground='#5A6932', background='#5A6932')
        self.pB = ttk.Progressbar(self.cadre2,orient ="horizontal",length = 700, mode ="determinate",style="green.Horizontal.TProgressbar")
        self.pB.place(x=50,y=601)
        self.pB["maximum"] = 100
        self.pB["value"] = 0

    def start(self):
        if not self.thread.isAlive():
            self.pB["value"] = 0
            self.pB["maximum"] = 100
            self.read_bytes()

    def read_bytes(self):
        self.bytes = self.cleaner.getProgress()
        self.pB["value"] = self.bytes
        if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            time.sleep(0.01)
            self.read_bytes

    #checkButtonDate

    def unlockDate(self):
        if self.listDate['state'] == 'disabled':
            self.listDate.configure(state='normal')
        elif self.listDate['state'] == 'normal' or self.listDate['state'] == 'active':
            self.listDate.configure(state='disabled')

    def unlockCaracteres(self):
        if self.entryCaracteresIndesirables['state'] == 'disabled':
            self.entryCaracteresIndesirables.configure(state='normal')

        elif self.entryCaracteresIndesirables['state'] == 'normal' or self.entryCaracteresIndesirables['state'] == 'active':
            self.entryCaracteresIndesirables.configure(state='disabled')


    def unlockAnonymisation(self):
        if self.entryAnonymisation['state'] == 'disabled':
            self.entryAnonymisation.configure(state='normal')
        elif self.entryAnonymisation['state'] == 'normal' or self.entryAnonymisation['state'] == 'active':
            self.entryAnonymisation.configure(state='disabled')

    def unlockDoublon(self):
        if self.entryDoublon['state'] == 'disabled':
            self.entryDoublon.configure(state='normal')
        elif self.entryDoublon['state'] == 'normal' or self.entryDoublon['state'] == 'active':
            self.entryDoublon.configure(state='disabled')

    def unlockCategorisation(self):
        if self.entryColonneCategorisation['state'] == 'disabled':
            self.entryColonneCategorisation.configure(state='normal')
            self.entryEntreeCategorisation.configure(state='normal')
            self.entrySortieCategorisation.configure(state='normal')
            self.listModeCategorisation.configure(state='normal')
        elif self.entryColonneCategorisation['state'] == 'normal' or self.entryColonneCategorisation['state'] == 'active':
            self.entryColonneCategorisation.configure(state='disabled')
            self.entryEntreeCategorisation.configure(state='disabled')
            self.entrySortieCategorisation.configure(state='disabled')
            self.listModeCategorisation.configure(state='disabled')

    def unlockCompilation(self):
        if self.buttonCompil['state'] == 'disabled':
            self.listeCompilation.configure(state='normal')
            self.buttonCompil.configure(state='normal')
        elif self.buttonCompil['state'] == 'normal' or self.buttonCompil['state'] == 'active':
            self.listeCompilation.configure(state='disabled')
            self.buttonCompil.configure(state='disabled')

    def unlockJointure(self):
        if self.buttonJointure['state'] == 'disabled':
            self.listeJointure.configure(state='normal')
            self.buttonJointure.configure(state='normal')
            self.entryJointureFichier1.configure(state='normal')
            self.entryJointureFichier2.configure(state='normal')
            self.entryJointureFichier3.configure(state='normal')
        elif self.buttonJointure['state'] == 'normal' or self.buttonJointure['state'] == 'active':
            self.listeJointure.configure(state='disabled')
            self.buttonJointure.configure(state='disabled')
            self.entryJointureFichier1.configure(state='disabled')
            self.entryJointureFichier2.configure(state='disabled')
            self.entryJointureFichier3.configure(state='disabled')


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

        if self.varCategorisation.get():
            self.colIndexC = int(self.entryColonneCategorisation.get())
            entryCategorisationKeyString = self.entrySortieCategorisation.get().split(",")
            entryCategorisationValueString = self.entryEntreeCategorisation.get().split(",")
            if self.listModeCategorisation.curselection()[0]==0:
                self.modeCateg='numerical'
            if self.listModeCategorisation.curselection()[0]==1:
                self.modeCateg='substitute'
            if self.modeCateg == 'substitute':
                for i in range(len(entryCategorisationKeyString)):
                    self.changes.update({entryCategorisationKeyString[i]:entryCategorisationValueString[i]})
            else:
                for i in range(len(entryCategorisationKeyString)):
                    self.changes.update({entryCategorisationKeyString[i]:entryCategorisationValueString[i].split(":")})


    #Sauvegarder avec menu
    def save(self):
        self.cleaner.saveWB()

    #Nettoyer
    def clean(self):
        if self.cleaner is None:
            self.cleaner = DC.Cleaner()
        else:
            pass
        self.getParam()
        self.cleaner.openWB(1, self.filename)
        self.thread = threading.Thread()
        self.thread.__init__(target=self.start(), args=())
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
        if self.modeCateg is not None:
            self.cleaner.categorize(self.modeCateg, self.colIndexC, self.changes)
        self.cleaner.purify()
        self.saveas()
        self.resetParam()
        self.resetUI()
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
                    self.buttonChargement.place_forget()
                    self.display()
                if keyLoad == 1:
                    self.listeCompilation.insert(tk.END, name)
                if keyLoad == 2:
                    self.listeJointure.insert(tk.END, name)
        else:
            if args[0].endswith('.csv'):
                self.df = pd.read_csv(args[0])
                self.filename = args[0]
            else:
                self.df = pd.read_excel(args[0])
                self.filename = args[0]
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
        self.colIndexC = None
        self.modeCateg =  None
        self.changes = {}

    def undo(self):
        self.load(None, True, self.cleaner.timeMachine('pullBack'))

    def resetCleaner(self):
        self.load(None, True, self.cleaner.timeMachine('fullReset'))

    def resetUI(self):
        self.entryCaracteresIndesirables.delete(0,tk.END)
        self.entryAnonymisation.delete(0,tk.END)
        self.entryDoublon.delete(0,tk.END)
        self.entryColonneCategorisation.delete(0,tk.END)
        self.entryEntreeCategorisation.delete(0,tk.END)
        self.entrySortieCategorisation.delete(0,tk.END)
        self.listeCompilation.delete(0,tk.END)
        self.listeJointure.delete(0,tk.END)
        self.entryJointureFichier1.delete(0,tk.END)
        self.entryJointureFichier2.delete(0,tk.END)
        self.entryJointureFichier3.delete(0,tk.END)

        self.entryCaracteresIndesirables.configure(state='disabled')
        self.entryAnonymisation.configure(state='disabled')
        self.entryDoublon.configure(state='disabled')
        self.entryColonneCategorisation.configure(state='disabled')
        self.entryEntreeCategorisation.configure(state='disabled')
        self.entrySortieCategorisation.configure(state='disabled')
        self.listeCompilation.configure(state='disabled')
        self.buttonCompil.configure(state='disabled')
        self.listeJointure.configure(state='disabled')
        self.buttonJointure.configure(state='disabled')
        self.entryJointureFichier1.configure(state='disabled')
        self.entryJointureFichier2.configure(state='disabled')
        self.entryJointureFichier3.configure(state='disabled')
        self.listDate.configure(state='disabled')
        self.listModeCategorisation.configure(state='disabled')

        self.varDate.set(0)
        self.varCell.set(0)
        self.varDoublon.set(0)
        self.varJointure.set(0)
        self.varCompilation.set(0)
        self.varAnonymisation.set(0)
        self.varCategorisation.set(0)



    #Afficher sur la zone
    def display(self):
        # ask for file if not loaded yet
            self.text.delete('1.0',tk.END)
            self.text.insert('end', str(self.df.head()) + '\n')

    #Sauvegarder un fichier sous
    def saveas(self):
        newName=tk.filedialog.asksaveasfile(title="Enregistrer sous.. un fichier", filetypes=[('Excel', ('*.xlsx'))])
        self.newPath = newName.name
        if self.colIndexAnonymisation is None:
            self.cleaner.saveWB(1, self.newPath)
        else:
            self.cleaner.saveWB(2, self.newPath)
        self.load(None, True, self.newPath)
        self.cleaner.openWB(1, self.filename)
        self.newPath = None

    #Effacer l'affichage
    def clear(self):
        self.text.delete('1.0',tk.END)


# --- main ---

if __name__ == '__main__':
    parent = tk.Tk()
    parent.eval('lappend auto_path {' +TK_DND_PATH+ '}')
    top = MyWindow(parent)
    parent.mainloop()
