from labyrinthe import *
from plateau import *
from pygameOutils import *
from jeuGraphique import *
from jeuGraphiqueReseau import *
import random


def deplacement_facile():
    print("Déplacement aléatoire / Facile")
    deplacement = random.randint(1, 6)
    print("Nombre de cases à avancer :", deplacement)
        


def deplacement_intermediaire():
    print("Stratégie de la main droite / Intermediare")
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Haut, Droite, Bas, Gauche
    current_direction_index = 1  # départ: Droite

    x, y = 0, 0  # Position initiale
    steps = 0

    while steps < 6:  # On fait 6 pas
        next_direction_index = (current_direction_index + 1) % 4
        next_x, next_y = x + directions[next_direction_index][0], y + directions[next_direction_index][1]
        print("Avancer à droite vers", (next_x, next_y))
        x, y = next_x, next_y
        current_direction_index = next_direction_index

        steps += 1


          
#Dificile
#maze = plateau 

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

def heuristic(node, goal):
    return abs(node.x - goal.x) + abs(node.y - goal.y)



def a_star(start, goal, Grille):
    open_list = []
    closed_list = []

    open_list.append(start)

    while open_list:
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node.x == goal.x and current_node.y == goal.y:
            path = []
            current = current_node
            while current is not None:
                path.append((current.x, current.y))
                current = current.parent
            return path[::-1]

        children = []
        for new_position in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            node_position = (current_node.x + new_position[0], current_node.y + new_position[1])

            if node_position[0] > (len(Grille) - 1) or node_position[0] < 0 or node_position[1] > (len(Grille[len(Grille)-1]) -1) or node_position[1] < 0:
                continue

            if Grille[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(node_position[0], node_position[1], current_node)
            children.append(new_node)

        for child in children:
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            child.g = current_node.g + 1
            child.h = heuristic(child, goal)
            child.f = child.g + child.h

            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            open_list.append(child)

            

def deplacement_difficile():
    print("Déplacement en fonction de la visibilité des pièges / Difficile")

    # Utilisation de l'algorithme A* pour trouver le chemin optimal
    # Création d'un labyrinthe (exemple)
    Grille = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    start = Node(0, 0)
    goal = Node(4, 4)

    path = a_star(start, goal, Grille)


    if path:
        print("Chemin optimal:", path)
    else:
        print("Aucun chemin trouvé.")



