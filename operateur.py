# -*- coding: UTF-8 -*-
__author__      = "Masson Charles, Pelloux Maxence"
__copyright__   = "Copyright 2018, Masson Charles & Pelloux Maxence"

from threading import Thread
import PFE_MondoClean.MondoClean.data_Cleaner_Module.data_cleaner as DC  #data_Cleaner as DC

class Operateur(Thread):

    def __init__(self, ui, cleaner, filename, banList, dateFormat, colIndexDoublon,
                colIndexAnonymisation, listeCheminCompil, cheminJointure, colComp1,
                colComp2, colJoints, modeCateg, colIndexC, changes, newPath, colIndexApparition, colIndexAdditionIdentification, colIndexAdditionAssommer):
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
        self.colIndexApparition = colIndexApparition
        self.colIndexAdditionIdentification = colIndexAdditionIdentification
        self.colIndexAdditionAssommer = colIndexAdditionAssommer
        self.key = None
        self.daemon = True

    def run(self):
        if self.key == 'clean':
            self.ui.clear()
            self.ui.feedback('Initialisation des traitements..')
            self.ui.feedback(self.cleaner.openWB(1, self.filename))
            if self.listeCheminCompil is not None:
                self.ui.feedback('Compilation...')
                self.ui.feedback(self.cleaner.aggreg(self.listeCheminCompil))
            if self.banList is not None:
                self.ui.feedback(self.cleaner.param(self.banList))
            self.ui.feedback('Purification...')
            self.ui.feedback(self.cleaner.purify())
            if self.dateFormat is not None:
                self.ui.feedback('Formattage des dates...')
                self.ui.feedback(self.cleaner.changeDate(self.dateFormat))
            self.ui.feedback('Formattage des nombres...')
            self.ui.feedback(self.cleaner.formatNumbers())
            if self.cheminJointure is not None:
                self.ui.feedback('Jointure des données...')
                self.ui.feedback(self.cleaner.joint(self.cheminJointure, self.colComp1, self.colComp2, self.colJoints))
            self.ui.feedback('Formattage des nombres...')
            self.ui.feedback(self.cleaner.formatNumbers())
            if self.colIndexAnonymisation is not None:
                self.ui.feedback('Anonymisation des données...')
                self.ui.feedback(self.cleaner.anonymize(self.colIndexAnonymisation))
            if self.modeCateg is not None:
                self.ui.feedback('Catégorisation des données...')
                self.ui.feedback(self.cleaner.categorize(self.modeCateg, self.colIndexC, self.changes))
            if self.colIndexApparition is not None:
                self.ui.feedback('Calcul apparition des valeurs...')
                self.ui.feedback(self.cleaner.count(self.colIndexApparition))
            if self.colIndexAdditionIdentification is not None:
                self.ui.feedback('Addition des valeurs...')
                self.ui.feedback(self.cleaner.summ(self.colIndexAdditionIdentification, self.colIndexAdditionAssommer))
            if self.colIndexDoublon is not None:
                self.ui.feedback('Identification des doublons...')
                self.ui.feedback(self.cleaner.doublons(self.colIndexDoublon))
            self.ui.feedback(self.cleaner.addIndex())
            self.ui.feedback('Purification...')
            self.ui.feedback(self.cleaner.purify())
            if self.banList is not None:
                self.ui.feedback(self.cleaner.resetBanned())
            self.callBackUI()
        if self.key == 'save':
            if self.colIndexAnonymisation is None:
                self.ui.feedback('Sauvegarde en cours...')
                self.ui.feedback(self.cleaner.saveWB(1, self.newPath))
            else:
                self.ui.feedback('Sauvegarde en cours...')
                self.ui.feedback(self.cleaner.saveWB(2, self.newPath))
            self.ui.feedback(self.cleaner.openWB(1, self.newPath))
            self.callBackUI()

    def setMod(self, key):
        self.key = key

    def callBackUI(self):
        if self.key == 'clean':
            self.ui.resetUI()
            self.ui.saveas()
            self.ui.resetParam()
        if self.key == 'save':
            self.ui.load(None, 'history_CLEAN', self.newPath)
            self.ui.newPath = None
