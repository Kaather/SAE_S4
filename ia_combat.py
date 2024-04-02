from labyrinthe import *
from plateau import *
from pygameOutils import *
from jeuGraphique import *
from jeuGraphiqueReseau import *


def combat_facile():
    print("aléatoire / Facile")

    #Générer un nombre aléatoire entre 1 et 6 pour représenter le niveau facile des combats
    combat = random.randint(1, 6)
    
    print("Déplacement aléatoire pour niveau facile:", combat)

        

def combat_intermediaire():
    print("minmax / Intermediare")
    
    #Définir la liste des personnages_force avec leurs forces respectives
    personnages_force = {
        1: {"force": 5},
        2: {"force": 8},
        3: {"force": 4},
        4: {"force": 7},
        5: {"force": 6},
        6: {"force": 9}
    }

    # Choisir l'attaque la plus efficace pour chaque personnage
    for personnage, details in personnages_force.items():
        if details["force"] >= 8:
            print(f"Personnage {personnage}: Attaque puissante")
        elif 6 <= details["force"] < 8:
            print(f"Personnage {personnage}: Attaque moyenne")
        else:
            print(f"Personnage {personnage}: Attaque faible")



          


def minimax_avec_renforcement(personnages_force, profondeur, maximisant):
    # Algorithme Minimax avec renforcement
    if profondeur == 0 or len(personnages_force) == 0:
        return sum([details["force"] for personnage, details in personnages_force.items()])  # Utilisation de la somme des forces

    if maximisant:
        meilleur_coup = float('-inf')
        for personnage in personnages_force:
            nouveau_personnages_force = {p: v for p, v in personnages_force.items() if p != personnage}  # Créer un nouveau dictionnaire sans le personnage actuel
            coup = minimax_avec_renforcement(nouveau_personnages_force, profondeur - 1, False)
            meilleur_coup = max(meilleur_coup, coup)
        return meilleur_coup
    else:
        pire_coup = float('inf')
        for personnage in personnages_force:
            nouveau_personnages_force = {p: v for p, v in personnages_force.items() if p != personnage}  # Créer un nouveau dictionnaire sans le personnage actuel
            coup = minimax_avec_renforcement(nouveau_personnages_force, profondeur - 1, True)
            pire_coup = min(pire_coup, coup)
        return pire_coup



def combat_difficile():
    # Fonction de combat difficile utilisant Minimax avec renforcement
    print("minmax avec renforcement / Difficile")
    
    # Liste des personnages_force avec leurs forces respectives
    personnages_force = {
        1: {"force": 5},
        2: {"force": 8},
        3: {"force": 4},
        4: {"force": 7},
        5: {"force": 6},
        6: {"force": 9}
    }

    # Appel de l'algorithme Minimax avec renforcement pour choisir le mouvement optimal
    meilleur_coup = minimax_avec_renforcement(personnages_force, 2, True)

    print("Mouvement optimal:", meilleur_coup)


