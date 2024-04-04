import pygame
import sys
from plateau import *
from pygameOutils import *
from labyrinthe import *
from entite import *
from bouton import *
from ia_combat import *

clock = pygame.time.Clock()
FPS = 60

def combatMonstre(joueurs_choix, monstre, compteur_lancers, choix, difficulte, vrai_joueur):
    valeur_avant_combat = []
    # stock les valeurs d'attaques, de magie et de vitesse de chaque joueur avant le combat
    for joueur in joueurs_choix:
        valeur_avant_combat.append([joueur.attaque, joueur.magie, joueur.vitesse])
    fond = [
        'img/map/desert.png',  
        'img/map/neige.png',
        'img/map/foret.png',
        'img/map/donjon.png'
    ]
    fond_image = pygame.image.load(fond[choix]).convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    potion_possible = False
    
    compteur(fond[choix], fond_image)

    bouton_potion_survole = False
    bouton_attaque_survole = False
    bouton_attaque_puissante_survole = False
    bouton_attaque_magique_survole = False
    bouton_quitter_survole = False
    en_combat = True
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
        if joueurs_choix[compteur_lancers].nom == "Healer":
            draw_text("Boost", SCREEN_WIDTH//37, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.555, BLACK)
        else:
            draw_text("Attaque puissante", SCREEN_WIDTH//37, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.555, BLACK)

        bouton_attaque_magique = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
        bouton_attaque_magique.fill(GREY_TR if not bouton_attaque_magique_survole else GREY)
        screen.blit(bouton_attaque_magique, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.755))
        if joueurs_choix[compteur_lancers].nom == "Healer":
            draw_text("Malus", SCREEN_WIDTH//37, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.755, BLACK)
        else:
            draw_text("Attaque magique", SCREEN_WIDTH//37, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.755, BLACK)

        # Affichage bouton utiliser potion (seulement si on a pas tout ses points de vie)
        if joueurs_choix[compteur_lancers].pv != joueurs_choix[compteur_lancers].pv_max :
            bouton_potion = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
            bouton_potion.fill(GREY_TR if not bouton_potion_survole else GREY)
            screen.blit(bouton_potion, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.155))
            draw_text("Boire potion", SCREEN_WIDTH//35, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.155, BLACK)
            potion_possible = True
            
        if vrai_joueur[compteur_lancers]:

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
                            # Met un filtre blanc flou
                            fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
                            fond_chargement.fill(WHITE_TR)
                            screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))

                            
                            # Calcul des positions initiales
                            bouton_width = SCREEN_WIDTH * 0.20
                            bouton_height = SCREEN_HEIGHT * 0.07
                            bouton_spacing = bouton_width * 0.25 # Espace entre les boutons
                            bouton_start_x = (SCREEN_WIDTH - (len(joueurs_choix) * bouton_spacing)) // 2
                            bouton_y = (SCREEN_HEIGHT - bouton_height) / 2

                            # Calcul de la largeur totale des boutons
                            total_button_width = len(joueurs_choix) * (bouton_width + bouton_spacing) - bouton_spacing

                            # Calcul de la position de départ horizontale
                            bouton_start_x = (SCREEN_WIDTH - total_button_width) // 2

                            # Affichage des boutons
                            for i in range(len(joueurs_choix)):
                                bouton_joueur = pygame.Surface((bouton_width, bouton_height), pygame.SRCALPHA)
                                bouton_joueur.fill(GREY_TR)
                                bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                screen.blit(bouton_joueur, (bouton_x, bouton_y))
                                draw_text(f"Joueur {i+1}", SCREEN_WIDTH//35, bouton_x + bouton_width // 2, bouton_y, BLACK)
                                
                                # affiche l'image du joueur au dessus du bouton
                                joueur_image = pygame.image.load(joueurs_choix[i].image).convert_alpha()
                                joueur_image = pygame.transform.scale(joueur_image, (SCREEN_WIDTH//10, SCREEN_WIDTH//10))
                                screen.blit(joueur_image, (bouton_x + bouton_spacing, bouton_y - SCREEN_HEIGHT*0.2))
                                
                                
                            # Attente de la sélection du joueur
                            soinFait = True
                            while soinFait:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mx, my = pygame.mouse.get_pos()
                                        for i in range(len(joueurs_choix)):
                                            bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                            bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)
                                            if bouton_rect.collidepoint((mx, my)):
                                                soin(joueurs_choix[i])
                                                compteur_lancers += 1
                                                soinFait = False
                                                
                                    for i in range(len(joueurs_choix)):
                                        bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                        bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)

                                        # Vérifier si la souris survole le bouton
                                        if bouton_rect.collidepoint(pygame.mouse.get_pos()):
                                            pygame.draw.rect(screen, (200, 200, 200), bouton_rect)  # Changer la couleur du bouton en hover
                                        else:
                                            pygame.draw.rect(screen, (150, 150, 150), bouton_rect)  # Couleur par défaut

                                        draw_text(f"Joueur {i+1}", SCREEN_WIDTH // 35, bouton_x + bouton_width // 2, bouton_y, BLACK)  
                                        draw_text("Choisissez un joueur à soigner", SCREEN_WIDTH // 35, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.7, BLACK)                                 
                                    

                                pygame.display.update()
                                clock.tick(FPS)                         
                        
                                        
                        else:
                            combat(1, joueurs_choix[compteur_lancers], monstre)
                            if comparaison_vitesse(joueurs_choix[compteur_lancers], monstre) :
                                if monstre.pv <= 0 :
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
                                        monstre_mort = True

                            if joueur_mort :
                                mort()
                                return False
                            
                            elif monstre_mort :
                                if monstre.nom == "Dragon" or monstre.nom == "Aguni" or monstre.nom == "Mort" or monstre.nom == "Gergoth" or monstre.nom == "Ange Déchu":
                                    gagne(fond_image)
                                    return True
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
                        if joueurs_choix[compteur_lancers].nom == 'Healer':
                            fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
                            fond_chargement.fill(WHITE_TR)
                            screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))
                            bonus_options = ['Attaque', 'Vitesse', 'Magie']

                            # Calcul des positions initiales
                            bouton_width = SCREEN_WIDTH * 0.20
                            bouton_height = SCREEN_HEIGHT * 0.07
                            bouton_spacing = bouton_width * 0.25 # Espace entre les boutons
                            bouton_start_x = (SCREEN_WIDTH - (len(joueurs_choix) * bouton_spacing)) // 2
                            bouton_y = (SCREEN_HEIGHT - bouton_height) / 2

                            # Calcul de la largeur totale des boutons
                            total_button_width = len(bonus_options) * (bouton_width + bouton_spacing) - bouton_spacing

                            # Calcul de la position de départ horizontale
                            bouton_start_x = (SCREEN_WIDTH - total_button_width) // 2

                            # Affichage des boutons pour les choix de bonus
                            for i, option in enumerate(bonus_options):
                                bouton_bonus = pygame.Surface((bouton_width, bouton_height), pygame.SRCALPHA)
                                bouton_bonus.fill(GREY_TR)
                                bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                screen.blit(bouton_bonus, (bouton_x, bouton_y))
                                draw_text(option, SCREEN_WIDTH//35, bouton_x + bouton_width // 2, bouton_y, BLACK)

                            # Attente de la sélection du bonus
                            choixBonusFait = False
                            while not choixBonusFait:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mx, my = pygame.mouse.get_pos()
                                        for i in range(len(bonus_options)):
                                            bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                            bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)
                                            if bouton_rect.collidepoint((mx, my)):
                                                bonus = bonus_options[i]
                                                choixBonusFait = True

                                    for i in range(len(bonus_options)):
                                        bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                        bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)

                                        # Vérifier si la souris survole le bouton
                                        if bouton_rect.collidepoint(pygame.mouse.get_pos()):
                                            pygame.draw.rect(screen, (200, 200, 200), bouton_rect)  # Changer la couleur du bouton en hover
                                        else:
                                            pygame.draw.rect(screen, (150, 150, 150), bouton_rect)  # Couleur par défaut

                                        draw_text(bonus_options[i], SCREEN_WIDTH // 35, bouton_x + bouton_width // 2, bouton_y, BLACK)  
                                        draw_text("Choisissez un bonus à appliquer", SCREEN_WIDTH // 35, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.7, BLACK)                                 

                                pygame.display.update()
                                clock.tick(FPS) 
                            
                            # Choisir le joueurs à booster
                            # Met un filtre blanc flou
                            fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
                            fond_chargement.fill(WHITE_TR)
                            screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))

                            
                            # Calcul des positions initiales
                            bouton_width = SCREEN_WIDTH * 0.20
                            bouton_height = SCREEN_HEIGHT * 0.07
                            bouton_spacing = bouton_width * 0.25 # Espace entre les boutons
                            bouton_start_x = (SCREEN_WIDTH - (len(joueurs_choix) * bouton_spacing)) // 2
                            bouton_y = (SCREEN_HEIGHT - bouton_height) / 2

                            # Calcul de la largeur totale des boutons
                            total_button_width = len(joueurs_choix) * (bouton_width + bouton_spacing) - bouton_spacing

                            # Calcul de la position de départ horizontale
                            bouton_start_x = (SCREEN_WIDTH - total_button_width) // 2

                            # Affichage des boutons
                            for i in range(len(joueurs_choix)):
                                bouton_joueur = pygame.Surface((bouton_width, bouton_height), pygame.SRCALPHA)
                                bouton_joueur.fill(GREY_TR)
                                bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                screen.blit(bouton_joueur, (bouton_x, bouton_y))
                                draw_text(f"Joueur {i+1}", SCREEN_WIDTH//35, bouton_x + bouton_width // 2, bouton_y, BLACK)
                                
                                # affiche l'image du joueur au dessus du bouton
                                joueur_image = pygame.image.load(joueurs_choix[i].image).convert_alpha()
                                joueur_image = pygame.transform.scale(joueur_image, (SCREEN_WIDTH//10, SCREEN_WIDTH//10))
                                screen.blit(joueur_image, (bouton_x + bouton_spacing, bouton_y - SCREEN_HEIGHT*0.2))
                                
                                
                            # Attente de la sélection du joueur
                            joueurChoisi = True
                            while joueurChoisi:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mx, my = pygame.mouse.get_pos()
                                        for i in range(len(joueurs_choix)):
                                            bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                            bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)
                                            if bouton_rect.collidepoint((mx, my)):
                                                appliquer_bonus(joueurs_choix[i], bonus)
                                                compteur_lancers += 1
                                                joueurChoisi = False
                                                
                                    for i in range(len(joueurs_choix)):
                                        bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                        bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)

                                        # Vérifier si la souris survole le bouton
                                        if bouton_rect.collidepoint(pygame.mouse.get_pos()):
                                            pygame.draw.rect(screen, (200, 200, 200), bouton_rect)  # Changer la couleur du bouton en hover
                                        else:
                                            pygame.draw.rect(screen, (150, 150, 150), bouton_rect)  # Couleur par défaut

                                        draw_text(f"Joueur {i+1}", SCREEN_WIDTH // 35, bouton_x + bouton_width // 2, bouton_y, BLACK)  
                                        draw_text("Choisissez un joueur à booster", SCREEN_WIDTH // 35, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.7, BLACK)  
                                        
                                pygame.display.update()
                                clock.tick(FPS)              
                                
                        else:
                            combat(2, joueurs_choix[compteur_lancers], monstre)
                            if comparaison_vitesse(joueurs_choix[compteur_lancers], monstre) :
                                if monstre.pv <= 0 :
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
                                        monstre_mort = True

                            if joueur_mort :
                                return False
                                    
                            elif monstre_mort :
                                if monstre.nom == "Dragon" or monstre.nom == "Aguni" or monstre.nom == "Mort" or monstre.nom == "Gergoth" or monstre.nom == "Ange Déchu":
                                    gagne(fond_image)
                                    return True
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
                        if joueurs_choix[compteur_lancers].nom == 'Healer':
                            fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
                            fond_chargement.fill(WHITE_TR)
                            screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))
                            bonus_options = ['Attaque', 'Vitesse', 'Magie']

                            # Calcul des positions initiales
                            bouton_width = SCREEN_WIDTH * 0.20
                            bouton_height = SCREEN_HEIGHT * 0.07
                            bouton_spacing = bouton_width * 0.25 # Espace entre les boutons
                            bouton_start_x = (SCREEN_WIDTH - (len(joueurs_choix) * bouton_spacing)) // 2
                            bouton_y = (SCREEN_HEIGHT - bouton_height) / 2

                            # Calcul de la largeur totale des boutons
                            total_button_width = len(bonus_options) * (bouton_width + bouton_spacing) - bouton_spacing

                            # Calcul de la position de départ horizontale
                            bouton_start_x = (SCREEN_WIDTH - total_button_width) // 2

                            # Affichage des boutons pour les choix de bonus
                            for i, option in enumerate(bonus_options):
                                bouton_bonus = pygame.Surface((bouton_width, bouton_height), pygame.SRCALPHA)
                                bouton_bonus.fill(GREY_TR)
                                bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                screen.blit(bouton_bonus, (bouton_x, bouton_y))
                                draw_text(option, SCREEN_WIDTH//35, bouton_x + bouton_width // 2, bouton_y, BLACK)

                            # Attente de la sélection du bonus
                            choixBonusFait = False
                            while not choixBonusFait:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mx, my = pygame.mouse.get_pos()
                                        for i in range(len(bonus_options)):
                                            bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                            bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)
                                            if bouton_rect.collidepoint((mx, my)):
                                                appliquer_malus(monstre, bonus_options[i])
                                                choixBonusFait = True
                                                compteur_lancers += 1

                                    for i in range(len(bonus_options)):
                                        bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                        bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)

                                        # Vérifier si la souris survole le bouton
                                        if bouton_rect.collidepoint(pygame.mouse.get_pos()):
                                            pygame.draw.rect(screen, (200, 200, 200), bouton_rect)  # Changer la couleur du bouton en hover
                                        else:
                                            pygame.draw.rect(screen, (150, 150, 150), bouton_rect)  # Couleur par défaut

                                        draw_text(bonus_options[i], SCREEN_WIDTH // 35, bouton_x + bouton_width // 2, bouton_y, BLACK)  
                                        draw_text("Choisissez un malus à appliquer", SCREEN_WIDTH // 35, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.7, BLACK)                                 

                                pygame.display.update()
                                clock.tick(FPS) 
                            
                        else:
                            combat(3, joueurs_choix[compteur_lancers], monstre)
                            if comparaison_vitesse(joueurs_choix[compteur_lancers], monstre) :
                                if monstre.pv <= 0 :
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
                                        monstre_mort = True

                            if joueur_mort :
                                mort()
                                return False
                                    
                            elif monstre_mort :
                                if monstre.nom == "Dragon" or monstre.nom == "Aguni" or monstre.nom == "Mort" or monstre.nom == "Gergoth" or monstre.nom == "Ange Déchu":
                                    gagne(fond_image)
                                    return True
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
                        en_combat = False
        
        else:
            time.sleep(2)
            if difficulte == "Facile" or difficulte == "Moyen" or difficulte == "Difficile":
                combat_facile(joueurs_choix, compteur_lancers, monstre) 
                                
                if joueurs_choix[compteur_lancers].pv <= 0 :
                    return False
                
                if monstre.pv <= 0 :
                    return True
                
                  
                compteur_lancers += 1  
                
                       

        pygame.display.update()
        clock.tick(FPS)
        
    if compteur_lancers >= len(joueurs_choix):
        compteur_lancers = 0
                
    # remet la valeur par defaut pour l'attaque, la magie et la vitesse
    for i, joueur in enumerate(joueurs_choix):
        joueur.attaque = valeur_avant_combat[i][0]
        joueur.magie = valeur_avant_combat[i][1]
        joueur.vitesse = valeur_avant_combat[i][2]

    return True
        
def combatMonstreReseau(numero, socket, joueurs_choix, monstre, compteur_lancers, choix):
    valeur_avant_combat = []
    for joueur in joueurs_choix:
        valeur_avant_combat.append([joueur.attaque, joueur.magie, joueur.vitesse])
        
    fond = [
        'img/map/desert.png',  
        'img/map/neige.png',
        'img/map/foret.png',
        'img/map/dongeon.png'
    ]
    fond_image = pygame.image.load(fond[choix]).convert()
    fond_image = pygame.transform.scale(fond_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    potion_possible = False
    
    compteur(fond[choix], fond_image)
    
    bouton_5_survole = False    
    bouton_potion_survole = False
    bouton_attaque_survole = False
    bouton_attaque_puissante_survole = False
    bouton_attaque_magique_survole = False
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

        bouton_5 = pygame.Surface((SCREEN_WIDTH//12.4, SCREEN_HEIGHT//22), pygame.SRCALPHA)
        bouton_5.fill(TRANSPARENT if not bouton_5_survole else BROWN)
        screen.blit(bouton_5, ((SCREEN_WIDTH*(0.92), SCREEN_HEIGHT*(0.001))))
        draw_text("Quitter", SCREEN_WIDTH//43, SCREEN_WIDTH*0.96, SCREEN_HEIGHT//(-120), BLACK)
        
        # Affichage du monstre monstre utilise la variable monstre
        monstre_image = pygame.image.load(monstre.image).convert_alpha()
        monstre_image = pygame.transform.scale(monstre_image, (SCREEN_WIDTH//8, SCREEN_WIDTH//8))
        screen.blit(monstre_image, (SCREEN_WIDTH*0.65, SCREEN_HEIGHT*0.4))
        
        # Affichage vie monstre
        draw_text(f"PV : {monstre.pv} / {monstre.pv_max}", 20, SCREEN_WIDTH*0.64, SCREEN_HEIGHT*0.65, BLACK)          
        
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
        if joueurs_choix[compteur_lancers].nom == 'Healer':
            draw_text("Soigner", SCREEN_WIDTH//35, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.355, BLACK)
        else:
            draw_text("Attaque", SCREEN_WIDTH//35, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.355, BLACK)

        bouton_attaque_puissante = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
        bouton_attaque_puissante.fill(GREY_TR if not bouton_attaque_puissante_survole else GREY)
        screen.blit(bouton_attaque_puissante, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.555))
        if joueurs_choix[compteur_lancers].nom == 'Healer':
            draw_text("Booster", SCREEN_WIDTH//37, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.555, BLACK)
        else:
            draw_text("Attaque puissante", SCREEN_WIDTH//37, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.555, BLACK)

        bouton_attaque_magique = pygame.Surface((SCREEN_WIDTH*0.27, SCREEN_HEIGHT*0.07), pygame.SRCALPHA)
        bouton_attaque_magique.fill(GREY_TR if not bouton_attaque_magique_survole else GREY)
        screen.blit(bouton_attaque_magique, ((SCREEN_WIDTH*0.76), SCREEN_HEIGHT*0.755))
        if joueurs_choix[compteur_lancers].nom == 'Healer':
            draw_text("Malus", SCREEN_WIDTH//35, SCREEN_WIDTH*0.88, SCREEN_HEIGHT*0.755, BLACK)
        else:
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
                    
                # attaque normale
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_attaque.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.385)).collidepoint((mx, my)):
                        if joueurs_choix[compteur_lancers].nom == 'Healer':
                            # Met un filtre blanc flou
                            fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
                            fond_chargement.fill(WHITE_TR)
                            screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))

                            
                            # Calcul des positions initiales
                            bouton_width = SCREEN_WIDTH * 0.20
                            bouton_height = SCREEN_HEIGHT * 0.07
                            bouton_spacing = bouton_width * 0.25 # Espace entre les boutons
                            bouton_start_x = (SCREEN_WIDTH - (len(joueurs_choix) * bouton_spacing)) // 2
                            bouton_y = (SCREEN_HEIGHT - bouton_height) / 2

                            # Calcul de la largeur totale des boutons
                            total_button_width = len(joueurs_choix) * (bouton_width + bouton_spacing) - bouton_spacing

                            # Calcul de la position de départ horizontale
                            bouton_start_x = (SCREEN_WIDTH - total_button_width) // 2

                            # Affichage des boutons
                            for i in range(len(joueurs_choix)):
                                bouton_joueur = pygame.Surface((bouton_width, bouton_height), pygame.SRCALPHA)
                                bouton_joueur.fill(GREY_TR)
                                bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                screen.blit(bouton_joueur, (bouton_x, bouton_y))
                                draw_text(f"Joueur {i+1}", SCREEN_WIDTH//35, bouton_x + bouton_width // 2, bouton_y, BLACK)
                                
                                # affiche l'image du joueur au dessus du bouton
                                joueur_image = pygame.image.load(joueurs_choix[i].image).convert_alpha()
                                joueur_image = pygame.transform.scale(joueur_image, (SCREEN_WIDTH//10, SCREEN_WIDTH//10))
                                screen.blit(joueur_image, (bouton_x + bouton_spacing, bouton_y - SCREEN_HEIGHT*0.2))
                                
                                
                            # Attente de la sélection du joueur
                            soinFait = True
                            while soinFait:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mx, my = pygame.mouse.get_pos()
                                        for i in range(len(joueurs_choix)):
                                            bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                            bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)
                                            if bouton_rect.collidepoint((mx, my)):
                                                soinFait = False
                                                # envoie des données au serveur
                                                data = {}
                                                data["healer"] = joueurs_choix[compteur_lancers].nom
                                                data["choix"] = "soin"
                                                data["joueur_choisi"] = i
                                                compteur_lancers += 1
                                                data["compteur_lancers"] = compteur_lancers
                                                socket.send(str.encode(str(data)))
                                                
                                                
                                    for i in range(len(joueurs_choix)):
                                        bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                        bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)

                                        # Vérifier si la souris survole le bouton
                                        if bouton_rect.collidepoint(pygame.mouse.get_pos()):
                                            pygame.draw.rect(screen, (200, 200, 200), bouton_rect)  # Changer la couleur du bouton en hover
                                        else:
                                            pygame.draw.rect(screen, (150, 150, 150), bouton_rect)  # Couleur par défaut

                                        draw_text(f"Joueur {i+1}", SCREEN_WIDTH // 35, bouton_x + bouton_width // 2, bouton_y, BLACK)  
                                        draw_text("Choisissez un joueur à soigner", SCREEN_WIDTH // 35, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.7, BLACK)                                 
                                    

                                pygame.display.update()
                                clock.tick(FPS)  
                            soin(joueurs_choix[i])  
                                       
                        else:   
                            combat(1, joueurs_choix[compteur_lancers], monstre)
                            if comparaison_vitesse(joueurs_choix[compteur_lancers], monstre) :
                                if monstre.pv <= 0 :
                                    monstre_mort = True
                                    data["monstre_mort"] = monstre_mort
                                    data["joueur_mort"] = joueur_mort
                                    socket.send(str.encode(str(data)))
                                    
                                else :
                                    monstre_attaque(joueurs_choix[compteur_lancers], monstre)
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
                                    attaque(joueurs_choix[compteur_lancers], monstre)
                                    if monstre.pv <= 0 :
                                        monstre_mort = True
                                        data["monstre_mort"] = monstre_mort
                                        data["joueur_mort"] = joueur_mort
                                        socket.send(str.encode(str(data)))

                            if joueur_mort :
                                mort()
                                return False                         
                            
                            elif monstre_mort :
                                if monstre.nom == "Dragon" or monstre.nom == "Aguni" or monstre.nom == "Mort" or monstre.nom == "Gergoth" or monstre.nom == "Ange Déchu":
                                    gagne(fond_image)
                                else:
                                    en_combat = False  
                                    for i, joueur in enumerate(joueurs_choix):
                                        joueur.attaque = valeur_avant_combat[i][0]
                                        joueur.magie = valeur_avant_combat[i][1]
                                        joueur.vitesse = valeur_avant_combat[i][2]
                                return True
                            
                # attaque puissante   
                if event.type == pygame.MOUSEMOTION:
                    mx, my = pygame.mouse.get_pos()
                    bouton_attaque_puissante_survole = bouton_attaque_puissante.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.585)).collidepoint((mx, my))                               
                                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_attaque_puissante.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.585)).collidepoint((mx, my)):
                        if joueurs_choix[compteur_lancers].nom == 'Healer':
                            fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
                            fond_chargement.fill(WHITE_TR)
                            screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))
                            bonus_options = ['Attaque', 'Vitesse', 'Magie']

                            # Calcul des positions initiales
                            bouton_width = SCREEN_WIDTH * 0.20
                            bouton_height = SCREEN_HEIGHT * 0.07
                            bouton_spacing = bouton_width * 0.25 # Espace entre les boutons
                            bouton_start_x = (SCREEN_WIDTH - (len(joueurs_choix) * bouton_spacing)) // 2
                            bouton_y = (SCREEN_HEIGHT - bouton_height) / 2

                            # Calcul de la largeur totale des boutons
                            total_button_width = len(bonus_options) * (bouton_width + bouton_spacing) - bouton_spacing

                            # Calcul de la position de départ horizontale
                            bouton_start_x = (SCREEN_WIDTH - total_button_width) // 2

                            # Affichage des boutons pour les choix de bonus
                            for i, option in enumerate(bonus_options):
                                bouton_bonus = pygame.Surface((bouton_width, bouton_height), pygame.SRCALPHA)
                                bouton_bonus.fill(GREY_TR)
                                bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                screen.blit(bouton_bonus, (bouton_x, bouton_y))
                                draw_text(option, SCREEN_WIDTH//35, bouton_x + bouton_width // 2, bouton_y, BLACK)

                            # Attente de la sélection du bonus
                            choixBonusFait = False
                            while not choixBonusFait:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mx, my = pygame.mouse.get_pos()
                                        for i in range(len(bonus_options)):
                                            bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                            bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)
                                            if bouton_rect.collidepoint((mx, my)):
                                                bonus = bonus_options[i]
                                                choixBonusFait = True

                                    for i in range(len(bonus_options)):
                                        bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                        bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)

                                        # Vérifier si la souris survole le bouton
                                        if bouton_rect.collidepoint(pygame.mouse.get_pos()):
                                            pygame.draw.rect(screen, (200, 200, 200), bouton_rect)  # Changer la couleur du bouton en hover
                                        else:
                                            pygame.draw.rect(screen, (150, 150, 150), bouton_rect)  # Couleur par défaut

                                        draw_text(bonus_options[i], SCREEN_WIDTH // 35, bouton_x + bouton_width // 2, bouton_y, BLACK)  
                                        draw_text("Choisissez un bonus à appliquer", SCREEN_WIDTH // 35, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.7, BLACK)                                 

                                pygame.display.update()
                                clock.tick(FPS) 
                            
                            # Choisir le joueurs à booster
                            # Met un filtre blanc flou
                            fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
                            fond_chargement.fill(WHITE_TR)
                            screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))

                            
                            # Calcul des positions initiales
                            bouton_width = SCREEN_WIDTH * 0.20
                            bouton_height = SCREEN_HEIGHT * 0.07
                            bouton_spacing = bouton_width * 0.25 # Espace entre les boutons
                            bouton_start_x = (SCREEN_WIDTH - (len(joueurs_choix) * bouton_spacing)) // 2
                            bouton_y = (SCREEN_HEIGHT - bouton_height) / 2

                            # Calcul de la largeur totale des boutons
                            total_button_width = len(joueurs_choix) * (bouton_width + bouton_spacing) - bouton_spacing

                            # Calcul de la position de départ horizontale
                            bouton_start_x = (SCREEN_WIDTH - total_button_width) // 2

                            # Affichage des boutons
                            for i in range(len(joueurs_choix)):
                                bouton_joueur = pygame.Surface((bouton_width, bouton_height), pygame.SRCALPHA)
                                bouton_joueur.fill(GREY_TR)
                                bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                screen.blit(bouton_joueur, (bouton_x, bouton_y))
                                draw_text(f"Joueur {i+1}", SCREEN_WIDTH//35, bouton_x + bouton_width // 2, bouton_y, BLACK)
                                
                                # affiche l'image du joueur au dessus du bouton
                                joueur_image = pygame.image.load(joueurs_choix[i].image).convert_alpha()
                                joueur_image = pygame.transform.scale(joueur_image, (SCREEN_WIDTH//10, SCREEN_WIDTH//10))
                                screen.blit(joueur_image, (bouton_x + bouton_spacing, bouton_y - SCREEN_HEIGHT*0.2))
                                
                                
                            # Attente de la sélection du joueur
                            joueurChoisi = True
                            while joueurChoisi:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mx, my = pygame.mouse.get_pos()
                                        for i in range(len(joueurs_choix)):
                                            bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                            bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)
                                            if bouton_rect.collidepoint((mx, my)):
                                                
                                                joueurChoisi = False
                                                # envoie en réseau
                                                data = {}
                                                data["bonus"] = bonus
                                                data["choix"] = "boost"
                                                data["joueur_choisi"] = i
                                                compteur_lancers += 1
                                                data["compteur_lancers"] = compteur_lancers
                                                socket.send(str.encode(str(data)))
                                                
                                                
                                                
                                    for i in range(len(joueurs_choix)):
                                        bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                        bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)

                                        # Vérifier si la souris survole le bouton
                                        if bouton_rect.collidepoint(pygame.mouse.get_pos()):
                                            pygame.draw.rect(screen, (200, 200, 200), bouton_rect)  # Changer la couleur du bouton en hover
                                        else:
                                            pygame.draw.rect(screen, (150, 150, 150), bouton_rect)  # Couleur par défaut

                                        draw_text(f"Joueur {i+1}", SCREEN_WIDTH // 35, bouton_x + bouton_width // 2, bouton_y, BLACK)  
                                        draw_text("Choisissez un joueur à booster", SCREEN_WIDTH // 35, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.7, BLACK)  
                                        
                                pygame.display.update()
                                clock.tick(FPS) 
                            appliquer_bonus(joueurs_choix[i], bonus)
                                    
                        else:
                            combat(1, joueurs_choix[compteur_lancers], monstre)
                            if comparaison_vitesse(joueurs_choix[compteur_lancers], monstre) :
                                if monstre.pv <= 0 :
                                    monstre_mort = True
                                    # envoie monstre mort
                                    data["monstre_mort"] = monstre_mort
                                    data["joueur_mort"] = joueur_mort
                                    socket.send(str.encode(str(data)))
                                    
                                else :
                                    monstre_attaque(joueurs_choix[compteur_lancers], monstre)
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
                                    attaque_puissante(joueurs_choix[compteur_lancers], monstre)
                                    if monstre.pv <= 0 :
                                        monstre_mort = True
                                        data["monstre_mort"] = monstre_mort
                                        data["joueur_mort"] = joueur_mort
                                        socket.send(str.encode(str(data)))

                            if joueur_mort :
                                mort()
                                return False
                                
                            elif monstre_mort :
                                if monstre.nom == "Dragon" or monstre.nom == "Aguni" or monstre.nom == "Mort" or monstre.nom == "Gergoth" or monstre.nom == "Ange Déchu":
                                    gagne(fond_image)
                                else:
                                    en_combat = False  
                                    for i, joueur in enumerate(joueurs_choix):
                                        joueur.attaque = valeur_avant_combat[i][0]
                                        joueur.magie = valeur_avant_combat[i][1]
                                        joueur.vitesse = valeur_avant_combat[i][2]    
                                return True               


                if event.type == pygame.MOUSEMOTION: 
                    mx, my = pygame.mouse.get_pos()
                    bouton_5_survole = bouton_5.get_rect(center=((SCREEN_WIDTH*0.965), SCREEN_HEIGHT*(0.015))).collidepoint((mx, my))
                    
                # attaque magique
                if event.type == pygame.MOUSEMOTION:
                    mx, my = pygame.mouse.get_pos()
                    bouton_attaque_magique_survole = bouton_attaque_magique.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.785)).collidepoint((mx, my))
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_attaque_magique.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.785)).collidepoint((mx, my)):
                        if joueurs_choix[compteur_lancers].nom == 'Healer':
                            fond_chargement = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT*0.61), pygame.SRCALPHA)
                            fond_chargement.fill(WHITE_TR)
                            screen.blit(fond_chargement, ((0), SCREEN_HEIGHT*0.2))
                            bonus_options = ['Attaque', 'Vitesse', 'Magie']

                            # Calcul des positions initiales
                            bouton_width = SCREEN_WIDTH * 0.20
                            bouton_height = SCREEN_HEIGHT * 0.07
                            bouton_spacing = bouton_width * 0.25 # Espace entre les boutons
                            bouton_start_x = (SCREEN_WIDTH - (len(joueurs_choix) * bouton_spacing)) // 2
                            bouton_y = (SCREEN_HEIGHT - bouton_height) / 2

                            # Calcul de la largeur totale des boutons
                            total_button_width = len(bonus_options) * (bouton_width + bouton_spacing) - bouton_spacing

                            # Calcul de la position de départ horizontale
                            bouton_start_x = (SCREEN_WIDTH - total_button_width) // 2

                            # Affichage des boutons pour les choix de bonus
                            for i, option in enumerate(bonus_options):
                                bouton_bonus = pygame.Surface((bouton_width, bouton_height), pygame.SRCALPHA)
                                bouton_bonus.fill(GREY_TR)
                                bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                screen.blit(bouton_bonus, (bouton_x, bouton_y))
                                draw_text(option, SCREEN_WIDTH//35, bouton_x + bouton_width // 2, bouton_y, BLACK)

                            # Attente de la sélection du bonus
                            choixBonusFait = False
                            while not choixBonusFait:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        mx, my = pygame.mouse.get_pos()
                                        for i in range(len(bonus_options)):
                                            bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                            bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)
                                            if bouton_rect.collidepoint((mx, my)):
                                                choixBonusFait = True
                                                # envoie en réseau
                                                data = {}
                                                data["Healer"] = joueurs_choix[compteur_lancers].nom
                                                data["malus"] = bonus_options[i]
                                                data["choix"] = "malus"
                                                compteur_lancers += 1
                                                data["compteur_lancers"] = compteur_lancers
                                                socket.send(str.encode(str(data)))
                                                
                                    for i in range(len(bonus_options)):
                                        bouton_x = bouton_start_x + i * (bouton_width + bouton_spacing)
                                        bouton_rect = pygame.Rect(bouton_x, bouton_y, bouton_width, bouton_height)

                                        # Vérifier si la souris survole le bouton
                                        if bouton_rect.collidepoint(pygame.mouse.get_pos()):
                                            pygame.draw.rect(screen, (200, 200, 200), bouton_rect)  # Changer la couleur du bouton en hover
                                        else:
                                            pygame.draw.rect(screen, (150, 150, 150), bouton_rect)  # Couleur par défaut

                                        draw_text(bonus_options[i], SCREEN_WIDTH // 35, bouton_x + bouton_width // 2, bouton_y, BLACK)  
                                        draw_text("Choisissez un malus à appliquer", SCREEN_WIDTH // 35, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 0.7, BLACK)                                 

                                pygame.display.update()
                                clock.tick(FPS) 
                            appliquer_malus(monstre, bonus_options[i])

                        else:
                            combat(1, joueurs_choix[compteur_lancers], monstre)
                            if comparaison_vitesse(joueurs_choix[compteur_lancers], monstre) :
                                if monstre.pv <= 0 :
                                    monstre_mort = True
                                    # envoie monstre mort
                                    data["monstre_mort"] = monstre_mort
                                    data["joueur_mort"] = joueur_mort
                                    socket.send(str.encode(str(data)))
                                    
                                else :
                                    monstre_attaque(joueurs_choix[compteur_lancers], monstre)
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
                                    attaque_magique(joueurs_choix[compteur_lancers], monstre)
                                    if monstre.pv <= 0 :
                                        monstre_mort = True
                                        data["monstre_mort"] = monstre_mort
                                        data["joueur_mort"] = joueur_mort
                                        socket.send(str.encode(str(data)))

                            if joueur_mort :
                                mort()
                                return False
                            
                            elif monstre_mort :
                                if monstre.nom == "Dragon" or monstre.nom == "Aguni" or monstre.nom == "Mort" or monstre.nom == "Gergoth" or monstre.nom == "Ange Déchu":
                                    gagne(fond_image) 
                                else:
                                    en_combat = False  
                                    for i, joueur in enumerate(joueurs_choix):
                                        joueur.attaque = valeur_avant_combat[i][0]
                                        joueur.magie = valeur_avant_combat[i][1]
                                        joueur.vitesse = valeur_avant_combat[i][2]
                                return True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_5.get_rect(center=(SCREEN_WIDTH*0.965, SCREEN_HEIGHT*0.015)).collidepoint((mx, my)):
                        joueurs_choix.clear()   
                        supprimer_classes()
                        en_combat = False
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if bouton_attaque.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.385)).collidepoint((mx, my)) or bouton_attaque_puissante.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.585)).collidepoint((mx, my)) or bouton_attaque_magique.get_rect(center=(SCREEN_WIDTH*0.89, SCREEN_HEIGHT*0.785)).collidepoint((mx, my)) and joueurs_choix[compteur_lancers].nom != 'Healer':
                        data = {}
                        data["pv"] = joueurs_choix[compteur_lancers].pv
                        data["potion"] = joueurs_choix[compteur_lancers].potion
                        data["monstre_mort"] = monstre_mort
                        data["joueur_mort"] = joueur_mort
                        data["monstre_pv"] = monstre.pv
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
                try :
                    data = eval(data)
                except:
                    print(data)
                
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
                    monstre.pv = data['monstre_pv']
                    compteur_lancers = data['compteur_lancers'] 
                    
                if len(data) == 2 :
                    data['monstre_mort'] = bool(data['monstre_mort'])
                    data['joueur_mort'] = bool(data['joueur_mort'])
                    monstre_mort = data['monstre_mort']
                    joueur_mort = data['joueur_mort']
                    
                if len(data) == 4 :
                    data['competeur_lancers'] = int(data['compteur_lancers'])
                    data['choix'] = str(data['choix'])
                    
                    compteur_lancers = data['compteur_lancers']
                    
                    if data['choix'] == "soin" :
                        data['joueur_choisi'] = int(data['joueur_choisi'])
                        soin(joueurs_choix[data['joueur_choisi']])
                        
                    if data['choix'] == "boost" :
                        data['bonus'] = str(data['bonus'])
                        data['joueur_choisi'] = int(data['joueur_choisi'])
                        appliquer_bonus(joueurs_choix[data['joueur_choisi']], data['bonus'])
                        
                    if data['choix'] == "malus" :
                        data['malus'] = str(data['malus'])
                        appliquer_malus(monstre, data['malus'])              
                    
                
                if joueur_mort :
                    mort()
                    return False
                    
                
                elif monstre_mort :
                    if monstre.nom == "Dragon" or monstre.nom == "Aguni" or monstre.nom == "Mort" or monstre.nom == "Gergoth" or monstre.nom == "Ange Déchu":
                        gagne(fond_image)
                    else:
                        en_combat = False
                        # remettre les valeurs par défaut (attaques, magie, vitesse)
                        for i, joueur in enumerate(joueurs_choix):
                            joueur.attaque = valeur_avant_combat[i][0]
                            joueur.magie = valeur_avant_combat[i][1]
                            joueur.vitesse = valeur_avant_combat[i][2]
                    return True
        
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
        
def compteur(image, fond_image):
    compteur = 5
    while compteur >= 1 :
        
        fond_image2 = pygame.image.load(image).convert()
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
    
    
        
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    running = True
    joueurs_choix = []
    graphe = None
    joueurs_choix.append(Joueur("Paladin", graphe, (5,10), 50, 20, 5, 30, 8, 0, 100, "img/classe/Paladin.png"))
    joueurs_choix.append(Joueur("Mage", graphe, (5,10), 50, 20, 5, 30, 8, 0, 100, "img/classe/Mage.png"))
    joueurs_choix.append(Joueur("Healer", graphe, (5,10), 50, 50, 5, 30, 8, 0, 100, "img/classe/Healer.png"))
    monstre1 = Monstre("loup", 50, 50, 10, 5, 15, "img/ennemi/loup.png")
    boss = []
    boss.append(Monstre("Dragon", 100, 100, 20, 10, 12, "img/ennemi/dragon.png"))
    boss.append(Monstre("Mort", 100, 100, 20, 10, 12, "img/ennemi/mort.png"))
    boss.append(Monstre("Aguni", 100, 100, 20, 10, 12, "img/ennemi/aguni.png"))
    boss.append(Monstre("Gergoth", 100, 100, 20, 10, 12, "img/ennemi/gergoth.png"))
    boss.append(Monstre("Ange Déchu", 100, 100, 20, 10, 12, "img/ennemi/angeDechu.png"))

    while running :
        combatMonstre(joueurs_choix, monstre1, 0, 1, "Facile", [False, True, False])
        running = False
        pygame.quit()
        sys.exit()