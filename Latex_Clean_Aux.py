# script nettoyage fichiers auxliaires LateX

from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import os


#Liste des extensions des fichiers auxiliaires LaTeX
liste_ext=[".cor",".bar",".aux",".log",".dvi"
           ,".bbl",".blg",".out",".synctex"
           ,".ps",".toc",".lua",".lub",".tab"
           ,".idx",".ilg",".ind",".lof",".lot"]

def nettoyage(rep):
    for fichier in os.listdir(rep):
            try:
                complet = rep +"/" +fichier
                if os.path.isdir(complet):
                    nettoyage(complet)
                (nom,extension)=os.path.splitext(fichier)
                if extension in liste_ext:
                    print("fichier supprimé:",fichier)
                    os.remove(complet)
                else:
                    print("fichier gardé:",fichier)
            except:
                champ_label=Label(Mafenetre, text= fichier + "Pas réussi")
                champ_label.pack()

def ouvrir_rep():
    rep = tkinter.filedialog.askdirectory(title="Choisissez un répertoire")
    nettoyage(rep)
    


# Programme principal
Mafenetre = Tk()
Mafenetre.title("Nettoyer Fichiers Auxliaires LaTeX")
     
# Création de la fenêtre
Mafenetre.message = Label(Mafenetre, text="Nettoyage fichiers auxiliaires LaTeX")
Mafenetre.message.pack()



Mafenetre.bouton_rep = Button(Mafenetre, text="Nettoyer un répertoire", command=ouvrir_rep)
Mafenetre.bouton_rep.pack()

Mafenetre.bouton_quitter = Button(Mafenetre, text="Quitter", command=Mafenetre.destroy)
Mafenetre.bouton_quitter.pack()


# Afficher la fenêtre

Mafenetre.mainloop()
