from threading import Thread
import PFE_MondoClean.MondoClean.data_Cleaner_Module.data_cleaner as DC #data_Cleaner as DC
import time

class BarManager(Thread):

    def __init__(self, ui, cleaner):
        Thread.__init__(self)
        self.ui = ui
        self.cleaner = cleaner
        self.daemon = True


    def run(self):
        while True:
            self.ui.setBarValue(self.cleaner.getProgress())
            time.sleep(0.1)
