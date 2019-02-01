# cleaner les fichiers sesamath
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import os
from random import shuffle

    
def shuffle_sesamath(fichier):
    #try:
        
        f = open(fichier,"r",)
        contenu_global=f.read()
        f.close()
        preambule , corps = contenu_global.split("\\begin{document}\n")
        lignes = corps.splitlines()
        begin_qcm = []
        end_qcm = []
        for i in range(len(lignes)):
            if "begin{ChoixQCM}" in lignes[i]:
                begin_qcm.append(i)
            if "end{ChoixQCM}" in lignes[i]:
                end_qcm.append(i)
        newlines = lignes[:begin_qcm[0]+1]
        for i in range(len(begin_qcm)-1):
            questions = lignes[begin_qcm[i]+1:end_qcm[i]]
            shuffle(questions)
            newlines = newlines + questions + lignes[end_qcm[i]:begin_qcm[i+1]+1]
            #newlines.append(lignes[end_qcm[i]:begin_qcm[i+1]+1])
        questions = lignes[begin_qcm[-1]+1:end_qcm[-1]]
        shuffle(questions)
        newlines = newlines + questions + lignes[end_qcm[-1]:]
        contenu = "\n".join(newlines)
        contenu = "\n\\begin{document}\n".join([preambule,contenu])
        
        s=open(fichier,"w")
        s.write(contenu)
        s.close()
        champ_label=Label(Mafenetre, text=fichier+" Fait")
        champ_label.pack()
        
            
##    except:
##        champ_label=Label(Mafenetre, text="Pas réussi")
##        champ_label.pack()
    
    
    
    
def Ouvrir():
    
    fichier = tkinter.filedialog.askopenfilename(title="Ouvrir un fichier",filetypes=[("fichiers latex",".tex"),("tous les fichiers",".*")])
    shuffle_sesamath(fichier)

def Ouvrir_rep():
    rep = tkinter.filedialog.askdirectory(title="Choisissez un répertoire")
    for fichier in os.listdir(rep):
        if fichier[-4:].lower() == ".tex":
            try:
                clean_sesamath(fichier)
            except:
                champ_label=Label(Mafenetre, text="Pas réussi")
                champ_label.pack()

# Programme principal
Mafenetre = Tk()
Mafenetre.title("Mélangeur de réponses QCM Sesamath")
     
# Création de la fenêtre
Mafenetre.message = Label(Mafenetre, text="Agir sur un fichier ou sur un répertoire ?")
Mafenetre.message.pack()

Mafenetre.bouton_fichier = Button(Mafenetre, text="Ouvrir fichier",command=Ouvrir)
Mafenetre.bouton_fichier.pack()

Mafenetre.bouton_rep = Button(Mafenetre, text="Ouvrir un répertoire", command=Ouvrir_rep)
Mafenetre.bouton_rep.pack()

Mafenetre.bouton_quitter = Button(Mafenetre, text="Quitter", command=Mafenetre.destroy)
Mafenetre.bouton_quitter.pack()


# Afficher la fenêtre

Mafenetre.mainloop()
