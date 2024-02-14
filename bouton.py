import pygame
import sys

# Couleurs
TRANSPARENT = (255, 255, 255, 0)
WHITE = (255, 255, 255)
WHITE_TR = (255, 255, 255, 100)
BROWN_TR = (130, 60, 20, 100)
BROWN = (130, 60, 20, 200)
BLACK = (0, 0, 0)
BLACK_TR = (0, 0, 0, 200)
GREEN = (0, 255, 0)
GREEN_TR = (0, 255, 0, 200)
RED = (255, 0, 0)
RED_TR = (255, 0, 0, 100)
GREY = (128, 128, 128)
GREY_TR = (128, 128, 128, 100)

font_path = "font/MedievalSharp-Bold.ttf"

class Bouton:
    def __init__(self, largeur, hauteur, pos_x, pos_y, couleur, survol, texte="", taille_texte=30):
        self.largeur = largeur
        self.hauteur = hauteur
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.bouton_normale = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
        self.bouton_survol = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
        self.bouton_actuelle = self.bouton_normale
        self.hovered = False
        self.texte = texte
        self.taille_texte = taille_texte
        self.police = pygame.font.Font(font_path, self.taille_texte)
        self.couleur_texte = BLACK
        
        self.set_couleur(couleur, survol)

    def dessiner(self, surface):
        # Dessiner le bouton sur la surface spécifiée
        surface.blit(self.bouton_actuelle, (self.pos_x, self.pos_y))

        # Rendre le texte
        texte_surface = self.police.render(self.texte, True, self.couleur_texte)
        texte_rect = texte_surface.get_rect(center=(self.pos_x + self.largeur // 2, self.pos_y + self.hauteur // 2))

        # Dessiner le texte sur le bouton
        surface.blit(texte_surface, texte_rect)

    def est_survol(self, mouse_x, mouse_y):
        # Vérifier si la souris est positionnée sur le bouton
        return self.pos_x < mouse_x < self.pos_x + self.largeur and \
               self.pos_y < mouse_y < self.pos_y + self.hauteur

    def set_couleur(self, couleur, survol):
        self.bouton_normale.fill(couleur)
        self.bouton_survol.fill(survol)

if __name__ == "__main__" :

    pygame.init()
    info = pygame.display.Info()

    SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
    fenetre = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    bouton_1 = Bouton(SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5, SCREEN_WIDTH//3, SCREEN_HEIGHT//3, BROWN_TR, BROWN, "Bouton marron", 40)
    bouton_2 = Bouton(SCREEN_WIDTH//4, SCREEN_HEIGHT//7.5, SCREEN_WIDTH//3, SCREEN_HEIGHT//8, GREY_TR, GREY, "Bouton gris", 35)

    running = True
    while running :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION: 
                mx, my = pygame.mouse.get_pos()
                bouton_1.hovered = bouton_1.est_survol(mx, my)
                bouton_2.hovered = bouton_2.est_survol(mx, my)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if bouton_1.est_survol(mx, my):
                    print("évènement bouton marron")
                    running = False
                elif bouton_2.est_survol(mx, my):
                    running = False
                    print("évènement bouton gris")

        bouton_1.bouton_actuelle = bouton_1.bouton_survol if bouton_1.hovered else bouton_1.bouton_normale
        bouton_2.bouton_actuelle = bouton_2.bouton_survol if bouton_2.hovered else bouton_2.bouton_normale


        fenetre.fill(BLACK)
        bouton_1.dessiner(fenetre)
        bouton_2.dessiner(fenetre)


        pygame.display.flip()
        pygame.time.Clock().tick(60)
