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
#import threading
import pandas as pd
import PFE_UI.UI.filePathGenerator.file as pg  #pathgen as pg
import PFE_UI.UI.operateur as operateur
import sys, os
import time
import PFE_MondoClean.MondoClean.data_Cleaner_Module.data_cleaner as DC #data_Cleaner as DC
import PFE_UI.UI.bar_manager as bm
if getattr(sys, 'frozen', False) and getattr(sys, '_MEIPASS', None):
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
        self.parent.title("Cleaneo")
        self.parent.resizable(width=False,height=False)
        #self.parent.rowconfigure(0, weight=1)
        #self.parent.columnconfigure(0, weight=1)
        self.filename = None
        self.df = None
        self.cleaner = None
        self.dateFormat= None
        self.colIndexDoublon= None
        self.colIndexAnonymisation= None
        self.colIndexApparition = None
        self.colIndexAdditionIdentification = None
        self.colIndexAdditionAssommer = None
        self.banList= None
        self.listeCheminCompil= None
        self.cheminJointure = None
        self.colComp1 = None
        self.colComp2 = None
        self.colJoints = None
        self.colIndexC = None
        self.modeCateg = None
        self.newPath = None
        self.changes = {}
        self.bytes=0
        self.maxbytes = 100

        self.frame = tk.Frame(self.parent, bg='white', width=1200, height=800)
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
        self.menufichier.add_command(label="Quitter",command=self.parent.destroy)


        #Deux grands Panels
        self.cadre4 = tk.PanedWindow(self.frame, bg='white', width=200, height=70)
        self.cadre4.pack(side=tk.TOP, fill='both')
        self.cadre3 = tk.PanedWindow(self.frame, bg='#5E5455', width=200, height=5)
        self.cadre3.pack(side=tk.TOP, fill='both')
        self.cadre6 = tk.PanedWindow(self.frame, bg='#5E5455', width=200, height=20)
        self.cadre6.pack(side=tk.TOP, fill='both')
        self.cadre5 = tk.PanedWindow(self.frame, bg='white', width=200, height=95)
        self.cadre5.pack(side=tk.BOTTOM, fill='both')
        self.cadre1 = tk.PanedWindow(self.frame, bg='white', width=1380, height=460)
        self.cadre1.pack(side =tk.LEFT, fill='both')
        self.cadre1.pack_propagate(0)




        #Petits panels du Panel cadre1
        self.cadreFichier =tk.PanedWindow(self.cadre1,width= 865, height= 290, bd= 2, relief = 'sunken')
        self.cadreFichier.place(x=10,y=160)
        self.cadreFichier.pack_propagate(0)

        self.cadreDate =tk.PanedWindow(self.cadre1,width= 450, height= 150, bd= 2, relief = 'sunken')
        self.cadreDate.place(x=10,y=5)
        self.cadreDate.pack_propagate(0)

        self.cadreAddition =tk.PanedWindow(self.cadre1,width= 460, height= 200, bd= 2, relief = 'sunken')
        self.cadreAddition.place(x=900,y=5)
        self.cadreAddition.pack_propagate(0)

        self.cadreAnonymisation =tk.PanedWindow(self.cadre1,width= 405, height= 150, bd= 2, relief = 'sunken')
        self.cadreAnonymisation.place(x=470,y=5)
        self.cadreAnonymisation.pack_propagate(0)

        self.cadreCategorisation =tk.PanedWindow(self.cadre1,width= 460, height= 210, bd= 2, relief = 'sunken')
        self.cadreCategorisation.place(x=900,y=240)
        self.cadreCategorisation.pack_propagate(0)

        #Titre panel paramètres
        self.labelTitreCadre1 = tk.Label(self.cadre6,text='Traitement et Paramètres',justify='center',width=71, bg='#5E5455',fg='white')
        self.labelTitreCadre1.place(x=390, y=0)

        #Image Doshas
        self.im=Image.open(self.dirPath+"filePathGenerator/images/LogoDoshas.JPG")
        self.photo=ImageTk.PhotoImage(self.im)
        self.labelDoshas=tk.Label(self.cadre4,image=self.photo, bg='white')
        self.labelDoshas.place(x=625, y=0, width=150 ,height=52)

        self.nomFichierLabel = tk.Label(self.cadre4, text='Fichier Principal: ')
        self.nomFichierLabel.place(x=0 ,y=50)

        self.varNomFichier = tk.StringVar()
        self.nomFichier = tk.Label(self.cadre4,fg='#5E5455',textvariable = self.varNomFichier)
        self.nomFichier.place(x=110 ,y=50)

        #Control panel (Clean/Reset/PullBack)
        self.play=Image.open(self.dirPath+"filePathGenerator/images/play.JPG")
        self.photoPlay=ImageTk.PhotoImage(self.play)
        self.button = tk.Button(self.cadre5,image=self.photoPlay, bg='white',command=self.clean, state='disabled')
        self.button.place(x=690, y=23, width=50, height=50)
        self.labelNettoyer = tk.Label(self.cadre5, text='Lancer le(s) traitement(s)', bg='white')
        self.labelNettoyer.place(x=630,y=73)

        self.pullBack=Image.open(self.dirPath+"filePathGenerator/images/retour.JPG")
        self.photoPullBack=ImageTk.PhotoImage(self.pullBack)
        self.buttonPullBack = tk.Button(self.cadre5,image=self.photoPullBack,command=self.undo, state='disabled')
        self.buttonPullBack.place(x=100, y=23, width=50, height=50)
        self.labelRetour = tk.Label(self.cadre5, text='Retour', bg='white')
        self.labelRetour.place(x=110,y=73)

        self.reset=Image.open(self.dirPath+"filePathGenerator/images/resetV1.JPG")
        self.photoReset=ImageTk.PhotoImage(self.reset)
        self.buttonReset = tk.Button(self.cadre5, bg='white',image=self.photoReset,command=self.resetCleaner, state='disabled')
        self.buttonReset.place(x=1200, y=23, width=50, height=50)
        self.labelReset = tk.Label(self.cadre5, text='Réinitialiser', bg='white')
        self.labelReset.place(x=1190,y=73)


        #Zone d'affichage
        self.text = tk.Text(self.cadre3,bg='white', width=196, height=5.5,bd =2, wrap='none')
        #scrollbar
        self.scrollbar = tk.Scrollbar(self.cadre3,orient='horizontal', command= self.text.xview)
        self.text['xscrollcommand'] = self.scrollbar.set
        self.scrollbar.grid(row=1, column=0, sticky = "ew")
        self.text.grid(row=0, column=0)


        #bouton Chargement
        self.buttonChargement = tk.Button(self.text, text='Importer un Fichier',bd='4',relief='raised',highlightcolor='black', command=lambda: self.load(0, False))
        self.buttonChargement.place(x=600, y=20, width=200, height=50)


        #cadreDate : Date,nombre,cellules vides
        self.banChar =tk.Label(self.cadreDate,text='Supprimer des Caractères Indésirables', fg ='#B04334')
        self.banChar.place(x=50, y=10)

        self.varCell=tk.IntVar()
        self.checkButtonCellule= tk.Checkbutton(self.cadreDate,variable= self.varCell,command=self.unlockCaracteres, state='disabled')
        self.checkButtonCellule.place(x=20,y=8)

        self.entryCaracteresIndesirables= tk.Entry(self.cadreDate,state='normal')
        self.entryCaracteresIndesirables.place(x=300, y=40,  width=140, height=25)
        self.entryCaracteresIndesirables.configure(state='disabled',disabledbackground='#E8E8E8')

        self.caracteresIndesirables= tk.Label(self.cadreDate, text='Valeurs')
        self.caracteresIndesirables.place(x=55, y=45, width=50, height=12)

        self.formatEntree =tk.Label(self.cadreDate,text='Format Entrée des dates ')
        self.formatEntree.place(x=35, y=110, width=200, height=12)

        self.cadreListDate = tk.PanedWindow(self.cadreDate)
        self.cadreListDate.place(x=390 ,y=85,width=50, height=52)
        self.listDate = tk.Listbox(self.cadreDate, state='normal')
        self.listDate.insert(tk.END,"AAAAMMJJ")
        self.listDate.insert(tk.END,"AAAAJJMM")
        self.listDate.insert(tk.END,"MMJJAAAA")
        self.listDate.insert(tk.END,"MMAAAAJJ")
        self.listDate.insert(tk.END,"JJMMAAAA")
        self.listDate.insert(tk.END,"JJAAAAMM")
        self.listDate.configure(state='disabled', exportselection=False, width=10, height=3)
        self.scrollbarListDate = tk.Scrollbar(self.cadreListDate,orient='vertical', command= self.listDate.yview)
        self.listDate['yscrollcommand'] = self.scrollbarListDate.set
        self.scrollbarListDate.grid(row=0, column=1, sticky = None)
        self.listDate.place(x=303, y=85)

        self.formatDate =tk.Label(self.cadreDate,text='Formater des Dates', fg ='#B04334')
        self.formatDate.place(x=50, y=80)

        self.varDate=tk.IntVar()
        self.checkButtonDate= tk.Checkbutton(self.cadreDate,variable= self.varDate,command=self.unlockDate, state='disabled')
        self.checkButtonDate.place(x=20,y=78)

        #cadreAnonymisation : Anonymisation et Doublon
        self.anonymisation =tk.Label(self.cadreAnonymisation,text='Anonymiser des données', fg ='#B04334')
        self.anonymisation.place(x=50, y=10)

        self.varAnonymisation=tk.IntVar()
        self.checkButtonAnonymisation= tk.Checkbutton(self.cadreAnonymisation,variable= self.varAnonymisation, command=self.unlockAnonymisation, state='disabled')
        self.checkButtonAnonymisation.place(x=20,y=10)

        self.entryAnonymisation = tk.Entry(self.cadreAnonymisation,state='normal')
        self.entryAnonymisation.place(x=250, y=45, width=140, height=25)
        self.entryAnonymisation.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneAnonymisation =tk.Label(self.cadreAnonymisation,text='N°Colonne(s) à anonymiser')
        self.colonneAnonymisation.place(x=40, y=50, width=180, height=12)

        self.identificationDoublon =tk.Label(self.cadreAnonymisation,text='Identifier des Doublons', fg ='#B04334')
        self.identificationDoublon.place(x=50, y=80)

        self.varDoublon=tk.IntVar()
        self.checkButtonDoublon= tk.Checkbutton(self.cadreAnonymisation,variable= self.varDoublon,command= self.unlockDoublon, state='disabled')
        self.checkButtonDoublon.place(x=20,y=78)

        self.entryDoublon= tk.Entry(self.cadreAnonymisation, state='normal')
        self.entryDoublon.place(x=250, y=115, width=140, height=25)
        self.entryDoublon.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneDoublon =tk.Label(self.cadreAnonymisation,text='N°Colonne(s) à traiter')
        self.colonneDoublon.place(x=25, y=120, width=180, height=12)

        #cadreAnonymisation : Compter et sommer
        self.apparitionValeur =tk.Label(self.cadreAddition,text='Compter des valeurs', fg ='#B04334')
        self.apparitionValeur.place(x=50, y=10)

        self.varApparition=tk.IntVar()
        self.checkApparitionValeur= tk.Checkbutton(self.cadreAddition,variable= self.varApparition,command= self.unlockApparition, state='disabled')
        self.checkApparitionValeur.place(x=20,y=8)

        self.entryApparition= tk.Entry(self.cadreAddition, state='normal')
        self.entryApparition.place(x=250, y=45, width=140, height=25)
        self.entryApparition.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneApparition =tk.Label(self.cadreAddition,text='N°Colonne(s) à traiter')
        self.colonneApparition.place(x=20, y=50, width=180, height=12)

        self.additionValeur =tk.Label(self.cadreAddition,text='Sommer des valeurs', fg ='#B04334')
        self.additionValeur.place(x=50, y=80)

        self.varAddition=tk.IntVar()
        self.checkAdditionValeur= tk.Checkbutton(self.cadreAddition,variable= self.varAddition,command= self.unlockAddition, state='disabled')
        self.checkAdditionValeur.place(x=20,y=78)

        self.entryAdditionIdentification = tk.Entry(self.cadreAddition, state='normal')
        self.entryAdditionIdentification.place(x=250, y=115, width=140, height=25)
        self.entryAdditionIdentification.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneAdditionIdentification =tk.Label(self.cadreAddition,text='N°Colonne à traiter')
        self.colonneAdditionIdentification.place(x=15, y=120, width=180, height=12)

        self.entryAdditionAssommer = tk.Entry(self.cadreAddition, state='normal')
        self.entryAdditionAssommer.place(x=250, y=145, width=140, height=25)
        self.entryAdditionAssommer.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneAdditionAssommer =tk.Label(self.cadreAddition,text='N°Colonne à sommer')
        self.colonneAdditionAssommer.place(x=20, y=150, width=180, height=12)


        #cadreFichier : Compilation et Jointure
        self.compilationFichier =tk.Label(self.cadreFichier,text='Compiler des Fichiers', fg ='#B04334')
        self.compilationFichier.place(x=50, y=30)

        self.varCompilation=tk.IntVar()
        self.checkButtonCompilationFichier= tk.Checkbutton(self.cadreFichier,variable= self.varCompilation, command = self.unlockCompilation, state='disabled')
        self.checkButtonCompilationFichier.place(x=20,y=28)

        self.buttonCompil = tk.Button(self.cadreFichier,state='normal',text='Importer un Fichier',bd='4',relief='raised', command=lambda: self.load(1, False))
        self.buttonCompil.place(x=300, y=30, width=140, height=25)
        self.buttonCompil.configure(state='disabled')

        self.resetCompil=Image.open(self.dirPath+"filePathGenerator/images/resetCompilV2.JPG")
        self.photoResetCompil=ImageTk.PhotoImage(self.resetCompil)
        self.buttonResetCompil = tk.Button(self.cadreFichier,image=self.photoResetCompil,state='normal',text='Reset',bd='4',relief='raised', command = self.resetListCompil)
        self.buttonResetCompil.place(x=440, y=35, width=20, height=20)
        self.buttonResetCompil.configure(state='disabled')

        self.listeCompilation = tk.Listbox(self.cadreFichier,state='normal')
        self.listeCompilation.place(x=200, y=64, width=550, height=40)
        self.listeCompilation.configure(state='disabled')

        self.fichiers =tk.Label(self.cadreFichier,text='Fichier(s) à compiler')
        self.fichiers.place(x=50, y=80, width=140, height=12)

        self.jointureFichier =tk.Label(self.cadreFichier,text='Réaliser une Jointure de fichiers', fg ='#B04334')
        self.jointureFichier.place(x=50, y=120)

        self.fichiersJointure =tk.Label(self.cadreFichier,text='Fichier à ajouter')
        self.fichiersJointure.place(x=45, y=160, width=120, height=12)

        self.listeJointure = tk.Listbox(self.cadreFichier,state='normal')
        self.listeJointure.place(x=200, y=150, width=550, height=30)
        self.listeJointure.configure(state='disabled')

        self.varJointure=tk.IntVar()
        self.checkButtonJointureFichier= tk.Checkbutton(self.cadreFichier,variable= self.varJointure, command=self.unlockJointure, state='disabled')
        self.checkButtonJointureFichier.place(x=20,y=118)

        self.buttonJointure = tk.Button(self.cadreFichier, text='Importer un Fichier',bd='4',relief='raised', command=lambda: self.load(2, False))
        self.buttonJointure.place(x=300, y=120, width=140, height=25)
        self.buttonJointure.configure(state='disabled')

        self.jointureFichier1 =tk.Label(self.cadreFichier,text='Fichier 1 - N° Colonne à matcher')
        self.jointureFichier1.place(x=50, y=195)

        self.entryJointureFichier1 = tk.Entry(self.cadreFichier, state='normal')
        self.entryJointureFichier1.place(x=300, y=195, width=140, height=25)
        self.entryJointureFichier1.configure(state='disabled',disabledbackground='#E8E8E8')

        self.jointureFichier2 =tk.Label(self.cadreFichier,text='Fichier 2 - N° Colonne à matcher')
        self.jointureFichier2.place(x=50, y=225)

        self.entryJointureFichier2 = tk.Entry(self.cadreFichier,state='normal')
        self.entryJointureFichier2.place(x=300, y=225, width=140, height=25)
        self.entryJointureFichier2.configure(state='disabled',disabledbackground='#E8E8E8')

        self.jointureFichier3 =tk.Label(self.cadreFichier,text='Fichier 2 - N° Colonne(s) à ajouter')
        self.jointureFichier3.place(x=50, y=255)

        self.entryJointureFichier3 = tk.Entry(self.cadreFichier,state='normal')
        self.entryJointureFichier3.place(x=300, y=255, width=140, height=25)
        self.entryJointureFichier3.configure(state='disabled',disabledbackground='#E8E8E8')

        #cadreCategorisation : Categorisation
        self.categorisation =tk.Label(self.cadreCategorisation,text='Catégoriser des données', fg ='#B04334')
        self.categorisation.place(x=50, y=10)

        self.varCategorisation=tk.IntVar()
        self.checkButtonCategorisation= tk.Checkbutton(self.cadreCategorisation,variable= self.varCategorisation, command=self.unlockCategorisation, state='disabled')
        self.checkButtonCategorisation.place(x=20,y=8)

        self.entryColonneCategorisation = tk.Entry(self.cadreCategorisation,state='normal')
        self.entryColonneCategorisation.place(x=250, y=95, width=140, height=25)
        self.entryColonneCategorisation.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneCategorisation =tk.Label(self.cadreCategorisation,text='N°Colonne à catégoriser')
        self.colonneCategorisation.place(x=30, y=100, width=200, height=12)

        self.entryEntreeCategorisation = tk.Entry(self.cadreCategorisation,state='normal')
        self.entryEntreeCategorisation.place(x=250, y=125, width=140, height=25)
        self.entryEntreeCategorisation.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneCategorisation =tk.Label(self.cadreCategorisation,text='Valeur(s) Entrée')
        self.colonneCategorisation.place(x=50, y=130, width=110, height=12)

        self.entrySortieCategorisation = tk.Entry(self.cadreCategorisation,state='normal')
        self.entrySortieCategorisation.place(x=250, y=155, width=140, height=25)
        self.entrySortieCategorisation.configure(state='disabled',disabledbackground='#E8E8E8')

        self.colonneCategorisation =tk.Label(self.cadreCategorisation,text='Valeur(s) Sortie')
        self.colonneCategorisation.place(x=50, y=160, width=110, height=12)

        self.colonneTypeDonnees =tk.Label(self.cadreCategorisation,text='Type de données')
        self.colonneTypeDonnees.place(x=35, y=55, width=140, height=12)

        self.listModeCategorisation = tk.Listbox(self.cadreCategorisation, state='normal')
        self.listModeCategorisation.place(x=250, y=45, width=140, height=40)
        self.listModeCategorisation.insert(tk.END,"Numérique")
        self.listModeCategorisation.insert(tk.END,"Chaine de caractères")
        self.listModeCategorisation.configure(state='disabled',exportselection=False)

    #Progressbar
        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure("green.Horizontal.TProgressbar",
            foreground='#5A6932', background='#5A6932')
        self.varBar = tk.DoubleVar()
        self.pB = ttk.Progressbar(self.cadre5, variable=self.varBar, orient="horizontal", length=1500, mode="determinate", style="green.Horizontal.TProgressbar")
        self.pB.place(x=0,y=0)
        self.pB["maximum"] = 100
        self.pB["value"] = 0

    #checkButtonDate

    def unlockDate(self):
        if self.listDate['state'] == 'disabled':
            self.listDate.configure(state='normal')
            self.formatDate.configure(fg='#5A6932')
        elif self.listDate['state'] == 'normal' or self.listDate['state'] == 'active':
            self.listDate.configure(state='disabled')
            self.formatDate.configure(fg='#B04334')

    def unlockCaracteres(self):
        if self.entryCaracteresIndesirables['state'] == 'disabled':
            self.entryCaracteresIndesirables.configure(state='normal')
            self.banChar.configure(fg='#5A6932')
        elif self.entryCaracteresIndesirables['state'] == 'normal' or self.entryCaracteresIndesirables['state'] == 'active':
            self.entryCaracteresIndesirables.configure(state='disabled')
            self.banChar.configure(fg='#B04334')


    def unlockAnonymisation(self):
        if self.entryAnonymisation['state'] == 'disabled':
            self.entryAnonymisation.configure(state='normal')
            self.anonymisation.configure(fg='#5A6932')
        elif self.entryAnonymisation['state'] == 'normal' or self.entryAnonymisation['state'] == 'active':
            self.entryAnonymisation.configure(state='disabled')
            self.anonymisation.configure(fg='#B04334')

    def unlockDoublon(self):
        if self.entryDoublon['state'] == 'disabled':
            self.entryDoublon.configure(state='normal')
            self.identificationDoublon.configure(fg='#5A6932')
        elif self.entryDoublon['state'] == 'normal' or self.entryDoublon['state'] == 'active':
            self.entryDoublon.configure(state='disabled')
            self.identificationDoublon.configure(fg='#B04334')

    def unlockApparition(self):
        if self.entryApparition['state'] =='disabled':
            self.entryApparition.configure(state ='normal')
            self.apparitionValeur.configure(fg='#5A6932')
        elif self.entryApparition['state'] =='normal' or self.entryApparition['state'] =='active':
            self.entryApparition.configure(state='disabled')
            self.apparitionValeur.configure(fg='#B04334')

    def unlockAddition(self):
        if self.entryAdditionIdentification['state'] == 'disabled':
            self.entryAdditionIdentification.configure(state = 'normal')
            self.entryAdditionAssommer.configure(state = 'normal')
            self.additionValeur.configure(fg='#5A6932')
        elif self.entryAdditionIdentification['state'] == 'normal' or self.entryAdditionIdentification['state'] == 'active':
            self.entryAdditionIdentification.configure(state='disabled')
            self.entryAdditionAssommer.configure(state = 'disabled')
            self.additionValeur.configure(fg='#B04334')

    def unlockCategorisation(self):
        if self.entryColonneCategorisation['state'] == 'disabled':
            self.entryColonneCategorisation.configure(state='normal')
            self.entryEntreeCategorisation.configure(state='normal')
            self.entrySortieCategorisation.configure(state='normal')
            self.listModeCategorisation.configure(state='normal')
            self.categorisation.configure(fg='#5A6932')
        elif self.entryColonneCategorisation['state'] == 'normal' or self.entryColonneCategorisation['state'] == 'active':
            self.entryColonneCategorisation.configure(state='disabled')
            self.entryEntreeCategorisation.configure(state='disabled')
            self.entrySortieCategorisation.configure(state='disabled')
            self.listModeCategorisation.configure(state='disabled')
            self.categorisation.configure(fg='#B04334')

    def unlockCompilation(self):
        if self.buttonCompil['state'] == 'disabled':
            self.listeCompilation.configure(state='normal')
            self.buttonCompil.configure(state='normal')
            self.buttonResetCompil.configure(state = 'normal')
            self.compilationFichier.configure(fg='#5A6932')
        elif self.buttonCompil['state'] == 'normal' or self.buttonCompil['state'] == 'active':
            self.listeCompilation.configure(state='disabled')
            self.buttonCompil.configure(state='disabled')
            self.buttonResetCompil.configure(state = 'disabled')
            self.compilationFichier.configure(fg='#B04334')

    def unlockJointure(self):
        if self.buttonJointure['state'] == 'disabled':
            self.listeJointure.configure(state='normal')
            self.buttonJointure.configure(state='normal')
            self.entryJointureFichier1.configure(state='normal')
            self.entryJointureFichier2.configure(state='normal')
            self.entryJointureFichier3.configure(state='normal')
            self.jointureFichier.configure(fg='#5A6932')
        elif self.buttonJointure['state'] == 'normal' or self.buttonJointure['state'] == 'active':
            self.listeJointure.configure(state='disabled')
            self.buttonJointure.configure(state='disabled')
            self.entryJointureFichier1.configure(state='disabled')
            self.entryJointureFichier2.configure(state='disabled')
            self.entryJointureFichier3.configure(state='disabled')
            self.jointureFichier.configure(fg='#B04334')


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

        if self.varApparition.get():
            entryApparitionString = self.entryApparition.get().split(",")
            self.colIndexApparition = [int(s) for s in entryApparitionString]

        if self.varAddition.get():
            entryAdditionIdentificationString = self.entryAdditionIdentification.get().split(",")
            self.colIndexAdditionIdentification = [int(s) for s in entryAdditionIdentificationString]
            entryAdditionAssommerString = self.entryAdditionAssommer.get()
            self.colIndexAdditionAssommer = int(entryAdditionAssommerString)

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
            barManager = bm.BarManager(self, self.cleaner)
            barManager.start()
        else:
            pass
        self.getParam()
        self.feedback('Initialisation des traitements..')
        operator = operateur.Operateur(self, self.cleaner, self.filename, self.banList, self.dateFormat,
                            self.colIndexDoublon, self.colIndexAnonymisation, self.listeCheminCompil, self.cheminJointure, self.colComp1,
                            self.colComp2, self.colJoints, self.modeCateg, self.colIndexC, self.changes, self.newPath, self.colIndexApparition,
                            self.colIndexAdditionIdentification, self.colIndexAdditionAssommer)
        operator.setMod('clean')
        operator.start()



    #Charger un fichier
    def load(self, keyLoad, update, *args):
        if update == False:
            name = askopenfilename(filetypes=[('Excel', ('*.xls', '*.xlsx'))])
            if name:
                if keyLoad == 0:
                    if name.endswith('.csv'):
                        self.feedback('Ouverture du fichier...')
                        self.df = pd.read_csv(name)
                    else:
                        self.feedback('Ouverture du fichier...')
                        self.df = pd.read_excel(name)
                    self.filename = name
                    self.varNomFichier.set(self.filename)
                    self.buttonChargement.place_forget()
                    self.enableCheckButtons()
                    self.display()
                if keyLoad == 1:
                    self.listeCompilation.insert(tk.END, name)
                if keyLoad == 2:
                    self.listeJointure.delete(0, tk.END)
                    self.listeJointure.insert(tk.END, name)

        else:
            self.feedback('Chargement du nouveau fichier...')
            if args[0].endswith('.csv'):
                self.df = pd.read_csv(args[0])
                self.filename = args[0]
                self.varNomFichier.set(self.filename)
            else:
                self.df = pd.read_excel(args[0])
                self.filename = args[0]
                self.varNomFichier.set(self.filename)
            self.display()

    def enableCheckButtons(self):
        self.checkButtonCellule.configure(state='normal')
        self.checkButtonDate.configure(state='normal')
        self.checkButtonDoublon.configure(state='normal')
        self.checkButtonAnonymisation.configure(state='normal')
        self.checkButtonCategorisation.configure(state='normal')
        self.checkButtonCompilationFichier.configure(state='normal')
        self.checkButtonJointureFichier.configure(state='normal')
        self.checkAdditionValeur.configure(state='normal')
        self.checkApparitionValeur.configure(state='normal')
        self.button.configure(state='normal')
        self.buttonReset.configure(state='normal')
        self.buttonPullBack.configure(state='normal')
    #Reset Paramètres
    def resetParam(self):
        self.dateFormat= None
        self.colIndexDoublon= None
        self.colIndexAnonymisation= None
        self.colIndexApparition = None
        self.colIndexAdditionIdentification = None
        self.colIndexAdditionAssommer = None
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
        self.entryApparition.delete(0,tk.END)
        self.entryAdditionIdentification.delete(0,tk.END)
        self.entryAdditionAssommer.delete(0,tk.END)
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
        self.entryApparition.configure(state='disabled')
        self.entryAdditionIdentification.configure(state='disabled')
        self.entryAdditionAssommer.configure(state='disabled')
        self.entryColonneCategorisation.configure(state='disabled')
        self.entryEntreeCategorisation.configure(state='disabled')
        self.entrySortieCategorisation.configure(state='disabled')
        self.listeCompilation.configure(state='disabled')
        self.buttonCompil.configure(state='disabled')
        self.buttonResetCompil.configure(state='disabled')
        self.listeJointure.configure(state='disabled')
        self.buttonJointure.configure(state='disabled')
        self.entryJointureFichier1.configure(state='disabled')
        self.entryJointureFichier2.configure(state='disabled')
        self.entryJointureFichier3.configure(state='disabled')
        self.listDate.configure(state='disabled')
        self.listModeCategorisation.configure(state='disabled')

        self.formatDate.configure(fg='#B04334')
        self.banChar.configure(fg='#B04334')
        self.anonymisation.configure(fg='#B04334')
        self.identificationDoublon.configure(fg='#B04334')
        self.apparitionValeur.configure(fg='#B04334')
        self.additionValeur.configure(fg='#B04334')
        self.categorisation.configure(fg='#B04334')
        self.compilationFichier.configure(fg='#B04334')
        self.jointureFichier.configure(fg='#B04334')


        self.varDate.set(0)
        self.varCell.set(0)
        self.varDoublon.set(0)
        self.varJointure.set(0)
        self.varCompilation.set(0)
        self.varAnonymisation.set(0)
        self.varApparition.set(0)
        self.varAddition.set(0)
        self.varCategorisation.set(0)
        self.varNomFichier.set('')



    #Afficher sur la zone
    def display(self):
            self.text.delete('1.0',tk.END)
            pd.set_option('expand_frame_repr', False)
            content = str(self.df.head()).replace('NaN', '   ')
            content = content.replace('NaT', '   ')
            self.text.insert('end', content )

    #Sauvegarder un fichier sous
    def saveas(self):
        newName=tk.filedialog.asksaveasfile(title="Enregistrer sous.. un fichier", filetypes=[('Excel', ('*.xlsx'))])
        if '.xlsx' in newName.name:
            self.newPath = newName.name
        elif '.csv' in newName.name:
            self.newPath = newName.name.replace('.csv','.xlsx')
        else:
            self.newPath = newName.name+'.xlsx'
        print(self.newPath)
        operator = operateur.Operateur(self, self.cleaner, self.filename, self.banList, self.dateFormat,
                            self.colIndexDoublon, self.colIndexAnonymisation, self.listeCheminCompil, self.cheminJointure, self.colComp1,
                            self.colComp2, self.colJoints, self.modeCateg, self.colIndexC, self.changes, self.newPath,
                            self.colIndexApparition, self.colIndexAdditionIdentification, self.colIndexAdditionAssommer)
        operator.setMod('save')
        operator.start()

    #Effacer l'affichage
    def clear(self):
        self.text.delete('1.0',tk.END)

    def setBarValue(self, value):
        self.varBar.set(value)
        self.parent.update_idletasks()

    def feedback(self, text):
        self.text.delete('1.0',tk.END)
        self.text.insert('end', text)

    def resetListCompil(self):
        self.listeCompilation.delete(0, tk.END)

# --- main ---

if __name__ == '__main__':
    parent = tk.Tk()
    parent.eval('lappend auto_path {' +TK_DND_PATH+ '}')
    top = MyWindow(parent)
    parent.mainloop()
