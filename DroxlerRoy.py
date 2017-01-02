import pygame
from pygame.locals import *
from pygame.math import Vector2

import numpy as np

import sys, getopt
import random

# Contient le tableau de villes. Une fois instancié, il n'est plus modifié.
cities = None

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
            villeA = cities[self.genes[index]]

            if index == nb_genes-1:
                villeB = cities[self.genes[0]]
            else:
                villeB = cities[self.genes[index+1]]

            distance += villeA.pos.distance_to(villeB.pos)
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
        # for index in range(0, len(cities)):
        # for index, value in enumerate(cities):
        #     available_indexes.append(index)
        available_indexes = list(range(len(cities)))


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
    global cities
    cities = tuple(cities_list)

    population = populate(5)

    print("Chromosomes")
    for chromo in population:
        print(chromo)

    print("Liste des villes")
    print(cities_list)

    # Ne pas oublier de mettre à jour l'affichage via l'objet window
    return True

def main(argv):
    """
        NAME
            TSP : Solve the travelling salesman problem using genetic algorithm

        SYNOPSIS
            python DroxlerRoy.py [--nogui] [--maxtime s] [filename]
            
        PARAMETERS
            [--nogui] : disable the gui, default to true

            [--maxtime s] : diffine the maximum time of exectution in seconds , default at 1000 s

            [filename] : Format expected :
                                        City_Name X_Position Y_Position
                                        i.e :
                                        v0 54 391
                                        v1 77 315

                                        It uses the /data/pb010.txt path
       
    """    
    optlist, args = getopt.getopt(argv, '' ,['nogui', 'maxtime=','help'])
    
    file = None
    gui = True
    maxtime = 1000
    
    if len(args) == 1:
        file = args[0]
    
    for o,a in optlist : 
        if o == "--maxtime":
            maxtime = a
        if o == "--nogui":
            gui = False
        if o == "--help":
             print(main.__doc__)
             sys.exit()
    
    cities_list = []
    
    if (gui):
        display()
    else:
         with open(file, "r") as fichier :
            for line in fichier :
                data = line.split()
                cities_list.append(City(float(data[1]),float(data[2])))
    
    display(cities_list)

        
def display(cities_list = None):
    LEFTCLICK = 1                     # Défini ainsi dans pygame
    WHITE = (255,255,255)
    POINTSIZE = 5


    window = pygame.display.set_mode((500, 500))

    if cities_list == None:
        cities_list = []
    else:
        for point in cities_list:
            pygame.draw.rect(window, WHITE, [point.pos.x, point.pos.y, POINTSIZE, POINTSIZE])

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
    main(sys.argv[1:])
