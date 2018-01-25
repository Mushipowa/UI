from tkinter import *
from tkinter.filedialog import *
fenetre = Tk()

# frame 1
Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE, bg="red")
Frame1.pack(side=LEFT, padx=600, pady=300)

menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer")
menu1.add_command(label="Editer")
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Fichier", menu=menu1)
menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Couper")
menu2.add_command(label="Copier")
menu2.add_command(label="Coller")
menubar.add_cascade(label="Editer", menu=menu2)
fenetre.config(menu=menubar)


class Interface(Frame):

    """Notre fenêtre principale.
    Tous les widgets sont stockés comme attributs de cette fenêtre."""

    def __init__(self, fenetre, **kwargs):
        Frame.__init__(self, fenetre, width=768, height=576, **kwargs)
        self.pack(fill=BOTH)
        self.filename = None



        self.bouton_cliquer = Button(self, text="ouvrir document", fg="red",
                command=self.cliquer)
        self.bouton_cliquer.pack(side="right")
        self.bouton_display = Button(self, text="aperçu document", fg="red",
                command=self.cliquer)
        self.bouton_display.pack(side="left")

    def cliquer(self):

        self.filename = askopenfilename(title="Ouvrir votre document",filetypes=[("Excel files", "*.xlsx *.xls"),('all files','.*')])
        fichier = open(filename, "r")
        content = fichier.read()

    def display(self):
        # ask for file if not loaded yet
        if self.df is None:
            self.load()

        # display if loaded
        if self.df is not None:
            self.text.insert('end', self.filename + '\n')
            self.text.insert('end', str(self.df.head()) + '\n')

interface = Interface(fenetre)
interface.mainloop()
interface.destroy()

bouton_quitter = Button(Frame1, text="Quitter",cursor="man",relief=RAISED, command=fenetre.quit)
bouton_quitter.pack(side=LEFT, padx=10, pady=10)
fenetre.mainloop()
