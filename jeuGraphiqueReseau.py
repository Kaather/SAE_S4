import pygame
import sys
import random
from plateau import *
from pygameOutils import *
from labyrinthe import *
from entite import *
import time
from bouton import *
from statistique import *
import combatMonstre

pygame.init()

info = pygame.display.Info()

# Définir les dimensions de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Labyrinthe")
clock = pygame.time.Clock()
FPS = 60
 

def affichageGraphiqueReseau(choix, graphe, joueurs_choix, socket, numero) :
    #temps de jeu
    start_time = time.time()
    monstre = []
    boss = []
    monstre_choisi = None
    
    monstre.append(Monstre("Loup", 50, 50, 10, 5, 15, "img/ennemi/loup.png"))
    monstre.append(Monstre("Gobelin", 60, 60, 15, 8, 10, "img/ennemi/gobelin.png"))
    monstre.append(Monstre("Orc", 70, 70, 20, 10, 12, "img/ennemi/orc.png"))
    monstre.append(Monstre("Troll", 80, 80, 25, 12, 14, "img/ennemi/troll.png"))
    monstre.append(Monstre("Slime", 40, 40, 5, 3, 20, "img/ennemi/slime.png"))
    monstre.append(Monstre("Squelette", 50, 50, 10, 5, 15, "img/ennemi/squelette.png"))
    monstre.append(Monstre("Zombie", 60, 60, 15, 8, 10, "img/ennemi/zombie.png"))
    monstre.append(Monstre("Fantome", 70, 70, 20, 10, 12, "img/ennemi/fantome.png"))
    monstre.append(Monstre("Momie", 80, 80, 25, 12, 14, "img/ennemi/momie.png"))
    
    boss.append(Monstre("Dragon", 100, 100, 20, 10, 12, "img/ennemi/dragon.png"))
    boss.append(Monstre("Mort", 100, 100, 20, 10, 12, "img/ennemi/mort.png"))
    boss.append(Monstre("Aguni", 100, 100, 20, 10, 12, "img/ennemi/aguni.png"))
    boss.append(Monstre("Gergoth", 100, 100, 20, 10, 12, "img/ennemi/gergoth.png"))
    boss.append(Monstre("Ange Déchu", 100, 100, 20, 10, 12, "img/ennemi/angeDechu.png"))

    fond = [
    'img/map/desert.png',  
    'img/map/neige.png',
    'img/map/foret.png',
    'img/map/donjon.png'
    ]
    
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
    ouvrir_shop = False
    
    
    liste_postion_joueur = []
    liste_position_piege = []
    liste_position_potion = []
    liste_position_argent = []

    monstre_battu = 0
    nb_tour = 0
    nb_potion = 0
    nb_argent = 0
    compteur_lancers = 0    
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
    _, _, piege_images, piege_doree_image, _, shop_image = evenement(graphe)
    _, potion_images, _, argent_images = ajouter_objet(graphe, [], [], [])
        
    if numero == "1" :
        piege_positions, piege_doree_positions, piege_images, piege_doree_image, shop_positions, shop_image = evenement(graphe)
        potion_positions, potion_images, argent_positions, argent_images = ajouter_objet(graphe, piege_positions, piege_doree_positions, shop_positions)
        
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
        time.sleep(0.5)
        
        serialisation = str(shop_positions)
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
                
                shop_positions = socket.recv(10000000).decode()
                shop_positions = eval(shop_positions)
                
                envoiePos = False                
            except Exception as e :
                pass

    running = True
    while running:
        bouton_quitter_survole = False
        # shop
        bouton_sortir_shop_survole = False
        bouton_achat_1_survole = False
        bouton_achat_2_survole = False
        bouton_achat_3_survole = False
        bouton_achat_4_survole = False
        if ouvrir_shop :
            shopping = True
            while shopping :

                mx, my = pygame.mouse.get_pos()

                shop_map_image = pygame.image.load('img/map/mapShop.png').convert()
                shop_map_image = pygame.transform.scale(shop_map_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                screen.blit(shop_map_image, (0, 0))
                
                bouton_quitter = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)
                bouton_quitter.fill(TRANSPARENT if not bouton_quitter_survole else BROWN)
                screen.blit(bouton_quitter, ((SCREEN_WIDTH*(0.92), SCREEN_HEIGHT*(0.001))))
                draw_text("Quitter", SCREEN_WIDTH//43, SCREEN_WIDTH*0.96, SCREEN_HEIGHT//(-120), BLACK)

                bouton_sortir_shop = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)
                bouton_sortir_shop.fill(TRANSPARENT if not bouton_sortir_shop_survole else BROWN)
                screen.blit(bouton_sortir_shop, ((SCREEN_WIDTH*0.92, SCREEN_HEIGHT//22)))
                draw_text("Sortir", SCREEN_WIDTH//43, SCREEN_WIDTH*0.96, SCREEN_HEIGHT//22, BLACK)

                joueur_image = pygame.image.load(joueurs_choix[compteur_lancers].image).convert_alpha()
                joueur_image = pygame.transform.scale(joueur_image, (SCREEN_WIDTH//8, SCREEN_WIDTH//8))
                screen.blit(joueur_image, (SCREEN_WIDTH*0.325, SCREEN_HEIGHT*0.65))

                bouton_achat_1 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//2), pygame.SRCALPHA)
                bouton_achat_1.fill(WHITE_TR if not bouton_achat_1_survole else WHITE)
                screen.blit(bouton_achat_1, ((SCREEN_WIDTH//21, SCREEN_HEIGHT//4)))
                draw_text("+ 10 Attaque", SCREEN_WIDTH//35, SCREEN_WIDTH//7, SCREEN_HEIGHT//1.55, BLACK)
                draw_text("300$", SCREEN_WIDTH//50, SCREEN_WIDTH//6.8, SCREEN_HEIGHT//1.43, BLACK)

                bouton_achat_2 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//2), pygame.SRCALPHA)
                bouton_achat_2.fill(WHITE_TR if not bouton_achat_2_survole else WHITE)
                screen.blit(bouton_achat_2, ((SCREEN_WIDTH//3.52, SCREEN_HEIGHT//4)))
                draw_text("+ 10 Magie", SCREEN_WIDTH//35, SCREEN_WIDTH//2.65, SCREEN_HEIGHT//1.55, BLACK)
                draw_text("300$", SCREEN_WIDTH//50, SCREEN_WIDTH//2.6, SCREEN_HEIGHT//1.43, BLACK)

                bouton_achat_3 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//2), pygame.SRCALPHA)
                bouton_achat_3.fill(WHITE_TR if not bouton_achat_3_survole else WHITE)
                screen.blit(bouton_achat_3, ((SCREEN_WIDTH//1.92, SCREEN_HEIGHT//4)))
                draw_text("+ 10 Vitesse", SCREEN_WIDTH//35, SCREEN_WIDTH//1.62, SCREEN_HEIGHT//1.55, BLACK)
                draw_text("300$", SCREEN_WIDTH//50, SCREEN_WIDTH//1.61, SCREEN_HEIGHT//1.43, BLACK)

                bouton_achat_4 = pygame.Surface((SCREEN_WIDTH//5, SCREEN_HEIGHT//2), pygame.SRCALPHA)
                bouton_achat_4.fill(WHITE_TR if not bouton_achat_4_survole else WHITE)
                screen.blit(bouton_achat_4, ((SCREEN_WIDTH//1.32, SCREEN_HEIGHT//4)))
                draw_text("+ 1 Potion", SCREEN_WIDTH//35, SCREEN_WIDTH//1.175, SCREEN_HEIGHT//1.55, BLACK)
                draw_text("100$", SCREEN_WIDTH//50, SCREEN_WIDTH//1.17, SCREEN_HEIGHT//1.43, BLACK)

                shop_attaque_image = pygame.image.load('img/element/attaque.png').convert()
                shop_attaque_image = pygame.transform.scale(shop_attaque_image, (SCREEN_WIDTH//3.5, SCREEN_WIDTH//3.5))
                shop_attaque_image.set_colorkey(BLACK)
                screen.blit(shop_attaque_image, (SCREEN_WIDTH//1000, SCREEN_WIDTH//10))
                
                shop_magie_image = pygame.image.load('img/element/magie.png').convert()
                shop_magie_image = pygame.transform.scale(shop_magie_image, (SCREEN_WIDTH//6, SCREEN_WIDTH//6))
                shop_magie_image.set_colorkey(BLACK)
                screen.blit(shop_magie_image, (SCREEN_WIDTH//3.34, SCREEN_WIDTH//6.3))
                
                shop_vitesse_image = pygame.image.load('img/element/vitesse.png').convert()
                shop_vitesse_image = pygame.transform.scale(shop_vitesse_image, (SCREEN_WIDTH//4.7, SCREEN_WIDTH//4.7))
                shop_vitesse_image.set_colorkey(BLACK)
                screen.blit(shop_vitesse_image, (SCREEN_WIDTH//1.91, SCREEN_WIDTH//7))

                shop_potion_image = pygame.image.load('img/element/Potion.png').convert()
                shop_potion_image = pygame.transform.scale(shop_potion_image, (SCREEN_WIDTH//5.5, SCREEN_WIDTH//5.5))
                shop_potion_image.set_colorkey(BLACK)
                screen.blit(shop_potion_image, (SCREEN_WIDTH//1.315, SCREEN_WIDTH//6.5))

                draw_text(f"Argent   :   {joueurs_choix[compteur_lancers].argent}", SCREEN_WIDTH//30, SCREEN_WIDTH//8, SCREEN_HEIGHT//40, BLACK)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == pygame.MOUSEMOTION: 
                        mx, my = pygame.mouse.get_pos()
                        bouton_quitter_survole = bouton_quitter.get_rect(center=((SCREEN_WIDTH*0.965), SCREEN_HEIGHT*(0.015))).collidepoint((mx, my))

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if bouton_quitter.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.015)).collidepoint((mx, my)):
                            shopping = False

                    if event.type == pygame.MOUSEMOTION: 
                        mx, my = pygame.mouse.get_pos()
                        bouton_sortir_shop_survole = bouton_sortir_shop.get_rect(center=((SCREEN_WIDTH*0.965), SCREEN_HEIGHT//16)).collidepoint((mx, my))
                        

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if bouton_sortir_shop.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT//16)).collidepoint((mx, my)):
                            liste_a_envoyer = []
                            liste_a_envoyer.append(joueurs_choix[compteur_lancers].position)
                            liste_a_envoyer.append(compteur_lancers)
                            liste_a_envoyer.append(ouvrir_piege_doree)
                            
                            # envoie les stats du joueur qui a bougé
                            liste_a_envoyer.append(joueurs_choix[compteur_lancers].pv)
                            liste_a_envoyer.append(joueurs_choix[compteur_lancers].potion)
                            liste_a_envoyer.append(joueurs_choix[compteur_lancers].argent)
                            liste_a_envoyer.append(joueurs_choix[compteur_lancers].position)
                            liste_a_envoyer.append(joueurs_choix[compteur_lancers].pv_max)
                            liste_a_envoyer.append(joueurs_choix[compteur_lancers].attaque)
                            liste_a_envoyer.append(joueurs_choix[compteur_lancers].magie)
                            liste_a_envoyer.append(joueurs_choix[compteur_lancers].vitesse)
                            liste_a_envoyer.append("None")
                            
                            compteur_lancers += 1
                            if compteur_lancers >= len(joueurs_choix):
                                compteur_lancers = 0
                                nb_tour += 1
                                print("nb_tour", nb_tour)
                                for joueur in joueurs_choix:
                                    liste_postion_joueur.append(joueur.position)
                                liste_position_potion.append(potion_positions)
                                liste_position_argent.append(argent_positions)
                                liste_position_piege.append(piege_positions)
                                
                            liste_a_envoyer[1] = compteur_lancers
                                                                                     
                            cases_accessibles = []
                            lancer_fait = False
                                
                            socket.send(str.encode(str(liste_a_envoyer)))
                            liste_a_envoyer = []
                            shopping = False

                    if joueurs_choix[compteur_lancers].argent >= 300 :
                        
                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_achat_1_survole = bouton_achat_1.get_rect(center=((SCREEN_WIDTH//21)+(SCREEN_WIDTH//5)//2, (SCREEN_HEIGHT//4)+(SCREEN_HEIGHT//2)//2)).collidepoint((mx, my))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_achat_1.get_rect(center=((SCREEN_WIDTH//21)+(SCREEN_WIDTH//5)//2, (SCREEN_HEIGHT//4)+(SCREEN_HEIGHT//2)//2)).collidepoint((mx, my)):
                                joueurs_choix[compteur_lancers].attaque += 10
                                joueurs_choix[compteur_lancers].argent -= 300
                                bouton_achat_1_survole = False

                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_achat_2_survole = bouton_achat_2.get_rect(center=((SCREEN_WIDTH//3.52)+(SCREEN_WIDTH//5)//2, (SCREEN_HEIGHT//4)+(SCREEN_HEIGHT//2)//2)).collidepoint((mx, my))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_achat_2.get_rect(center=((SCREEN_WIDTH//3.52)+(SCREEN_WIDTH//5)//2, (SCREEN_HEIGHT//4)+(SCREEN_HEIGHT//2)//2)).collidepoint((mx, my)):
                                joueurs_choix[compteur_lancers].magie += 10
                                joueurs_choix[compteur_lancers].argent -= 300
                                bouton_achat_2_survole = False

                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_achat_3_survole = bouton_achat_3.get_rect(center=((SCREEN_WIDTH//1.92)+(SCREEN_WIDTH//5)//2, (SCREEN_HEIGHT//4)+(SCREEN_HEIGHT//2)//2)).collidepoint((mx, my))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_achat_3.get_rect(center=((SCREEN_WIDTH//1.92)+(SCREEN_WIDTH//5)//2, (SCREEN_HEIGHT//4)+(SCREEN_HEIGHT//2)//2)).collidepoint((mx, my)):
                                joueurs_choix[compteur_lancers].vitesse += 10
                                joueurs_choix[compteur_lancers].argent -= 300
                                bouton_achat_3_survole = False

                    if joueurs_choix[compteur_lancers].argent >= 100 :

                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_achat_4_survole = bouton_achat_4.get_rect(center=((SCREEN_WIDTH//1.32)+(SCREEN_WIDTH//5)//2, (SCREEN_HEIGHT//4)+(SCREEN_HEIGHT//2)//2)).collidepoint((mx, my))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_achat_4.get_rect(center=((SCREEN_WIDTH//1.32)+(SCREEN_WIDTH//5)//2, (SCREEN_HEIGHT//4)+(SCREEN_HEIGHT//2)//2)).collidepoint((mx, my)):
                                joueurs_choix[compteur_lancers].potion += 1
                                joueurs_choix[compteur_lancers].argent -= 100
                                bouton_achat_4_survole = False

                pygame.display.update()
                clock.tick(FPS)
                        
            lancer_fait = False
            ouvrir_shop = False
            
        # Combat final        
        if ouvrir_piege_doree:
            if combatMonstre.combatMonstreReseau(numero, socket, joueurs_choix, monstre_choisi, compteur_lancers, choix):
                ouvrir_piege_doree = False
                running = False   
                # calcul du temps de jeu
                duree = time.time() - start_time
                partie_finie = True
                monstre_battu = 6
            else:
                partie_finie = False
                duree = time.time() - start_time
                running = False
                
            if numero == str(len(joueurs_choix)) : 
                mise_en_stat(joueurs_choix, monstre_battu, partie_finie, nb_tour, choix, int(duree), nb_potion, nb_argent)  
            
            socket.close()
            pygame.quit()
            sys.exit()
     
        if joueurs_piegee:
            if not combatMonstre.combatMonstreReseau(numero, socket, joueurs_choix, monstre_choisi, compteur_lancers, choix):
                joueurs_piegee = False
                partie_finie = False
                duree = time.time() - start_time
                running = False
                if numero == str(len(joueurs_choix)) :
                    mise_en_stat(joueurs_choix, monstre_battu, partie_finie, nb_tour, choix, int(duree), nb_potion, nb_argent)
                socket.close()
                pygame.quit()
                sys.exit()
            joueurs_piegee = False
            monstre_battu += 1

        rectangles = []
        if compteur_lancers >= len(joueurs_choix):
            nb_tour += 1
            print("nb_tour", nb_tour)
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
                    
                    monstre_choisi = random.choice(boss)
                    boss.remove(monstre_choisi)
                    
                    liste_a_envoyer.append(monstre_choisi.nom)
                    
                    socket.send(str.encode(str(liste_a_envoyer)))
                    liste_a_envoyer = []
                    
        if joueur_sur_shop(joueurs_choix[compteur_lancers], shop_positions) :
            bouton_shop = pygame.Surface((SCREEN_WIDTH*0.215, SCREEN_HEIGHT*0.18), pygame.SRCALPHA)
            bouton_shop.fill(WHITE_TR)
            screen.blit(bouton_shop, ((SCREEN_WIDTH*0.755), SCREEN_HEIGHT*0.73))
            draw_text("Ouvrir le", SCREEN_WIDTH//28, SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.725, BLACK)
            draw_text("Shop !", SCREEN_WIDTH//28, SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.825, BLACK)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_shop.get_rect(center=(SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.775)).collidepoint((mx, my)):
                    ouvrir_shop = True
                    
        for shop_position in shop_positions :
            x, y = shop_position
            screen.blit(shop_image, ((x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.49) - (SCREEN_HEIGHT//36), (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 11) - (SCREEN_HEIGHT//36)))                    

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
                                                                
                                nb_argent, nb_potion = verifier_objet_stat(case, potion_positions, potion_images, argent_positions, argent_images, joueurs_choix[compteur_lancers], nb_argent, nb_potion)
                                
                                joueurs_choix[compteur_lancers].position = case

                                cases_accessibles = []
                                compteur_lancers += 1
                                if compteur_lancers >= len(joueurs_choix):
                                    nb_tour += 1
                                    print("nb_tour", nb_tour)
                                    for joueur in joueurs_choix:
                                        liste_postion_joueur.append(joueur.position)
                                    liste_position_potion.append(potion_positions)
                                    liste_position_argent.append(argent_positions)
                                    liste_position_piege.append(piege_positions)                                
                                    compteur_lancers = 0
                                lancer_fait = False
                                
                                liste_a_envoyer.append(case)
                                liste_a_envoyer.append(compteur_lancers)
                                liste_a_envoyer.append(ouvrir_piege_doree)
                                
                                # envoie les stats du joueur qui a bougé
                                liste_a_envoyer.append(joueurs_choix[compteur_lancers - 1].pv)
                                liste_a_envoyer.append(joueurs_choix[compteur_lancers - 1].potion)
                                liste_a_envoyer.append(joueurs_choix[compteur_lancers - 1].argent)
                                liste_a_envoyer.append(joueurs_choix[compteur_lancers - 1].position)
                                liste_a_envoyer.append(joueurs_choix[compteur_lancers - 1].pv_max)
                                liste_a_envoyer.append(joueurs_choix[compteur_lancers - 1].attaque)
                                liste_a_envoyer.append(joueurs_choix[compteur_lancers - 1].magie)
                                liste_a_envoyer.append(joueurs_choix[compteur_lancers - 1].vitesse)
                                
                                if joueur_sur_piege(joueurs_choix[compteur_lancers - 1], piege_positions) :
                                    for joueur in joueurs_choix:
                                        joueur.position = case
                                    verifier_piege(case, piege_positions, piege_images)
                                    monstre_choisi = random.choice(monstre)
                                    monstre.remove(monstre_choisi)                                    
                                    joueurs_piegee = True
                                    liste_a_envoyer.append(monstre_choisi.nom)  
                                else :
                                    liste_a_envoyer.append("None")
                                    
                                                                 
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
                        nb_tour += 1 
                            
                        
        else:
            try :
                pygame.display.update()
                clock.tick(FPS)
                liste_recu = []
                data = socket.recv(100000).decode()
                if data[0] != "[":
                    liste_recu = []
                    pygame.display.update()
                    clock.tick(FPS)
                    data = socket.recv(100000).decode()
                liste_recu = eval(data)
                
                if len(liste_recu) == 12 :
                
                    cases = liste_recu[0]
                    
                    compteur_lancers = liste_recu[1]
                    joueurs_choix[compteur_lancers - 1].position = cases
                    nb_argent, nb_potion = verifier_objet_stat(cases, potion_positions, potion_images, argent_positions, argent_images, joueurs_choix[compteur_lancers - 1], nb_argent, nb_potion)
                    joueurs_choix[compteur_lancers - 1].pv = liste_recu[3]
                    joueurs_choix[compteur_lancers - 1].potion = liste_recu[4]
                    joueurs_choix[compteur_lancers - 1].argent = liste_recu[5]
                    joueurs_choix[compteur_lancers - 1].position = liste_recu[6]
                    joueurs_choix[compteur_lancers - 1].pv_max = liste_recu[7]
                    joueurs_choix[compteur_lancers - 1].attaque = liste_recu[8]
                    joueurs_choix[compteur_lancers - 1].magie = liste_recu[9]
                    joueurs_choix[compteur_lancers - 1].vitesse = liste_recu[10]
                    if joueur_sur_piege(joueurs_choix[compteur_lancers - 1], piege_positions) :
                        joueurs_piegee = True
                        for joueur in joueurs_choix:
                            joueur.position = cases
                        verifier_piege(cases, piege_positions, piege_images)
                        monstre_choisi_nom = liste_recu[11]
                        for monster in monstre :
                            if monster.nom == monstre_choisi_nom :
                                monstre_choisi = monster
                                monstre.remove(monstre_choisi)   
                    liste_recu = []
                    
                elif len(liste_recu) == 2 :
                    ouvrir_piege_doree = liste_recu[0]
                    nom_boss = liste_recu[1]
                    for monstre in boss:
                        if monstre.nom == nom_boss :
                            monstre_choisi = monstre
                            boss.remove(monstre_choisi)
                    liste_recu = []
                
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
