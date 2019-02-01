#!/usr/local/bin/python
# -*- coding:utf-8 -*-


import os
import re
import tkinter.filedialog
import tkinter.messagebox
from tkinter import *

regex = r"\\MethodeRefExercice\*\{([\d|\w]*)\}"
re_refexo = r"\\RefExercice\{([\d|\w]*)\}"

re_vspace = r"\\vspace\{([\d|\w|\.|-]*)\}"

new_preamble = r"""
\newcommand{\ofg}[1]{\og #1 \fg}
\renewcommand{\labelitemi}{$\diamond$}
\newcommand{\vspacekill}[1]{}
\newcommand{\pagerefkill}[1]{\textcolor{red}{\textbf{** à modifier **}}}
\newcommand{\RefExercice}[1]{\textcolor{red}{\textbf{** à modifier **}}}
\newcommand{\mathscr}[1]{\mathcal{#1}}
\newcommandx{\MotDefinition}[3][1,3]{#2}
\newcommand{\upc}[1]{#1\%}
\newcommand{\correction}{\textbf{Correction:}}
\newcommand{\MethodeRefExercice}[1]{}
%\renewcommand{\MethodeRefExercice*}[1]{}
\newcommand{\ExerciceRefMethode}[1]{}
\newcommand{\calc}{}
\newcommand{\roc}{\textbf{ROC}}
"""


class LaTeXCommand:
    def __init__(self, nom, arg=1, optn=False):
        self.nom = nom
        self.arg = arg
        self.optn = optn

    def find(self, contenu):
        return contenu.find(self.nom)

    def findCommand(self, texte):
        index = texte.find(self.nom)
        avant = texte[:index]
        apres = texte[index+len(self.nom):]
        argOptn = ""
        listeArg = []
        if self.optn:
            if apres[0] == "[":
                i = 0
                while apres[i] != "]":
                    i = i + 1
                argOptn = apres[1:i]
                apres = apres[i+2:]
            else:
                apres = apres[1:]
        else:
            apres = apres[1:]
        argRest = self.arg
        avantManip = "{"+apres
        while argRest != 0:
            argRest = argRest - 1
            ouvert2 = apres.find("{")
            ferme1 = apres.find("}")
            if ouvert2 == -1:
                ouvert2 = ferme1
            while ouvert2 < ferme1:
                ouvert2 = apres.find("{", ferme1+1)
                ferme1 = apres.find("}", ferme1+1)
            listeArg.append(apres[:ferme1])
            apres = apres[ferme1+2:]
        longueurArgument = 0
        for argument in listeArg:
            longueurArgument = longueurArgument + len(argument)+2

        apres = avantManip[longueurArgument:]
        return index, avant, apres, argOptn, listeArg

    def cleanCommand(self, contenu):
        passe = 0
        while self.nom in contenu:
            passe = passe + 1
            index, avant, apres, argOptn, listeArg = self.findCommand(contenu)
            # print("Passe"+str(passe),apres)
            contenu = avant+apres
        return contenu

    def replaceCommand(self, contenu, listeReplace):
        while self.nom in contenu:
            index, avant, apres, argOptn, listeArg = self.findCommand(contenu)
            texte = ""
            for argument in listeReplace:
                if type(argument) is type("c"):
                    texte = texte + argument
                elif argument == 0:
                    texte = texte + "[" + argOptn + "]"
                else:
                    texte = texte + "{" + listeArg[argument-1] + "}"
            contenu = avant + texte + apres
        return contenu


class Sesamath:
    def __init__(self, fichier):
        self.fichier = fichier

    def lire_original(self):
        try:
            f = open(self.fichier, "r")
            self.original = f.read()
            f.close
            self.preambule, self.corps = self.original.split(
                r"\begin{document}")
        except:
            print("erreur lecture fichier")

    def process(self):
        self.lire_original()
        print("Sesa OK")


listeCommandesClean = [LaTeXCommand("\\vspace"),
                       LaTeXCommand("\\MethodeRefExercice"),
                       LaTeXCommand("\\ExerciceRefMethode")]

listeCommandesReplace = [[LaTeXCommand("\\MotDefinition", 2, True), ["\\textbf", 1]],
                         [LaTeXCommand("\\pageref"), [
                             "\\textcolor{red}{** texte à modifier**}"]],
                         [LaTeXCommand(r"\RefExercice"), [
                             "\\textcolor{red}{** texte à modifier**}"]],
                         [LaTeXCommand("\\ofg"), ["\\og ", 1, " \\fg "]],
                         [LaTeXCommand("\\serie"), ["\\section", 1]],
                         [LaTeXCommand("\\expcopimul", 3), [
                             "e^{", 1, "i\\frac{", 2, "\\pi}", 3, "}"]],
                         [LaTeXCommand("\\expcopim", 2, False), [
                             "e^{-i\\frac{", 1, "\\pi}{", 2, "}}"]],
                         [LaTeXCommand("\\expcopi", 2, False), [
                             "e^{i\\frac{", 1, "\\pi}{", 2, "}}"]],
                         [LaTeXCommand("\\expco"), ["e^", 1]],
                         [LaTeXCommand("\\ang", 2), [
                             r"\widehat{\left( \vect", 1, r";\vect", 2, r"\right)}"]],
                         [LaTeXCommand(r"\coopoint", 3), [
                             1, r"\left( ", 2, ";", 3, r"\right)"]],
                         [LaTeXCommand(r"\coovec", 3), [
                             r"\vect{", 1, "}", "[", 2, "][", 3, "]"]],
                         [LaTeXCommand(r"\coo", 2), [
                             r"\left(", 1, ";", 2, r"\right)"]],
                         [LaTeXCommand(r"\ucm"), [1, "cm "]]]
# [LaTeXCommand(r"\af"),[[r"z_",1]]]


listeRemplaceSimple = [[r"\exercicesbase", r"\fexo{}{Exercices de base}{}"],
                       [r"\exercicesbac", r"\fexo{}{Exercices Bac}{}"],
                       ["\\exercice", "\n\n\\textbf{Exercice:}\n\n"],
                       ["{exercice*}", "{exercice}"],
                       ["exemple*1", "exemple"],
                       [r"\begin{colonne*exercice}", "\n"],
                       [r"\end{colonne*exercice}", "\n"],
                       ["{corrige}", "{solution}"],
                       [r"\pathtexgraphfig/", "figures/figures-texgraph/"],
                       # [r"\ce","e"],
                       # [r"\ci","i"],
                       [r"\displaystyle", ""],
                       # [r"\di",""],
                       [r"\columnbreak", ""],
                       [r"\tice", r"\textbf{TICE}"],
                       [r"\roc", r"\textbf{ROC}"],
                       [r"\algo", r"\textbf{ALGO}"],
                       [r"\vv{", r"\vect{"],
                       [r"\pathmanuel/", ""],
                       [r"\OUV", "(O;U,V)"],
                       [r"\Ouv", r"(O;\vect{u},\vect{v})"],
                       [r"\cours", r"\fexo{}{Cours}{}"],
                       [r"\mafrac", r"\frac"],
                       ["oldalgorithme", "verbatim"],
                       [r"[\textbf{ALGO}]", ""],
                       [r"\TopStrut", ""],
                       [r"\BotStrut", ""],
                       [r"\nombre{", r"\np{"],
                       [r"\RefItem{", r"\ref{"]

                       ]


def clean_sesamath(fichier):
    try:
        sesa = Sesamath(fichier)
        sesa.process()
        f = open(fichier, "r", encoding='utf8')
        print("ouverture fichier")
        contenu_global = f.read()
        print("lecture fichier")
        f.close()
        preambule, contenu = contenu_global.split("\\begin{document}\n")

        for couple in listeRemplaceSimple:
            contenu = contenu.replace(couple[0], couple[1])

        #contenu = cleanMotDefinition(contenu)
        contenu = contenu.replace("exemples*1", "exemples")
        contenu = contenu.replace("methode*1", "methode")
        contenu = contenu.replace("MethodeRefExercice*", "MethodeRefExercice")
        contenu = contenu.replace("RefExercice*", "RefExercice")
        for commande in listeCommandesClean:
            contenu = commande.cleanCommand(contenu)
        contenu = contenu.replace("\\linebreak", "")
        contenu = contenu.replace("\\newpage", "")
        contenu = contenu.replace("mathscr", "mathcal")
        contenu = contenu.replace("\\begin{Ctableau}", "\\begin{tableau}[C]")
        contenu = contenu.replace("{Ctableau}", "{tableau}")
        contenu = contenu.replace("end{tableau}", "end{tabularx}")
        contenu = contenu.replace("\\Sup", "\\geq")
        contenu = contenu.replace("\\Inf", "\\leq")
        contenu = contenu.replace("proprieta", "propriete")
        contenu = contenu.replace(
            "\\correction", "\n\n\\textbf{Correction}\n\n")
        contenu = contenu.replace("\\exercice", "\n\n\\exercice\n\n")
        for couple in listeCommandesReplace:
            print(couple)
            contenu = couple[0].replaceCommand(contenu, couple[1])
        print("sortie")
        contenu = re.sub(regex, "", contenu)

        contenu = re.sub(re_refexo, "", contenu)
        contenu = re.sub(re_vspace, "", contenu)
        print("remplacement simple contenu effectué")
        lignes = contenu.splitlines()
        newlignes = []
        index_ligne = 4
        for ligne in lignes:
            index_ligne = index_ligne + 1
            if "{solution}" in ligne:
                ligne = ligne.replace(" ", "")
            if "\\begin{tableau}" in ligne:
                x, y = ligne.split(r"\begin{tableau}")
                pos_accolade_ouvert = []
                pos_accolade_ferme = []
                for i in range(len(y)):
                    if y[i] == "{":
                        pos_accolade_ouvert.append(i)

                for i in range(len(y)):
                    if y[i] == "}":
                        pos_accolade_ferme.append(i)
                arg1 = y[pos_accolade_ouvert[0]:pos_accolade_ferme[0]+1]
                arg2 = y[pos_accolade_ouvert[1]+1:pos_accolade_ferme[1]]
                colonnes = int(arg2)
                argument = "\\begin{tabularx}"+arg1 + "{|m{3cm}|"
                for i in range(colonnes):
                    argument = argument + "C|"
                ligne = argument + "}"
            newlignes.append(ligne)

        contenu = "\n".join(newlignes)
        contenu = "\n\\begin{document}\n".join([preambule,contenu])
        s=open(fichier,"w",encoding='utf8')
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
