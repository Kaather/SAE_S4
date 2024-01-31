'''Nathan Rousselle TD1 / TPA
Voici mon programme de jeu de plateau, malheureusement incomplet par manque de temps :( 
j'ai pu créer un labyrinthe qui est possible à parcourir entièrement, il est par ailleurs généré
aléatoirement, il est possible de s'y déplacer dedans à 1, 2, 3 et 4 joueurs.
Chaque classe possède ses propres statistiques, je n'ai pas pu réellement les équilibrer.
Il est possible pour les joueurs de ramasser de l'argent, j'avais prévu de faire un magasin mais
je n'ai pas pu le faire malheureusement bien que sa conception me semble clair et facilement réalisable
Les joueurs peuvent ramasser des potions et en consommer
Les joueurs peuvent entrer dans des pièges pour combattre des monstres (il n'y a qu'un seul monstre malheureusement)
Je n'ai pas pu créer le combat final par manque de temps mais en affrontant les 5 monstres (donc en allant dans les 5 pièges)
il est possible d'activer le piège en or en se rendant à sa position, un message s'affichera et vous pourrez ouvrir le piege 
ce qui vous montrera directement le message de victoire.
Je n'ai pas eu le temps d'écrire les règles de mon jeu.
J'ai pensé à ajouter des fonctionnalité comme s'échanger des potions / de l'argent ou pouvoir se provoquer
en duel entre joueurs (facile) mais aussi être dans le noir dans le labyrinthe et il s'éclaire au fur et à mesure où
l'on avance dedans (faisable).
j'ai pensé à faire des animations mais evidemment je l'aurai fais à la toute fin
Je tiens à très sincèrement m'excuser pour l'horrible qualité de ce code (répétition sans fin, non lisibilité du code, ...)
'''


import pygame
import sys
from labyrinthe import *
from plateau import *
from pygameOutils import *
from jeuGraphique import *

# Initialiser Pygame
pygame.init()

def nb_joueurs() :
    graphe = None

    bouton_1_survole = False
    bouton_2_survole = False
    bouton_3_survole = False
    bouton_4_survole = False
    bouton_5_survole = False

    fond_image = pygame.image.load('img/map/dongeon.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    while running:

        screen.blit(fond_image, (0, 0))
        draw_text("Combien de joueurs ?", 120, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.2, BLACK)

        mx, my = pygame.mouse.get_pos()

        
        bouton_1 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)
        bouton_2 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)
        bouton_3 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)
        bouton_4 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)
        bouton_5 = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)


        bouton_1.fill(BROWN_TR if not bouton_1_survole else BROWN)
        bouton_2.fill(BROWN_TR if not bouton_2_survole else BROWN)
        bouton_3.fill(BROWN_TR if not bouton_3_survole else BROWN)
        bouton_4.fill(BROWN_TR if not bouton_4_survole else BROWN)
        bouton_5.fill(TRANSPARENT if not bouton_5_survole else BROWN)
        

        screen.blit(bouton_1, ((SCREEN_WIDTH*0.12) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
        screen.blit(bouton_2, ((SCREEN_WIDTH*0.373) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
        screen.blit(bouton_3, ((SCREEN_WIDTH*0.626) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
        screen.blit(bouton_4, ((SCREEN_WIDTH*0.88) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
        screen.blit(bouton_5, ((SCREEN_WIDTH*(0.92), SCREEN_HEIGHT*(0.001))))
        

        draw_text("1 Joueur", 51, SCREEN_WIDTH*0.12, SCREEN_HEIGHT*(0.655), BLACK)
        draw_text("2 Joueurs", 51, SCREEN_WIDTH*0.373, SCREEN_HEIGHT*(0.655), BLACK)
        draw_text("3 Joueurs", 51, SCREEN_WIDTH*0.626, SCREEN_HEIGHT*(0.655), BLACK)
        draw_text("4 Joueurs", 51, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*(0.655), BLACK)
        draw_text("Retour", 30, SCREEN_WIDTH*0.96, -5, BLACK)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_1_survole = bouton_1.get_rect(center=((SCREEN_WIDTH*0.12), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
                bouton_2_survole = bouton_2.get_rect(center=((SCREEN_WIDTH*0.373), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
                bouton_3_survole = bouton_3.get_rect(center=((SCREEN_WIDTH*0.626), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
                bouton_4_survole = bouton_4.get_rect(center=((SCREEN_WIDTH*0.88), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
                bouton_5_survole = bouton_5.get_rect(center=((SCREEN_WIDTH*0.965), SCREEN_HEIGHT*(0.015))).collidepoint((mx, my))   
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_1.get_rect(center=((SCREEN_WIDTH*0.12), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                    classes = [1]
                    running = False
                if bouton_2.get_rect(center=((SCREEN_WIDTH*0.373), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                    classes = [1, 2]
                    running = False
                if bouton_3.get_rect(center=((SCREEN_WIDTH*0.626), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                    classes = [1, 2, 3]
                    running = False
                if bouton_4.get_rect(center=((SCREEN_WIDTH*0.88), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)) :
                    classes = [1, 2, 3, 4]
                    running = False
                if bouton_5.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.015)).collidepoint((mx, my)):
                    classes = []
                    running = False

        pygame.display.update()

    if classes :

        for player in range(len(classes)):
            archetypes(player + 1, graphe)
        map_choix(graphe, joueurs_choix)

def archetypes(number, graphe) :

    bouton_1_survole = False
    bouton_2_survole = False
    bouton_3_survole = False
    bouton_4_survole = False
    bouton_5_survole = False
    bouton_6_survole = False

    fond_image = pygame.image.load('img/map/dongeon.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    imgPaladin = pygame.image.load("img/classe/Paladin.png").convert_alpha()
    imgArcher = pygame.image.load("img/classe/Archer.png").convert_alpha()
    imgMage = pygame.image.load("img/classe/Mage.png").convert_alpha()
    imgBerserk = pygame.image.load("img/classe/Berserk.png").convert_alpha()
    imgAssassin = pygame.image.load("img/classe/Assassin.png").convert_alpha()
    imgHealer = pygame.Surface((0, 0))
    if number != 1 :
        imgHealer = pygame.image.load("img/classe/Healer.png").convert_alpha()

    imgPaladin = pygame.transform.scale(imgPaladin, (175, 175)) 
    imgArcher = pygame.transform.scale(imgArcher, (175, 175)) 
    imgMage = pygame.transform.scale(imgMage, (175, 175)) 
    imgBerserk = pygame.transform.scale(imgBerserk, (175, 175)) 
    imgAssassin = pygame.transform.scale(imgAssassin, (175, 175))
    if number != 1 : 
        imgHealer = pygame.transform.scale(imgHealer, (175, 175)) 

    imgPaladin_rect = imgPaladin.get_rect(center=(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.42))
    imgArcher_rect = imgArcher.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.42))
    imgMage_rect = imgMage.get_rect(center=(SCREEN_WIDTH * 0.9, SCREEN_HEIGHT * 0.42))
    imgBerserk_rect = imgBerserk.get_rect(center=(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.78))
    imgAssassin_rect = imgAssassin.get_rect(center=(SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.78))
    if number != 1 :
        imgHealer_rect = imgHealer.get_rect(center=(SCREEN_WIDTH * 0.9, SCREEN_HEIGHT * 0.78))

    running = True
    while running:

        screen.blit(fond_image, (0, 0))
        draw_text("Choisissez votre classe !", 80, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.01, BLACK)
        draw_text(f"Joueur {number} :", 70, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.15, BLACK)

        mx, my = pygame.mouse.get_pos()

        
        bouton_1 = pygame.Surface((SCREEN_WIDTH//6, SCREEN_HEIGHT//12), pygame.SRCALPHA)
        bouton_2 = pygame.Surface((SCREEN_WIDTH//6, SCREEN_HEIGHT//12), pygame.SRCALPHA)
        bouton_3 = pygame.Surface((SCREEN_WIDTH//6, SCREEN_HEIGHT//12), pygame.SRCALPHA)
        bouton_4 = pygame.Surface((SCREEN_WIDTH//6, SCREEN_HEIGHT//12), pygame.SRCALPHA)
        bouton_5 = pygame.Surface((SCREEN_WIDTH//6, SCREEN_HEIGHT//12), pygame.SRCALPHA)
        if number != 1 :
            bouton_6 = pygame.Surface((SCREEN_WIDTH//6, SCREEN_HEIGHT//12), pygame.SRCALPHA)


        bouton_1.fill(BROWN_TR if not bouton_1_survole else BROWN)
        bouton_2.fill(BROWN_TR if not bouton_2_survole else BROWN)
        bouton_3.fill(BROWN_TR if not bouton_3_survole else BROWN)
        bouton_4.fill(BROWN_TR if not bouton_4_survole else BROWN)
        bouton_5.fill(BROWN_TR if not bouton_5_survole else BROWN)
        if number != 1 :
            bouton_6.fill(BROWN_TR if not bouton_6_survole else BROWN)
        

        screen.blit(bouton_1, ((SCREEN_WIDTH*0.1) - (SCREEN_WIDTH//6/2), SCREEN_HEIGHT*(0.55)))
        screen.blit(bouton_2, ((SCREEN_WIDTH*0.5) - (SCREEN_WIDTH//6/2), SCREEN_HEIGHT*(0.55)))
        screen.blit(bouton_3, ((SCREEN_WIDTH*0.9) - (SCREEN_WIDTH//6/2), SCREEN_HEIGHT*(0.55)))
        screen.blit(bouton_4, ((SCREEN_WIDTH*0.1) - (SCREEN_WIDTH//6/2), SCREEN_HEIGHT*(0.9)))
        screen.blit(bouton_5, ((SCREEN_WIDTH*0.5) - (SCREEN_WIDTH//6/2), SCREEN_HEIGHT*(0.9)))
        if number != 1 :
            screen.blit(bouton_6, ((SCREEN_WIDTH*0.9) - (SCREEN_WIDTH//6/2), SCREEN_HEIGHT*(0.9)))
        

        draw_text("Paladin", 41, SCREEN_WIDTH*0.1, SCREEN_HEIGHT*(0.555), BLACK)
        draw_text("Archer", 41, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*(0.555), BLACK)
        draw_text("Mage", 41, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*(0.555), BLACK)
        draw_text("Berserk", 41, SCREEN_WIDTH*0.1, SCREEN_HEIGHT*(0.905), BLACK)
        draw_text("Assassin", 41, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*(0.905), BLACK)
        if number != 1 :
            draw_text("Healer", 41, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*(0.905), BLACK)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_1_survole = bouton_1.get_rect(center=((SCREEN_WIDTH*0.1), (SCREEN_HEIGHT*(0.55) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my))
                bouton_2_survole = bouton_2.get_rect(center=((SCREEN_WIDTH*0.5), (SCREEN_HEIGHT*(0.55) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my))
                bouton_3_survole = bouton_3.get_rect(center=((SCREEN_WIDTH*0.9), (SCREEN_HEIGHT*(0.55) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my))
                bouton_4_survole = bouton_4.get_rect(center=((SCREEN_WIDTH*0.1), (SCREEN_HEIGHT*(0.9) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my))
                bouton_5_survole = bouton_5.get_rect(center=((SCREEN_WIDTH*0.5), (SCREEN_HEIGHT*(0.9) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my))
                if number != 1 :
                    bouton_6_survole = bouton_6.get_rect(center=((SCREEN_WIDTH*0.9), (SCREEN_HEIGHT*(0.9) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_1.get_rect(center=((SCREEN_WIDTH*0.1), (SCREEN_HEIGHT*(0.55) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)):
                    joueurs_choix.append(Joueur("Paladin", graphe, (5,10), 100, 100, 16, 12, 10, 5, 100, "img/classe/Paladin.png"))
                    running = False

                if bouton_2.get_rect(center=((SCREEN_WIDTH*0.5), (SCREEN_HEIGHT*(0.55) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)):
                    joueurs_choix.append(Joueur("Archer", graphe, (5,10), 80, 80, 15, 5, 20, 5, 100, "img/classe/Archer.png"))
                    running = False

                if bouton_3.get_rect(center=((SCREEN_WIDTH*0.9), (SCREEN_HEIGHT*(0.55) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)):
                    joueurs_choix.append(Joueur("Mage", graphe, (5,10), 80, 80, 5, 25, 8, 5, 100, "img/classe/Mage.png"))
                    running = False

                if bouton_4.get_rect(center=((SCREEN_WIDTH*0.1), (SCREEN_HEIGHT*(0.9) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)) :
                    joueurs_choix.append(Joueur("Berserk", graphe, (5,10),120, 120, 20, 5, 12, 5, 100, "img/classe/Berserk.png"))
                    running = False

                if bouton_5.get_rect(center=((SCREEN_WIDTH*0.5), (SCREEN_HEIGHT*(0.9) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)):
                    joueurs_choix.append(Joueur("Assassin", graphe, (5,10), 90, 90, 20, 10, 15, 5, 100, "img/classe/Assassin.png"))
                    running = False

                if number != 1 :    
                    if bouton_6.get_rect(center=((SCREEN_WIDTH*0.9), (SCREEN_HEIGHT*(0.9) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)) :
                        joueurs_choix.append(Joueur("Healer", graphe, (5,10), 70, 70, 0, 30, 10, 5, 100, "img/classe/Healer.png"))
                        running = False


        screen.blit(imgPaladin, imgPaladin_rect)
        screen.blit(imgArcher, imgArcher_rect)
        screen.blit(imgMage, imgMage_rect)
        screen.blit(imgBerserk, imgBerserk_rect)
        screen.blit(imgAssassin, imgAssassin_rect)
        if number != 1 :
            screen.blit(imgHealer, imgHealer_rect)

        pygame.display.update()

    return joueurs_choix

def map_choix(graphe, joueurs_choix) :
    bouton_1_survole = False
    bouton_2_survole = False
    bouton_3_survole = False
    bouton_4_survole = False

    fond_image = pygame.image.load('img/map/dongeon.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    while running:

        screen.blit(fond_image, (0, 0))
        draw_text("Choisissez votre map !", 110, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.2, BLACK)

        mx, my = pygame.mouse.get_pos()

        
        bouton_1 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)
        bouton_2 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)
        bouton_3 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)
        bouton_4 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)


        bouton_1.fill(BROWN_TR if not bouton_1_survole else BROWN)
        bouton_2.fill(BROWN_TR if not bouton_2_survole else BROWN)
        bouton_3.fill(BROWN_TR if not bouton_3_survole else BROWN)
        bouton_4.fill(BROWN_TR if not bouton_4_survole else BROWN)
        

        screen.blit(bouton_1, ((SCREEN_WIDTH*0.12) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
        screen.blit(bouton_2, ((SCREEN_WIDTH*0.373) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
        screen.blit(bouton_3, ((SCREEN_WIDTH*0.626) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
        screen.blit(bouton_4, ((SCREEN_WIDTH*0.88) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
        

        draw_text("Desert", 51, SCREEN_WIDTH*0.12, SCREEN_HEIGHT*(0.655), BLACK)
        draw_text("Neige", 51, SCREEN_WIDTH*0.373, SCREEN_HEIGHT*(0.655), BLACK)
        draw_text("Foret", 51, SCREEN_WIDTH*0.626, SCREEN_HEIGHT*(0.655), BLACK)
        draw_text("Dongeon", 51, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*(0.655), BLACK)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_1_survole = bouton_1.get_rect(center=((SCREEN_WIDTH*0.12), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
                bouton_2_survole = bouton_2.get_rect(center=((SCREEN_WIDTH*0.373), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
                bouton_3_survole = bouton_3.get_rect(center=((SCREEN_WIDTH*0.626), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
                bouton_4_survole = bouton_4.get_rect(center=((SCREEN_WIDTH*0.88), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_1.get_rect(center=((SCREEN_WIDTH*0.12), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                    affichageGraphique(0, graphe, joueurs_choix)
                    running = False
                if bouton_2.get_rect(center=((SCREEN_WIDTH*0.373), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                    affichageGraphique(1, graphe, joueurs_choix)
                    running = False
                if bouton_3.get_rect(center=((SCREEN_WIDTH*0.626), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                    affichageGraphique(2, graphe, joueurs_choix)
                    running = False
                if bouton_4.get_rect(center=((SCREEN_WIDTH*0.88), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)) :
                    affichageGraphique(3, graphe, joueurs_choix)
                    running = False



        pygame.display.update()


def regles() :
    bouton_5_survole = False

    fond_image = pygame.image.load('img/map/desert.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    while running :

        screen.blit(fond_image, (0, 0))
        mx, my = pygame.mouse.get_pos()

        bouton_5 = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)
        bouton_5.fill(TRANSPARENT if not bouton_5_survole else BROWN)
        screen.blit(bouton_5, ((SCREEN_WIDTH*(0.92), SCREEN_HEIGHT*(0.001))))
        draw_text("Quitter", 30, SCREEN_WIDTH*0.96, -5, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_5_survole = bouton_5.get_rect(center=((SCREEN_WIDTH*0.965), SCREEN_HEIGHT*(0.015))).collidepoint((mx, my))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_5.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.015)).collidepoint((mx, my)):
                    running = False 

        pygame.display.update()

def credit() : 
    bouton_5_survole = False

    fond_image = pygame.image.load('img/map/neige.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    running = True
    while running :

        screen.blit(fond_image, (0, 0))
        mx, my = pygame.mouse.get_pos()

        draw_text("Creator :", 90, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.15, BLACK)
        draw_text("Nathan Rousselle", 60, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.35, BLACK)
        draw_text("With the help of :", 70, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.60, BLACK)
        draw_text("Lionnel Conoir", 40, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.80, BLACK)

        bouton_5 = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)
        bouton_5.fill(TRANSPARENT if not bouton_5_survole else BROWN)
        screen.blit(bouton_5, ((SCREEN_WIDTH*(0.92), SCREEN_HEIGHT*(0.001))))
        draw_text("Quitter", 30, SCREEN_WIDTH*0.96, -5, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_5_survole = bouton_5.get_rect(center=((SCREEN_WIDTH*0.965), SCREEN_HEIGHT*(0.015))).collidepoint((mx, my))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_5.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.015)).collidepoint((mx, my)):
                    running = False 

        pygame.display.update()

def main_menu():
    bouton_1_survole = False
    bouton_2_survole = False
    bouton_3_survole = False
    bouton_4_survole = False

    fond_image = pygame.image.load('img/map/foret.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while True:

        # Afficher l'arrière-plan
        screen.blit(fond_image, (0, 0))
        draw_text("Monster Slayer", 120, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.1, BLACK)

        mx, my = pygame.mouse.get_pos()

        bouton_1 = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
        bouton_2 = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
        bouton_3 = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
        bouton_4 = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//14), pygame.SRCALPHA)


        bouton_1.fill(BROWN_TR if not bouton_1_survole else BROWN)
        bouton_2.fill(BROWN_TR if not bouton_2_survole else BROWN)
        bouton_3.fill(BROWN_TR if not bouton_3_survole else BROWN)
        bouton_4.fill(BROWN_TR if not bouton_4_survole else BROWN)


        screen.blit(bouton_1, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.4)))
        screen.blit(bouton_2, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.6)))
        screen.blit(bouton_3, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
        screen.blit(bouton_4, ((SCREEN_WIDTH*0.86), SCREEN_HEIGHT*0.9))

        draw_text("Jouer", 60, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.375) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)
        draw_text("Règles", 60, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.575) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)
        draw_text("Quitter", 60, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)
        draw_text("Crédits", 30, SCREEN_WIDTH*0.921, SCREEN_HEIGHT*0.91, BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_1_survole = bouton_1.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.4) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))
                bouton_2_survole = bouton_2.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.6) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))
                bouton_3_survole = bouton_3.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))
                bouton_4_survole = bouton_4.get_rect(center=((SCREEN_WIDTH*0.922), SCREEN_HEIGHT*(0.932))).collidepoint((mx, my))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_1.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.4) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)):
                    nb_joueurs()
                if bouton_2.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.6) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)):
                    regles()
                if bouton_3.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)):
                    pygame.quit()
                    print("Aucune statistiques disponibles !")
                    sys.exit()                    
                if bouton_4.get_rect(center=((SCREEN_WIDTH*0.922), SCREEN_HEIGHT*(0.932))).collidepoint((mx, my)) :
                    credit()
                    
        pygame.display.update()

if __name__ == "__main__":
    main_menu()