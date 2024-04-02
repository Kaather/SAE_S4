from plateau import *
from pygameOutils import *
from labyrinthe import *
from entite import *


def mise_en_stat(joueurs_choix, monstre_tue, partie, nombre_tour, nombre_potion, nombre_argent, map, graphe, liste_position_argent, liste_position_potion, liste_position_piege, liste_postion_joueur):
    # mettre les joueurs dans un dict
    data = {}
    for i in range(len(joueurs_choix)):
        data["joueur " + str(i + 1)] = str(joueurs_choix[i])
    data["monstre_tue"] = monstre_tue
    data["partie"] = partie
    data["nombre_tour"] = nombre_tour
    data["nombre_potion"] = nombre_potion
    data["nombre_argent"] = nombre_argent
    if map == 0:
        data["map"] = "desert"
    elif map == 1:
        data["map"] = "neige"
    elif map == 2:
        data["map"] = "foret"
    elif map == 3:
        data["map"] = "dongeon"
    
    data["graphe"] = graphe
    data["liste_position_argent"] = liste_position_argent
    data["liste_position_potion"] = liste_position_potion
    data["liste_position_piege"] = liste_position_piege
    data["liste_postion_joueur"] = liste_postion_joueur

    print(data)


if __name__ == "__main__":
    
    graphe = None
    joueurs_choix = []
    joueurs_choix.append(Joueur("Mage", graphe, (5,10), 80, 80, 5, 30, 8, 5, 100, "img/classe/Mage.png"))
    joueurs_choix.append(Joueur("Paladin", graphe, (5,10), 100, 100, 5, 30, 8, 5, 100, "img/classe/Paladin.png"))
    joueurs_choix.append(Joueur("Berserk", graphe, (5,10), 80, 80, 5, 30, 8, 5, 100, "img/classe/Berserk.png"))
    joueurs_choix.append(Joueur("Archer", graphe, (5,10), 100, 100, 5, 30, 8, 5, 100, "img/classe/Archer.png"))
    monstre_tue = 0
    partie = False
    degat_recu = 0
    nombre_tour = 5
    nombre_potion = 5
    nombre_argent = 100
    choix = 1
    graphes = [[(10, 5), (5, 6), (6, 7)], [(10, 5), (5, 6), (6, 7)], [(10, 5), (5, 6), (6, 7)], [(10, 5), (5, 6), (6, 7)], [(10, 5), (5, 6), (6, 7)], [(10, 5), (5, 6), (6, 7)], [(10, 5), (5, 6), (6, 7)]]
    liste_position_argent = [(1,1), (2,2), (3,3)]
    liste_position_potion = [(4,4), (5,5), (6,6)]
    liste_position_piege = [(7,7), (8,8), (9,9)]
    liste_postion_joueur = [(10,10), (11,11), (12,12)]
    
    
    mise_en_stat(joueurs_choix, monstre_tue, partie, nombre_tour, nombre_potion, nombre_argent, choix, graphe, liste_position_argent, liste_position_potion, liste_position_piege, liste_postion_joueur)