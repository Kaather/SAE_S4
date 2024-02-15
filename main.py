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

    if numero == "1":
        bouton_2_survole = False
        bouton_3_survole = False
        bouton_4_survole = False
        bouton_5_survole = False
        running = True
        while running:
            screen.blit(fond_image, (0, 0))
            draw_text("Combien de joueurs ?", 120, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.2, BLACK)

            mx, my = pygame.mouse.get_pos()

            bouton_2 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)
            bouton_3 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)
            bouton_4 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)
            bouton_5 = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)

            bouton_2.fill(BROWN_TR if not bouton_2_survole else BROWN)
            bouton_3.fill(BROWN_TR if not bouton_3_survole else BROWN)
            bouton_4.fill(BROWN_TR if not bouton_4_survole else BROWN)
            bouton_5.fill(TRANSPARENT if not bouton_5_survole else BROWN)

            screen.blit(bouton_2, ((SCREEN_WIDTH*0.373) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
            screen.blit(bouton_3, ((SCREEN_WIDTH*0.626) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
            screen.blit(bouton_4, ((SCREEN_WIDTH*0.88) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
            screen.blit(bouton_5, ((SCREEN_WIDTH*(0.92), SCREEN_HEIGHT*(0.001))))

            draw_text("2 Joueurs", 51, SCREEN_WIDTH*0.373, SCREEN_HEIGHT*(0.655), BLACK)
            draw_text("3 Joueurs", 51, SCREEN_WIDTH*0.626, SCREEN_HEIGHT*(0.655), BLACK)
            draw_text("4 Joueurs", 51, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*(0.655), BLACK)
            draw_text("Quitter", 30, SCREEN_WIDTH*0.96, -5, BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    mx, my = pygame.mouse.get_pos()
                    bouton_2_survole = bouton_2.get_rect(center=((SCREEN_WIDTH*0.373), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
                    bouton_3_survole = bouton_3.get_rect(center=((SCREEN_WIDTH*0.626), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
                    bouton_4_survole = bouton_4.get_rect(center=((SCREEN_WIDTH*0.88), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
                    bouton_5_survole = bouton_5.get_rect(center=((SCREEN_WIDTH*0.965), SCREEN_HEIGHT*(0.015))).collidepoint((mx, my))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_2.get_rect(center=((SCREEN_WIDTH*0.373), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                        classes = [1, 2]
                        max_joueurs = 2
                        running = False
                        socket.send(str.encode(str(classes)))
                    if bouton_3.get_rect(center=((SCREEN_WIDTH*0.626), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                        classes = [1, 2, 3]
                        max_joueurs = 3
                        running = False
                        socket.send(str.encode(str(classes)))
                    if bouton_4.get_rect(center=((SCREEN_WIDTH*0.88), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)) :
                        classes = [1, 2, 3, 4]
                        max_joueurs = 4
                        running = False
                        socket.send(str.encode(str(classes)))
                    if bouton_5.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.015)).collidepoint((mx, my)):
                        classes = []
                        running = False
                        socket.send(str.encode(str(classes)))

            pygame.display.update()

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
    bouton_1_survole = False
    bouton_2_survole = False
    bouton_3_survole = False

    fond_image = pygame.image.load('img/map/donjon.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    difficulte = None  # Initialisation de la variable de difficulté

    running = True
    while running:
        screen.blit(fond_image, (0, 0))
        draw_text("Choisissez la difficulté :", 80, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.2, BLACK)

        mx, my = pygame.mouse.get_pos()

        bouton_1 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)
        bouton_2 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)
        bouton_3 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//10), pygame.SRCALPHA)

        bouton_1.fill(BROWN_TR if not bouton_1_survole else BROWN)
        bouton_2.fill(BROWN_TR if not bouton_2_survole else BROWN)
        bouton_3.fill(BROWN_TR if not bouton_3_survole else BROWN)

        screen.blit(bouton_1, ((SCREEN_WIDTH*0.200) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
        screen.blit(bouton_2, ((SCREEN_WIDTH*0.500) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))
        screen.blit(bouton_3, ((SCREEN_WIDTH*0.800) - (SCREEN_WIDTH//5/2), SCREEN_HEIGHT*(0.65)))

        draw_text("Facile", 51, SCREEN_WIDTH*0.200, SCREEN_HEIGHT*(0.655), BLACK)
        draw_text("Moyen", 51, SCREEN_WIDTH*0.500, SCREEN_HEIGHT*(0.655), BLACK)
        draw_text("Difficile", 51, SCREEN_WIDTH*0.800, SCREEN_HEIGHT*(0.655), BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                bouton_1_survole = bouton_1.get_rect(center=((SCREEN_WIDTH*0.200), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
                bouton_2_survole = bouton_2.get_rect(center=((SCREEN_WIDTH*0.500), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
                bouton_3_survole = bouton_3.get_rect(center=((SCREEN_WIDTH*0.800), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_1.get_rect(center=((SCREEN_WIDTH*0.200), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                    difficulte = "Facile"
                    running = False
                    deplacement_facile()
                if bouton_2.get_rect(center=((SCREEN_WIDTH*0.500), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                    difficulte = "Moyen"
                    running = False
                    deplacement_intermediaire()
                if bouton_3.get_rect(center=((SCREEN_WIDTH*0.800), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                    difficulte = "Difficile"
                    running = False
                    deplacement_difficile()


        pygame.display.update()

    print(difficulte)
    return difficulte

def archetypes_multi(number, graphe, socket) :

    bouton_1_survole = False
    bouton_2_survole = False
    bouton_3_survole = False
    bouton_4_survole = False
    bouton_5_survole = False
    bouton_6_survole = False

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
                    liste = ["Paladin", graphe, (5,10), 100, 100, 16, 12, 10, 5, 100, "img/classe/Paladin.png"]
                    joueur = Joueur("Paladin", graphe, (5,10), 100, 100, 16, 12, 10, 5, 100, "img/classe/Paladin.png")
                    socket.send(str.encode(str(liste)))
                    running = False

                if bouton_2.get_rect(center=((SCREEN_WIDTH*0.5), (SCREEN_HEIGHT*(0.55) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)):
                    liste = ["Archer", graphe, (5,10), 80, 80, 15, 5, 20, 5, 100, "img/classe/Archer.png"]
                    joueur = Joueur("Archer", graphe, (5,10), 80, 80, 15, 5, 20, 5, 100, "img/classe/Archer.png")
                    socket.send(str.encode(str(liste)))
                    running = False

                if bouton_3.get_rect(center=((SCREEN_WIDTH*0.9), (SCREEN_HEIGHT*(0.55) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)):
                    liste = ["Mage", graphe, (5,10), 80, 80, 5, 25, 8, 5, 100, "img/classe/Mage.png"]
                    joueur = Joueur("Mage", graphe, (5,10), 80, 80, 5, 25, 8, 5, 100, "img/classe/Mage.png")
                    socket.send(str.encode(str(liste)))
                    running = False

                if bouton_4.get_rect(center=((SCREEN_WIDTH*0.1), (SCREEN_HEIGHT*(0.9) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)) :
                    liste = ["Berserk", graphe, (5,10),120, 120, 20, 5, 12, 5, 100, "img/classe/Berserk.png"]
                    joueur = Joueur("Berserk", graphe, (5,10),120, 120, 20, 5, 12, 5, 100, "img/classe/Berserk.png")
                    socket.send(str.encode(str(liste)))
                    running = False

                if bouton_5.get_rect(center=((SCREEN_WIDTH*0.5), (SCREEN_HEIGHT*(0.9) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)):
                    liste = ["Assassin", graphe, (5,10), 90, 90, 20, 10, 15, 5, 100, "img/classe/Assassin.png"]
                    joueur = Joueur("Assassin", graphe, (5,10), 90, 90, 20, 10, 15, 5, 100, "img/classe/Assassin.png")
                    socket.send(str.encode(str(liste)))
                    running = False

                if number != 1 :    
                    if bouton_6.get_rect(center=((SCREEN_WIDTH*0.9), (SCREEN_HEIGHT*(0.9) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)) :
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

        pygame.display.update()
    return joueur

def map_choix_multi(graphe, joueurs_choix, numero, socket):
    bouton_1_survole = False
    bouton_2_survole = False
    bouton_3_survole = False
    bouton_4_survole = False

    fond_image = pygame.image.load('img/map/donjon.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    if numero == "1":
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
            draw_text("donjon", 51, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*(0.655), BLACK)

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
                        socket.send(str.encode(str(0)))
                        maps = 0
                        running = False
                    if bouton_2.get_rect(center=((SCREEN_WIDTH*0.373), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                        socket.send(str.encode(str(1)))
                        maps = 1
                        running = False
                    if bouton_3.get_rect(center=((SCREEN_WIDTH*0.626), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                        socket.send(str.encode(str(2)))
                        maps = 2
                        running = False
                    if bouton_4.get_rect(center=((SCREEN_WIDTH*0.88), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)) :
                        socket.send(str.encode(str(3)))
                        maps = 3
                        running = False

            pygame.display.update()
    
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

    bouton_1_survole = False
    bouton_2_survole = False
    bouton_3_survole = False
    bouton_4_survole = False
    bouton_5_survole = False

    fond_image = pygame.image.load('img/map/donjon.png').convert()
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
                if bouton_4.get_rect(center=((SCREEN_WIDTH*0.88), (SCREEN_HEIGHT*(0.65) + SCREEN_HEIGHT//10/2))).collidepoint((mx, my)):
                    classes = [1, 2, 3, 4]
                    running = False
                if bouton_5.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.015)).collidepoint((mx, my)):
                    classes = []
                    running = False

        pygame.display.update()

    # Check if "Retour" button was clicked
    if not classes:
        return

    difficulte = choix_difficulte()

    if classes:
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
                    joueurs_choix.append(Joueur("Paladin", graphe, (5,10), 100, 100, 16, 12, 10, 3, 100, "img/classe/Paladin.png"))
                    running = False

                if bouton_2.get_rect(center=((SCREEN_WIDTH*0.5), (SCREEN_HEIGHT*(0.55) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)):
                    joueurs_choix.append(Joueur("Archer", graphe, (5,10), 80, 80, 15, 5, 20, 3, 100, "img/classe/Archer.png"))
                    running = False

                if bouton_3.get_rect(center=((SCREEN_WIDTH*0.9), (SCREEN_HEIGHT*(0.55) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)):
                    joueurs_choix.append(Joueur("Mage", graphe, (5,10), 80, 80, 5, 25, 8, 3, 100, "img/classe/Mage.png"))
                    running = False

                if bouton_4.get_rect(center=((SCREEN_WIDTH*0.1), (SCREEN_HEIGHT*(0.9) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)) :
                    joueurs_choix.append(Joueur("Berserk", graphe, (5,10),120, 120, 20, 5, 12, 3, 100, "img/classe/Berserk.png"))
                    running = False

                if bouton_5.get_rect(center=((SCREEN_WIDTH*0.5), (SCREEN_HEIGHT*(0.9) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)):
                    joueurs_choix.append(Joueur("Assassin", graphe, (5,10), 90, 90, 20, 10, 15, 3, 100, "img/classe/Assassin.png"))
                    running = False

                if number != 1 :    
                    if bouton_6.get_rect(center=((SCREEN_WIDTH*0.9), (SCREEN_HEIGHT*(0.9) + SCREEN_HEIGHT//12/2))).collidepoint((mx, my)) :
                        joueurs_choix.append(Joueur("Healer", graphe, (5,10), 70, 70, 0, 30, 10, 3, 100, "img/classe/Healer.png"))
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

    fond_image = pygame.image.load('img/map/donjon.png').convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    bouton_desert = Bouton(SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22, SCREEN_WIDTH//1.04, SCREEN_HEIGHT//50, TRANSPARENT, BROWN, "Desert", SCREEN_WIDTH//45)
    bouton_neige = Bouton(SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22, SCREEN_WIDTH//1.04, SCREEN_HEIGHT//50, TRANSPARENT, BROWN, "Neige", SCREEN_WIDTH//45)
    bouton_foret = Bouton(SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22, SCREEN_WIDTH//1.04, SCREEN_HEIGHT//50, TRANSPARENT, BROWN, "Foret", SCREEN_WIDTH//45)
    bouton_donjon = Bouton(SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22, SCREEN_WIDTH//1.04, SCREEN_HEIGHT//50, TRANSPARENT, BROWN, "Quitter", SCREEN_WIDTH//45)

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
        draw_text("Donjon", 51, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*(0.655), BLACK)



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