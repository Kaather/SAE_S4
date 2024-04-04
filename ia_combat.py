from labyrinthe import *
from plateau import *
from pygameOutils import *
from jeuGraphique import *
from jeuGraphiqueReseau import *
from combatMonstre import *
from pygameOutils import *
import random


def combat_facile(joueurs_choix, compteur_lancers, monstre):
    if joueurs_choix[compteur_lancers].nom == "Healer" :

        if joueurs_choix[compteur_lancers].pv < joueurs_choix[compteur_lancers].pv_max :
            capacite = random.randint(1, 4)

            if capacite == 1 and joueurs_choix[compteur_lancers].potions > 0 :
                joueurs_choix[compteur_lancers].utiliser_potion()
            
            if capacite == 2 :
                joueur_selectionne = random.randint(1, len(joueurs_choix))

                if joueur_selectionne == 1 :
                    soin(joueurs_choix[0])

                if joueur_selectionne == 2 :
                    soin(joueurs_choix[1])

                if joueur_selectionne == 3 :
                    soin(joueurs_choix[2])

                if joueur_selectionne == 4 :
                    soin(joueurs_choix[3])

            if capacite == 3 :
                choix_bonus = random.randint(1, 3)

                if choix_bonus == 1 :
                    joueur_selectionne = random.randint(1, len(joueurs_choix))

                    if joueur_selectionne == 1 :
                        joueurs_choix[0].attaque = joueurs_choix[0].attaque + 10

                    if joueur_selectionne == 2 :
                        joueurs_choix[1].attaque = joueurs_choix[1].attaque + 10

                    if joueur_selectionne == 3 :
                        joueurs_choix[2].attaque = joueurs_choix[2].attaque + 10

                    if joueur_selectionne == 4 :
                        joueurs_choix[3].attaque = joueurs_choix[3].attaque + 10

                if choix_bonus == 2 :
                    joueur_selectionne = random.randint(1, len(joueurs_choix))

                    if joueur_selectionne == 1 :
                        joueurs_choix[0].magie = joueurs_choix[0].magie + 10
                    
                    if joueur_selectionne == 2 :
                        joueurs_choix[1].magie = joueurs_choix[1].magie + 10

                    if joueur_selectionne == 3 :
                        joueurs_choix[2].magie = joueurs_choix[2].magie + 10

                    if joueur_selectionne == 4 :
                        joueurs_choix[3].magie = joueurs_choix[3].magie + 10
                
                if choix_bonus == 3 :
                    joueur_selectionne = random.randint(1, len(joueurs_choix))

                    if joueur_selectionne == 1 :
                        joueurs_choix[0].vitesse = joueurs_choix[0].vitesse + 10

                    if joueur_selectionne == 2 :
                        joueurs_choix[1].vitesse = joueurs_choix[1].vitesse + 10

                    if joueur_selectionne == 3 :
                        joueurs_choix[2].vitesse = joueurs_choix[2].vitesse + 10

                    if joueur_selectionne == 4 :
                        joueurs_choix[3].vitesse = joueurs_choix[3].vitesse + 10

            if capacite == 4 :
                choix_malus = random.randint(1, 3)

                if choix_malus == 1 :
                    monstre.attaque = monstre.attaque - 10

                if choix_malus == 2 :
                    monstre.magie = monstre.magie - 10
                
                if choix_malus == 3 :
                    monstre.vitesse = monstre.vitesse - 10

        else :
            capacite = random.randint(1, 3)

            if capacite == 1 :
                joueur_selectionne = random.randint(1, len(joueurs_choix))

                if joueur_selectionne == 1 :
                    soin(joueurs_choix[0])

                if joueur_selectionne == 2 :
                    soin(joueurs_choix[1])

                if joueur_selectionne == 3 :
                    soin(joueurs_choix[2])

                if joueur_selectionne == 4 :
                    soin(joueurs_choix[3])

            if capacite == 2 :
                choix_bonus = random.randint(1, 3)

                if choix_bonus == 1 :
                    joueur_selectionne = random.randint(1, len(joueurs_choix))

                    if joueur_selectionne == 1 :
                        joueurs_choix[0].attaque = joueurs_choix[0].attaque + 10

                    if joueur_selectionne == 2 :
                        joueurs_choix[1].attaque = joueurs_choix[1].attaque + 10

                    if joueur_selectionne == 3 :
                        joueurs_choix[2].attaque = joueurs_choix[2].attaque + 10

                    if joueur_selectionne == 4 :
                        joueurs_choix[3].attaque = joueurs_choix[3].attaque + 10

                if choix_bonus == 2 :
                    joueur_selectionne = random.randint(1, len(joueurs_choix))

                    if joueur_selectionne == 1 :
                        joueurs_choix[0].magie = joueurs_choix[0].magie + 10
                    
                    if joueur_selectionne == 2 :
                        joueurs_choix[1].magie = joueurs_choix[1].magie + 10

                    if joueur_selectionne == 3 :
                        joueurs_choix[2].magie = joueurs_choix[2].magie + 10

                    if joueur_selectionne == 4 :
                        joueurs_choix[3].magie = joueurs_choix[3].magie + 10
                
                if choix_bonus == 3 :
                    joueur_selectionne = random.randint(1, len(joueurs_choix))

                    if joueur_selectionne == 1 :
                        joueurs_choix[0].vitesse = joueurs_choix[0].vitesse + 10

                    if joueur_selectionne == 2 :
                        joueurs_choix[1].vitesse = joueurs_choix[1].vitesse + 10

                    if joueur_selectionne == 3 :
                        joueurs_choix[2].vitesse = joueurs_choix[2].vitesse + 10

                    if joueur_selectionne == 4 :
                        joueurs_choix[3].vitesse = joueurs_choix[3].vitesse + 10

            if capacite == 3 :
                choix_malus = random.randint(1, 3)

                if choix_malus == 1 :
                    monstre.attaque = monstre.attaque - 10
                    if monstre.attaque < 0 :
                        monstre.attaque = 5

                if choix_malus == 2 :
                    monstre.magie = monstre.magie - 10
                    if monstre.magie < 0 :
                        monstre.magie = 5
                
                if choix_malus == 3 :
                    monstre.vitesse = monstre.vitesse - 10
                    if monstre.vitesse < 0 :
                        monstre.vitesse = 5

    else : 

        if joueurs_choix[compteur_lancers].pv < joueurs_choix[compteur_lancers].pv_max :
            capacite = random.randint(1, 4)

            if capacite == 1 :
                attaque(joueurs_choix[compteur_lancers], monstre)

            if capacite == 2 :
                attaque_puissante(joueurs_choix[compteur_lancers], monstre)

            if capacite == 3 :
                attaque_puissante(joueurs_choix[compteur_lancers], monstre)

            if capacite == 4 :
                joueurs_choix[compteur_lancers].utiliser_potion()

        else :
            capacite = random.randint(1, 3)

            if capacite == 1 :
                attaque(joueurs_choix[compteur_lancers], monstre)

            if capacite == 2 :
                attaque_puissante(joueurs_choix[compteur_lancers], monstre)

            if capacite == 3 :
                attaque_puissante(joueurs_choix[compteur_lancers], monstre)
        

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


