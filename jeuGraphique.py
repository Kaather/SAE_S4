import pygame
import sys
from plateau import *
from pygameOutils import *
from labyrinthe import *
from entite import *
from bouton import *

pygame.init()

info = pygame.display.Info()

# Définir les dimensions de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
# SCREEN_WIDTH, SCREEN_HEIGHT = 760, 520
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Labyrinthe")
clock = pygame.time.Clock()
FPS = 60
 

def affichageGraphique(choix, graphe, joueurs_choix) :

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

    dragon = Monstre("Dragon", 100, 100, 20, 10, 12, "img/ennemi/dragon.png")
    
    fond_image = pygame.image.load(fond[choix]).convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fond_image, (0, 0))

    bouton_quitter_survole = False
    lancer_fait = False
    de_resultat = None
    potion_possible = False
    joueurs_piegee = False
    piege_doree_possible = False
    ouvrir_piege_doree = False
    ouvrir_shop = False
    shopping = False
    

    monstre_battu = 0

    compteur_lancers = 0

    compteur_loup = 0

    laby = Grille(largeur, hauteur)
    laby.construireBordure()
    graphe = labyrinthe(largeur, hauteur)
    laby.construireAvecGraphe(graphe)

    piege_positions, piege_doree_positions, piege_images, piege_doree_image, shop_positions, shop_image = evenement(graphe)

    potion_positions, potion_images, argent_positions, argent_images = ajouter_objet(graphe, piege_positions, piege_doree_positions, shop_positions)

    running = True
    while running:

        rectangles = []

        screen.blit(fond_image, (0, 0))
        
        for y in range(laby.getHauteur()):
            for x in range(laby.getLargeur()):
                case = laby.getCase(x, y)
                murs = case.getMurs()

                base_x = (x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.63)
                base_y = (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 14)

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

        bouton_quitter = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)
        bouton_quitter.fill(TRANSPARENT if not bouton_quitter_survole else BROWN)
        screen.blit(bouton_quitter, ((SCREEN_WIDTH*(0.92), SCREEN_HEIGHT*(0.001))))
        draw_text("Quitter", SCREEN_WIDTH//43, SCREEN_WIDTH*0.96, SCREEN_HEIGHT//(-120), BLACK)


        afficherJoueursLaby(joueurs_choix)

        # Affichage du menu stats / objet d'un joueur

        fond_player = pygame.Surface((SCREEN_WIDTH//4.3, SCREEN_HEIGHT), pygame.SRCALPHA)
        fond_player.fill(WHITE_TR)
        screen.blit(fond_player, ((SCREEN_WIDTH*0.001), SCREEN_HEIGHT*(0.001)))
        draw_text(f"Joueur {compteur_lancers + 1} :", SCREEN_WIDTH//25, SCREEN_WIDTH*0.09, SCREEN_HEIGHT*0.01, BLACK)

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

        if not lancer_fait:  
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
        if joueurs_choix[compteur_lancers].pv != joueurs_choix[compteur_lancers].pv_max :
            bouton_potion = pygame.Surface((SCREEN_WIDTH*0.17, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
            bouton_potion.fill(WHITE_TR)
            screen.blit(bouton_potion, ((SCREEN_WIDTH*0.78), SCREEN_HEIGHT*0.155))
            draw_text("Boire potion", SCREEN_WIDTH//35, SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.155, BLACK)
            potion_possible = True
        
        if joueur_sur_shop(joueurs_choix[compteur_lancers], shop_positions) :
            bouton_shop = pygame.Surface((SCREEN_WIDTH*0.215, SCREEN_HEIGHT*0.18), pygame.SRCALPHA)
            bouton_shop.fill(WHITE_TR)
            screen.blit(bouton_shop, ((SCREEN_WIDTH*0.755), SCREEN_HEIGHT*0.73))
            draw_text("Ouvrir le", SCREEN_WIDTH//28, SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.725, BLACK)
            draw_text("Shop !", SCREEN_WIDTH//28, SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.825, BLACK)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_shop.get_rect(center=(SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.775)).collidepoint((mx, my)):
                    ouvrir_shop = True

        # Affichage bouton ouvrir piège dorée (seulement si on a fait les 5 pièges et qu'on est sur la case du piège dorée)
        if monstre_battu == 5 :
            piege_doree_possible = True 
            draw_text("Vous pouvez aller", SCREEN_WIDTH//45, SCREEN_WIDTH*0.11, SCREEN_HEIGHT*0.83, BLACK)
            draw_text("ouvrir le piège dorée !", SCREEN_WIDTH//45, SCREEN_WIDTH*0.115, SCREEN_HEIGHT*0.88, BLACK)
        if piege_doree_possible == True and joueur_sur_piege_doree(joueurs_choix[compteur_lancers], piege_doree_positions) :
            bouton_piege_doree = pygame.Surface((SCREEN_WIDTH*0.215, SCREEN_HEIGHT*0.18), pygame.SRCALPHA)
            bouton_piege_doree.fill(WHITE_TR)
            screen.blit(bouton_piege_doree, ((SCREEN_WIDTH*0.755), SCREEN_HEIGHT*0.73))
            draw_text("Ouvrir le", SCREEN_WIDTH//28, SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.725, BLACK)
            draw_text("piège dorée !", SCREEN_WIDTH//28, SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.825, BLACK)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_piege_doree.get_rect(center=(SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.775)).collidepoint((mx, my)):
                    ouvrir_piege_doree = True

        for piege_position in piege_positions:
            x, y = piege_position
            screen.blit(piege_images[piege_positions.index(piege_position)], ((x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.35) - (SCREEN_HEIGHT//36), (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 8.8) - (SCREEN_HEIGHT//36)))
    
        for piege_doree_position in piege_doree_positions:
            x, y = piege_doree_position
            screen.blit(piege_doree_image, ((x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.35) - (SCREEN_HEIGHT//36), (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 8.8) - (SCREEN_HEIGHT//36)))

        for shop_position in shop_positions :
            x, y = shop_position
            screen.blit(shop_image, ((x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.49) - (SCREEN_HEIGHT//36), (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 11) - (SCREEN_HEIGHT//36)))

        for potion_position in potion_positions:
            x, y = potion_position
            screen.blit(potion_images[potion_positions.index(potion_position)], ((x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.35) - (SCREEN_HEIGHT//45), (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 8.8) - (SCREEN_HEIGHT//45)))

        for argent_position in argent_positions:
            x, y = argent_position
            screen.blit(argent_images[argent_positions.index(argent_position)], ((x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.35) - (SCREEN_HEIGHT//45), (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 8.8) - (SCREEN_HEIGHT//45)))

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

                        verifier_objet(case, potion_positions, potion_images, argent_positions, argent_images, joueurs_choix[compteur_lancers])
                            
                        joueurs_choix[compteur_lancers].position = case

                        if joueur_sur_piege(joueurs_choix[compteur_lancers], piege_positions) :
                            verifier_piege(case, piege_positions, piege_images)
                            joueurs_piegee = True

                        cases_accessibles = []
                        compteur_lancers += 1
                        if compteur_lancers >= len(joueurs_choix):
                            compteur_lancers = 0
                        lancer_fait = False
                        break

            if potion_possible == True :
                if event.type == pygame.MOUSEMOTION: 
                    mx, my = pygame.mouse.get_pos()
                    potion_possible = bouton_potion.get_rect(center=(SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.19)).collidepoint((mx, my))
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_potion.get_rect(center=(SCREEN_WIDTH*0.864, SCREEN_HEIGHT*0.19)).collidepoint((mx, my)): 
                        joueurs_choix[compteur_lancers].utiliser_potion()
                        potion_possible = False
                    
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
                while en_combat and joueurs_piegee :         

                    if compteur_lancers >= len(joueurs_choix):
                        compteur_lancers = 0

                    mx, my = pygame.mouse.get_pos()

                    combat_image = pygame.image.load('img/map/mapPiege.png').convert()
                    combat_image = pygame.transform.scale(combat_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                    screen.blit(combat_image, (0, 0))

                    bouton_quitter = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)
                    bouton_quitter.fill(TRANSPARENT if not bouton_quitter_survole else BROWN)
                    screen.blit(bouton_quitter, ((SCREEN_WIDTH*(0.92), SCREEN_HEIGHT*(0.001))))
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
                    if joueurs_choix[compteur_lancers].pv != joueurs_choix[compteur_lancers].pv_max :
                        bouton_potion = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
                        bouton_potion.fill(GREY_TR if not bouton_potion_survole else GREY)
                        screen.blit(bouton_potion, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.155))
                        draw_text("Boire potion", SCREEN_WIDTH//35, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.155, BLACK)
                        potion_possible = True

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
                                    compteur_lancers += 1                                 
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
                                        attaque(joueurs_choix[compteur_lancers], liste_loup[compteur_loup])
                                        if liste_loup[compteur_loup].pv <= 0 :
                                            monstre_battu += 1
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
                                    for joueur in joueurs_choix:
                                        joueur.position = case
                                    compteur_lancers += 1
                                    joueurs_piegee = False
                                    en_combat = False

                                else :
                                    compteur_lancers += 1


                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_quitter_survole = bouton_quitter.get_rect(center=((SCREEN_WIDTH*0.965), SCREEN_HEIGHT*(0.015))).collidepoint((mx, my))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_quitter.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.015)).collidepoint((mx, my)):
                                joueurs_choix.clear()   
                                supprimer_classes()
                                running = False                       
                                en_combat = False

                    pygame.display.update()
                    clock.tick(FPS)
                    
                if compteur_lancers >= len(joueurs_choix):
                    compteur_lancers = 0
            
            # Dans le shop
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

                ouvrir_shop = False

                compteur_lancers += 1  
                if compteur_lancers >= len(joueurs_choix):
                    compteur_lancers = 0

            # Combat final        
            if ouvrir_piege_doree :

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

                    bouton_quitter = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)
                    bouton_quitter.fill(TRANSPARENT if not bouton_quitter_survole else BROWN)
                    screen.blit(bouton_quitter, ((SCREEN_WIDTH*(0.92), SCREEN_HEIGHT*(0.001))))
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
                    if joueurs_choix[compteur_lancers].pv != joueurs_choix[compteur_lancers].pv_max :
                        bouton_potion = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
                        bouton_potion.fill(GREY_TR if not bouton_potion_survole else GREY)
                        screen.blit(bouton_potion, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.155))
                        draw_text("Boire potion", SCREEN_WIDTH//35, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.155, BLACK)
                        potion_possible = True

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
                                    compteur_lancers += 1                                 
                                    potion_possible = False
                                    

                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_attaque_survole = bouton_attaque.get_rect(center=((SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.385))).collidepoint((mx, my))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_attaque.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.385)).collidepoint((mx, my)):
                                combat(1, joueurs_choix[compteur_lancers], dragon)
                                if comparaison_vitesse(joueurs_choix[compteur_lancers], dragon) :
                                    if dragon.pv <= 0 :
                                        boss_battu = True
                                        monstre_mort = True

                                    else :
                                        monstre_attaque(joueurs_choix[compteur_lancers], dragon)
                                        if joueurs_choix[compteur_lancers].pv <= 0 :
                                            joueur_mort = True

                                else :
                                    if joueurs_choix[compteur_lancers].pv <= 0 :
                                            joueur_mort = True

                                    else :
                                        attaque(joueurs_choix[compteur_lancers], dragon)
                                        if dragon.pv <= 0 :
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
                                    for joueur in joueurs_choix:
                                        joueur.position = case
                                    compteur_lancers += 1
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

                                        pygame.display.update()
                                        clock.tick(FPS)

                                    joueurs_choix.clear()   
                                    supprimer_classes()
                                    running = False
                                    
                                else :
                                    compteur_lancers += 1

                        if event.type == pygame.MOUSEMOTION: 
                            mx, my = pygame.mouse.get_pos()
                            bouton_quitter_survole = bouton_quitter.get_rect(center=((SCREEN_WIDTH*0.965), SCREEN_HEIGHT*(0.015))).collidepoint((mx, my))

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if bouton_quitter.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.015)).collidepoint((mx, my)):
                                joueurs_choix.clear()   
                                supprimer_classes()
                                running = False                       
                                en_combat = False

                    pygame.display.update()
                    clock.tick(FPS)
                    
                if compteur_lancers >= len(joueurs_choix):
                    compteur_lancers = 0
                

            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_quitter_survole = bouton_quitter.get_rect(center=((SCREEN_WIDTH*0.965), SCREEN_HEIGHT*(0.015))).collidepoint((mx, my))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_quitter.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.015)).collidepoint((mx, my)):
                    joueurs_choix.clear()   
                    supprimer_classes()
                    running = False



        pygame.display.update()

        clock.tick(FPS)


if __name__ == "__main__":

    choix = 2
    graphe = None
    joueurs_choix = []
    joueurs_choix.append(Joueur("Paladin", graphe, (5,10), 100, 100, 16, 12, 10, 3, 100, "img/classe/Paladin.png"))            
    affichageGraphique(choix, graphe, joueurs_choix) 
