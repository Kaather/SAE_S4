class Entite:
    def __init__(self, nom, pv_max, pv, attaque, magie, vitesse, chemin_image):
        self.nom = nom
        self.pv = pv
        self.pv_max = pv_max
        self.attaque = attaque
        self.magie = magie
        self.vitesse = vitesse
        self.image = chemin_image

class Joueur(Entite):
    def __init__(self, nom, graphe, position, pv_max, pv, attaque, magie, vitesse, potion, argent, chemin_image):
        super().__init__(nom, pv_max, pv, attaque, magie, vitesse, chemin_image)
        self.graphe = graphe
        self.position = position
        self.potion = 5
        self.argent = 100
        self.lancer_fait = False

    def deplacer(self, direction):
        x, y = self.position
        dx, dy = direction

        new_x = x + dx
        new_y = y + dy

        new_position = (new_x, new_y)
        voisines = self.graphe[self.position]

        if new_position in voisines:
            self.position = new_position
            return True
        else:
            print(f"Le déplacement vers {new_position} n'est pas possible.")
            return False

    def afficher_position(self):
        print(f"{self.nom} est à la position {self.position}")

    def ajouter_potion(self, quantite):
        self.potion += quantite

    def utiliser_potion(self) :
        if self.potion > 0:
            # Calculer la quantité de soin
            soin = min(50, self.pv_max - self.pv)
            self.pv += soin
            self.potion -= 1

    def ajouter_argent(self, quantite):
        self.argent += quantite

    def __str__(self):
        return f"{self.nom} est à la position {self.position}, PV: {self.pv}, Attaque: {self.attaque}, Magie: {self.magie}, Vitesse: {self.vitesse}, Potions: {self.potion}"

class Monstre(Entite):
    def __init__(self, nom, pv_max, pv, attaque, magie, vitesse, chemin_image):
        super().__init__(nom, pv_max, pv, attaque, magie, vitesse, chemin_image)

    

if __name__ == '__main__' :

    Paladin = Joueur("Paladin", {}, (7,13), 100, 100, 20, 30, 10, 5, 100, "img/classe/Paladin.png")
    monstre1 = Monstre("Monstre 1", 50, 50, 10, 5, 15, "img/enemy/monstre1.png")

    print(Paladin)
    print(monstre1)