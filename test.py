from entite import *
from labyrinthe import *
from plateau import *


largeur = 10
hauteur = 10

laby = Grille(largeur, hauteur)
laby.construireBordure()
graphe = labyrinthe(largeur, hauteur)
laby.construireAvecGraphe(graphe)
print(laby)

Paladin = Joueur("Paladin", graphe, (5,10), 80, 60, 5, 30, 8, 5, 100, "img/classe/Paladin.png")
Paladin.afficher_position()

while True:
    print("1. Déplacer vers la droite")
    print("2. Déplacer vers la gauche")
    print("3. Déplacer vers le haut")
    print("4. Déplacer vers le bas")
    print("5. Quitter")
    
    choix = input("Choisissez une option : ")

    if choix == '1':
        Paladin.deplacer((1, 0))
    elif choix == '2':
        Paladin.deplacer((-1, 0))
    elif choix == '3':
        Paladin.deplacer((0, -1))
    elif choix == '4':
        Paladin.deplacer((0, 1))
    elif choix == '5':
        break
    else:
        print("Option invalide. Veuillez choisir un numéro entre 1 et 5.")

    print(laby)
    Paladin.afficher_position()


