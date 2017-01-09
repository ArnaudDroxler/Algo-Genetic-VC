import pygame
from pygame.locals import *
from pygame.math import Vector2

import numpy as np

import sys, getopt
import random

# Contient le tableau de villes. Une fois instancié, il n'est plus modifié.
cities = None
population_size = 50
mutation_rate = 20
WHITE = (255,255,255)
BLACK = (0,0,0)
POINTSIZE = 3


################################################################################
#  Algorithme génétique
################################################################################

def populate(count):
    """Crée une population de n individus selon la liste de ville auparavant déterminée"""
    population = []

    available_indexes = []

    # Pour chaque échantillon de la population à créer
    for i in range(0,count):
        indexes_list = []
        
        available_indexes = list(range(len(cities)))

        # On utilise ici une liste d'index afin de minimiser les appels au random
        # Tant qu'il reste encore des index (attention, ils ne sont pas forcément consécutifs)
        while (len(available_indexes) > 0):
            # On tire au hasard un index entre 0 et la longueur de la chaine
            index = random.randrange(0, len(available_indexes))
            # On ajoute la valeur contenue à l'index à la séquence de villes
            indexes_list.append(available_indexes[index])
            # On retire l'index de la ville
            del available_indexes[index]
        population.append(Chromosome(indexes_list))

    return population

def selection(population):
    population = sorted(population, key=lambda chromosome: chromosome.cost)
    population = population[:(int)(len(population)/2)]

    return population

def crossing(population, size):
    """ Principe global de mutation : Mutation XO.
        On selectionne deux Chromosomes x et y parmis la population.
        On détermine une section où on va insérer la section de y dans le même endroit de x.
        Il faut pour ceci préparer x à recevoir les gènes de y en :
            Déterminant les valeurs de la portion de y qui sera insérée.
            Remplacer ces valeurs dans x par un marqueur.
            Mettre en place ces marqueurs à la position de la section que l'on échange.
            Pour ceci, on condense tous les indexes sans les marqueurs, que l'on décale
            par n rotations à droite, où n est le nombre de marqueurs entre la fin de la section
            et la fin des gênes.
            A la fin, on insère la section de y.

            exemple complet :

            Chromosomes retenus
            [8, 7, 2, 3, 0, 5, 1, 6, 4, 9]] : Cost : 2433.6255091876656
            [4, 9, 0, 3, 5, 6, 2, 7, 1, 8]] : Cost : 2468.848455299176

            Section (valeurs) à échanger (choisie arbitrairement, indexs 3 à 5)
            [3, 5, 6]

            X sans les valeurs de la section
            [8, 7, 2, None, 0, None, 1, None, 4, 9]

            Nombre de None après l'index 5
            1

            Liste sans les None, avant décalage
            [8, 7, 2, 0, 1, 4, 9]
            Liste sans les None, après décalage
            [7, 2, 0, 1, 4, 9, 8]

            Portion à insérer
            [3, 5, 6]

            Nouveaux gênes après croisements
            [7, 2, 0, 3, 5, 6, 1, 4, 9, 8]

    """
    start_xo_index = int(len(population[0].genes) / 2 - len(population[0].genes) / 4)
    end_xo_index = int(len(population[0].genes) / 2 + len(population[0].genes) / 4)

    nb_to_create = size - len(population)

    for chromosome_index in range(0, nb_to_create):
        # Choix des chromosomes, pour le moment consécutifs
        # TODO : Changer le choix des échantillons dans la population
        if chromosome_index < len(population):
            chromosome_x = population[chromosome_index - len(population)]
            chromosome_y = population[chromosome_index - len(population) + 1]
        else:
            chromosome_x = population[chromosome_index - len(population)]
            chromosome_y = population[0]

        # Détermination des valeurs à supprimer dans x, tirées de la portion y
        list_to_replace = chromosome_y.genes[start_xo_index:end_xo_index+1]

        # Remplacement de ces valeurs dans x avec des None
        new_genes_list = [value if value not in list_to_replace else None for value in chromosome_x.genes]

        # Comptage du nombre de None à droite de la section (pour le décalage)
        nb_none_right = new_genes_list[end_xo_index+1:].count(None)

        # Suppression des None dans la liste pour les rotations
        new_genes_list = [value for value in new_genes_list if not value == None]

        # Rotation à droite des éléments
        for counter in range(0,nb_none_right):
            new_genes_list.insert(len(new_genes_list), new_genes_list.pop(0))
        list_to_insert = chromosome_y.genes[start_xo_index:end_xo_index+1]

        # Insertion des valeurs de y dans la section préparée
        new_genes_list[start_xo_index:start_xo_index] = list_to_insert

        # Ajout du nouveau chromosome à la population
        population.append(Chromosome(new_genes_list))

    return population

def mutate(population):
    """Pour l'instant, la mutation est un simple swap d'indexes au hasard"""
    for counter in range(0, int(len(population) / 100 * mutation_rate)):
        chromosome = random.choice(population)
        chromosome.mutate()

    return population

def solve(cities_list, rounds = 100, window = None):
    #Synthaxe horrible pour définir l'attribut statique de la liste de ville. A changer.
    global cities
    global population_size
    cities = tuple(cities_list)

    population = populate(population_size)

    print("========================================")
    print("Chromosomes initiaux")
    for chromo in population:
        print(chromo)

    while rounds > 0:
        population = selection(population)
        population = crossing(population, population_size)
        population = mutate(population)
        rounds -= 1

    # Ne pas oublier de mettre à jour l'affichage via l'objet window
    print("Résultat")
    population = sorted(population, key=lambda chromosome: chromosome.cost)
    for chromo in population:
        print(chromo)

    if window != None:
        draw_best_path(population, window)

    print("========================================")

    return True

################################################################################
#  Fin Algorithme génétique
################################################################################

def ga_solve(file = None, gui=True, maxtime=0):
    return true

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
                cities_list.append(City((int(data[1]),int(data[2]))))
    display(cities_list)

################################################################################
#  Affichage
################################################################################

def clear_window(window):
    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, [0, 0, 50, 20], 2)

    for point in cities:
        pygame.draw.rect(window, WHITE, [point.pos.x, point.pos.y, POINTSIZE, POINTSIZE])

def draw_best_path(population, window):
    clear_window(window)

    print(population[0])

    list_points = []
    best_genes_list = population[0].genes
    for gene in best_genes_list:
        list_points.append(cities[gene].pos)

    list_points.append(cities[best_genes_list[0]].pos)
    pygame.draw.lines(window, WHITE, False, list_points, 1)


def display(cities_list = None):
    LEFTCLICK = 1                     # Défini ainsi dans pygame

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
                    solve(cities_list, 20, window)
                else:
                    x_mouse, y_mouse = event.pos[0], event.pos[1]
                    # Attention : envoie une liste de tuples! La synthaxe est fine.
                    cities_list.append(City(pos=(x_mouse, y_mouse)))
                    pygame.draw.rect(window, WHITE, (x_mouse, y_mouse, POINTSIZE, POINTSIZE))

        pygame.display.update()

################################################################################
#  Classes
################################################################################

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
        self.cost = 0
        if not self.genes == None:
            self.cost = self.set_distance()

    def mutate(self):
        """Mutation du chromosome simple en inversant deux indexes au hasard.
           On ne garde la mutation que si elle est meilleure"""
        old_combinaison = list(self.genes)
        old_cost = self.cost

        index1 = random.randrange(0, len(self.genes))
        index2 =  random.randrange(0, len(self.genes))

        self.genes[index1], self.genes[index2] = self.genes[index2], self.genes[index1]

        new_cost = self.set_distance()

        if (new_cost > old_cost):
            self.genes = old_combinaison
            self.cost = old_cost
        else:
            self.cost = new_cost

    def set_distance(self):
        nb_genes = len(self.genes)
        distance = 0

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


################################################################################
#  Fin Classes
################################################################################

if __name__ == '__main__':
    main(sys.argv[1:])
