import pygame
from pygame.locals import *
from pygame.math import Vector2

import random
import numpy as np
from numpy import sqrt

import sys


class Cities(object):
    """Tableau figé qui représente les villes.
       Classe très mal faite pour le moment, il faudra trouver une solution"""
    cities_array = None

    def __init__(self, cities_list):
        # Tuple des villes que le commercial doit parcourir. Il devra être de la bonne taille à l'instanciation
        Cities.cities_array = np.asarray(cities_list)


class City(object):
    """Représente une ville possible, avec un identifiant (à voir si il reste),
       un nom inutile, et une position. Les infos inutiles pourraient devenir
       utiles à l'avenir.
    """
    # On ne garde qu'une liste d'indexes pour les gênes afin de ne pas dupliquer l'information
    last_id = 0

    #Pour pos, passer un tuple (x,y)
    def __init__(self, pos, name = None):
        self.id = City.last_id
        self.name = name
        self.pos = Vector2(pos)
        City.last_id = City.last_id + 1

    def __repr__(self):
        return "[id:" + str(self.id) + " X:" + str(self.pos[0]) + " Y:" + str(self.pos[1]) + "]"

class Chromosome(object):
    """ représentation d'un individu sous la forme d'un chemin (suite de villes)
    et d'un coût"""

    def __init__(self, genes=None):
        self.genes = genes
        self.cost = self.set_distance()

    def set_distance(self):
        nb_genes = len(self.genes)
        distance = 0

        # On pourra changer pour la classe Vec2D, qui fournit des méthodes de distance
        for index in range(0, len(self.genes)):
            villeA = Cities.cities_array[self.genes[index]]

            if index == nb_genes-1:
                villeB = Cities.cities_array[self.genes[0]]
            else:
                villeB = Cities.cities_array[self.genes[index+1]]

            distance += villeA.pos.distance_to(villeB.pos)

            print("distance", distance)

        return distance

    def __repr__(self):
        return '[%s]' % ', '.join(map(str, self.genes)) + "] : Cost : " + str(self.cost)


def ga_solve(file = None, gui=True, maxtime=0):
    return true

def populate(count):
    """Crée une population de n individus selon la liste de ville auparavant déterminée"""
    population = set()

    available_indexes = []

    # Pour chaque échantillon de la population à créer
    for i in range(0,count):
        indexes_list = []

        # On instancie une liste d'index de 0 à n-ville - 1
        for index in range(0, len(Cities.cities_array)):
            available_indexes.append(index)

        # On utilise ici une liste d'index afin de minimiser les appels au random
        # Tant qu'il reste encore des index (attention, ils ne sont pas forcément consécutifs)
        while (len(available_indexes) > 0):
            # On tire au hasard un index entre 0 et la longueur de la chaine
            index = random.randint(0, len(available_indexes)-1)
            # On ajoute la valeur contenue à l'index à la séquence de villes
            indexes_list.append(available_indexes[index])
            # On retire l'index de la ville
            del available_indexes[index]

        population.add(Chromosome(indexes_list))

    return population


def solve(cities_list, window):
    #Synthaxe horrible pour définir l'attribut statique de la liste de ville. A changer.
    Cities(cities_list)

    population = populate(5)

    print("Print les Chromosomes")
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

    graphic = False

    if (graphic):
        display()
    else:
        # A remplacer par la lecture du fichier, et le résultat doit aller dans une liste
        cities_list = (City((0,0)),City((20, 20)),City((40, 40)), City((60, 60)))
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
