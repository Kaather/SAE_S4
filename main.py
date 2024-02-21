import pygame
import sys
from labyrinthe import *
from plateau import *
from pygameOutils import *
from jeuGraphique import *
from jeuGraphiqueReseau import *
from bouton import *
from ia_deplacement import *
import socket
import time
import os


pygame.init()

def nb_joueurs_multi(socket, numero):
    graphe = None
    fond_image = pygame.image.load('img/map/donjon.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bouton_2j = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.373, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "2 Joueurs", SCREEN_WIDTH//25)
    bouton_3j = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.626, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "3 Joueurs", SCREEN_WIDTH//25)
    bouton_4j = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "4 Joueurs", SCREEN_WIDTH//25)
    bouton_quitter = Bouton(SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22, SCREEN_WIDTH//1.04, SCREEN_HEIGHT//50, TRANSPARENT, BROWN, "Quitter", SCREEN_WIDTH//45)

    if numero == "1":
        running = True
        while running:
            screen.blit(fond_image, (0, 0))
            draw_text("Combien de joueurs ?", 120, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.2, BLACK)
            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    mx, my = pygame.mouse.get_pos()
                    bouton_2j.hovered = bouton_2j.est_survol(mx, my)
                    bouton_3j.hovered = bouton_3j.est_survol(mx, my)
                    bouton_4j.hovered = bouton_4j.est_survol(mx, my)
                    bouton_quitter.hovered = bouton_quitter.est_survol(mx, my)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_2j.est_survol(mx, my):
                        classes = [1, 2]
                        max_joueurs = 2
                        running = False
                        socket.send(str.encode(str(classes)))

                    if bouton_3j.est_survol(mx, my):
                        classes = [1, 2, 3]
                        max_joueurs = 3
                        running = False
                        socket.send(str.encode(str(classes)))

                    if bouton_4j.est_survol(mx, my):
                        classes = [1, 2, 3, 4]
                        max_joueurs = 4
                        running = False
                        socket.send(str.encode(str(classes)))

                    if bouton_quitter.est_survol(mx, my):
                        classes = []
                        running = False
                        socket.send(str.encode(str(classes)))

            bouton_2j.bouton_actuelle = bouton_2j.bouton_survol if bouton_2j.hovered else bouton_2j.bouton_normale
            bouton_3j.bouton_actuelle = bouton_3j.bouton_survol if bouton_3j.hovered else bouton_3j.bouton_normale
            bouton_4j.bouton_actuelle = bouton_4j.bouton_survol if bouton_4j.hovered else bouton_4j.bouton_normale
            bouton_quitter.bouton_actuelle = bouton_quitter.bouton_survol if bouton_quitter.hovered else bouton_quitter.bouton_normale

            bouton_2j.dessiner(screen)
            bouton_3j.dessiner(screen)
            bouton_4j.dessiner(screen)
            bouton_quitter.dessiner(screen)

            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

    else:
        fond_image = pygame.image.load('img/map/donjon.png').convert()
        fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        classes = None
        while classes is None:
            screen.blit(fond_image, (0, 0))
            draw_text("En attente du joueur 1...", 120, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.2, BLACK)
            pygame.display.update()
            try:
                classes = socket.recv(1024).decode()
                classes = eval(classes)
                if classes == []:
                    pygame.quit()
                    sys.exit()
                elif classes == [1, 2]:
                    max_joueurs = 2
                elif classes == [1, 2, 3]:
                    max_joueurs = 3
                elif classes == [1, 2, 3, 4]:
                    max_joueurs = 4                
            except Exception as e:
                print("Erreur de réception des données:", e)
                continue 
    if classes:
        
        for player in range(len(classes)):
            if str(player + 1) == numero: 
                joueur = archetypes_multi(player + 1, graphe, socket)
                if player + 1 == max_joueurs:
                    joueurs_choix.append(joueur)                                  
            else:
                while len(joueurs_choix) != player + 1:
                    screen.blit(fond_image, (0, 0))
                    draw_text("En attente du choix des joueurs...", 120, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.2, BLACK)
                    pygame.display.update()
                    try:
                        data = socket.recv(1024).decode()
                        liste = eval(data)
                        joueur = Joueur(liste[0], liste[1], liste[2], liste[3], liste[4], liste[5], liste[6], liste[7], liste[8], liste[9], liste[10])                
                        joueurs_choix.append(joueur)                                                
                    except Exception as e:
                        print("Erreur de réception des données:", e)
                        continue              
        map_choix_multi(graphe, joueurs_choix, numero, socket)

def choix_difficulte():

    fond_image = pygame.image.load('img/map/donjon.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bouton_facile = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.2, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "Facile", SCREEN_WIDTH//25)
    bouton_moyen = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "Moyen", SCREEN_WIDTH//25)
    bouton_difficile = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.8, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "Difficile", SCREEN_WIDTH//25)

    difficulte = None

    running = True
    while running:
        screen.blit(fond_image, (0, 0))
        draw_text("Choisissez la difficulté :", SCREEN_WIDTH//16, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.2, BLACK)
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                bouton_facile.hovered = bouton_facile.est_survol(mx, my)
                bouton_moyen.hovered = bouton_moyen.est_survol(mx, my)
                bouton_difficile.hovered = bouton_difficile.est_survol(mx, my)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_facile.est_survol(mx, my):
                    difficulte = "Facile"
                    running = False
                    deplacement_facile()

                if bouton_moyen.est_survol(mx, my):
                    difficulte = "Moyen"
                    running = False
                    deplacement_intermediaire()

                if bouton_difficile.est_survol(mx, my):
                    difficulte = "Difficile"
                    running = False
                    deplacement_difficile()

        bouton_facile.bouton_actuelle = bouton_facile.bouton_survol if bouton_facile.hovered else bouton_facile.bouton_normale
        bouton_moyen.bouton_actuelle = bouton_moyen.bouton_survol if bouton_moyen.hovered else bouton_moyen.bouton_normale
        bouton_difficile.bouton_actuelle = bouton_difficile.bouton_survol if bouton_difficile.hovered else bouton_difficile.bouton_normale

        bouton_facile.dessiner(screen)
        bouton_moyen.dessiner(screen)
        bouton_difficile.dessiner(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    print(difficulte)
    return difficulte

def archetypes_multi(number, graphe, socket) :

    fond_image = pygame.image.load('img/map/donjon.png').convert()
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

    bouton_paladin = Bouton(SCREEN_WIDTH//6, SCREEN_HEIGHT//12, SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.6, BROWN_TR, BROWN, "Paladin", SCREEN_WIDTH//30)
    bouton_archer = Bouton(SCREEN_WIDTH//6, SCREEN_HEIGHT//12, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.6, BROWN_TR, BROWN, "Archer", SCREEN_WIDTH//30)
    bouton_mage = Bouton(SCREEN_WIDTH//6, SCREEN_HEIGHT//12, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.6, BROWN_TR, BROWN, "Mage", SCREEN_WIDTH//30)
    bouton_berserk = Bouton(SCREEN_WIDTH//6, SCREEN_HEIGHT//12, SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.95, BROWN_TR, BROWN, "Berserk", SCREEN_WIDTH//30)
    bouton_assassin = Bouton(SCREEN_WIDTH//6, SCREEN_HEIGHT//12, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.95, BROWN_TR, BROWN, "Assassin", SCREEN_WIDTH//30)
    if number != 1 :
        bouton_healer = Bouton(SCREEN_WIDTH//6, SCREEN_HEIGHT//12, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.95, BROWN_TR, BROWN, "Healer", SCREEN_WIDTH//30)

    running = True
    while running:

        screen.blit(fond_image, (0, 0))
        draw_text("Choisissez votre classe !", 80, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.01, BLACK)
        draw_text(f"Joueur {number} :", 70, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.15, BLACK)
        mx, my = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_paladin.hovered = bouton_paladin.est_survol(mx, my)
                bouton_archer.hovered = bouton_archer.est_survol(mx, my)
                bouton_mage.hovered = bouton_mage.est_survol(mx, my)
                bouton_berserk.hovered = bouton_berserk.est_survol(mx, my)
                bouton_assassin.hovered = bouton_assassin.est_survol(mx, my)
                if number != 1 :
                    bouton_healer.hovered = bouton_healer.est_survol(mx, my)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_paladin.est_survol(mx, my):
                    liste = ["Paladin", graphe, (5,10), 100, 100, 16, 12, 10, 5, 100, "img/classe/Paladin.png"]
                    joueur = Joueur("Paladin", graphe, (5,10), 100, 100, 16, 12, 10, 5, 100, "img/classe/Paladin.png")
                    socket.send(str.encode(str(liste)))
                    running = False

                if bouton_archer.est_survol(mx, my):
                    liste = ["Archer", graphe, (5,10), 80, 80, 15, 5, 20, 5, 100, "img/classe/Archer.png"]
                    joueur = Joueur("Archer", graphe, (5,10), 80, 80, 15, 5, 20, 5, 100, "img/classe/Archer.png")
                    socket.send(str.encode(str(liste)))
                    running = False

                if bouton_mage.est_survol(mx, my):
                    liste = ["Mage", graphe, (5,10), 80, 80, 5, 25, 8, 5, 100, "img/classe/Mage.png"]
                    joueur = Joueur("Mage", graphe, (5,10), 80, 80, 5, 25, 8, 5, 100, "img/classe/Mage.png")
                    socket.send(str.encode(str(liste)))
                    running = False

                if bouton_berserk.est_survol(mx, my):
                    liste = ["Berserk", graphe, (5,10),120, 120, 20, 5, 12, 5, 100, "img/classe/Berserk.png"]
                    joueur = Joueur("Berserk", graphe, (5,10),120, 120, 20, 5, 12, 5, 100, "img/classe/Berserk.png")
                    socket.send(str.encode(str(liste)))
                    running = False

                if bouton_assassin.est_survol(mx, my):
                    liste = ["Assassin", graphe, (5,10), 90, 90, 20, 10, 15, 5, 100, "img/classe/Assassin.png"]
                    joueur = Joueur("Assassin", graphe, (5,10), 90, 90, 20, 10, 15, 5, 100, "img/classe/Assassin.png")
                    socket.send(str.encode(str(liste)))
                    running = False

                if number != 1 :    
                    if bouton_healer.est_survol(mx, my):
                        liste = ["Healer", graphe, (5,10), 70, 70, 0, 30, 10, 5, 100, "img/classe/Healer.png"]
                        joueur = Joueur("Healer", graphe, (5,10), 70, 70, 0, 30, 10, 5, 100, "img/classe/Healer.png")
                        socket.send(str.encode(str(liste)))
                        running = False


        screen.blit(imgPaladin, imgPaladin_rect)
        screen.blit(imgArcher, imgArcher_rect)
        screen.blit(imgMage, imgMage_rect)
        screen.blit(imgBerserk, imgBerserk_rect)
        screen.blit(imgAssassin, imgAssassin_rect)
        if number != 1 :
            screen.blit(imgHealer, imgHealer_rect)

        bouton_paladin.bouton_actuelle = bouton_paladin.bouton_survol if bouton_paladin.hovered else bouton_paladin.bouton_normale
        bouton_archer.bouton_actuelle = bouton_archer.bouton_survol if bouton_archer.hovered else bouton_archer.bouton_normale
        bouton_mage.bouton_actuelle = bouton_mage.bouton_survol if bouton_mage.hovered else bouton_mage.bouton_normale
        bouton_berserk.bouton_actuelle = bouton_berserk.bouton_survol if bouton_berserk.hovered else bouton_berserk.bouton_normale
        bouton_assassin.bouton_actuelle = bouton_assassin.bouton_survol if bouton_assassin.hovered else bouton_assassin.bouton_normale
        if number != 1 :
            bouton_healer.bouton_actuelle = bouton_healer.bouton_survol if bouton_healer.hovered else bouton_healer.bouton_normale

        bouton_paladin.dessiner(screen)
        bouton_archer.dessiner(screen)
        bouton_mage.dessiner(screen)
        bouton_berserk.dessiner(screen)
        bouton_assassin.dessiner(screen)
        if number != 1 :
            bouton_healer.dessiner(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    return joueur

def map_choix_multi(graphe, joueurs_choix, numero, socket):
    
    fond_image = pygame.image.load('img/map/donjon.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bouton_desert = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.12, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "Desert", SCREEN_WIDTH//30)
    bouton_neige = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.373, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "Neige", SCREEN_WIDTH//30)
    bouton_foret = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.626, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "Foret", SCREEN_WIDTH//30)
    bouton_donjon = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "Donjon", SCREEN_WIDTH//30)

    if numero == "1":
        running = True
        while running:

            screen.blit(fond_image, (0, 0))
            draw_text("Choisissez votre map !", 110, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.2, BLACK)

            mx, my = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION: 
                    mx, my = pygame.mouse.get_pos()
                    bouton_desert.hovered = bouton_desert.est_survol(mx, my)
                    bouton_neige.hovered = bouton_neige.est_survol(mx, my)
                    bouton_foret.hovered = bouton_foret.est_survol(mx, my)
                    bouton_donjon.hovered = bouton_donjon.est_survol(mx, my)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_desert.est_survol(mx, my):
                        socket.send(str.encode(str(0)))
                        maps = 0
                        running = False
                    if bouton_neige.est_survol(mx, my):
                        socket.send(str.encode(str(1)))
                        maps = 1
                        running = False
                    if bouton_foret.est_survol(mx, my):
                        socket.send(str.encode(str(2)))
                        maps = 2
                        running = False
                    if bouton_donjon.est_survol(mx, my):
                        socket.send(str.encode(str(3)))
                        maps = 3
                        running = False

            bouton_desert.bouton_actuelle = bouton_desert.bouton_survol if bouton_desert.hovered else bouton_desert.bouton_normale
            bouton_neige.bouton_actuelle = bouton_neige.bouton_survol if bouton_neige.hovered else bouton_neige.bouton_normale
            bouton_foret.bouton_actuelle = bouton_foret.bouton_survol if bouton_foret.hovered else bouton_foret.bouton_normale
            bouton_donjon.bouton_actuelle = bouton_donjon.bouton_survol if bouton_donjon.hovered else bouton_donjon.bouton_normale

            bouton_desert.dessiner(screen)
            bouton_neige.dessiner(screen)
            bouton_foret.dessiner(screen)
            bouton_donjon.dessiner(screen)
            
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)
    
    else:
        fond_image = pygame.image.load('img/map/donjon.png').convert()
        fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        running = True
        while running:
            screen.blit(fond_image, (0, 0))
            draw_text("En attente du joueur 1...", 120, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.2, BLACK)
            pygame.display.update()
            try:
                data = socket.recv(1024).decode()
                if data == "0":
                    maps = 0
                    running = False
                elif data == "1":
                    maps = 1
                    running = False
                elif data == "2":
                    maps = 2
                    running = False
                elif data == "3":
                    maps = 3
                    running = False
            except Exception as e:
                print("Erreur de réception des données:", e)
                continue
    time.sleep(2)
    affichageGraphiqueReseau(maps, graphe, joueurs_choix, socket, numero)

def nb_joueurs() :
    graphe = None

    fond_image = pygame.image.load('img/map/donjon.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bouton_1j = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.12, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "1 Joueur", SCREEN_WIDTH//25)
    bouton_2j = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.373, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "2 Joueurs", SCREEN_WIDTH//25)
    bouton_3j = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.626, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "3 Joueurs", SCREEN_WIDTH//25)
    bouton_4j = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "4 Joueurs", SCREEN_WIDTH//25)
    bouton_retour = Bouton(SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22, SCREEN_WIDTH//1.04, SCREEN_HEIGHT//50, TRANSPARENT, BROWN, "Retour", SCREEN_WIDTH//45)

    running = True
    while running:

        screen.blit(fond_image, (0, 0))
        draw_text("Combien de joueurs ?", 120, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.2, BLACK)
        
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                bouton_1j.hovered = bouton_1j.est_survol(mx, my)
                bouton_2j.hovered = bouton_2j.est_survol(mx, my)
                bouton_3j.hovered = bouton_3j.est_survol(mx, my)
                bouton_4j.hovered = bouton_4j.est_survol(mx, my)
                bouton_retour.hovered = bouton_retour.est_survol(mx, my)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_1j.est_survol(mx, my):
                    classes = [1]
                    running = False

                if bouton_2j.est_survol(mx, my):
                    classes = [1, 2]
                    running = False

                if bouton_3j.est_survol(mx, my):
                    classes = [1, 2, 3]
                    running = False

                if bouton_4j.est_survol(mx, my):
                    classes = [1, 2, 3, 4]
                    running = False

                if bouton_retour.est_survol(mx, my):
                    classes = []
                    running = False

        bouton_1j.bouton_actuelle = bouton_1j.bouton_survol if bouton_1j.hovered else bouton_1j.bouton_normale
        bouton_2j.bouton_actuelle = bouton_2j.bouton_survol if bouton_2j.hovered else bouton_2j.bouton_normale
        bouton_3j.bouton_actuelle = bouton_3j.bouton_survol if bouton_3j.hovered else bouton_3j.bouton_normale
        bouton_4j.bouton_actuelle = bouton_4j.bouton_survol if bouton_4j.hovered else bouton_4j.bouton_normale
        bouton_retour.bouton_actuelle = bouton_retour.bouton_survol if bouton_retour.hovered else bouton_retour.bouton_normale

        bouton_1j.dessiner(screen)
        bouton_2j.dessiner(screen)
        bouton_3j.dessiner(screen)
        bouton_4j.dessiner(screen)
        bouton_retour.dessiner(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    if not classes:
        return

    difficulte = choix_difficulte()

    if classes:
        for player in range(len(classes)):
            archetypes(player + 1, graphe)
        map_choix(graphe, joueurs_choix)


def archetypes(number, graphe) :

    fond_image = pygame.image.load('img/map/donjon.png').convert()
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

    bouton_paladin = Bouton(SCREEN_WIDTH//6, SCREEN_HEIGHT//12, SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.6, BROWN_TR, BROWN, "Paladin", SCREEN_WIDTH//30)
    bouton_archer = Bouton(SCREEN_WIDTH//6, SCREEN_HEIGHT//12, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.6, BROWN_TR, BROWN, "Archer", SCREEN_WIDTH//30)
    bouton_mage = Bouton(SCREEN_WIDTH//6, SCREEN_HEIGHT//12, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.6, BROWN_TR, BROWN, "Mage", SCREEN_WIDTH//30)
    bouton_berserk = Bouton(SCREEN_WIDTH//6, SCREEN_HEIGHT//12, SCREEN_WIDTH*0.1, SCREEN_HEIGHT*0.95, BROWN_TR, BROWN, "Berserk", SCREEN_WIDTH//30)
    bouton_assassin = Bouton(SCREEN_WIDTH//6, SCREEN_HEIGHT//12, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.95, BROWN_TR, BROWN, "Assassin", SCREEN_WIDTH//30)
    if number != 1 :
        bouton_healer = Bouton(SCREEN_WIDTH//6, SCREEN_HEIGHT//12, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.95, BROWN_TR, BROWN, "Healer", SCREEN_WIDTH//30)

    running = True
    while running:

        screen.blit(fond_image, (0, 0))
        draw_text("Choisissez votre classe !", 80, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.01, BLACK)
        draw_text(f"Joueur {number} :", 70, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.15, BLACK)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_paladin.hovered = bouton_paladin.est_survol(mx, my)
                bouton_archer.hovered = bouton_archer.est_survol(mx, my)
                bouton_mage.hovered = bouton_mage.est_survol(mx, my)
                bouton_berserk.hovered = bouton_berserk.est_survol(mx, my)
                bouton_assassin.hovered = bouton_assassin.est_survol(mx, my)
                if number != 1 :
                    bouton_healer.hovered = bouton_healer.est_survol(mx, my)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_paladin.est_survol(mx, my):
                    joueurs_choix.append(Joueur("Paladin", graphe, (5,10), 100, 100, 16, 12, 10, 3, 100, "img/classe/Paladin.png"))
                    running = False

                if bouton_archer.est_survol(mx, my):
                    joueurs_choix.append(Joueur("Archer", graphe, (5,10), 80, 80, 15, 5, 20, 3, 100, "img/classe/Archer.png"))
                    running = False

                if bouton_mage.est_survol(mx, my):
                    joueurs_choix.append(Joueur("Mage", graphe, (5,10), 80, 80, 5, 25, 8, 3, 100, "img/classe/Mage.png"))
                    running = False

                if bouton_berserk.est_survol(mx, my):
                    joueurs_choix.append(Joueur("Berserk", graphe, (5,10),120, 120, 20, 5, 12, 3, 100, "img/classe/Berserk.png"))
                    running = False

                if bouton_assassin.est_survol(mx, my):
                    joueurs_choix.append(Joueur("Assassin", graphe, (5,10), 90, 90, 20, 10, 15, 3, 100, "img/classe/Assassin.png"))
                    running = False

                if number != 1 :    
                    if bouton_healer.est_survol(mx, my):
                        joueurs_choix.append(Joueur("Healer", graphe, (5,10), 70, 70, 0, 30, 10, 3, 100, "img/classe/Healer.png"))
                        running = False


        screen.blit(imgPaladin, imgPaladin_rect)
        screen.blit(imgArcher, imgArcher_rect)
        screen.blit(imgMage, imgMage_rect)
        screen.blit(imgBerserk, imgBerserk_rect)
        screen.blit(imgAssassin, imgAssassin_rect)
        if number != 1 :
            screen.blit(imgHealer, imgHealer_rect)

        bouton_paladin.bouton_actuelle = bouton_paladin.bouton_survol if bouton_paladin.hovered else bouton_paladin.bouton_normale
        bouton_archer.bouton_actuelle = bouton_archer.bouton_survol if bouton_archer.hovered else bouton_archer.bouton_normale
        bouton_mage.bouton_actuelle = bouton_mage.bouton_survol if bouton_mage.hovered else bouton_mage.bouton_normale
        bouton_berserk.bouton_actuelle = bouton_berserk.bouton_survol if bouton_berserk.hovered else bouton_berserk.bouton_normale
        bouton_assassin.bouton_actuelle = bouton_assassin.bouton_survol if bouton_assassin.hovered else bouton_assassin.bouton_normale
        if number != 1 :
            bouton_healer.bouton_actuelle = bouton_healer.bouton_survol if bouton_healer.hovered else bouton_healer.bouton_normale

        bouton_paladin.dessiner(screen)
        bouton_archer.dessiner(screen)
        bouton_mage.dessiner(screen)
        bouton_berserk.dessiner(screen)
        bouton_assassin.dessiner(screen)
        if number != 1 :
            bouton_healer.dessiner(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

    return joueurs_choix


def map_choix(graphe, joueurs_choix) :

    fond_image = pygame.image.load('img/map/donjon.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bouton_desert = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.12, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "Desert", SCREEN_WIDTH//30)
    bouton_neige = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.373, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "Neige", SCREEN_WIDTH//30)
    bouton_foret = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.626, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "Foret", SCREEN_WIDTH//30)
    bouton_donjon = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//10, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.65, BROWN_TR, BROWN, "Donjon", SCREEN_WIDTH//30)

    running = True
    while running:

        screen.blit(fond_image, (0, 0))
        draw_text("Choisissez votre map !", SCREEN_WIDTH//12, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.2, BLACK)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_desert.hovered = bouton_desert.est_survol(mx, my)
                bouton_neige.hovered = bouton_neige.est_survol(mx, my)
                bouton_foret.hovered = bouton_foret.est_survol(mx, my)
                bouton_donjon.hovered = bouton_donjon.est_survol(mx, my)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_desert.est_survol(mx, my):
                    affichageGraphique(0, graphe, joueurs_choix)
                    running = False

                if bouton_neige.est_survol(mx, my):
                    affichageGraphique(1, graphe, joueurs_choix)
                    running = False

                if bouton_foret.est_survol(mx, my):
                    affichageGraphique(2, graphe, joueurs_choix)
                    running = False

                if bouton_donjon.est_survol(mx, my):
                    affichageGraphique(3, graphe, joueurs_choix)
                    running = False

        bouton_desert.bouton_actuelle = bouton_desert.bouton_survol if bouton_desert.hovered else bouton_desert.bouton_normale
        bouton_neige.bouton_actuelle = bouton_neige.bouton_survol if bouton_neige.hovered else bouton_neige.bouton_normale
        bouton_foret.bouton_actuelle = bouton_foret.bouton_survol if bouton_foret.hovered else bouton_foret.bouton_normale
        bouton_donjon.bouton_actuelle = bouton_donjon.bouton_survol if bouton_donjon.hovered else bouton_donjon.bouton_normale

        bouton_desert.dessiner(screen)
        bouton_neige.dessiner(screen)
        bouton_foret.dessiner(screen)
        bouton_donjon.dessiner(screen)
           
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)


def regles():

    fond_image = pygame.image.load('img/map/desert.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bouton_quitter = Bouton(SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22, SCREEN_WIDTH//1.04, SCREEN_HEIGHT//50, TRANSPARENT, BROWN, "Quitter", SCREEN_WIDTH//45)

    running = True
    while running:

        screen.blit(fond_image, (0, 0))
        mx, my = pygame.mouse.get_pos()

        # Affichage des règles
        draw_text("Règle 1", SCREEN_WIDTH//45, SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.3, BLACK)
        draw_text("Règle 2", SCREEN_WIDTH//45, SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.4, BLACK)
        draw_text("Règle 3", SCREEN_WIDTH//45, SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.5, BLACK)
        draw_text("Règle 4", SCREEN_WIDTH//45, SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.6, BLACK)
        draw_text("Règle 5", SCREEN_WIDTH//45, SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.7, BLACK)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                bouton_quitter.hovered = bouton_quitter.est_survol(mx, my)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_quitter.est_survol(mx, my):
                    running = False

        bouton_quitter.bouton_actuelle = bouton_quitter.bouton_survol if bouton_quitter.hovered else bouton_quitter.bouton_normale

        bouton_quitter.dessiner(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

def credit() : 

    fond_image = pygame.image.load('img/map/neige.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    bouton_quitter = Bouton(SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22, SCREEN_WIDTH//1.04, SCREEN_HEIGHT//50, TRANSPARENT, BROWN, "Quitter", SCREEN_WIDTH//45)

    running = True
    while running :

        screen.blit(fond_image, (0, 0))
        mx, my = pygame.mouse.get_pos()

        draw_text("Creator :", SCREEN_WIDTH//12, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.09, BLACK)
        draw_text("Nathan Rousselle", SCREEN_WIDTH//20, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.35, BLACK)
        draw_text("With the help of :", SCREEN_WIDTH//16, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.55, BLACK)
        draw_text("Lionnel Conoir", SCREEN_WIDTH//20, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.75, BLACK)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_quitter.hovered = bouton_quitter.est_survol(mx, my)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_quitter.est_survol(mx, my):
                    running = False 

        bouton_quitter.bouton_actuelle = bouton_quitter.bouton_survol if bouton_quitter.hovered else bouton_quitter.bouton_normale

        bouton_quitter.dessiner(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

def main_menu():
    multi = False
    
    fond_image = pygame.image.load('img/map/foret.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bouton_jouer = Bouton(SCREEN_WIDTH//3, SCREEN_HEIGHT//7, SCREEN_WIDTH/2, SCREEN_HEIGHT*0.4, BROWN_TR, BROWN, "Jouer", SCREEN_WIDTH//25)
    bouton_multi = Bouton(SCREEN_WIDTH//3, SCREEN_HEIGHT//7, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.55, BROWN_TR, BROWN, "Multi", SCREEN_WIDTH//25)
    bouton_regles = Bouton(SCREEN_WIDTH//3, SCREEN_HEIGHT//7, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.7, BROWN_TR, BROWN, "Règles", SCREEN_WIDTH//25)
    bouton_credits = Bouton(SCREEN_WIDTH//7, SCREEN_HEIGHT//12, SCREEN_WIDTH//1.085, SCREEN_HEIGHT*0.95, BROWN_TR, BROWN, "Crédits", SCREEN_WIDTH//40)
    bouton_quitter = Bouton(SCREEN_WIDTH//3, SCREEN_HEIGHT//7, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.85, BROWN_TR, BROWN, "Quitter", SCREEN_WIDTH//25)

    while True:
        # Afficher l'arrière-plan
        screen.blit(fond_image, (0, 0))
        draw_text("Monster Slayer", SCREEN_WIDTH//12, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.1, BLACK)

        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_jouer.hovered = bouton_jouer.est_survol(mx, my)
                bouton_multi.hovered = bouton_multi.est_survol(mx, my)
                bouton_regles.hovered = bouton_regles.est_survol(mx, my)
                bouton_credits.hovered = bouton_credits.est_survol(mx, my)
                bouton_quitter.hovered = bouton_quitter.est_survol(mx, my)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_jouer.est_survol(mx, my):
                    nb_joueurs()
                if bouton_multi.est_survol(mx, my):
                    try :
                        if not multi:                        
                            multi = True
                        
                            host = '127.0.0.1'
                            port = 5555
                            
                            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            client_socket.connect((host, port))

                            numero = client_socket.recv(1024).decode()
                            print(f"Vous êtes le joueur {numero}")

                        nb_joueurs_multi(client_socket, numero)
                        
                    except WindowsError as e:
                        multi = False
                        compteur = 4
                        fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
                        fond_chargement.fill(WHITE_TR)
                        screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))
                        draw_text(f"Impossible de se connecter au serveur !", SCREEN_WIDTH//19, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.35, BLACK)
                        draw_text(f"Lancer le serveur ou connectez-vous à internet.", SCREEN_WIDTH//30, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.55, BLACK)
                        while compteur >= 1 :
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()

                            pygame.display.update()
                            clock.tick(FPS)
                            pygame.time.delay(1000)
                            compteur -= 1  

                if bouton_regles.est_survol(mx, my):
                    regles()

                if bouton_credits.est_survol(mx, my):
                    credit()
                    
                if bouton_quitter.est_survol(mx, my):
                    print("Aucune statistique rentrée !")
                    pygame.quit()
                    
                    if multi:
                        client_socket.close()
                    
                    sys.exit()

        bouton_jouer.bouton_actuelle = bouton_jouer.bouton_survol if bouton_jouer.hovered else bouton_jouer.bouton_normale
        bouton_multi.bouton_actuelle = bouton_multi.bouton_survol if bouton_multi.hovered else bouton_multi.bouton_normale
        bouton_regles.bouton_actuelle = bouton_regles.bouton_survol if bouton_regles.hovered else bouton_regles.bouton_normale
        bouton_credits.bouton_actuelle = bouton_credits.bouton_survol if bouton_credits.hovered else bouton_credits.bouton_normale
        bouton_quitter.bouton_actuelle = bouton_quitter.bouton_survol if bouton_quitter.hovered else bouton_quitter.bouton_normale

        bouton_jouer.dessiner(screen)
        bouton_multi.dessiner(screen)
        bouton_regles.dessiner(screen)
        bouton_credits.dessiner(screen)
        bouton_quitter.dessiner(screen)
           
        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

if __name__ == "__main__":
    main_menu()