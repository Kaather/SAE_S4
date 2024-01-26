import pygame
import sys
import random
from entite import *
from plateau import *
from labyrinthe import *


# Initialisation de Pygame
pygame.init()

info = pygame.display.Info()

# Définir les dimensions de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Exemple de rectangles")

# Couleurs
TRANSPARENT = (255, 255, 255, 0)
WHITE = (255, 255, 255)
WHITE_TR = (255, 255, 255, 100)
BROWN_TR = (130, 60, 20, 100)
BROWN = (130, 60, 20, 200)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLACK_TR = (0, 0, 0, 100)
RED = (255, 0, 0)
RED_MENU = (255, 0, 0, 128)
GREY = (128, 128, 128)
GREY_TR = (128, 128, 128, 100)

screen.fill(WHITE)

# Initialiser l'écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Monster Slayer")

# Charger la police
font_path = "font/MedievalSharp-Bold.ttf"  # Assurez-vous de spécifier le bon chemin
font = pygame.font.Font(font_path, 30)

# Utiliser la police pour afficher du texte
texte_surface = font.render("Votre texte", True, BLACK)

vitesse_fond = 5 # Vitesse de déplacement du fond

current_player = 0

largeur = 11
hauteur = 11

classes = []

joueurs_choix = []

class Rectangle:
    """Classe qui va permettre de créer des rectangles sur pygame"""
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Point:
    """Classe qui représente un point"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, color, radius, offset_x=0, offset_y=0):
        pygame.draw.circle(screen, color, (self.x + offset_x, self.y + offset_y), radius)


# Fonctions pour afficher le texte
def draw_text(text, size, x, y, color):
    font = pygame.font.Font(font_path, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)


def background(choice):
    backgrounds = [
        'img/map/mapDesert.png',  
        'img/map/mapSnow.png',
        'img/map/mapForest.png',
        'img/map/mapDungeon.png'
        ]
    
    background_image = pygame.image.load(backgrounds[choice]).convert()
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background_image, (0, 0))

def supprimer_joueurs_choix():
    global joueurs_choix
    joueurs_choix = []

def supprimer_classes():
    global classes
    classes = []


def dice(graphe, joueur):
    de = random.randint(1, 6) 
    cases_accessibles = []

    cases_accessibles.append(joueur.position)

    for i in range(1, de + 1):
        nouvelles_cases = []
        for case in cases_accessibles:
            nouvelles_cases.extend(graphe[case])
        cases_accessibles.extend(nouvelles_cases)

    return de, cases_accessibles

def afficherJoueurLaby(joueur):
    
    joueur_image = pygame.image.load(joueur.image).convert()
    joueur_image.set_colorkey(BLACK)
    joueur_image = pygame.transform.scale(joueur_image, (45, 45))  
    screen.blit(joueur_image, (joueur.position[0] * 52 + 361, joueur.position[1] * 52 + 58))

def afficherJoueursLaby(joueurs):
    positions = {}  # Dictionnaire pour stocker les positions des joueurs

    # Parcours des joueurs et ajout de leurs positions au dictionnaire
    for joueur in joueurs:
        joueur_image = pygame.image.load(joueur.image).convert()
        joueur_image.set_colorkey(BLACK)
        joueur_image = pygame.transform.scale(joueur_image, (45, 45))  
        screen.blit(joueur_image, (joueur.position[0] * 52 + 361, joueur.position[1] * 52 + 58))
        position = joueur.position
        if position not in positions:
            positions[position] = []
        positions[position].append(joueur)

    for position, joueurs_sur_case in positions.items():
        # S'il y a plus d'un joueur sur la même case
        if len(joueurs_sur_case) > 1:
            joueur_courant = joueurs_sur_case[0]
            distance_min = float('inf')

            for joueur in joueurs_sur_case:
                # Calculez la distance entre le joueur courant et le joueur sur la même case
                distance = abs(joueur_courant.position[0] - joueur.position[0]) + abs(joueur_courant.position[1] - joueur.position[1])
                
                if distance < distance_min:
                    joueur_courant = joueur
                    distance_min = distance

            afficherJoueurLaby(joueur_courant)
        else:
            afficherJoueurLaby(joueurs_sur_case[0])

def piege(graphe):
    pieges_normaux = []  # Liste pour stocker les informations sur les pièges normaux
    pieges_dores = []  # Liste pour stocker les informations sur les pièges dorés
    piege_images = []  # Liste pour stocker les images des pièges
    piege_doree_image = pygame.image.load('img/element/piegeDoree.png').convert()

    # Positions exclues pour les pièges
    exclusions = [(5, 10), (4, 10), (6, 10), (5, 9)]

    # Générer une liste de toutes les cases valides du graphe
    cases_valides = list(graphe.keys())

    # Ajouter des pièges normaux jusqu'à ce que la liste atteigne 4 éléments
    while len(pieges_normaux) < 5 :
        position = random.choice(cases_valides)

        # Vérifier si la position est valide et ne se trouve pas dans les exclusions
        if position not in [p[0] for p in pieges_normaux] and position not in exclusions:
            pieges_normaux.append(position)  # Ajouter la position du piège normal
            piege_images.append(pygame.image.load('img/element/piege.png').convert())
            piege_images[-1].set_colorkey(BLACK)
            piege_images[-1] = pygame.transform.scale(piege_images[-1], (42, 42))

    # Ajouter un piège en or
    doree_piege_position = random.choice(cases_valides)

    # S'assurer que la position du piège en or n'entre pas en conflit avec les autres pièges
    while doree_piege_position in pieges_normaux or doree_piege_position in exclusions:
        doree_piege_position = random.choice(cases_valides)

    pieges_dores.append(doree_piege_position)  # Ajouter la position du piège en or
    piege_doree_image.set_colorkey(BLACK)
    piege_doree_image = pygame.transform.scale(piege_doree_image, (42, 42))

    return pieges_normaux, pieges_dores, piege_images, piege_doree_image

def joueur_sur_piege(joueur, pieges):
    return joueur.position in pieges

def joueur_sur_piege_doree(joueur, piege_doree):
    return joueur.position in piege_doree


def ajouter_objet(graphe, piege_positions, piege_doree_positions):
    potion_positions = []  # Liste pour stocker les positions des potions
    potion_images = []  # Liste pour stocker les images des potions
    argent_positions = []  # Liste pour stocker les positions de l'argent
    argent_images = []  # Liste pour stocker les images de l'argent

    # Positions exclues pour les objets
    exclusions = [(5, 10), (4, 10), (6, 10), (5, 9)]

    # Générer une liste de toutes les cases valides du graphe
    cases_valides = list(graphe.keys())

    # Exclure les positions des pièges et pièges dorés de la liste des cases valides
    cases_valides = [case for case in cases_valides if case not in piege_positions and case not in piege_doree_positions]

    while len(potion_positions) < 10:
        position = random.choice(cases_valides)

        # Vérifier si la position est valide et ne se trouve pas dans les exclusions
        if (
            position not in potion_positions and
            position not in exclusions
        ):
            potion_positions.append(position)
            potion_images.append(pygame.image.load('img/element/Potion.png').convert())

            potion_images[-1].set_colorkey(BLACK)
            potion_images[-1] = pygame.transform.scale(potion_images[-1], (30, 30))

    while len(argent_positions) < 10:
        position = random.choice(cases_valides)

        # Vérifier si la position est valide et ne se trouve pas dans les exclusions
        if (
            position not in argent_positions and
            position not in exclusions
        ):
            argent_positions.append(position)
            argent_images.append(pygame.image.load('img/element/argent.png').convert())

            argent_images[-1].set_colorkey(BLACK)
            argent_images[-1] = pygame.transform.scale(argent_images[-1], (30, 30))

    return potion_positions, potion_images, argent_positions, argent_images




def verifier_objet(joueur_position, potion_positions, potion_images, argent_positions, argent_images, joueur):
    if joueur_position in potion_positions:
        index = potion_positions.index(joueur_position)
        potion_positions.pop(index)
        del potion_images[index]
        joueur.ajouter_potion(1)

    if joueur_position in argent_positions:
        index = argent_positions.index(joueur_position)
        argent_positions.pop(index)
        del argent_images[index]
        joueur.ajouter_argent(100)

def verifier_piege(joueur_position, piege_positions, piege_images) :
    if joueur_position in piege_positions :
        index = piege_positions.index(joueur_position)
        piege_positions.pop(index)
        del piege_images[index]

def comparaison_vitesse(joueur, monstre):
    return joueur.vitesse > monstre.vitesse

def attaque(joueur, monstre) :
    monstre.pv = monstre.pv - joueur.attaque

def attaque_puissante(joueur, monstre) :
    if random.randint(1, 3) == 1:
        pass
    else:
        monstre.pv = monstre.pv - (((joueur.attaque + joueur.magie) / 2) * 1.5)

def attaque_magique(joueur, monstre) :
    monstre.pv = monstre.pv - joueur.magie 

def choix_attaque(attaque_choisi, joueur, monstre) :
    if attaque_choisi == 1 :
        attaque(joueur, monstre)
    elif attaque_choisi == 2 :
        attaque_puissante(joueur, monstre)
    else :
        attaque_magique(joueur, monstre)

def monstre_attaque(joueur, monstre) :
    if random.randint(1, 3) == 1:
        joueur.pv = joueur.pv - monstre.attaque
    else :
        pass  

def combat(attaque_choisi, joueur, monstre) :
    if comparaison_vitesse(joueur, monstre) :
        choix_attaque(attaque_choisi, joueur, monstre)
    else :
        monstre_attaque(joueur, monstre)



if __name__ == '__main__' :

    rectangle1 = Rectangle((BLACK), 50, 50, 20, 5)
    rectangle2 = Rectangle((BLACK), 200, 200, 5, 20)
    pointRouge = Point(100,200)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        background_image = pygame.image.load('img/map/mapForest.png').convert()
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        rectangle1.draw()
        rectangle2.draw()
        pointRouge.draw((RED), 5)

        pygame.display.flip()