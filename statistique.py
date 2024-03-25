from plateau import *
from pygameOutils import *
from labyrinthe import *
from entite import *
import json
import requests

def mise_en_stat(joueurs_choix, monstre_tue, partie, nombre_tour, map, duree, nombre_potion, nombre_argent):
    # mettre les joueurs dans un dict
    data = {}
    for i in range(len(joueurs_choix)):
        data["joueur " + str(i + 1)] = joueurs_choix[i].__dict__()
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
    
    # data["graphe"] = graphe
    # data["liste_position_argent"] = liste_position_argent
    # data["liste_position_potion"] = liste_position_potion
    # data["liste_position_piege"] = liste_position_piege
    # data["liste_postion_joueur"] = liste_postion_joueur
    
    data["duree"] = duree
    
    mise_sur_site(data)

def mise_sur_site(data):
    # Convertir le dictionnaire en chaîne JSON
    data_json = json.dumps(data)

    # Encodage de la chaîne JSON pour l'URL
    encoded_data = requests.utils.quote(data_json, safe='')

    # Créer l'URL avec les données encodées
    url = "https://sae-cdfr.jrcandev.netlib.re/App/ajout.php?nouvelles_donnees=" + encoded_data
    
    print(url)

    # Envoyer la requête POST
    response = requests.post(url)
    print(response.text)


if __name__ == "__main__":
    
    graphe = None
    joueurs_choix = []
    joueurs_choix.append(Joueur("Mage", graphe, (5,10), 80, 80, 5, 30, 8, 5, 100, "img/classe/Mage.png"))
    joueurs_choix.append(Joueur("Paladin", graphe, (5,10), 100, 100, 5, 30, 8, 5, 100, "img/classe/Paladin.png"))
    joueurs_choix.append(Joueur("Berserk", graphe, (5,10), 80, 80, 5, 30, 8, 5, 100, "img/classe/Berserk.png"))
    # joueurs_choix.append(Joueur("Archer", graphe, (5,10), 100, 100, 5, 30, 8, 5, 100, "img/classe/Archer.png"))
    monstre_tue = 0
    partie = False
    degat_recu = 0
    nombre_tour = 5
    nombre_potion = 5
    nombre_argent = 100
    choix = 1
    duree = 5    
    
    mise_en_stat(joueurs_choix, monstre_tue, partie, nombre_tour, nombre_potion, nombre_argent, choix, duree)