import pygame
import sys
from plateau import *
from pygameOutils import *
from labyrinthe import *
from entite import *
import time
from bouton import *
# from statistique import *

pygame.init()

info = pygame.display.Info()

# Définir les dimensions de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Labyrinthe")
clock = pygame.time.Clock()
FPS = 60
 

def affichageGraphiqueReseau(choix, graphe, joueurs_choix, socket, numero) :

    fond = [
    'img/map/desert.png',  
    'img/map/neige.png',
    'img/map/foret.png',
    'img/map/dongeon.png'
    ]

    liste_loup = []
    
    i = 0
    while i < 5 :
        liste_loup.append(Monstre("Loup", 50, 50, 10, 5, 15, "img/ennemi/loup.png"))
        i += 1

    dragon = Monstre("Dragon", 25, 25, 5, 5, 2, "img/ennemi/dragon.png")
    
    fond_image = pygame.image.load(fond[choix]).convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fond_image, (0, 0))

    bouton_5_survole = False
    lancer_fait = False
    de_resultat = None
    potion_possible = False
    joueurs_piegee = False
    piege_doree_possible = False
    ouvrir_piege_doree = False
    liste_postion_joueur = []
    liste_position_piege = []
    liste_position_potion = []
    liste_position_argent = []

    monstre_battu = 0
    nb_tour = 0
    nb_potion = 0
    nb_argent = 0

    compteur_lancers = 0

    compteur_loup = 0
    
    laby = Grille(largeur, hauteur)
    laby.construireBordure()     
    
    if numero == "1" :
        graphe = labyrinthe(largeur, hauteur)
        serialisation = str(graphe)
        socket.send(serialisation.encode())
        time.sleep(0.5)
    else :
        enoieLaby = True
        graphe = ""
        while enoieLaby:
            try :
                graphe += socket.recv(10000000).decode()
                graphe = eval(graphe)
                enoieLaby = False
            except Exception as e :
                pass
                
    laby.construireAvecGraphe(graphe)
    
    # creer les images
    _, _, piege_images, piege_doree_image = evenement(graphe)
    _, potion_images, _, argent_images = ajouter_objet(graphe, [], [])
        
    if numero == "1" :
        piege_positions, piege_doree_positions, piege_images, piege_doree_image = evenement(graphe)
        potion_positions, potion_images, argent_positions, argent_images = ajouter_objet(graphe, piege_positions, piege_doree_positions)
        
        serialisation = str(piege_doree_positions)
        socket.send(serialisation.encode())
        time.sleep(0.5)
        
        serialisation = str(piege_positions)
        socket.send(serialisation.encode())
        time.sleep(0.5)
                
        serialisation = str(potion_positions)
        socket.send(serialisation.encode())
        time.sleep(0.5)
        
        serialisation = str(argent_positions)
        socket.send(serialisation.encode())
    else:
        envoiePos = True
        while envoiePos:
            try :
                piege_doree_positions = socket.recv(10000000).decode()
                piege_doree_positions = eval(piege_doree_positions)
                
                piege_positions = socket.recv(10000000).decode()
                piege_positions = eval(piege_positions)
                
                potion_positions = socket.recv(10000000).decode()
                potion_positions = eval(potion_positions)
                
                argent_positions = socket.recv(10000000).decode()
                argent_positions = eval(argent_positions)
                
                envoiePos = False                
            except Exception as e :
                pass

    running = True
    while running:
        # Combat final        
        if ouvrir_piege_doree:
            compteur = 5
            while compteur >= 1 :
                
                fond_image2 = pygame.image.load(fond[choix]).convert()
                fond_image2 = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(fond_image2, (0, 0))
                draw_text(f"Un joueur a ouvert la porte dorée !", SCREEN_WIDTH//17, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)
                draw_text(f"Rassemblez vous et préparez vous au combat final !", SCREEN_WIDTH//25, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.45, BLACK)
                draw_text(f"{compteur}", SCREEN_WIDTH//13, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.65, BLACK)

                fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
                fond_chargement.fill(WHITE_TR)
                screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
                clock.tick(FPS)
                pygame.time.delay(1000)
                compteur -= 1

            bouton_menu_survole = False
            bouton_potion_survole = False
            bouton_attaque_survole = False
            bouton_attaque_puissante_survole = False
            bouton_attaque_magique_survole = False
            en_combat = True
            compteur_lancers = 0
            joueur_mort = False
            monstre_mort = False
            while en_combat and ouvrir_piege_doree : 
                if compteur_lancers >= len(joueurs_choix):
                    compteur_lancers = 0
                    
                mx, my = pygame.mouse.get_pos()

                combat_image = pygame.image.load('img/map/mapPiege.png').convert()
                combat_image = pygame.transform.scale(combat_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(combat_image, (0, 0))

                bouton_5 = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)
                bouton_5.fill(TRANSPARENT if not bouton_5_survole else BROWN)
                screen.blit(bouton_5, ((SCREEN_WIDTH*(0.92), SCREEN_HEIGHT*(0.001))))
                draw_text("Quitter", SCREEN_WIDTH//43, SCREEN_WIDTH*0.96, SCREEN_HEIGHT//(-120), BLACK)
                
                # Affichage du monstre dragon utilise la variable dragon
                dragon_image = pygame.image.load(dragon.image).convert_alpha()
                dragon_image = pygame.transform.scale(dragon_image, (SCREEN_WIDTH//8, SCREEN_WIDTH//8))
                screen.blit(dragon_image, (SCREEN_WIDTH*0.65, SCREEN_HEIGHT*0.4))
                
                # Affichage vie monstre
                draw_text(f"PV : {dragon.pv} / {dragon.pv_max}", 20, SCREEN_WIDTH*0.64, SCREEN_HEIGHT*0.65, BLACK)          
                
                rectangle_vert = pygame.Surface((((SCREEN_WIDTH//8.2) * (dragon.pv) // dragon.pv_max), SCREEN_HEIGHT//30), pygame.SRCALPHA)
                rectangle_vert.fill(GREEN)
                screen.blit(rectangle_vert, ((SCREEN_WIDTH*0.703), SCREEN_HEIGHT*(0.65)))
                
                morc_rectangle1 = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//150), pygame.SRCALPHA)
                morc_rectangle1.fill(BLACK)
                screen.blit(morc_rectangle1, ((SCREEN_WIDTH*0.7), SCREEN_HEIGHT*(0.65)))

                morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//150), pygame.SRCALPHA)
                morc_rectangle2.fill(BLACK)
                screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.7), SCREEN_HEIGHT*(0.68)))

                morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//300, SCREEN_HEIGHT//30), pygame.SRCALPHA)
                morc_rectangle2.fill(BLACK)
                screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.7), SCREEN_HEIGHT*(0.65)))

                morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//300, SCREEN_HEIGHT//30), pygame.SRCALPHA)
                morc_rectangle2.fill(BLACK)
                screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.822), SCREEN_HEIGHT*(0.65)))
                
                
                # Affichage joueurs 
                quotient_x = 0.4
                quotient_y = 0.55
                for joueur in joueurs_choix :
                    
                    joueur_image = pygame.image.load(joueur.image).convert_alpha()
                    joueur_image = pygame.transform.scale(joueur_image, (SCREEN_WIDTH//16, SCREEN_WIDTH//16))
                    screen.blit(joueur_image, (SCREEN_WIDTH*quotient_x, SCREEN_HEIGHT*quotient_y))
                    if quotient_x == 0.4 :
                        quotient_x = 0.5
                    else :
                        quotient_x = 0.4
                    if quotient_y == 0.55:
                        quotient_y = 0.7
                    elif quotient_y == 0.7:
                        quotient_y = 0.4
                    elif quotient_y == 0.4:
                        quotient_y = 0.25
                    elif quotient_y == 0.25:
                        quotient_y = 0.55

                # Affichage stats / objets du joueurs courant

                fond_player = pygame.Surface((SCREEN_WIDTH//4.3, SCREEN_HEIGHT), pygame.SRCALPHA)
                fond_player.fill(WHITE_TR)
                screen.blit(fond_player, ((SCREEN_WIDTH*0.001), SCREEN_HEIGHT*(0.001)))
                draw_text(f"Joueur {compteur_lancers + 1} :", SCREEN_WIDTH//25, SCREEN_WIDTH*0.09, SCREEN_HEIGHT*0.01, BLACK)

                # Affichage point de vie

                draw_text(f"PV : {joueurs_choix[compteur_lancers].pv} / {joueurs_choix[compteur_lancers].pv_max}", SCREEN_WIDTH//65, SCREEN_WIDTH*0.05, SCREEN_HEIGHT*0.12, BLACK)

                # Rectangles pour afficher une barre de vie
                rectangle_vert = pygame.Surface((((SCREEN_WIDTH//8.2) * (joueurs_choix[compteur_lancers].pv) // joueurs_choix[compteur_lancers].pv_max), SCREEN_HEIGHT//30), pygame.SRCALPHA)
                rectangle_vert.fill(GREEN)
                screen.blit(rectangle_vert, ((SCREEN_WIDTH*0.103), SCREEN_HEIGHT*(0.12)))

                morc_rectangle1 = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//150), pygame.SRCALPHA)
                morc_rectangle1.fill(BLACK)
                screen.blit(morc_rectangle1, ((SCREEN_WIDTH*0.1), SCREEN_HEIGHT*(0.12)))

                morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//150), pygame.SRCALPHA)
                morc_rectangle2.fill(BLACK)
                screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.1), SCREEN_HEIGHT*(0.15)))

                morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//300, SCREEN_HEIGHT//30), pygame.SRCALPHA)
                morc_rectangle2.fill(BLACK)
                screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.1), SCREEN_HEIGHT*(0.12)))

                morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//300, SCREEN_HEIGHT//30), pygame.SRCALPHA)
                morc_rectangle2.fill(BLACK)
                screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.222), SCREEN_HEIGHT*(0.12)))

                # Affichage statistiques et objets
                draw_text(f"Attaque  :   {joueurs_choix[compteur_lancers].attaque}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.2, BLACK)
                draw_text(f"Magie   :   {joueurs_choix[compteur_lancers].magie}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.3, BLACK)
                draw_text(f"Vitesse   :   {joueurs_choix[compteur_lancers].vitesse}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.4, BLACK)
                draw_text(f"Potion   :   {joueurs_choix[compteur_lancers].potion}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.5, BLACK)
                draw_text(f"Argent   :   {joueurs_choix[compteur_lancers].argent}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.075, SCREEN_HEIGHT*0.6, BLACK)

                # Affichage des boutons de compétences / utilisables (potions)
                bouton_attaque = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
                bouton_attaque.fill(GREY_TR if not bouton_attaque_survole else GREY)
                screen.blit(bouton_attaque, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.355))
                draw_text("Attaque", SCREEN_WIDTH//35, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.355, BLACK)

                bouton_attaque_puissante = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
                bouton_attaque_puissante.fill(GREY_TR if not bouton_attaque_puissante_survole else GREY)
                screen.blit(bouton_attaque_puissante, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.555))
                draw_text("Attaque puissante", SCREEN_WIDTH//37, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.555, BLACK)

                bouton_attaque_magique = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
                bouton_attaque_magique.fill(GREY_TR if not bouton_attaque_magique_survole else GREY)
                screen.blit(bouton_attaque_magique, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.755))
                draw_text("Attaque magique", SCREEN_WIDTH//37, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.755, BLACK)
                
                # Affichage bouton utiliser potion (seulement si on a pas tout ses points de vie)
                if joueurs_choix[compteur_lancers].pv != joueurs_choix[compteur_lancers].pv_max and numero == str(compteur_lancers + 1) :
                    bouton_potion = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
                    bouton_potion.fill(GREY_TR if not bouton_potion_survole else GREY)
                    screen.blit(bouton_potion, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.155))
                    draw_text("Boire potion", SCREEN_WIDTH//35, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.155, BLACK)
                    potion_possible = True

                if numero == str(compteur_lancers + 1) :
                    data = {}
                        
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        
                        if potion_possible == True :

                            if event.type == pygame.MOUSEMOTION: 
                                mx, my = pygame.mouse.get_pos()
                                bouton_potion_survole = bouton_potion.get_rect(center=((SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.185))).collidepoint((mx, my))

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if bouton_potion.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.185)).collidepoint((mx, my)):
                                    joueurs_choix[compteur_lancers].utiliser_potion()                             
                                    potion_possible = False
                             

                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_attaque_survole = bouton_attaque.get_rect(center=((SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.385))).collidepoint((mx, my))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_attaque.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.385)).collidepoint((mx, my)):
                                combat(1, joueurs_choix[compteur_lancers], dragon)
                                if comparaison_vitesse(joueurs_choix[compteur_lancers], dragon) :
                                    if dragon.pv <= 0 :
                                        monstre_mort = True
                                        # envoie monstre mort
                                        data["monstre_mort"] = monstre_mort
                                        data["joueur_mort"] = joueur_mort
                                        socket.send(str.encode(str(data)))
                                        
                                    else :
                                        monstre_attaque(joueurs_choix[compteur_lancers], dragon)
                                        if joueurs_choix[compteur_lancers].pv <= 0 :
                                            joueur_mort = True
                                            data["monstre_mort"] = monstre_mort
                                            data["joueur_mort"] = joueur_mort
                                            socket.send(str.encode(str(data)))

                                else :
                                    if joueurs_choix[compteur_lancers].pv <= 0:
                                            joueur_mort = True
                                            data["monstre_mort"] = monstre_mort
                                            data["joueur_mort"] = joueur_mort
                                            socket.send(str.encode(str(data)))

                                    else :
                                        attaque(joueurs_choix[compteur_lancers], dragon)
                                        if dragon.pv <= 0 :
                                            monstre_mort = True
                                            data["monstre_mort"] = monstre_mort
                                            data["joueur_mort"] = joueur_mort
                                            socket.send(str.encode(str(data)))

                                if joueur_mort :

                                    menu_mort = True
                                    while menu_mort :
                                        mx, my = pygame.mouse.get_pos()
                                        screen.blit(fond_image, (0, 0))
                                        draw_text("Vous avez perdu !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)

                                        bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
                                        bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
                                        screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
                                        draw_text("Quitter", SCREEN_WIDTH//20, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)

                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                socket.close()
                                                pygame.quit()
                                                sys.exit()
                                                

                                            if event.type == pygame.MOUSEMOTION: 
                                                mx, my = pygame.mouse.get_pos()
                                                bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)) :
                                                    joueurs_choix.clear()   
                                                    supprimer_classes()
                                                    running = False
                                                    en_combat = False
                                                    menu_mort = False
                                                    socket.close()

                                        pygame.display.update()
                                        clock.tick(FPS)
                                
                                elif monstre_mort :
                                    # mise_en_stat(joueurs_choix, monstre_battu, True, nb_tour, nb_potion, nb_argent, choix, graphe, liste_position_argent, liste_position_potion, liste_position_piege, liste_postion_joueur)
                                    joueurs_piegee = False
                                    ouvrir_piege_doree = False
                                    en_combat = False
                                    running2 = True
                                    while running2 :
                                        mx, my = pygame.mouse.get_pos()
                                        screen.blit(fond_image, (0, 0))
                                        draw_text("Vous avez gagné !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)
                                        bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
                                        bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
                                        screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
                                        draw_text("Quitter", SCREEN_WIDTH//20, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)

                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()

                                            if event.type == pygame.MOUSEMOTION: 
                                                mx, my = pygame.mouse.get_pos()
                                                bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)):
                                                    running2 = False
                                                    socket.close()
                                                    break

                                        pygame.display.update()
                                        clock.tick(FPS)

                                    joueurs_choix.clear()   
                                    supprimer_classes()
                                    running = False
                                    
                                    
                        # attaque puissante   
                        if event.type == pygame.MOUSEMOTION:
                            mx, my = pygame.mouse.get_pos()
                            bouton_attaque_puissante_survole = bouton_attaque_puissante.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.585)).collidepoint((mx, my))                               
                                             
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_attaque_puissante.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.585)).collidepoint((mx, my)):
                                combat(1, joueurs_choix[compteur_lancers], dragon)
                                if comparaison_vitesse(joueurs_choix[compteur_lancers], dragon) :
                                    if dragon.pv <= 0 :
                                        monstre_mort = True
                                        # envoie monstre mort
                                        data["monstre_mort"] = monstre_mort
                                        data["joueur_mort"] = joueur_mort
                                        socket.send(str.encode(str(data)))
                                        
                                    else :
                                        monstre_attaque(joueurs_choix[compteur_lancers], dragon)
                                        if joueurs_choix[compteur_lancers].pv <= 0 :
                                            joueur_mort = True
                                            data["monstre_mort"] = monstre_mort
                                            data["joueur_mort"] = joueur_mort
                                            socket.send(str.encode(str(data)))

                                else :
                                    if joueurs_choix[compteur_lancers].pv <= 0:
                                            joueur_mort = True
                                            data["monstre_mort"] = monstre_mort
                                            data["joueur_mort"] = joueur_mort
                                            socket.send(str.encode(str(data)))

                                    else :
                                        attaque_puissante(joueurs_choix[compteur_lancers], dragon)
                                        if dragon.pv <= 0 :
                                            monstre_mort = True
                                            data["monstre_mort"] = monstre_mort
                                            data["joueur_mort"] = joueur_mort
                                            socket.send(str.encode(str(data)))

                                if joueur_mort :

                                    menu_mort = True
                                    while menu_mort :
                                        mx, my = pygame.mouse.get_pos()
                                        screen.blit(fond_image, (0, 0))
                                        draw_text("Vous avez perdu !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)

                                        bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
                                        bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
                                        screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
                                        draw_text("Quitter", SCREEN_WIDTH//20, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)

                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                socket.close()
                                                pygame.quit()
                                                sys.exit()
                                                

                                            if event.type == pygame.MOUSEMOTION: 
                                                mx, my = pygame.mouse.get_pos()
                                                bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)) :
                                                    joueurs_choix.clear()   
                                                    supprimer_classes()
                                                    running = False
                                                    en_combat = False
                                                    menu_mort = False
                                                    socket.close()

                                        pygame.display.update()
                                        clock.tick(FPS)
                                
                                elif monstre_mort :
                                    joueurs_piegee = False
                                    ouvrir_piege_doree = False
                                    en_combat = False
                                    running2 = True
                                    while running2 :
                                        mx, my = pygame.mouse.get_pos()
                                        screen.blit(fond_image, (0, 0))
                                        draw_text("Vous avez gagné !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)
                                        bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
                                        bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
                                        screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
                                        draw_text("Quitter", SCREEN_WIDTH//20, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)

                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()

                                            if event.type == pygame.MOUSEMOTION: 
                                                mx, my = pygame.mouse.get_pos()
                                                bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)):
                                                    running2 = False
                                                    socket.close()
                                                    break

                                        pygame.display.update()
                                        clock.tick(FPS)

                                    joueurs_choix.clear()   
                                    supprimer_classes()
                                    running = False


                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_5_survole = bouton_5.get_rect(center=((SCREEN_WIDTH*0.965), SCREEN_HEIGHT*(0.015))).collidepoint((mx, my))
                            
                        # attaque magique
                        if event.type == pygame.MOUSEMOTION:
                            mx, my = pygame.mouse.get_pos()
                            bouton_attaque_magique_survole = bouton_attaque_magique.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.785)).collidepoint((mx, my))
                            
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_attaque_magique.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.785)).collidepoint((mx, my)):
                                combat(1, joueurs_choix[compteur_lancers], dragon)
                                if comparaison_vitesse(joueurs_choix[compteur_lancers], dragon) :
                                    if dragon.pv <= 0 :
                                        monstre_mort = True
                                        # envoie monstre mort
                                        data["monstre_mort"] = monstre_mort
                                        data["joueur_mort"] = joueur_mort
                                        socket.send(str.encode(str(data)))
                                        
                                    else :
                                        monstre_attaque(joueurs_choix[compteur_lancers], dragon)
                                        if joueurs_choix[compteur_lancers].pv <= 0 :
                                            joueur_mort = True
                                            data["monstre_mort"] = monstre_mort
                                            data["joueur_mort"] = joueur_mort
                                            socket.send(str.encode(str(data)))

                                else :
                                    if joueurs_choix[compteur_lancers].pv <= 0:
                                            joueur_mort = True
                                            data["monstre_mort"] = monstre_mort
                                            data["joueur_mort"] = joueur_mort
                                            socket.send(str.encode(str(data)))

                                    else :
                                        attaque_magique(joueurs_choix[compteur_lancers], dragon)
                                        if dragon.pv <= 0 :
                                            monstre_mort = True
                                            data["monstre_mort"] = monstre_mort
                                            data["joueur_mort"] = joueur_mort
                                            socket.send(str.encode(str(data)))

                                if joueur_mort :

                                    menu_mort = True
                                    while menu_mort :
                                        mx, my = pygame.mouse.get_pos()
                                        screen.blit(fond_image, (0, 0))
                                        draw_text("Vous avez perdu !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)

                                        bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
                                        bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
                                        screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
                                        draw_text("Quitter", SCREEN_WIDTH//20, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)

                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                socket.close()
                                                pygame.quit()
                                                sys.exit()
                                                

                                            if event.type == pygame.MOUSEMOTION: 
                                                mx, my = pygame.mouse.get_pos()
                                                bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)) :
                                                    joueurs_choix.clear()   
                                                    supprimer_classes()
                                                    running = False
                                                    en_combat = False
                                                    menu_mort = False
                                                    socket.close()

                                        pygame.display.update()
                                        clock.tick(FPS)
                                
                                elif monstre_mort :
                                    joueurs_piegee = False
                                    ouvrir_piege_doree = False
                                    en_combat = False
                                    running2 = True
                                    while running2 :
                                        mx, my = pygame.mouse.get_pos()
                                        screen.blit(fond_image, (0, 0))
                                        draw_text("Vous avez gagné !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)
                                        bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
                                        bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
                                        screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
                                        draw_text("Quitter", SCREEN_WIDTH//20, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)

                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()

                                            if event.type == pygame.MOUSEMOTION: 
                                                mx, my = pygame.mouse.get_pos()
                                                bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)):
                                                    running2 = False
                                                    socket.close()
                                                    break

                                        pygame.display.update()
                                        clock.tick(FPS)

                                    joueurs_choix.clear()   
                                    supprimer_classes()
                                    running = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_5.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.015)).collidepoint((mx, my)):
                                joueurs_choix.clear()   
                                supprimer_classes()
                                running = False                       
                                en_combat = False
                                
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            data = {}
                            data["pv"] = joueurs_choix[compteur_lancers].pv
                            data["potion"] = joueurs_choix[compteur_lancers].potion
                            data["monstre_mort"] = monstre_mort
                            data["joueur_mort"] = joueur_mort
                            data["monstre_pv"] = dragon.pv
                            compteur_lancers += 1
                            data["compteur_lancers"] = compteur_lancers
                            socket.send(str.encode(str(data)))

                    pygame.display.update()
                    clock.tick(FPS)
                
                else:
                    data = {}
                    pygame.display.update()
                    clock.tick(FPS)
                    data = socket.recv(1024).decode()
                    
                    # Si c'est un dictionnaire                            
                    if data[0] == "{":
                        data = eval(data)
                        
                        # si il y a 6 éléments dans le dictionnaire
                        if len(data) == 6 :
                        
                            data['pv'] = int(data['pv'])
                            data['potion'] = int(data['potion'])
                            data['monstre_mort'] = bool(data['monstre_mort'])
                            data['joueur_mort'] = bool(data['joueur_mort'])
                            data['monstre_pv'] = int(data['monstre_pv'])                        
                            data['compteur_lancers'] = int(data['compteur_lancers'])

                            joueurs_choix[compteur_lancers].pv = data['pv']
                            joueurs_choix[compteur_lancers].potion = data['potion']
                            monstre_mort = data['monstre_mort']
                            joueur_mort = data['joueur_mort']
                            dragon.pv = data['monstre_pv']
                            compteur_lancers = data['compteur_lancers'] 
                            
                        if len(data) == 2 :
                            data['monstre_mort'] = bool(data['monstre_mort'])
                            data['joueur_mort'] = bool(data['joueur_mort'])
                            monstre_mort = data['monstre_mort']
                            joueur_mort = data['joueur_mort']
                            
                        
                        if joueur_mort :

                            menu_mort = True
                            while menu_mort :
                                mx, my = pygame.mouse.get_pos()
                                screen.blit(fond_image, (0, 0))
                                draw_text("Vous avez perdu !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)

                                bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
                                bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
                                screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
                                draw_text("Quitter", SCREEN_WIDTH//20, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)

                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        socket.close()
                                        pygame.quit()
                                        sys.exit()
                                        

                                    if event.type == pygame.MOUSEMOTION: 
                                        mx, my = pygame.mouse.get_pos()
                                        bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)) :
                                            joueurs_choix.clear()   
                                            supprimer_classes()
                                            running = False
                                            en_combat = False
                                            menu_mort = False
                                            socket.close()

                                pygame.display.update()
                                clock.tick(FPS)
                        
                        elif monstre_mort :
                            joueurs_piegee = False
                            ouvrir_piege_doree = False
                            en_combat = False
                            running2 = True
                            while running2 :
                                mx, my = pygame.mouse.get_pos()
                                screen.blit(fond_image, (0, 0))
                                draw_text("Vous avez gagné !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)
                                bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
                                bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
                                screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
                                draw_text("Quitter", SCREEN_WIDTH//20, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)

                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()

                                    if event.type == pygame.MOUSEMOTION: 
                                        mx, my = pygame.mouse.get_pos()
                                        bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)):
                                            running2 = False
                                            socket.close()
                                            break

                                pygame.display.update()
                                clock.tick(FPS)

                            joueurs_choix.clear()   
                            supprimer_classes()
                            running = False
            
                    
        if joueurs_piegee == True :

            compteur = 5
            while compteur >= 1 :
            
                fond_image2 = pygame.image.load(fond[choix]).convert()
                fond_image2 = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(fond_image2, (0, 0))
                draw_text(f"Un joueur est tombé sur un piège !", SCREEN_WIDTH//16, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)
                draw_text(f"Rassemblez vous et préparez vous au combat !", SCREEN_WIDTH//22, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.45, BLACK)
                draw_text(f"{compteur}", SCREEN_WIDTH//13, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.65, BLACK)

                fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
                fond_chargement.fill(WHITE_TR)
                screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.update()
                clock.tick(FPS)
                pygame.time.delay(1000)
                compteur -= 1

            bouton_menu_survole = False
            bouton_potion_survole = False
            bouton_attaque_survole = False
            bouton_attaque_puissante_survole = False
            bouton_attaque_magique_survole = False
            en_combat = True
            compteur_lancers = 0
            joueur_mort = False
            monstre_mort = False
            lancer_fait = False
            while en_combat and joueurs_piegee :
                if compteur_lancers >= len(joueurs_choix):
                    compteur_lancers = 0                        

                mx, my = pygame.mouse.get_pos()

                combat_image = pygame.image.load('img/map/mapPiege.png').convert()
                combat_image = pygame.transform.scale(combat_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(combat_image, (0, 0))

                bouton_5 = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)
                bouton_5.fill(TRANSPARENT if not bouton_5_survole else BROWN)
                screen.blit(bouton_5, ((SCREEN_WIDTH*(0.92), SCREEN_HEIGHT*(0.001))))
                draw_text("Quitter", SCREEN_WIDTH//43, SCREEN_WIDTH*0.96, SCREEN_HEIGHT//(-120), BLACK)
                
                # Affichage du monstre
                loup_image = pygame.image.load(liste_loup[compteur_loup].image).convert_alpha()
                loup_image = pygame.transform.scale(loup_image, (SCREEN_WIDTH//8, SCREEN_WIDTH//8))
                screen.blit(loup_image, (SCREEN_WIDTH*0.65, SCREEN_HEIGHT*0.4))

                # Affichage vie monstre

                draw_text(f"PV : {liste_loup[compteur_loup].pv*len(joueurs_choix)} / {liste_loup[compteur_loup].pv_max*len(joueurs_choix)}", SCREEN_WIDTH//65, SCREEN_WIDTH*0.64, SCREEN_HEIGHT*0.65, BLACK)

                rectangle_vert = pygame.Surface((((SCREEN_WIDTH//8.2) * (liste_loup[compteur_loup].pv) // liste_loup[compteur_loup].pv_max), SCREEN_HEIGHT//30), pygame.SRCALPHA)
                rectangle_vert.fill(GREEN)
                screen.blit(rectangle_vert, ((SCREEN_WIDTH*0.703), SCREEN_HEIGHT*(0.65)))

                morc_rectangle1 = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//150), pygame.SRCALPHA)
                morc_rectangle1.fill(BLACK)
                screen.blit(morc_rectangle1, ((SCREEN_WIDTH*0.7), SCREEN_HEIGHT*(0.65)))

                morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//150), pygame.SRCALPHA)
                morc_rectangle2.fill(BLACK)
                screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.7), SCREEN_HEIGHT*(0.68)))

                morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//300, SCREEN_HEIGHT//30), pygame.SRCALPHA)
                morc_rectangle2.fill(BLACK)
                screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.7), SCREEN_HEIGHT*(0.65)))

                morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//300, SCREEN_HEIGHT//30), pygame.SRCALPHA)
                morc_rectangle2.fill(BLACK)
                screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.822), SCREEN_HEIGHT*(0.65)))

                # Affichage joueurs 
                quotient_x = 0.4
                quotient_y = 0.55
                for joueur in joueurs_choix :
                    
                    joueur_image = pygame.image.load(joueur.image).convert_alpha()
                    joueur_image = pygame.transform.scale(joueur_image, (SCREEN_WIDTH//16, SCREEN_WIDTH//16))
                    screen.blit(joueur_image, (SCREEN_WIDTH*quotient_x, SCREEN_HEIGHT*quotient_y))
                    if quotient_x == 0.4 :
                        quotient_x = 0.5
                    else :
                        quotient_x = 0.4

                    if quotient_y == 0.55:
                        quotient_y = 0.7
                    elif quotient_y == 0.7:
                        quotient_y = 0.4
                    elif quotient_y == 0.4:
                        quotient_y = 0.25
                    elif quotient_y == 0.25:
                        quotient_y = 0.55

                # Affichage stats / objets du joueurs courant

                fond_player = pygame.Surface((SCREEN_WIDTH//4.3, SCREEN_HEIGHT), pygame.SRCALPHA)
                fond_player.fill(WHITE_TR)
                screen.blit(fond_player, ((SCREEN_WIDTH*0.001), SCREEN_HEIGHT*(0.001)))
                draw_text(f"Joueur {compteur_lancers + 1} :", SCREEN_WIDTH//25, SCREEN_WIDTH*0.09, SCREEN_HEIGHT*0.01, BLACK)

                # Affichage point de vie

                draw_text(f"PV : {joueurs_choix[compteur_lancers].pv} / {joueurs_choix[compteur_lancers].pv_max}", SCREEN_WIDTH//65, SCREEN_WIDTH*0.05, SCREEN_HEIGHT*0.12, BLACK)

                # Rectangles pour afficher une barre de vie
                rectangle_vert = pygame.Surface((((SCREEN_WIDTH//8.2) * (joueurs_choix[compteur_lancers].pv) // joueurs_choix[compteur_lancers].pv_max), SCREEN_HEIGHT//30), pygame.SRCALPHA)
                rectangle_vert.fill(GREEN)
                screen.blit(rectangle_vert, ((SCREEN_WIDTH*0.103), SCREEN_HEIGHT*(0.12)))

                morc_rectangle1 = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//150), pygame.SRCALPHA)
                morc_rectangle1.fill(BLACK)
                screen.blit(morc_rectangle1, ((SCREEN_WIDTH*0.1), SCREEN_HEIGHT*(0.12)))

                morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//150), pygame.SRCALPHA)
                morc_rectangle2.fill(BLACK)
                screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.1), SCREEN_HEIGHT*(0.15)))

                morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//300, SCREEN_HEIGHT//30), pygame.SRCALPHA)
                morc_rectangle2.fill(BLACK)
                screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.1), SCREEN_HEIGHT*(0.12)))

                morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//300, SCREEN_HEIGHT//30), pygame.SRCALPHA)
                morc_rectangle2.fill(BLACK)
                screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.222), SCREEN_HEIGHT*(0.12)))

                # Affichage statistiques et objets
                draw_text(f"Attaque  :   {joueurs_choix[compteur_lancers].attaque}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.2, BLACK)
                draw_text(f"Magie   :   {joueurs_choix[compteur_lancers].magie}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.3, BLACK)
                draw_text(f"Vitesse   :   {joueurs_choix[compteur_lancers].vitesse}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.4, BLACK)
                draw_text(f"Potion   :   {joueurs_choix[compteur_lancers].potion}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.5, BLACK)
                draw_text(f"Argent   :   {joueurs_choix[compteur_lancers].argent}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.075, SCREEN_HEIGHT*0.6, BLACK)

                # Affichage des boutons de compétences / utilisables (potions)
                bouton_attaque = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
                bouton_attaque.fill(GREY_TR if not bouton_attaque_survole else GREY)
                screen.blit(bouton_attaque, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.355))
                draw_text("Attaque", SCREEN_WIDTH//35, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.355, BLACK)

                bouton_attaque_puissante = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
                bouton_attaque_puissante.fill(GREY_TR if not bouton_attaque_puissante_survole else GREY)
                screen.blit(bouton_attaque_puissante, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.555))
                draw_text("Attaque puissante", SCREEN_WIDTH//37, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.555, BLACK)

                bouton_attaque_magique = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
                bouton_attaque_magique.fill(GREY_TR if not bouton_attaque_magique_survole else GREY)
                screen.blit(bouton_attaque_magique, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.755))
                draw_text("Attaque magique", SCREEN_WIDTH//37, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.755, BLACK)

                # Affichage bouton utiliser potion (seulement si on a pas tout ses points de vie)
                if joueurs_choix[compteur_lancers].pv != joueurs_choix[compteur_lancers].pv_max and numero == str(compteur_lancers + 1) :
                    bouton_potion = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
                    bouton_potion.fill(GREY_TR if not bouton_potion_survole else GREY)
                    screen.blit(bouton_potion, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.155))
                    draw_text("Boire potion", SCREEN_WIDTH//35, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.155, BLACK)
                    potion_possible = True
                    
                pygame.display.update()
                clock.tick(FPS)

                if numero == str(compteur_lancers + 1) :
                    data = {}
                        
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        
                        if potion_possible == True :

                            if event.type == pygame.MOUSEMOTION: 
                                mx, my = pygame.mouse.get_pos()
                                bouton_potion_survole = bouton_potion.get_rect(center=((SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.185))).collidepoint((mx, my))

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if bouton_potion.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.185)).collidepoint((mx, my)):
                                    joueurs_choix[compteur_lancers].utiliser_potion()                            
                                    potion_possible = False
                                    

                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_attaque_survole = bouton_attaque.get_rect(center=((SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.385))).collidepoint((mx, my))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_attaque.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.385)).collidepoint((mx, my)):
                                combat(1, joueurs_choix[compteur_lancers], liste_loup[compteur_loup])
                                if comparaison_vitesse(joueurs_choix[compteur_lancers], liste_loup[compteur_loup]) :
                                    if liste_loup[compteur_loup].pv <= 0 :
                                        monstre_battu += 1
                                        data["pv_loup"] = liste_loup[compteur_loup].pv
                                        compteur_loup += 1
                                        monstre_mort = True
                                        
                                    else :
                                        monstre_attaque(joueurs_choix[compteur_lancers], liste_loup[compteur_loup])
                                        if joueurs_choix[compteur_lancers].pv <= 0 :
                                            joueur_mort = True

                                else :
                                    if joueurs_choix[compteur_lancers].pv <= 0:
                                            joueur_mort = True

                                    else :
                                        attaque(joueurs_choix[compteur_lancers], liste_loup[compteur_loup])
                                        if liste_loup[compteur_loup].pv <= 0 :
                                            monstre_battu += 1
                                            data["pv_loup"] = liste_loup[compteur_loup].pv
                                            compteur_loup += 1
                                            monstre_mort = True

                                if joueur_mort :

                                    menu_mort = True
                                    while menu_mort :
                                        mx, my = pygame.mouse.get_pos()
                                        screen.blit(fond_image, (0, 0))
                                        draw_text("Vous avez perdu !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)

                                        bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
                                        bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
                                        screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
                                        draw_text("Quitter", SCREEN_WIDTH//20, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)

                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                socket.close()
                                                pygame.quit()
                                                sys.exit()
                                                

                                            if event.type == pygame.MOUSEMOTION: 
                                                mx, my = pygame.mouse.get_pos()
                                                bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)) :
                                                    joueurs_choix.clear()   
                                                    supprimer_classes()
                                                    running = False
                                                    en_combat = False
                                                    menu_mort = False
                                                    socket.close()

                                        pygame.display.update()
                                        clock.tick(FPS)
                                
                                elif monstre_mort :
                                    joueurs_piegee = False
                                    en_combat = False
                                    
                        # Bouton attaque puissante
                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_attaque_puissante_survole = bouton_attaque_puissante.get_rect(center=((SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.585))).collidepoint((mx, my))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_attaque_puissante.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.585)).collidepoint((mx, my)):
                                combat(2, joueurs_choix[compteur_lancers], liste_loup[compteur_loup])
                                if comparaison_vitesse(joueurs_choix[compteur_lancers], liste_loup[compteur_loup]) :
                                    if liste_loup[compteur_loup].pv <= 0 :
                                        monstre_battu += 1
                                        data["pv_loup"] = liste_loup[compteur_loup].pv
                                        compteur_loup += 1
                                        monstre_mort = True

                                    else :
                                        monstre_attaque(joueurs_choix[compteur_lancers], liste_loup[compteur_loup])
                                        if joueurs_choix[compteur_lancers].pv <= 0 :
                                            joueur_mort = True

                                else :
                                    if joueurs_choix[compteur_lancers].pv <= 0 :
                                            joueur_mort = True

                                    else :
                                        attaque_puissante(joueurs_choix[compteur_lancers], liste_loup[compteur_loup])
                                        if liste_loup[compteur_loup].pv <= 0 :
                                            monstre_battu += 1
                                            data["pv_loup"] = liste_loup[compteur_loup].pv
                                            compteur_loup += 1
                                            monstre_mort = True

                                if joueur_mort :

                                    menu_mort = True
                                    while menu_mort :
                                        mx, my = pygame.mouse.get_pos()
                                        screen.blit(fond_image, (0, 0))
                                        draw_text("Vous avez perdu !", 140, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)

                                        bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
                                        bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
                                        screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
                                        draw_text("Quitter", 60, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)

                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()

                                            if event.type == pygame.MOUSEMOTION: 
                                                mx, my = pygame.mouse.get_pos()
                                                bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)) :
                                                    joueurs_choix.clear()   
                                                    supprimer_classes()
                                                    running = False
                                                    en_combat = False
                                                    menu_mort = False

                                        pygame.display.update()
                                        clock.tick(FPS)
                                        
                                
                                elif monstre_mort :
                                    compteur_lancers += 1
                                    joueurs_piegee = False
                                    en_combat = False

                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_attaque_magique_survole = bouton_attaque_magique.get_rect(center=((SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.785))).collidepoint((mx, my))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_attaque_magique.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.785)).collidepoint((mx, my)):
                                combat(3, joueurs_choix[compteur_lancers], liste_loup[compteur_loup])
                                if comparaison_vitesse(joueurs_choix[compteur_lancers], liste_loup[compteur_loup]) :
                                    if liste_loup[compteur_loup].pv <= 0 :
                                        monstre_battu += 1
                                        data["pv_loup"] = liste_loup[compteur_loup].pv
                                        compteur_loup += 1
                                        monstre_mort = True

                                    else :
                                        monstre_attaque(joueurs_choix[compteur_lancers], liste_loup[compteur_loup])
                                        if joueurs_choix[compteur_lancers].pv <= 0 :
                                            joueur_mort = True

                                else :
                                    if joueurs_choix[compteur_lancers].pv <= 0 :
                                            joueur_mort = True

                                    else :
                                        attaque_magique(joueurs_choix[compteur_lancers], liste_loup[compteur_loup])
                                        if liste_loup[compteur_loup].pv <= 0 :
                                            monstre_battu += 1
                                            data["pv_loup"] = liste_loup[compteur_loup].pv
                                            compteur_loup += 1
                                            monstre_mort = True

                                if joueur_mort :

                                    menu_mort = True
                                    while menu_mort :
                                        mx, my = pygame.mouse.get_pos()
                                        screen.blit(fond_image, (0, 0))
                                        draw_text("Vous avez perdu !", 140, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)

                                        bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
                                        bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
                                        screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
                                        draw_text("Quitter", 60, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)

                                        for event in pygame.event.get():
                                            if event.type == pygame.QUIT:
                                                pygame.quit()
                                                sys.exit()

                                            if event.type == pygame.MOUSEMOTION: 
                                                mx, my = pygame.mouse.get_pos()
                                                bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

                                            if event.type == pygame.MOUSEBUTTONDOWN:
                                                if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)) :
                                                    joueurs_choix.clear()   
                                                    supprimer_classes()
                                                    running = False
                                                    en_combat = False
                                                    menu_mort = False

                                        pygame.display.update()
                                        clock.tick(FPS)
                                
                                elif monstre_mort :
                                    compteur_lancers += 1
                                    joueurs_piegee = False
                                    en_combat = False


                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_5_survole = bouton_5.get_rect(center=((SCREEN_WIDTH*0.965), SCREEN_HEIGHT*(0.015))).collidepoint((mx, my))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_5.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.015)).collidepoint((mx, my)):
                                joueurs_choix.clear()   
                                supprimer_classes()
                                running = False                       
                                en_combat = False
                                
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            data = {}
                            try:
                                data["pv"] = joueurs_choix[compteur_lancers].pv
                                data["potion"] = joueurs_choix[compteur_lancers].potion
                            except IndexError:
                                data["pv"] = joueurs_choix[compteur_lancers - 1].pv
                                data["potion"] = joueurs_choix[compteur_lancers - 1].potion
                            data["monstre_mort"] = monstre_mort
                            data["joueur_mort"] = joueur_mort
                            data["monstre_battu"] = monstre_battu
                            data["compteur_loup"] = compteur_loup
                            if compteur_loup < 5 :
                                data["pv_loup"] = liste_loup[compteur_loup].pv
                            else:
                                data["pv_loup"] = liste_loup[compteur_loup - 1].pv
                            compteur_lancers += 1
                            data["compteur_lancers"] = compteur_lancers
                            socket.send(str.encode(str(data)))

                    pygame.display.update()
                    clock.tick(FPS)
                
                else:
                    data = {}
                    pygame.display.update()
                    clock.tick(FPS)
                    data = socket.recv(1024).decode()
                    
                    # Si c'est un dictionnaire                            
                    if data[0] == "{":
                        data = eval(data)
                        
                        data['pv'] = int(data['pv'])
                        data['potion'] = int(data['potion'])
                        data['monstre_mort'] = bool(data['monstre_mort'])
                        data['joueur_mort'] = bool(data['joueur_mort'])
                        data['monstre_battu'] = int(data['monstre_battu'])
                        data['compteur_loup'] = int(data['compteur_loup'])
                        data['pv_loup'] = int(data['pv_loup'])
                        data['compteur_lancers'] = int(data['compteur_lancers'])

                        joueurs_choix[compteur_lancers].pv = data['pv']
                        joueurs_choix[compteur_lancers].potion = data['potion']
                        monstre_mort = data['monstre_mort']
                        joueur_mort = data['joueur_mort']
                        monstre_battu = data['monstre_battu']
                        compteur_loup = data['compteur_loup']
                        if compteur_loup < 5 :
                            liste_loup[compteur_loup].pv = data['pv_loup']
                        else:
                            liste_loup[compteur_loup - 1].pv = data['pv_loup']
                        compteur_lancers = data['compteur_lancers'] 
                        
                        if joueur_mort :

                            menu_mort = True
                            while menu_mort :
                                mx, my = pygame.mouse.get_pos()
                                screen.blit(fond_image, (0, 0))
                                draw_text("Vous avez perdu !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)

                                bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
                                bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
                                screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
                                draw_text("Quitter", SCREEN_WIDTH//20, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)

                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        socket.close()
                                        pygame.quit()
                                        sys.exit()
                                        

                                    if event.type == pygame.MOUSEMOTION: 
                                        mx, my = pygame.mouse.get_pos()
                                        bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.8) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)) :
                                            joueurs_choix.clear()   
                                            supprimer_classes()
                                            running = False
                                            en_combat = False
                                            menu_mort = False
                                            socket.close()

                                pygame.display.update()
                                clock.tick(FPS)
                        
                        elif monstre_mort :
                            joueurs_piegee = False
                            en_combat = False


        rectangles = []
        if compteur_lancers >= len(joueurs_choix):
            compteur_lancers = 0

        screen.blit(fond_image, (0, 0))
        
        for y in range(laby.getHauteur()):
            for x in range(laby.getLargeur()):
                base_x = (x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.63)
                base_y = (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 14)
                
                case = laby.getCase(x, y)
                murs = case.getMurs()
                if (x != 5) and (y != 11):
                    if 'N' in murs:
                        rectangles.append(
                            Rectangle(BLACK, base_x, base_y, SCREEN_HEIGHT//13.8, SCREEN_WIDTH//120))
                    if 'S' in murs:
                        rectangles.append(
                            Rectangle(BLACK, base_x, base_y + SCREEN_HEIGHT//13.8, SCREEN_HEIGHT//11.5, SCREEN_WIDTH//120))
                    if 'E' in murs:
                        rectangles.append(
                            Rectangle(BLACK, base_x + SCREEN_HEIGHT//13.8, base_y, SCREEN_WIDTH//120, SCREEN_HEIGHT//11.5))
                    if 'W' in murs:
                        rectangles.append(
                            Rectangle(BLACK, base_x, base_y, SCREEN_WIDTH//120, SCREEN_HEIGHT//13.8))
                else:
                    if 'N' in murs:
                        rectangles.append(
                            Rectangle(BLACK, base_x, base_y, SCREEN_HEIGHT//13.8, SCREEN_WIDTH//120))
                    if 'E' in murs:
                        rectangles.append(
                            Rectangle(BLACK, base_x + SCREEN_HEIGHT//13.8, base_y, SCREEN_WIDTH//120, SCREEN_HEIGHT//11.5))
                    if 'W' in murs:
                        rectangles.append(
                            Rectangle(BLACK, base_x, base_y, SCREEN_WIDTH//120, SCREEN_HEIGHT//13.8))
                        
        # Ajustements pour les valeurs spécifiques
        base_x = (SCREEN_WIDTH // 3.63)
        base_y = (SCREEN_HEIGHT // 14)

        rectangles.append(Rectangle(BLACK, SCREEN_WIDTH //
                            2.089, SCREEN_HEIGHT//1.143, SCREEN_WIDTH//120, SCREEN_HEIGHT//13.8))
        rectangles.append(Rectangle(BLACK, SCREEN_WIDTH //
                            1.925, SCREEN_HEIGHT//1.143, SCREEN_WIDTH//120, SCREEN_HEIGHT//13.8))

        for rectangle in rectangles:
            rectangle.draw()
        
        mx, my = pygame.mouse.get_pos()

        bouton_5 = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)
        bouton_5.fill(TRANSPARENT if not bouton_5_survole else BROWN)
        screen.blit(bouton_5, ((SCREEN_WIDTH*(0.92), SCREEN_HEIGHT*(0.001))))
        draw_text("Quitter", SCREEN_WIDTH//43, SCREEN_WIDTH*0.96, SCREEN_HEIGHT//(-120), BLACK)


        afficherJoueursLaby(joueurs_choix)

        # Affichage du menu stats / objet d'un joueur

        fond_player = pygame.Surface((SCREEN_WIDTH//4.3, SCREEN_HEIGHT), pygame.SRCALPHA)
        fond_player.fill(WHITE_TR)
        screen.blit(fond_player, ((SCREEN_WIDTH*0.001), SCREEN_HEIGHT*(0.001)))
        draw_text(f"Joueur {compteur_lancers + 1} :", SCREEN_WIDTH//25, SCREEN_WIDTH*0.09, SCREEN_HEIGHT*0.01, BLACK)
        
        # Affichage du joueur
        draw_text(f"C'est le joueur : {numero}", 50, SCREEN_WIDTH*0.9, SCREEN_HEIGHT*0.01, BLACK)

        # Affichage point de vie

        draw_text(f"PV : {joueurs_choix[compteur_lancers].pv} / {joueurs_choix[compteur_lancers].pv_max}", SCREEN_WIDTH//70, SCREEN_WIDTH*0.05, SCREEN_HEIGHT*0.12, BLACK)
        
        # Rectangles pour afficher une barre de vie

        rectangle_vert = pygame.Surface((((SCREEN_WIDTH//8.2) * (joueurs_choix[compteur_lancers].pv) // joueurs_choix[compteur_lancers].pv_max), SCREEN_HEIGHT//30), pygame.SRCALPHA)
        rectangle_vert.fill(GREEN)
        screen.blit(rectangle_vert, ((SCREEN_WIDTH*0.103), SCREEN_HEIGHT*(0.12)))

        morc_rectangle1 = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//150), pygame.SRCALPHA)
        morc_rectangle1.fill(BLACK)
        screen.blit(morc_rectangle1, ((SCREEN_WIDTH*0.1), SCREEN_HEIGHT*(0.12)))

        morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//8, SCREEN_HEIGHT//150), pygame.SRCALPHA)
        morc_rectangle2.fill(BLACK)
        screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.1), SCREEN_HEIGHT*(0.15)))

        morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//300, SCREEN_HEIGHT//30), pygame.SRCALPHA)
        morc_rectangle2.fill(BLACK)
        screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.1), SCREEN_HEIGHT*(0.12)))

        morc_rectangle2 = pygame.Surface((SCREEN_WIDTH//300, SCREEN_HEIGHT//30), pygame.SRCALPHA)
        morc_rectangle2.fill(BLACK)
        screen.blit(morc_rectangle2, ((SCREEN_WIDTH*0.222), SCREEN_HEIGHT*(0.12)))

        if not lancer_fait and numero == str(compteur_lancers + 1) :
            de, cases_accessibles = dice(graphe, joueurs_choix[compteur_lancers])
            de_resultat = de
            lancer_fait = True
            
        # Affichage statistiques et objets

        draw_text(f"Attaque  :   {joueurs_choix[compteur_lancers].attaque}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.2, BLACK)
        draw_text(f"Magie   :   {joueurs_choix[compteur_lancers].magie}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.3, BLACK)
        draw_text(f"Vitesse   :   {joueurs_choix[compteur_lancers].vitesse}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.4, BLACK)
        draw_text(f"Potion   :   {joueurs_choix[compteur_lancers].potion}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.5, BLACK)
        draw_text(f"Argent   :   {joueurs_choix[compteur_lancers].argent}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.075, SCREEN_HEIGHT*0.6, BLACK)
        draw_text(f"Dé résultat : {de_resultat}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.075, SCREEN_HEIGHT*0.7, BLACK)

       # Affichage bouton utiliser potion (seulement si on a pas tout ses points de vie)
        if joueurs_choix[compteur_lancers].pv != joueurs_choix[compteur_lancers].pv_max and joueurs_choix[compteur_lancers].potion > 0 and numero == str(compteur_lancers + 1):
            bouton_potion = pygame.Surface((SCREEN_WIDTH*0.17, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
            bouton_potion.fill(WHITE_TR)
            screen.blit(bouton_potion, ((SCREEN_WIDTH*0.78), SCREEN_HEIGHT*0.155))
            draw_text("Boire potion", SCREEN_WIDTH//35, SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.155, BLACK)
            potion_possible = True
        
        # Affichage bouton ouvrir piège dorée (seulement si on a fait les 5 pièges et qu'on est sur la case du piège dorée)
        if monstre_battu == 5:
            piege_doree_possible = True 
            draw_text("Vous pouvez aller", SCREEN_WIDTH//45, SCREEN_WIDTH*0.11, SCREEN_HEIGHT*0.83, BLACK)
            draw_text("ouvrir le piège dorée !", SCREEN_WIDTH//45, SCREEN_WIDTH*0.115, SCREEN_HEIGHT*0.88, BLACK)
        if piege_doree_possible == True and joueur_sur_piege_doree(joueurs_choix[compteur_lancers], piege_doree_positions) :
            bouton_piege_doree = pygame.Surface((SCREEN_WIDTH*0.215, SCREEN_HEIGHT*0.18), pygame.SRCALPHA)
            bouton_piege_doree.fill(WHITE_TR)
            screen.blit(bouton_piege_doree, ((SCREEN_WIDTH*0.755), SCREEN_HEIGHT*0.73))
            draw_text("Ouvrir le", SCREEN_WIDTH//28, SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.725, BLACK)
            draw_text("piège doré !", SCREEN_WIDTH//28, SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.825, BLACK)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_piege_doree.get_rect(center=(SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.775)).collidepoint((mx, my)):
                    ouvrir_piege_doree = True
                    # envoie de l'ouverture du piège dorée
                    liste_a_envoyer = []
                    liste_a_envoyer.append(ouvrir_piege_doree)
                    
                    socket.send(str.encode(str(liste_a_envoyer)))
                    

        for piege_position in piege_positions:
            x, y = piege_position
            screen.blit(piege_images[piege_positions.index(piege_position)], ((x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.35) - (SCREEN_HEIGHT//36), (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 8.8) - (SCREEN_HEIGHT//36)))
    
        for piege_doree_position in piege_doree_positions:
            x, y = piege_doree_position
            screen.blit(piege_doree_image, ((x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.35) - (SCREEN_HEIGHT//36), (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 8.8) - (SCREEN_HEIGHT//36)))

        for potion_position in potion_positions:
            x, y = potion_position
            screen.blit(potion_images[potion_positions.index(potion_position)], ((x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.35) - (SCREEN_HEIGHT//45), (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 8.8) - (SCREEN_HEIGHT//45)))

        for argent_position in argent_positions:
            x, y = argent_position
            screen.blit(argent_images[argent_positions.index(argent_position)], ((x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.35) - (SCREEN_HEIGHT//45), (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 8.8) - (SCREEN_HEIGHT//45)))

        if numero == str(compteur_lancers + 1) :
            for case in cases_accessibles:
                x, y = case
                pointRouge = Point((x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.35), (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 8.8))
                pointRouge.draw((RED), (SCREEN_HEIGHT//150))
        

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    for case in cases_accessibles:
                        x, y = case
                        point_x = (x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.45)
                        point_y = (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 9.2)

                        if point_x - (SCREEN_HEIGHT//60) <= mx <= point_x + (SCREEN_HEIGHT//20) and point_y - (SCREEN_HEIGHT//35) <= my <= point_y + (SCREEN_HEIGHT//30):
                            if int(numero) - 1 == joueurs_choix.index(joueurs_choix[compteur_lancers]) :
                                liste_a_envoyer = []
                                                                
                                nb_argent, nb_potion, argent_positions, potion_positions = verifier_objet_stat(case, potion_positions, potion_images, argent_positions, argent_images, joueurs_choix[compteur_lancers], nb_argent, nb_potion)
                                
                                joueurs_choix[compteur_lancers].position = case

                                cases_accessibles = []
                                compteur_lancers += 1
                                if compteur_lancers >= len(joueurs_choix):
                                    nb_tour += 1
                                    for joueur in joueurs_choix:
                                        liste_postion_joueur.append(joueur.position)
                                    liste_position_potion.append(potion_positions)
                                    liste_position_argent.append(argent_positions)
                                    liste_position_piege.append(piege_positions)   
                                    print("liste_position_potion", liste_position_potion)
                                    print("liste_position_argent", liste_position_argent)                                 
                                    compteur_lancers = 0
                                lancer_fait = False
                                
                                liste_a_envoyer.append(case)
                                liste_a_envoyer.append(compteur_lancers)
                                liste_a_envoyer.append(ouvrir_piege_doree)
                                
                                if joueur_sur_piege(joueurs_choix[compteur_lancers - 1], piege_positions) :
                                    for joueur in joueurs_choix:
                                        joueur.position = case
                                    verifier_piege(case, piege_positions, piege_images)
                                    joueurs_piegee = True
                                    
                                socket.send(str.encode(str(liste_a_envoyer)))
                                liste_a_envoyer = []
                                        
                if potion_possible == True :
                    if event.type == pygame.MOUSEMOTION: 
                        mx, my = pygame.mouse.get_pos()
                        potion_possible = bouton_potion.get_rect(center=(SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.19)).collidepoint((mx, my))
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if bouton_potion.get_rect(center=(SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.19)).collidepoint((mx, my)): 
                            joueurs_choix[compteur_lancers].utiliser_potion()
                            potion_possible = False

                if piege_doree_possible == True :
                    if event.type == pygame.MOUSEMOTION: 
                        mx, my = pygame.mouse.get_pos()
                                
                                                                                                           
                    if compteur_lancers >= len(joueurs_choix):
                        compteur_lancers = 0   
                            
                        
        else:
            try :
                pygame.display.update()
                clock.tick(FPS)
                liste_recu = []
                data = socket.recv(100000).decode()
                if data[0] != "[":
                    pygame.display.update()
                    clock.tick(FPS)
                    data = socket.recv(100000).decode()
                liste_recu = eval(data)
                
                if len(liste_recu) == 3 :
                
                    cases = liste_recu[0]
                    compteur_lancers = liste_recu[1]
                    joueurs_choix[compteur_lancers - 1].position = cases
                    nb_argent, nb_potion, argent_positions, potion_positions = verifier_objet_stat(cases, potion_positions, potion_images, argent_positions, argent_images, joueurs_choix[compteur_lancers - 1], nb_argent, nb_potion)
                    if joueur_sur_piege(joueurs_choix[compteur_lancers - 1], piege_positions) :
                        for joueur in joueurs_choix:
                            joueur.position = cases
                        verifier_piege(cases, piege_positions, piege_images)
                        joueurs_piegee = True
                    liste_recu = []
                elif len(liste_recu) == 1 :
                    ouvrir_piege_doree = liste_recu[0]
                
            except Exception as e :
                pass



        pygame.display.update()

        clock.tick(FPS)


if __name__ == "__main__":

    choix = 2
    graphe = None
    joueurs_choix = []
    joueurs_choix.append(Joueur("Mage", graphe, (5,10), 80, 80, 5, 30, 8, 5, 100, "img/classe/Mage.png"))
    joueurs_choix.append(Joueur("Paladin", graphe, (5,10), 100, 100, 5, 30, 8, 5, 100, "img/classe/Paladin.png"))
    joueurs_choix.append(Joueur("Berserk", graphe, (5,10), 80, 80, 5, 30, 8, 5, 100, "img/classe/Berserk.png"))
    joueurs_choix.append(Joueur("Archer", graphe, (5,10), 100, 100, 5, 30, 8, 5, 100, "img/classe/Archer.png")) 
