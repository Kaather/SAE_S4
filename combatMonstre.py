import pygame
import sys
from plateau import *
from pygameOutils import *
from labyrinthe import *
from entite import *
from bouton import *
from jeuGraphique import *



def combatMonstre(joueurs_choix, monstre, compteur_lancers, monstre_battu, choix):
    fond = [
        'img/map/desert.png',  
        'img/map/neige.png',
        'img/map/foret.png',
        'img/map/dongeon.png'
    ]
    fond_image = pygame.image.load(fond[choix]).convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    potion_possible = False
    compteur = 5
    while compteur >= 1 :
        
        fond_image2 = pygame.image.load(fond[choix]).convert()
        fond_image2 = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(fond_image2, (0, 0))
        fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
        fond_chargement.fill(WHITE_TR)
        screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))
        draw_text(f"Un joueur est tombé sur un piège !", SCREEN_WIDTH//16, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)
        draw_text(f"Rassemblez vous et préparez vous au combat !", SCREEN_WIDTH//22, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.45, BLACK)
        draw_text(f"{compteur}", SCREEN_WIDTH//13, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.65, BLACK)

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
    bouton_quitter_survole = False
    en_combat = True
    compteur_lancers = 0
    joueur_mort = False
    monstre_mort = False
    while en_combat:         

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
        monstre_image = pygame.image.load(monstre.image).convert_alpha()
        monstre_image = pygame.transform.scale(monstre_image, (SCREEN_WIDTH//8, SCREEN_WIDTH//8))
        screen.blit(monstre_image, (SCREEN_WIDTH*0.65, SCREEN_HEIGHT*0.4))

        # Affichage vie monstre

        draw_text(f"PV : {monstre.pv*len(joueurs_choix)} / {monstre.pv_max*len(joueurs_choix)}", SCREEN_WIDTH//65, SCREEN_WIDTH*0.64, SCREEN_HEIGHT*0.65, BLACK)

        rectangle_vert = pygame.Surface((((SCREEN_WIDTH//8.2) * (monstre.pv) // monstre.pv_max), SCREEN_HEIGHT//30), pygame.SRCALPHA)
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
        if joueurs_choix[compteur_lancers].nom == "Healer":
            draw_text("Soin", SCREEN_WIDTH//35, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.355, BLACK)
        else:
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
                    if joueurs_choix[compteur_lancers].nom == 'Healer':
                        soin(joueurs_choix[compteur_lancers], joueurs_choix)
                        compteur_lancers += 1
                    else:
                        combat(1, joueurs_choix[compteur_lancers], monstre)
                        if comparaison_vitesse(joueurs_choix[compteur_lancers], monstre) :
                            if monstre.pv <= 0 :
                                monstre_battu += 1
                                monstre_mort = True

                            else :
                                monstre_attaque(joueurs_choix[compteur_lancers], monstre)
                                if joueurs_choix[compteur_lancers].pv <= 0 :
                                    joueur_mort = True

                        else :
                            if joueurs_choix[compteur_lancers].pv <= 0 :
                                    joueur_mort = True

                            else :
                                attaque(joueurs_choix[compteur_lancers], monstre)
                                if monstre.pv <= 0 :
                                    monstre_battu += 1
                                    monstre_mort = True

                        if joueur_mort :
                            mort()
                        
                        elif monstre_mort :
                            if monstre.nom == "Dragon":
                                gagne(fond_image)
                                sys.exit()
                            else:
                                compteur_lancers += 1
                                en_combat = False

                        else :
                            compteur_lancers += 1
                            
                        
            # attaque puissante
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                bouton_attaque_puissante_survole = bouton_attaque_puissante.get_rect(center=((SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.585))).collidepoint((mx, my))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_attaque_puissante.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.585)).collidepoint((mx, my)):
                    combat(2, joueurs_choix[compteur_lancers], monstre)
                    if comparaison_vitesse(joueurs_choix[compteur_lancers], monstre) :
                        if monstre.pv <= 0 :
                            monstre_battu += 1
                            monstre_mort = True

                        else :
                            monstre_attaque(joueurs_choix[compteur_lancers], monstre)
                            if joueurs_choix[compteur_lancers].pv <= 0 :
                                joueur_mort = True

                    else :
                        if joueurs_choix[compteur_lancers].pv <= 0 :
                                joueur_mort = True

                        else :
                            attaque_puissante(joueurs_choix[compteur_lancers], monstre)
                            if monstre.pv <= 0 :
                                monstre_battu += 1
                                monstre_mort = True

                    if joueur_mort :
                        mort()
                            
                    elif monstre_mort :
                        if monstre.nom == "Dragon":
                            gagne(fond_image)
                            sys.exit()
                        else:
                            compteur_lancers += 1
                            en_combat = False
                        
                    else :
                        compteur_lancers += 1            
                        
            # attaque magique
            if event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                bouton_attaque_magique_survole = bouton_attaque_magique.get_rect(center=((SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.785))).collidepoint((mx, my))
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_attaque_magique.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.785)).collidepoint((mx, my)):
                    combat(3, joueurs_choix[compteur_lancers], monstre)
                    if comparaison_vitesse(joueurs_choix[compteur_lancers], monstre) :
                        if monstre.pv <= 0 :
                            monstre_battu += 1
                            monstre_mort = True

                        else :
                            monstre_attaque(joueurs_choix[compteur_lancers], monstre)
                            if joueurs_choix[compteur_lancers].pv <= 0 :
                                joueur_mort = True

                    else :
                        if joueurs_choix[compteur_lancers].pv <= 0 :
                                joueur_mort = True

                        else :
                            attaque_magique(joueurs_choix[compteur_lancers], monstre)
                            if monstre.pv <= 0 :
                                monstre_battu += 1
                                monstre_mort = True

                    if joueur_mort :
                        mort()
                            
                    elif monstre_mort :
                        if monstre.nom == "Dragon":
                            gagne(fond_image)
                            sys.exit()
                        else:
                            compteur_lancers += 1
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
        
def mort():
    menu_mort = True
    bouton_menu_survole = False
    
    fond_image2 = pygame.image.load('img/map/mapPiege.png').convert()
    fond_image2 = pygame.transform.scale(fond_image2, (SCREEN_WIDTH, SCREEN_HEIGHT))

    while menu_mort : 
        mx, my = pygame.mouse.get_pos()
        screen.blit(fond_image2, (0, 0))
              
        fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
        fond_chargement.fill(WHITE_TR)
        screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))
        
        draw_text("Vous avez perdu !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)

        bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
        bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
        screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.6)))
        
        draw_text("Quitter", SCREEN_WIDTH//20, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.61) + (SCREEN_HEIGHT//7.5*0.)), BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_menu_survole = bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.6) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_menu.get_rect(center=((SCREEN_WIDTH/2), SCREEN_HEIGHT*(0.6) + (SCREEN_HEIGHT//7.5*0.5))).collidepoint((mx, my)) :
                    joueurs_choix.clear()   
                    supprimer_classes()
                    running = False
                    en_combat = False
                    menu_mort = False
                    
        pygame.display.update()
        clock.tick(FPS)
        
def gagne(fond_image):
    bouton_menu_survole = False
    running2 = True
    while running2 :
        mx, my = pygame.mouse.get_pos()
        screen.blit(fond_image, (0, 0))
        draw_text("Vous avez gagné !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)
        draw_text("Vous avez gagné !", SCREEN_WIDTH//10, SCREEN_WIDTH*0.5, SCREEN_HEIGHT*0.2, BLACK)
        bouton_menu = pygame.Surface((SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5), pygame.SRCALPHA)
        bouton_menu.fill(BROWN_TR if not bouton_menu_survole else BROWN)
        screen.blit(bouton_menu, ((SCREEN_WIDTH/2) - (SCREEN_WIDTH//4/2), SCREEN_HEIGHT*(0.8)))
        draw_text("Quitter", SCREEN_WIDTH//20, SCREEN_WIDTH//2, (SCREEN_HEIGHT*(0.775) + (SCREEN_HEIGHT//7.5*0.3)), BLACK)
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
    
        
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    joueurs_choix = []
    graphe = None
    joueurs_choix.append(Joueur("Healer", graphe, (5,10), 80, 80, 5, 30, 8, 5, 100, "img/classe/Healer.png"))
    joueurs_choix.append(Joueur("Paladin", graphe, (5,10), 100, 50, 5, 30, 8, 5, 100, "img/classe/Paladin.png"))
    monstre1 = Monstre("Dragon", 50, 50, 10, 5, 15, "img/ennemi/loup.png")

    while running :
        combatMonstre(joueurs_choix, monstre1, 0, 0, 2)
        running = False
        pygame.quit()
        sys.exit()