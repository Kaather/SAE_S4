from random import randint, choice
from plateau import *
from filepile import *


def initialisation(largeur:int, hauteur: int)-> dict:
    '''La fonction renvoie un dictionnaire contenant chaque case du labyrinthe (clés)
et la liste de leur cases voisines (valeurs) initialement vide.
Une case est définie comme un tuple de ses coordonnées sur le labyrinthe.'''
    dico_graphe = {}

    for x in range(largeur):
        for y in range(hauteur):
            dico_graphe[(x,y)] = []   # déclaration d'une clé (x, y) avec pour valeur []

    return dico_graphe


def sur_bordure(case: tuple, dimensions: tuple)-> bool:
    '''La fonction précise si la case est sur la bordure du labyrinthe.'''
    x, y = case
    lim_x, lim_y = dimensions

    return (x == 0 or x == lim_x or y == 0 or y == lim_y)


def voisine_possible(case: tuple, dico: dict, contraintes: tuple)-> bool:
    '''La fonction précise si la case peut être définie comme une case voisine,
en tenant compte de sa position dans le labyrinthe et du nombre de cases voisines
qu'elle possède déjà.'''
    limite = 3    # nombre maximal de cases voisines 

    if sur_bordure(case, contraintes):   # si la case est sur le bord
        limite = 2                           # la limite diminue
    
    limite = limite - len(dico[case])    # la limite diminue en fonction du nombre actuel de voisines
    
    return limite != 0 and dico[case] == []  # si la limite est non nulle et que la case n'a pas de voisines


def voisines_possibles(case: tuple, dico: dict, taille: tuple)-> list:
    '''La fonction renvoie la liste des cases voisines qu'il est possible de déclarer
à la case définie dans le dictionnaire.'''
    liste2 = []
    x, y = case

    if x != 0 and voisine_possible((x-1, y), dico, taille):             # case de gauche
        liste2.append((x-1, y))
    
    if x != taille[0]-1 and voisine_possible((x+1, y), dico, taille):   # case de droite
        liste2.append((x+1, y))
    
    if y != 0 and voisine_possible((x, y-1), dico, taille):             # case de dessus
        liste2.append((x, y-1))
    
    if y != taille[1]-1 and voisine_possible((x, y+1), dico, taille):   # case de dessous
        liste2.append((x, y+1))
    
    return liste2


def choix(liste: list, nb: int)-> list:
    '''La fonction renvoie un nombre de cases choisie alétoirement dans la liste donnée.'''
    selection = []

    for i in range(nb):

        case_choisie = choice(liste)    # choice : la fonction choisit un élément de la liste
        liste.remove(case_choisie)      # on le retire de la liste proposée
        selection.append(case_choisie)

    return selection


def labyrinthe(largeur: int, hauteur: int)-> dict:
    '''La fonction renvoie un dictionnaire constitués contenant chaque case du labyrinthe (clé)
et la liste de leur cases voisines définies aléatoirement (valeur).
Une case est définie comme un tuple de ses coordonnées sur le labyrinthe.'''

    dico_laby = initialisation(largeur, hauteur)    # création du dictionnaire initial des cases
    pile = Pile(largeur * hauteur)                  # création d'une pile stockant les chemins à explorer
    pile.empiler([(0,0)])                           # empilement du premier chemin :
                                                       # chemin partant de la case (0, 0)
    while not pile.est_vide():

        chemin_actuel = pile.depiler()              # dépilement d'un chemin
        case_actuelle = chemin_actuel[-1]           # dernière case du chemin
        
        possibilites = voisines_possibles(case_actuelle,        # cases permettant de prolonger le chemin
                                          dico_laby,
                                          (largeur, hauteur))
        limite = len(possibilites)                              # nombre de cases possibles

        if limite != 0:                                 # si des cases sont accessibles : le chemin peut se prolonger
            nb_voisine = randint(0, limite)                 # choix alétoire du nombre de cases

            if nb_voisine == 0 or pile.est_vide():          # si aucune case n'est prévue ou qu'il n'y a plus de chemin
                nb_voisine = 1                                  # on en prend quand même une

            if nb_voisine > 0:
                voisines_ajoutees = choix(possibilites, nb_voisine)   # choix des cases voisines
                for case in voisines_ajoutees:
                    dico_laby[case_actuelle].append(case)                 # déclaration dans le dictionnaire 
                    dico_laby[case].append(case_actuelle)
                    pile.empiler(chemin_actuel + [case])                  # définition des chemins possibles
        
        else :                                          # si le chemin ne peut se prolonger
            chemin_actuel.pop()                             # on revient une case en arrière
            
            if chemin_actuel != []:                     # si on ne revient avant le début du chemin
                pile.empiler(chemin_actuel)                 # on empile de nouveau le chemin (avec une case en moins)
    
    return dico_laby


def affichage_laby(largeur: int, hauteur: int):
    '''La fonction affiche un labyrinthe correspondant aux dimensions largeur x hauteur,
généré de façon aléatoire.'''
    graphe = labyrinthe(largeur, hauteur)  # création du dictionnaire du graphe modélisant le labyrinthe
    laby = Grille(largeur, hauteur)        # création d'une grille
    laby.construireBordure()               # avec une bordure
    laby.construireAvecGraphe(graphe)      # création des murs sur la grille, en suivant le graphe
    print(laby)


## Programme principal
if __name__ == '__main__':             
    affichage_laby(10, 10)