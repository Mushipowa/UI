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
        self.feed = None
        self.key = None
        self.daemon = True

    def run(self):
        try:
            if self.key == 'clean':
                self.ui.clear()
                self.ui.feedback('Initialisation des traitements..')
                self.feed = self.cleaner.openWB(1, self.filename)
                if type(self.feed) is not str:
                    raise self.feed
                elif self.feed != '':
                    raise Exception(self.feed)
                else:
                    self.ui.feedback(self.feed)

                if self.listeCheminCompil is not None:
                    self.ui.clear()
                    self.ui.feedback('Compilation...')
                    self.feed = self.cleaner.aggreg(self.listeCheminCompil)
                    print(self.feed)
                    if type(self.feed) is not str:
                        raise self.feed
                    elif self.feed != '':
                        raise Exception(self.feed)
                    else:
                        self.ui.feedback(self.feed)

                if self.banList is not None:
                    self.feed = self.cleaner.param(self.banList)
                    if type(self.feed) is not str:
                        raise self.feed
                    elif self.feed != '':
                        raise Exception(self.feed)
                    else:
                        self.ui.feedback(self.feed)

                self.ui.clear()
                self.ui.feedback('Purification...')
                self.feed = self.cleaner.purify()
                if type(self.feed) is not str:
                    raise self.feed
                elif self.feed != '':
                    raise Exception(self.feed)
                else:
                    self.ui.feedback(self.feed)

                if self.dateFormat is not None:
                    self.ui.clear()
                    self.ui.feedback('Formattage des dates...')
                    self.feed = self.cleaner.changeDate(self.dateFormat)
                    if type(self.feed) is not str:
                        raise self.feed
                    elif self.feed != '':
                        raise Exception(self.feed)
                    else:
                        self.ui.feedback(self.feed)

                self.ui.clear()
                self.ui.feedback('Formattage des nombres...')
                self.feed = self.cleaner.formatNumbers()
                if type(self.feed) is not str:
                    raise self.feed
                elif self.feed != '':
                    raise Exception(self.feed)
                else:
                    self.ui.feedback(self.feed)

                if self.cheminJointure is not None:
                    self.ui.clear()
                    self.ui.feedback('Jointure des données...')
                    self.feed = self.cleaner.joint(self.cheminJointure, self.colComp1, self.colComp2, self.colJoints)
                    if type(self.feed) is not str:
                        raise self.feed
                    elif self.feed != '':
                        raise Exception(self.feed)
                    else:
                        self.ui.feedback(self.feed)

                self.ui.clear()
                self.ui.feedback('Formattage des nombres...')
                self.feed = self.cleaner.formatNumbers()
                if type(self.feed) is not str:
                    raise self.feed
                elif self.feed != '':
                    raise Exception(self.feed)
                else:
                    self.ui.feedback(self.feed)

                if self.colIndexAnonymisation is not None:
                    self.ui.clear()
                    self.ui.feedback('Anonymisation des données...')
                    self.feed = self.cleaner.anonymize(self.colIndexAnonymisation)
                    if type(self.feed) is not str:
                        raise self.feed
                    elif self.feed != '':
                        raise Exception(self.feed)
                    else:
                        self.ui.feedback(self.feed)

                if self.modeCateg is not None:
                    self.ui.clear()
                    self.ui.feedback('Catégorisation des données...')
                    self.feed = self.cleaner.categorize(self.modeCateg, self.colIndexC, self.changes)
                    if type(self.feed) is not str:
                        raise self.feed
                    elif self.feed != '':
                        raise Exception(self.feed)
                    else:
                        self.ui.feedback(self.feed)

                if self.colIndexApparition is not None:
                    self.ui.clear()
                    self.ui.feedback('Calcul apparition des valeurs...')
                    self.feed = self.cleaner.count(self.colIndexApparition)
                    if type(self.feed) is not str:
                        raise self.feed
                    elif self.feed != '':
                        raise Exception(self.feed)
                    else:
                        self.ui.feedback(self.feed)

                if self.colIndexAdditionIdentification is not None:
                    self.ui.clear()
                    self.ui.feedback('Addition des valeurs...')
                    self.feed = self.cleaner.summ(self.colIndexAdditionIdentification, self.colIndexAdditionAssommer)
                    if type(self.feed) is not str:
                        raise self.feed
                    elif self.feed != '':
                        raise Exception(self.feed)
                    else:
                        self.ui.feedback(self.feed)

                if self.colIndexDoublon is not None:
                    self.ui.clear()
                    self.ui.feedback('Identification des doublons...')
                    self.ui.feed = self.cleaner.doublons(self.colIndexDoublon)
                    if type(self.feed) is not str:
                        raise self.feed
                    elif self.feed != '':
                        raise Exception(self.feed)
                    else:
                        self.ui.feedback(self.feed)

                self.feed = self.cleaner.addIndex()
                if type(self.feed) is not str:
                    raise self.feed
                elif self.feed != '':
                    raise Exception(self.feed)
                else:
                    self.ui.feedback(self.feed)

                self.ui.clear()
                self.ui.feedback('Purification...')
                self.feed = self.cleaner.purify()
                if type(self.feed) is not str:
                    raise self.feed
                elif self.feed != '':
                    raise Exception(self.feed)
                else:
                    self.ui.feedback(self.feed)

                if self.banList is not None:
                    self.feed = self.cleaner.resetBanned()
                    if type(self.feed) is not str:
                        raise self.feed
                    elif self.feed != '':
                        raise Exception(self.feed)
                    else:
                        self.ui.feedback(self.feed)
                self.callBackUI()

            if self.key == 'save':
                if self.colIndexAnonymisation is None:
                    self.ui.feedback('Sauvegarde en cours...')
                    self.feed = self.cleaner.saveWB(1, self.newPath)
                    if type(self.feed) is not str:
                        raise self.feed
                    elif self.feed != '':
                        raise Exception(self.feed)
                    else:
                        self.ui.feedback(self.feed)
                else:
                    self.ui.clear()
                    self.ui.feedback('Sauvegarde en cours...')
                    self.feed = self.cleaner.saveWB(2, self.newPath)
                    if type(self.feed) is not str:
                        raise self.feed
                    elif self.feed != '':
                        raise Exception(self.feed)
                    else:
                        self.ui.feedback(self.feed)
                self.feed = self.cleaner.openWB(1, self.newPath)
                if type(self.feed) is not str:
                    raise self.feed
                elif self.feed != '':
                    raise Exception(self.feed)
                else:
                    self.ui.feedback(self.feed)
                self.callBackUI()
        except Exception as e:
            self.ui.pop(str(e))
            self.ui.resetUI()
            self.ui.resetParam()
            self.ui.cleaner.timeMachine('pullBack@', self.filename)
            self.ui.load(None, 'cancel', self.filename)

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
