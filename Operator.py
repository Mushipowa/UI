from threading import Thread
import PFE_MondoClean.MondoClean.data_Cleaner_Module.data_Cleaner as DC  #data_Cleaner as DC

class Operator(Thread):

    def __init__(self, ui, cleaner, filename, banList, dateFormat, colIndexDoublon,
                colIndexAnonymisation, listeCheminCompil, cheminJointure, colComp1,
                colComp2, colJoints, modeCateg, colIndexC, changes, newPath):
        Thread.__init__(self)
        self.ui = ui
        self.cleaner = cleaner
        self.filename = filename
        self.banList = banList
        self.dateFormat = dateFormat
        self.colIndexDoublon = colIndexDoublon
        self.colIndexAnonymisation = colIndexAnonymisation
        self.listeCheminCompil = listeCheminCompil
        self.cheminJointure = cheminJointure
        self.colComp1 = colComp1
        self.colComp2 = colComp2
        self.colJoints = colJoints
        self.modeCateg = modeCateg
        self.colIndexC = colIndexC
        self.changes = changes
        self.newPath = newPath
        self.key = None
        self.daemon = True

    def run(self):
        if self.key == 'clean':
            self.cleaner.openWB(1, self.filename)
            if self.banList is not None:
                self.cleaner.param(self.banList)
            self.ui.feedback('Purification...')
            self.cleaner.purify()
            if self.dateFormat is not None:
                self.ui.feedback('Formattage des dates...')
                self.cleaner.changeDate(self.dateFormat)
            if self.colIndexDoublon is not None:
                self.ui.feedback('Identification des doublons...')
                self.cleaner.doublons(self.colIndexDoublon)
            if self.colIndexAnonymisation is not None:
                self.ui.feedback('Anonymisation des données...')
                self.cleaner.anonymize(self.colIndexAnonymisation)
            if self.listeCheminCompil is not None:
                self.ui.feedback('Compilation...')
                self.cleaner.aggreg(self.listeCheminCompil)
            if self.cheminJointure is not None:
                self.ui.feedback('Jointure des données...')
                self.cleaner.joint(self.cheminJointure, self.colComp1, self.colComp2, self.colJoints)
            if self.modeCateg is not None:
                self.ui.feedback('Catégorisation des données...')
                self.cleaner.categorize(self.modeCateg, self.colIndexC, self.changes)
            self.cleaner.purify()
            self.callBackUI()
        if self.key == 'save':
            if self.colIndexAnonymisation is None:
                self.ui.feedback('Sauvegarde en cours...')
                self.cleaner.saveWB(1, self.newPath)
            else:
                self.ui.feed('Sauvegarde en cours...')
                self.cleaner.saveWB(2, self.newPath)
            self.cleaner.openWB(1, self.newPath)
            self.callBackUI()

    def setMod(self, key):
        self.key = key

    def callBackUI(self):
        if self.key == 'clean':
            self.ui.saveas()
            self.ui.resetParam()
            self.ui.resetUI()
            self.ui.display()
        if self.key == 'save':
            self.ui.load(None, True, self.newPath)
            self.ui.newPath = None
