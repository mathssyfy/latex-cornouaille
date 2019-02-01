# cleaner les fichiers sesamath
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import os


new_preamble = r"""\newcounter{questionqcm}
\setcounter{questionqcm}{0}
\newenvironment{QCM}{}{}
\newenvironment{GroupeQCM}{
\begin{exercice}
\setcounter{questionqcm}{0}
}{


\end{exercice}}
\newenvironment{ChoixQCM}[1]{
\begin{multicols}{#1}
\begin{enumerate}
}{
\end{enumerate}
\end{multicols}
}
\newcommand{\reponseQCM}[1]{\textbf{#1}}
\newcommand{\upc}[1]{#1\%}"""
class Sesamath:
    def __init__(self,fichier):
        self.fichier = fichier
        
    def lire_original(self):
        try:
            f = open(self.fichier,"r")
            self.original = f.read()
            f.close
            self.preambule, self.corps = self.original.split(r"\begin{document}")
        except:
            print("erreur lecture fichier")

    def process(self):
        self.lire_original()
        print("Sesa OK")
    
def clean_sesamath(fichier):
    try:
        sesa = Sesamath(fichier)
        sesa.process()
        f = open(fichier,"r",)
        contenu_global=f.read()
        f.close()
        preambule , corps = contenu_global.split("\\begin{document}\n")
        if r"newenvironment{ChoixQCM}" not in preambule:
            preambule = preambule + new_preamble
        contenu = corps.replace("\\begin{corrige}","\\setcounter{enumii}{0}\n\\begin{solution}")
        contenu = contenu.replace("end{corrige}","end{solution}")
        contenu = contenu.replace("exercice*","exercice")
        contenu = contenu.replace("mathscr","mathcal")
        contenu = contenu.replace("begin{exercice}","begin{enumerate}\n\\setcounter{enumi}{\\value{questionqcm}}\\stepcounter{questionqcm}\n\\item ")
        contenu = contenu.replace("end{exercice}","end{enumerate}")
        
        lignes = contenu.splitlines()
        newlignes = []
        for ligne in lignes:
            if "{solution}" in ligne:
                ligne = ligne.replace(" ","")
                newlignes.append(ligne)
            else:
                newlignes.append(ligne)
        contenu = "\n".join(newlignes)
        contenu = "\n\\begin{document}\n".join([preambule,contenu])
        s=open(fichier,"w")
        s.write(contenu)
        s.close()
        champ_label=Label(Mafenetre, text=fichier+" Fait")
        champ_label.pack()
        
            
    except:
        champ_label=Label(Mafenetre, text="Pas réussi")
        champ_label.pack()
    
    
    
    
def Ouvrir():
    
    fichier = tkinter.filedialog.askopenfilename(title="Ouvrir un fichier",filetypes=[("fichiers latex",".tex"),("tous les fichiers",".*")])
    clean_sesamath(fichier)

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
Mafenetre.title("Sesamath Power !")
     
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
