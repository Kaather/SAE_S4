import pygame
import sys
import random
from plateau import *
from pygameOutils import *
from labyrinthe import *
from entite import *
from bouton import *
import combatMonstre
import time
import statistique
from ia_deplacement import *
from ia_combat import * 

pygame.init()

info = pygame.display.Info()

# Définir les dimensions de la fenêtre
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
# SCREEN_WIDTH, SCREEN_HEIGHT = 760, 520
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Labyrinthe")
clock = pygame.time.Clock()
FPS = 60
 

def affichageGraphique(choix, graphe, joueurs_choix, difficulte, vrai_joueur) :
    duree = 0
    nombre_tour = 0
    # Calcul de la durée de la partie
    time_start = time.time()
    nb_argent = 0
    nb_potion = 0
    argent_positions = []
    potion_positions = []

    fond = [
    'img/map/desert.png',  
    'img/map/neige.png',
    'img/map/foret.png',
    'img/map/donjon.png'
    ]

    monstre = []
    boss = []
    
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
    
    
    fond_image = pygame.image.load(fond[choix]).convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fond_image, (0, 0))

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
    
    laby = Grille(largeur, hauteur)
    laby.construireBordure()
    graphe = labyrinthe(largeur, hauteur)
    laby.construireAvecGraphe(graphe)

    piege_positions, piege_doree_positions, piege_images, piege_doree_image, shop_positions, shop_image = evenement(graphe)
    piege_positions, piege_doree_positions, piege_images, piege_doree_image, shop_positions, shop_image = evenement(graphe)

    potion_positions, potion_images, argent_positions, argent_images = ajouter_objet(graphe, piege_positions, piege_doree_positions, shop_positions)

    bouton_quitter = Bouton(SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22, SCREEN_WIDTH//1.04, SCREEN_HEIGHT//50, TRANSPARENT, BROWN, "Quitter", SCREEN_WIDTH//45)
    bouton_sortir = Bouton(SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22, SCREEN_WIDTH//1.04, SCREEN_HEIGHT//16, TRANSPARENT, BROWN, "Sortir", SCREEN_WIDTH//45)
    bouton_potion = Bouton(SCREEN_WIDTH*0.17, SCREEN_HEIGHT*0.07, SCREEN_WIDTH*0.85, SCREEN_HEIGHT*0.155, WHITE_TR, WHITE, "Boire potion", SCREEN_WIDTH//35)
    bouton_shop = Bouton(SCREEN_WIDTH*0.215, SCREEN_HEIGHT*0.18, SCREEN_WIDTH*0.85, SCREEN_HEIGHT*0.78, WHITE_TR, WHITE, "Ouvrir le \nshop !", SCREEN_WIDTH//26)
    bouton_piege_doree = Bouton(SCREEN_WIDTH*0.215, SCREEN_HEIGHT*0.18, SCREEN_WIDTH*0.85, SCREEN_HEIGHT*0.73, WHITE_TR, WHITE, "Ouvrir le \npiège doré !", SCREEN_WIDTH//28)
    bouton_achat_attaque = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//2, SCREEN_WIDTH//6.75, SCREEN_HEIGHT//1.95, WHITE_TR, WHITE, "", SCREEN_WIDTH//100)
    bouton_achat_magie = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//2, SCREEN_WIDTH//2.62, SCREEN_HEIGHT//1.95, WHITE_TR, WHITE, "", SCREEN_WIDTH//100)
    bouton_achat_vitesse = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//2, SCREEN_WIDTH//1.605, SCREEN_HEIGHT//1.95, WHITE_TR, WHITE, "", SCREEN_WIDTH//100)
    bouton_achat_potion = Bouton(SCREEN_WIDTH//5, SCREEN_HEIGHT//2, SCREEN_WIDTH//1.165, SCREEN_HEIGHT//1.95, WHITE_TR, WHITE, "", SCREEN_WIDTH//100)

    running = True
    cases_explorees = [] 
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

        afficherJoueursLaby(joueurs_choix)
        
        cercle_joueur = Cercle(RED, joueurs_choix[compteur_lancers].position[0] * (SCREEN_HEIGHT//13.8) + (SCREEN_WIDTH // 3.35), joueurs_choix[compteur_lancers].position[1] * (SCREEN_HEIGHT//13.8) + (SCREEN_HEIGHT // 8.8), 20, 3)

        # Affichage du menu stats / objet d'un joueur

        fond_player = pygame.Surface((SCREEN_WIDTH//4.3, SCREEN_HEIGHT), pygame.SRCALPHA)
        fond_player.fill(WHITE_TR)
        screen.blit(fond_player, ((SCREEN_WIDTH*0.001), SCREEN_HEIGHT*(0.001)))
        draw_text(f"Joueur {compteur_lancers + 1} :", SCREEN_WIDTH//25, SCREEN_WIDTH*0.09, SCREEN_HEIGHT*0.01, BLACK)

        if not lancer_fait:  
            de, cases_accessibles = dice(graphe, joueurs_choix[compteur_lancers])   
            de_resultat = de
            lancer_fait = True
            # Ajouter les cases accessibles à la liste des cases explorées
            cases_explorees.extend(cases_accessibles)

        barre_joueur = BarreVie(SCREEN_WIDTH//9.5, SCREEN_HEIGHT//8, joueurs_choix[compteur_lancers].pv, joueurs_choix[compteur_lancers].pv_max)

        # Affichage statistiques et objets

        draw_text(f"Attaque  :   {joueurs_choix[compteur_lancers].attaque}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.2, BLACK)
        draw_text(f"Magie   :   {joueurs_choix[compteur_lancers].magie}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.3, BLACK)
        draw_text(f"Vitesse   :   {joueurs_choix[compteur_lancers].vitesse}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.4, BLACK)
        draw_text(f"Potion   :   {joueurs_choix[compteur_lancers].potion}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.07, SCREEN_HEIGHT*0.5, BLACK)
        draw_text(f"Argent   :   {joueurs_choix[compteur_lancers].argent}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.075, SCREEN_HEIGHT*0.6, BLACK)
        draw_text(f"Dé résultat : {de_resultat}", SCREEN_WIDTH//43, SCREEN_WIDTH*0.075, SCREEN_HEIGHT*0.7, BLACK)


        # Affichage bouton utiliser potion (seulement si on a pas tout ses points de vie)
        if joueurs_choix[compteur_lancers].pv != joueurs_choix[compteur_lancers].pv_max :
            potion_possible = True
            
        if vrai_joueur[compteur_lancers]:
            if joueur_sur_shop(joueurs_choix[compteur_lancers], shop_positions) :
                bouton_shop.hovered = bouton_shop.est_survol(mx, my)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_shop.est_survol(mx, my):
                        ouvrir_shop = True

        # Affichage bouton ouvrir piège dorée (seulement si on a fait les 5 pièges et qu'on est sur la case du piège dorée)
        if monstre_battu == 5:
            piege_doree_possible = True 
            draw_text("Vous pouvez aller", SCREEN_WIDTH//45, SCREEN_WIDTH*0.11, SCREEN_HEIGHT*0.83, BLACK)
            draw_text("ouvrir le piège dorée !", SCREEN_WIDTH//45, SCREEN_WIDTH*0.115, SCREEN_HEIGHT*0.88, BLACK)
            
        if vrai_joueur[compteur_lancers]:

            if piege_doree_possible == True and joueur_sur_piege_doree(joueurs_choix[compteur_lancers], piege_doree_positions) :
                bouton_piege_doree.hovered = bouton_piege_doree.est_survol(mx, my)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_piege_doree.est_survol(mx, my):
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

        for y in range(laby.getHauteur()):
            for x in range(laby.getLargeur()):
                base_x = (x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.63)
                base_y = (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 14)
                # Vérifiez si la case a déjà été explorée avant de dessiner le rectangle d'ombre
                if (x, y) not in cases_explorees: 
                    carre_ombre = RectangleOmbre(BLACK, base_x, base_y, SCREEN_HEIGHT//13.8, SCREEN_HEIGHT//13.8)
                    carre_ombre.draw()

        if vrai_joueur[compteur_lancers]:
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

                    mx, my = pygame.mouse.get_pos()

                    for case in cases_accessibles:
                        x, y = case
                        point_x = (x * (SCREEN_HEIGHT//13.8)) + (SCREEN_WIDTH // 3.45)
                        point_y = (y * (SCREEN_HEIGHT//13.8)) + (SCREEN_HEIGHT // 9.2)


                        if point_x - (SCREEN_HEIGHT//60) <= mx <= point_x + (SCREEN_HEIGHT//20) and point_y - (SCREEN_HEIGHT//35) <= my <= point_y + (SCREEN_HEIGHT//30):                           
                            nb_argent, nb_potion = verifier_objet_stat(case, potion_positions, potion_images, argent_positions, argent_images, joueurs_choix[compteur_lancers], nb_argent, nb_potion)
                            joueurs_choix[compteur_lancers].position = case

                            if joueur_sur_piege(joueurs_choix[compteur_lancers], piege_positions) :
                                verifier_piege(case, piege_positions, piege_images)
                                joueurs_piegee = True

                            cases_accessibles = []
                            compteur_lancers += 1
                            if compteur_lancers >= len(joueurs_choix):
                                compteur_lancers = 0
                                nombre_tour += 1
                            lancer_fait = False
                            break
                            
                if potion_possible == True :
                    if event.type == pygame.MOUSEMOTION: 
                        mx, my = pygame.mouse.get_pos()
                        bouton_potion.hovered = bouton_potion.est_survol(mx, my)
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if bouton_potion.est_survol(mx, my):
                            joueurs_choix[compteur_lancers].utiliser_potion()
                            potion_possible = False
                        
                        
                if joueurs_piegee == True :
                    for joueur in joueurs_choix:
                        joueur.position = case
                    choix_monstre = random.choice(monstre)
                    monstre.remove(choix_monstre)
                    if combatMonstre.combatMonstre(joueurs_choix, choix_monstre, 0, choix, difficulte, vrai_joueur) == False:
                        time_end = time.time()
                        duree = time_end - time_start
                        running = False
                        statistique.mise_en_stat(joueurs_choix, monstre_battu, False, nombre_tour, choix, int(duree), nb_potion, nb_argent)
                        break   
                    joueurs_piegee = False
                    compteur_lancers = 0
                    monstre_battu += 1
                
                # Dans le shop        
                if ouvrir_shop :
                    shopping = True
                    while shopping :

                        mx, my = pygame.mouse.get_pos()

                        shop_map_image = pygame.image.load('img/map/mapShop.png').convert()
                        shop_map_image = pygame.transform.scale(shop_map_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                        screen.blit(shop_map_image, (0, 0))

                        joueur_image = pygame.image.load(joueurs_choix[compteur_lancers].image).convert_alpha()
                        joueur_image = pygame.transform.scale(joueur_image, (SCREEN_WIDTH//8, SCREEN_WIDTH//8))
                        screen.blit(joueur_image, (SCREEN_WIDTH*0.325, SCREEN_HEIGHT*0.65))

                        bouton_achat_attaque.bouton_actuelle = bouton_achat_attaque.bouton_survol if bouton_achat_attaque.hovered else bouton_achat_attaque.bouton_normale
                        bouton_achat_magie.bouton_actuelle = bouton_achat_magie.bouton_survol if bouton_achat_magie.hovered else bouton_achat_magie.bouton_normale
                        bouton_achat_vitesse.bouton_actuelle = bouton_achat_vitesse.bouton_survol if bouton_achat_vitesse.hovered else bouton_achat_vitesse.bouton_normale
                        bouton_achat_potion.bouton_actuelle = bouton_achat_potion.bouton_survol if bouton_achat_potion.hovered else bouton_achat_potion.bouton_normale

                        bouton_achat_attaque.dessiner(screen)
                        bouton_achat_magie.dessiner(screen)
                        bouton_achat_vitesse.dessiner(screen)
                        bouton_achat_potion.dessiner(screen)

                        draw_text("+ 10 Attaque", SCREEN_WIDTH//35, SCREEN_WIDTH//7, SCREEN_HEIGHT//1.55, BLACK)
                        draw_text("300$", SCREEN_WIDTH//50, SCREEN_WIDTH//6.8, SCREEN_HEIGHT//1.43, BLACK)

                        draw_text("+ 10 Magie", SCREEN_WIDTH//35, SCREEN_WIDTH//2.65, SCREEN_HEIGHT//1.55, BLACK)
                        draw_text("300$", SCREEN_WIDTH//50, SCREEN_WIDTH//2.6, SCREEN_HEIGHT//1.43, BLACK)

                        draw_text("+ 10 Vitesse", SCREEN_WIDTH//35, SCREEN_WIDTH//1.62, SCREEN_HEIGHT//1.55, BLACK)
                        draw_text("200$", SCREEN_WIDTH//50, SCREEN_WIDTH//1.61, SCREEN_HEIGHT//1.43, BLACK)

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
                                bouton_quitter.hovered = bouton_quitter.est_survol(mx, my)
                                bouton_sortir.hovered = bouton_sortir.est_survol(mx, my)

                                if joueurs_choix[compteur_lancers].argent >= 300 :

                                    bouton_achat_attaque.hovered = bouton_achat_attaque.est_survol(mx, my)
                                    bouton_achat_magie.hovered = bouton_achat_magie.est_survol(mx, my)

                                if joueurs_choix[compteur_lancers].argent >= 200 :

                                    bouton_achat_vitesse.hovered = bouton_achat_vitesse.est_survol(mx, my)

                                if joueurs_choix[compteur_lancers].argent >= 100 :
                                    
                                    bouton_achat_potion.hovered = bouton_achat_potion.est_survol(mx, my)

                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if bouton_quitter.est_survol(mx, my) :
                                    shopping = False
                                    running = False


                                if bouton_sortir.est_survol(mx, my) :
                                    shopping = False

                                if joueurs_choix[compteur_lancers].argent >= 300 :
                            
                                    if bouton_achat_attaque.est_survol(mx, my) :
                                        joueurs_choix[compteur_lancers].attaque += 10
                                        joueurs_choix[compteur_lancers].argent -= 300
                                        bouton_achat_attaque.hovered = False

                                    if bouton_achat_magie.est_survol(mx, my) :
                                        joueurs_choix[compteur_lancers].magie += 10
                                        joueurs_choix[compteur_lancers].argent -= 300
                                        bouton_achat_magie.hovered = False

                                if joueurs_choix[compteur_lancers].argent >= 200 :

                                    if bouton_achat_vitesse.est_survol(mx, my) :
                                        joueurs_choix[compteur_lancers].vitesse += 10
                                        joueurs_choix[compteur_lancers].argent -= 200
                                        bouton_achat_vitesse.hovered = False

                                if joueurs_choix[compteur_lancers].argent >= 100 :

                                    if bouton_achat_potion.est_survol(mx, my) :
                                        joueurs_choix[compteur_lancers].potion += 1
                                        joueurs_choix[compteur_lancers].argent -= 100
                                        bouton_achat_potion.hovered = False

                        bouton_quitter.bouton_actuelle = bouton_quitter.bouton_survol if bouton_quitter.hovered else bouton_quitter.bouton_normale
                        bouton_sortir.bouton_actuelle = bouton_sortir.bouton_survol if bouton_sortir.hovered else bouton_sortir.bouton_normale

                        bouton_quitter.dessiner(screen)
                        bouton_sortir.dessiner(screen)

                        pygame.display.flip()
                        pygame.time.Clock().tick(FPS)

                    compteur_lancers += 1
                    if compteur_lancers >= len(joueurs_choix):
                        compteur_lancers = 0
                        nombre_tour += 1
                                
                    lancer_fait = False
                    ouvrir_shop = False
                    
                # Combat final        
                if ouvrir_piege_doree :
                    choix_boss = random.choice(boss)
                    if combatMonstre.combatMonstre(joueurs_choix, choix_boss, 0, choix, difficulte, vrai_joueur):
                        # calcul de la durée total de la partie
                        time_end = time.time()
                        duree = time_end - time_start
                        running = False
                        partie_finie = True
                        monstre_battu = 6
                    else:
                        time_end = time.time()
                        duree = time_end - time_start
                        running = False   
                        partie_finie = False
                        
                        
                    statistique.mise_en_stat(joueurs_choix, monstre_battu, partie_finie, nombre_tour, choix, int(duree), nb_potion, nb_argent)         
                    sys.exit()
                    
            cercle_joueur.draw()

            bouton_quitter.bouton_actuelle = bouton_quitter.bouton_survol if bouton_quitter.hovered else bouton_quitter.bouton_normale

            bouton_quitter.dessiner(screen)

            if joueurs_choix[compteur_lancers].pv != joueurs_choix[compteur_lancers].pv_max :
                bouton_potion.bouton_actuelle = bouton_potion.bouton_survol if bouton_potion.hovered else bouton_potion.bouton_normale

                bouton_potion.dessiner(screen)

            if joueur_sur_shop(joueurs_choix[compteur_lancers], shop_positions) :
                bouton_shop.bouton_actuelle = bouton_shop.bouton_survol if bouton_shop.hovered else bouton_shop.bouton_normale

                bouton_shop.dessiner(screen)
                
            if piege_doree_possible == True and joueur_sur_piege_doree(joueurs_choix[compteur_lancers], piege_doree_positions) :  
                bouton_piege_doree.bouton_actuelle = bouton_piege_doree.bouton_survol if bouton_piege_doree.hovered else bouton_piege_doree.bouton_normale

                bouton_piege_doree.dessiner(screen)

        else:
            if difficulte == "Facile" or difficulte == "Moyen" or difficulte == "Difficile":
                time.sleep(1)
                deplacement_facile(cases_accessibles, joueurs_choix[compteur_lancers])
                case = joueurs_choix[compteur_lancers].position
                
                nb_argent, nb_potion = verifier_objet_stat(case, potion_positions, potion_images, argent_positions, argent_images, joueurs_choix[compteur_lancers], nb_argent, nb_potion)
                joueurs_choix[compteur_lancers].position = case

                if joueur_sur_piege(joueurs_choix[compteur_lancers], piege_positions) :
                    verifier_piege(case, piege_positions, piege_images)
                    joueurs_piegee = True
                    
                if joueur_sur_shop(joueurs_choix[compteur_lancers], shop_positions) :
                    if joueurs_choix[compteur_lancers].argent < 100 :
                        shopping = False
                    else :
                        shopping = True
                        while shopping :
                            if joueurs_choix[compteur_lancers].argent >= 100 :
                                choix_achat = random.randint(1, 4)
                                if choix_achat == 1 and joueurs_choix[compteur_lancers].argent >= 300 :
                                    joueurs_choix[compteur_lancers].attaque += 10
                                    joueurs_choix[compteur_lancers].argent -= 300
                                elif choix_achat == 2 and joueurs_choix[compteur_lancers].argent >= 300:
                                    joueurs_choix[compteur_lancers].magie += 10
                                    joueurs_choix[compteur_lancers].argent -= 300
                                elif choix_achat == 3 and joueurs_choix[compteur_lancers].argent >= 100:
                                    joueurs_choix[compteur_lancers].potion += 1
                                    joueurs_choix[compteur_lancers].argent -= 100
                                elif choix_achat == 4 and joueurs_choix[compteur_lancers].argent >= 200:
                                    joueurs_choix[compteur_lancers].vitesse += 10
                                    joueurs_choix[compteur_lancers].argent -= 200 
                            else :
                                shopping = False
                                
                if joueurs_piegee == True :
                    for joueur in joueurs_choix:
                        joueur.position = case
                    choix_monstre = random.choice(monstre)
                    monstre.remove(choix_monstre)
                    if not combatMonstre.combatMonstre(joueurs_choix, choix_monstre, 0, choix, difficulte, vrai_joueur):
                        time_end = time.time()
                        duree = time_end - time_start
                        running = False
                        statistique.mise_en_stat(joueurs_choix, monstre_battu, False, nombre_tour, choix, int(duree), nb_potion, nb_argent)
                        break
                    joueurs_piegee = False
                    compteur_lancers = 0
                    monstre_battu += 1
                
                if piege_doree_possible == True and joueur_sur_piege_doree(joueurs_choix[compteur_lancers], piege_doree_positions) :
                    choix_boss = random.choice(boss)
                    if combatMonstre.combatMonstre(joueurs_choix, choix_boss, 0, choix, difficulte, vrai_joueur):
                        time_end = time.time()
                        duree = time_end - time_start
                        running = False
                        partie_finie = True
                        monstre_battu = 6
                    else:
                        time_end = time.time()
                        duree = time_end - time_start
                        running = False
                        partie_finie = False
                    statistique.mise_en_stat(joueurs_choix, monstre_battu, partie_finie, nombre_tour, choix, int(duree), nb_potion, nb_argent)
                    
                    
                cases_accessibles = []
                compteur_lancers += 1
                if compteur_lancers >= len(joueurs_choix):
                    compteur_lancers = 0
                    nombre_tour += 1
                lancer_fait = False
                    
                        
                        
        barre_joueur.afficher_barre_vie(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(FPS)

if __name__ == "__main__":

    choix = 2
    graphe = None
    joueurs_choix = []
    joueurs_choix.append(Joueur("Paladin", graphe, (5,10), 100, 100, 16, 12, 10, 3, 100, "img/classe/Paladin.png"))
    joueurs_choix.append(Joueur("Assassin", graphe, (5,10), 90, 90, 20, 10, 15, 3, 100, "img/classe/Assassin.png"))            
    affichageGraphique(choix, graphe, joueurs_choix, "Facile", [False, False]) 