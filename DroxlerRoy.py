import pygame
from pygame.locals import *

import random
import numpy as np

import sys

class City(object):
    """Représente une ville possible"""
    # Il reste à voir si on garde l'id ou juste l'index de la référence du tuple(Tableau de villes
    # que le chromosome référence). Probablement que l'index.
    last_id = 0

    #Pour pos, passer un tuple (x,y)
    def __init__(self, pos, name = None):
        City.last_id = City.last_id + 1

        self.id = City.last_id
        self.name = name
        self.pos = pos

    def __repr__(self):
        return "[id:" + str(self.id) + " X:" + str(self.pos[0]) + " Y:" + str(self.pos[1]) + "]"

class Chromosome(object):
    """ représentation d'un individu sous la forme d'un chemin (suite de villes)
    et d'un coût"""

    def __init__(self, genes=None, cost=None):
        self.genes = genes
        self.cost = cost

    def __repr__(self):
        return '[%s]' % ', '.join(map(str, self.genes)) + "] : Cost : " + str(self.cost)


def ga_solve(file = None, gui=True, maxtime=0):
    return true

def populate(count, cities):
    population = set()

    available_indexes = []

    # Pour chaque échantillon de la population à créer
    for i in range(0,count):
        indexes_list = []

        for index in range(0, len(cities)):
            available_indexes.append(index)
            print(index)

        while (len(available_indexes) > 0):
            index = random.randint(0, len(available_indexes)-1)
            print("Index : ", index)
            print("liste_indexs avant : ", indexes_list)
            indexes_list.append(available_indexes[index])
            print("liste_indexs après : ", indexes_list)
            print("Indexs disponibles avant remove : ", available_indexes)
            del available_indexes[index]
            print("Indexs disponibles après remove : ", available_indexes)

        population.add(Chromosome(indexes_list, 0))

    return population


def solve(cities_list, window):
    # Tuple des villes que le commercial doit parcourir. Il devra être de la bonne taille à l'instanciation
    cities = np.asarray(cities_list)

    population = populate(10, cities)

    for chromo in population:
        print(chromo)

    print("Liste des villes")
    print(cities_list)

    # Ne pas oublier de mettre à jour l'affichage via l'objet window
    return True

def main():
    """
        NAME
            aStarDistance : Calculate the distance beetween cities using A* Algorith"

        SYNOPSIS
            aStarDistance [cities_description_file] [links_description_file] optionnal:[heuristic_method]

        DESCRIPTION
            This method permits to specify the description files for the cities and the links beetween them.

        PARAMETERS
            [from_city] : City name from where to start

            [to_city] : City name to join

            [heuristic_method]   : Number 0 to 4 describing the heuristic method to use with the A* Algorithm
                                   0 : No heuristic method (DEFAULT)
                                   1 : Distance beetween cities using only X axis
                                   2 : Distance beetween cities using only Y axis
                                   3 : Bird flying distance
                                   4 : Manhattan distance
        FILES
            [cities_description_file] : Format expected :
                                        City_Name X_Position Y_Position
                                        i.e :
                                        Copenhagen 687 1323
                                        Hamburg 774 1175

                                        It uses the /data/positions.txt path


            [links_description_file] : The links beetween cities file. Format expected :
                                       City_Name_From City_Name_To Distance_In_Km

                                       i.e :
                                       Copenhagen Hamburg 180
                                       Hamburg Amsterdam 338

                                       It uses the /data/connections.txt path
    """
    position_file = './data/positions.txt'
    connection_file = './data/connections.txt'


    # print(main.__doc__)

    graphic = True

    if (graphic):
        display()
    else:
        # A remplacer par la lecture du fichier, et le résultat doit aller dans une liste
        cities_list = ()
        display(cities_list)

def display(cities_list = None):
    LEFTCLICK = 1                     # Défini ainsi dans pygame
    WHITE = (255,255,255)
    POINTSIZE = 5

    if cities_list == None:
        cities_list = []

    window = pygame.display.set_mode((500, 500))

    # Draw a rectangle outline
    lauch_button = pygame.draw.rect(window, WHITE, [0, 0, 50, 20], 2)

    continued = True

    while continued:
        mouse_xy = pygame.mouse.get_pos()
        over_launch = lauch_button.collidepoint(mouse_xy)

        for event in pygame.event.get():
            # On est obligé de faire en deux lignes car les événements parcourus peuvent retourner false.
            # On gère la fermeture via ESCAPE ou via la croix de la fenêtre
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT):
                continued = False

            # Gestion des événements souris
            if event.type == MOUSEBUTTONDOWN and event.button == LEFTCLICK:
                if over_launch:
                    solve(cities_list, window)
                else:
                    x_mouse, y_mouse = event.pos[0], event.pos[1]
                    # Attention : envoie une liste de tuples! La synthaxe est fine.
                    cities_list.append(City(pos=(x_mouse, y_mouse)))
                    pygame.draw.rect(window, WHITE, (x_mouse, y_mouse, POINTSIZE, POINTSIZE))

        pygame.display.update()

if __name__ == '__main__':
    main()
