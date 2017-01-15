"""
    Auteurs                      : Arnaud Droxler & Axel Roy
    Date dernière modification   : 15 Janvier 2017
    But                          : Implémentation d'un algorithme génétique pour résoudre
                                   le problème du voyageur de commerce

    Informations à propos des choix pour l'algorithme génétique

    ***********************************************************************************
                          Orientation globale de l'algorithme
    ***********************************************************************************

    L'algorithme génétique utilise les trois phases habituelles d'un algorithme génétique,
    soit la sélection, le croisement puis les mutations.

    De manière générale, il y a deux aspects que l'on peut rechercher de l'algorithme :
    * La vitesse de convergence
    * La robustesse et la constance des résultats (ne pas bloquer sur un minimum local)

    Nous avons volontairement donné la priorité à la résistance de l'algorithme en
    implémentant des méthodes qui génèrent beaucoup de bruit sur les gênes des chromosomes
    de la population.

    ***********************************************************************************
                                        Population
    ***********************************************************************************

    Aucune méthode gourmande n'a été utilisée pour essayer de générer une solution bonne
    dès le départ. On aurait par exemple pu essayer de partir d'un point et de chercher
    toujours la ville la plus proche.

    Nous avons préféré opter pour une génération de la population totalement aléatoire.

    ***********************************************************************************
                                        Selection
    ***********************************************************************************

    Nous avons choisi de privilégier une selection élitiste, très simple et très rapide
    implémentée par une simple list comprehension.

    ***********************************************************************************
                                        Croisements
    ***********************************************************************************

    Nous avons utilisé un croisement en deux points, avec réarrangement via la
    méthode du croisement ox. Cette méthode est relativement gourmande, mais génère des
    résultats très pertinents.

    Un soin tout particulier a été accordé à l'algorithme, en partant des explications
    de la documentation fournie avec ce travail pratique, en décorticant les étapes et
    en trouvant une méthode d'implémentation rapide via des rotations. Elle est
    précisément décrite dans la méthode ox_cross.

    ***********************************************************************************
                                        Mutations
    ***********************************************************************************

    Pour les mutations, on selectionne au hasard des chromosome qui vont générer
    une mutation. Le chromosome selectionné n'est jamais remplacé, on génère un nouveau
    chromosome, sans se soucier de son efficacité. C'est la prochaine phase de selection
    qui va le garder ou non.


    ***********************************************************************************
                                        Tests
    ***********************************************************************************

    Le programme a été fait pour que les paramètres pour l'algorithme soient facilement
    modifiables. Des tests ont été effectués pour paramétrer au mieux ces facteurs, en
    lancant n fois l'expérience et en récupérant les résultats moyens.

    Il en sort qu'il n'est pas utile d'utiliser de grandes populations pour aboutir à
    de bons résultats, cela a plutôt tendance à faire baisser les performances.

    Etant donné l'implémentation des mutations (qui retournent un nouveau chromosome),
    il est utile de mettre un taux de mutation plus élevé que les 30% que l'on retrouve
    dans la documentation scientifique du domaine.

    Les paramètres ne sont pas encore totalement optimisés par manque de temps.

    L'utilisation en tant que module a été testée avec le PVC-tester-3.5, et il n'a
    pas fourni d'erreur. On pourrait tenter de réduire la constante TIMELIMIT qui fixe
    le temps qu'il faut laisser pour l'aggrégation des résultat et le retour des
    méthodes, mais on risque de fournir des timeout pour le testeur.

    ***********************************************************************************
                                        Conclusions
    ***********************************************************************************

    Globalement, on peut constater que les choix effectués dans les méthodes de selection,
    croisements et mutations permettent d'explorer largement le domaine des solutions,
    mais que les performances en terme de convergence sont affectés. Ceci est volontaire,
    et les résultats pour un nombre de villes conséquents avec un temps court fourni des
    résultats tout de même très satisfaisants.

    On peut voir en mode graphique qu'en laissant suffisamment de temps, on arrive rarement
    à une solution qui présente des croisements de routes, l'algorithme réussi à démeler
    fortement les noeuds.

    Nous avons implémenté une augmentation du nombre de mutations en fin de temps à disposition
    pour faire en sorte qu'il ne reste pas bloqué dans un minimum local, et il est visuellement
    possible d'observer qu'il arrive que cela permet de sortir d'un minimum local.

    En effet, il n'est pas rare que l'algorithme parte d'un chemin sans croisements
    et trouve un nouveau chemin très différent, qui comporte des croisements de chemins,
    le fait muter et le dénoue.

    Les avantages de cette implémentation sont les suivants :
    * Etant donné que l'on repose entièrement sur l'aléatoire, on ne dirige pas
      les résultats dans un minimum local.
    * L'algorithme a la capacité de sortir des minimums locaux.
    * Il est robuste et optimisé pour les phases critiques qui demandent beaucoup
      de calculs

    Les inconvénients sont les suivants :
    * Il pourrait converger plus rapidement vers une solution acceptable.
    * Il n'implémente pas de notion de convergence pour stopper la recherche.

      Il est possible de le faire facilement en comparant à chaque boucle l'ancien
      meilleur résultat avec le nouveau, et de faire en sorte que si c'est le cas
      x fois, on stop la recherche. Ce critère n'est pas très pertinent tout de même.

      L'idéal serait de comparer la distance moyenne entre les échantillons de
      la population, et de faire en sorte que si il sont tous très semblables on
      peut dire qu'il n'est pas utile de faire plus.

      La première n'a pas été implémentée car elle ne paraît pas apporter grand chose,
      hormis allourdir la procédure.

      La deuxième est beaucoup plus intéressant mais allourdi énormément la boucle
      principale de l'algorithme.

    ***********************************************************************************
                              Améliorations et perspectives
    ***********************************************************************************

    L'algorithme peut être amélioré pour ce qui est de la vitesse de convergence,
    ceci en générant une population plus dirigée, puis en changeant la selection
    élitiste par une autre méthode (la méthode par tournoi semble une bonne option).

    On pourrait imaginer lancer plusieurs expériences en parralèlle et récupérer
    le meilleur résultat parmis celles-ci.

    En terme de programmation, l'utilisation d'une heapq semble être une bonne
    option, mais il faut vérifier qu'elle apporte vraiment plus qu'elle ne coûte,
    car les tris sont effectués à un seul moment actuellement, tandis qu'une heapq
    trie à chaque ajout/suppression.

    Un profilage montre que l'estimation du coût, le tri des listes et le croisement
    sont les sections critiques de l'algorithme.

"""

import pygame
from pygame.locals import *
from pygame.math import Vector2
from itertools import cycle
import sys, getopt
import random
from math import sqrt
from time import time
from math import hypot

# Contient le tableau de villes. Une fois instancié, il n'est plus modifié.
# Il est global pour éviter de le passer à chaque méthode, ce qui impacte
# légèrement les performances
cities = None
# Nombre de chromosomes formant la population
population_size = 20
# Pourcentage de la population qui va subir une mutation
mutation_rate = 50
# Pourcentage des chromosomes gardés lors de la phase de selection
selection_rate = 60

# Sert à l'enregistrement du temps lors de l'appel comme module
starting_time = 0

# Constantes pour PyGame
WHITE = (255,255,255)
BLACK = (0,0,0)

# Taille des points pour représenter les villes
POINTSIZE = 2
# Temps que l'on laisse à disposition pour retourner la solution. Avec 0.05s on est très très large, cela prend en général 0.005s
TIMELIMIT = 0.05
# Temps laissé à l'Algorithme par défaut si aucun paramètre n'est passé.
DEFAULTMAXTIME = 20

################################################################################
#  Algorithme génétique
################################################################################

def populate(count):
    """Crée une population de n individus selon la liste de ville auparavant déterminée"""
    population = []

    available_indexes = []

    # Pour chaque échantillon de la population à créer
    for _ in range(0,count):
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
    """Seleciton purement élitiste, volontairement afin de ne pas perdre de temps à sélectionner.
    On se contente de trier et de selectionner les x% meilleurs.
    Cela se couple avec la volonté des croisements et des selections de parcourir au maximum le
    domaine de solution en favorisant le hasard, et le fait que les mutations créent des nouveaux chromosomes.
    A la fin de la mutation, la population a une taille plus grande que la taille définie via la variable globale
    population_size.
    On se retrouve avec des chromosomes très différents, dans la population, ce qui implique que la selection
    par roulette demanderai du temps pour en pas réellement améliorer le tirage.
    """
    population = sorted(population, key=lambda chromosome: chromosome.cost)
    population = population[:(int)(len(population)/100 * selection_rate)]

    return population

def crossing(population, size):
    """ Le croisement s'effectue via la méthode de croisement en deux points (ox).
    Les deux chromosomes qui sont utilisés pour le croisement sont choisi aléatoirement.
    La portion qui est réarrangée pour être réorganisée est toujours de la taille de la moitié
    des gênes qui composent un chemin. On pourrait imaginer faire varier la longueur à chaque
    croisement, mais il faut vérifier que ca apporte vraiment quelque chose.

    """
    start_ox_index = int(len(population[0].genes) / 2 - len(population[0].genes) / 4)
    end_ox_index = int(len(population[0].genes) / 2 + len(population[0].genes) / 4)

    nb_to_create = size - len(population)

    for chromosome_index in range(0, nb_to_create):
        chromosome_x = random.choice(population)
        chromosome_y = random.choice(population)

        new_genes_list = ox_cross(chromosome_x, chromosome_y, start_ox_index, end_ox_index)

        # Ajout du nouveau chromosome à la population
        population.append(Chromosome(new_genes_list))

    return population

def ox_cross(chromosome_x, chromosome_y, start_ox_index, end_ox_index):
    """ Principe global de mutation : Mutation ox.
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

    # Détermination des valeurs à supprimer dans x, tirées de la portion y
    list_to_replace = chromosome_y.genes[start_ox_index:end_ox_index+1]

    # Remplacement de ces valeurs dans x avec des None
    new_genes_list = [value if value not in list_to_replace else None for value in chromosome_x.genes]

    # Comptage du nombre de None à droite de la section (pour le décalage)
    nb_none_right = new_genes_list[end_ox_index+1:].count(None)

    # Suppression des None dans la liste pour les rotations
    new_genes_list = [value for value in new_genes_list if not value == None]

    # Rotation à droite des éléments
    for _ in range(0,nb_none_right):
        new_genes_list.insert(len(new_genes_list), new_genes_list.pop(0))
    list_to_insert = chromosome_y.genes[start_ox_index:end_ox_index+1]

    # Insertion des valeurs de y dans la section préparée
    new_genes_list[start_ox_index:start_ox_index] = list_to_insert

    return new_genes_list

def mutate(population):
    """ Mutation appliquée sur la population. Les échantillons qui subissent une mutation
        Sont choisis totalement au hasard. On fait muter un certain taux de la population.
        Très important, les mutations crées de nouveaux échantillons pour la population,
        on ne perd pas les chromosomes de base.
    """
    for _ in range(0, int(len(population) / 100 * mutation_rate)):
        chromosome = random.choice(population)
        population.append(chromosome.mutate())

    return population

def solve(cities_list, window = None, maxtime = DEFAULTMAXTIME, gui = False):
    """ Résolution du problème du voyageur commercial.
        cities list est une liste de ville qui sera utilisée pour résoudre le problème.
        Les autres paramètres sont facultatifs :
        window est l'instance de la fenêtre PyGame.
        maxtime est le temps total de calcul désiré, en seconde.
        gui détermine si on désire le rendu graphique en temps réel
    """
    global cities
    global starting_time
    global TIMELIMIT
    global selection_rate
    global mutation_rate

    # Second seuil de mutation pour tenter de faire sortir d'un minimum local
    second_mutation_rate = 60
    # Détermine si on est dans le second seuil de mutation
    augmentation_up = False
    # Pourcentage d'erreur pour le calcul du temps écoulé entre deux cycles.
    # Il est très grand pour ne pas prendre de risque pour l'évaluation via PVC-tester
    time_error_rate = 0.02

    if gui:
        font = pygame.font.Font(None, 30)

    # On fige volontairement la définition des villes en tuple, de manière globale
    cities = tuple(cities_list)

    # Création de la population
    population = populate(population_size)

    # Calcul du temps écoulé depuis le lancement du programme
    elapsed_time = time() - starting_time
    time_left = maxtime - elapsed_time
    time_left -= time_left * time_error_rate

    # Boucle principale de l'algorithme génétique
    while time_left > TIMELIMIT:
        time1 = time()
        population = selection(population)

        if gui:
            draw_best_path(population, window)

        population = crossing(population, population_size)
        population = mutate(population)

        # Dès que les 3/4 du temps est passé, on tente d'augmenter le taux de mutation
        # pour éviter de rester dans un minimum local
        if time_left < maxtime/4 and not augmentation_up:
            mutation_rate = second_mutation_rate
            augmentation_up = True

        time2 = time()
        elapsed_time = time2 - time1
        elapsed_time = elapsed_time + elapsed_time * time_error_rate
        time_left -= elapsed_time

    # Mise en forme du retour de la meilleure solution trouvée
    population = sorted(population, key=lambda chromosome: chromosome.cost)
    best_solution = population[0]
    best_cost = best_solution.cost
    best_path = [cities_list[city].name for city in best_solution.genes]

    # Dessin du meilleur chemin si on est en mode graphique
    if window != None:
        draw_best_path(population, window)
        text = font.render("Coût : " + str(population[0].cost), True, WHITE)
        textRect = text.get_rect()
        window.blit(text, textRect)

    print("Meilleur cout", best_cost )

    return best_cost, best_path

################################################################################
#  Fin Algorithme génétique
################################################################################

def ga_solve(file = None, gui=True, maxtime=DEFAULTMAXTIME):
    """Point d'entrée pour l'utilisation de cet algorithme comme module"""
    return parametre(file,gui,maxtime)

def parametre(file = None, gui=True, maxtime=DEFAULTMAXTIME):
    """
    Gestion des paramètres, suivant si le mode graphique est demandé, si on utilise
    l'algorithme en import et si on a défini un temps limite.
    """
    window = None
    cities_list = None
    global starting_time
    starting_time = time()

    if(file):
        cities_list = []
        with open(file, "r") as fichier :
            for line in fichier :
                data = line.split()
                cities_list.append(City((int(data[1]),int(data[2])), data[0]))
    if(gui):
        window = pygame.display.set_mode((500, 500))

    if (gui and not file):
        maxtime = DEFAULTMAXTIME
        return display(cities_list, maxtime,gui,window)
    elif(not gui and file):
        return solve(cities_list, window, maxtime, gui)
    elif(gui and file):
        return display(cities_list,maxtime,gui,window)


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
    maxtime = DEFAULTMAXTIME

    if len(args) == 1:
        file = args[0]

    for o,a in optlist :
        if o == "--maxtime":
            maxtime = int(a)
        if o == "--nogui":
            gui = False
        if o == "--help":
             print(main.__doc__)
             sys.exit()

    parametre(file,gui,maxtime)

################################################################################
#  Affichage
################################################################################

def clear_window(window):
    """ Dessin de la fenêtre avec les villes """
    window.fill(BLACK)

    for point in cities:
        pygame.draw.rect(window, WHITE, [point.pos.x, point.pos.y, POINTSIZE, POINTSIZE])

def draw_best_path(population, window):
    """Dessin du meilleur chemin trouvé. Attention, la population doit être triée!
    On pourrait la modifier pour ne passer que le meilleur chromosome"""
    clear_window(window)

    list_points = []
    best_genes_list = population[0].genes
    for gene in best_genes_list:
        list_points.append(cities[gene].pos)

    list_points.append(cities[best_genes_list[0]].pos)
    pygame.draw.lines(window, WHITE, False, list_points, 1)
    pygame.display.update()


def display(cities_list = None, maxtime = DEFAULTMAXTIME, gui = True, window = None):
    """Gestion de l'affichage via PyGame"""
    LEFTCLICK = 1                     # Défini ainsi dans pygame
    global starting_time

    pygame.init()
    pygame.display.set_caption('Problème du voyageur commercial')
    font = pygame.font.Font(None, 30)
    text = font.render("Temps : " + str(maxtime) +  "secondes. Pressez enter pour lancer", True, WHITE)
    textRect = text.get_rect()
    window.blit(text, textRect)
    cost = -1
    best_path = []
    max_time_relauch = maxtime

    if cities_list == None:
        cities_list = []
    else:
        for point in cities_list:
            pygame.draw.rect(window, WHITE, [point.pos.x, point.pos.y, POINTSIZE, POINTSIZE])

    continued = True

    while continued:
        mouse_xy = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # On est obligé de faire en deux lignes car les événements parcourus peuvent retourner false.
            # On gère la fermeture via ESCAPE ou via la croix de la fenêtre
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT):
                continued = False
                return cost, best_path

            if (event.type == KEYDOWN and event.key == K_RETURN):
                starting_time = time()
                cost, best_path = solve(cities_list, window, max_time_relauch, gui)

            # Gestion des événements souris
            if event.type == MOUSEBUTTONDOWN and event.button == LEFTCLICK:
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
        # return "[id:" + str(self.id) + " name : "+ self.name + " X:" + str(self.pos[0]) + " Y:" + str(self.pos[1]) + "]"
        return "[id:{0.id} name:{0.name} X:{0.pos.x} Y:{0.pos.y}]".format(self)

class Chromosome(object):
    """ représentation d'un individu sous la forme d'un chemin (suite de villes)
    et d'un coût"""

    def __init__(self, genes=None):
        self.genes = genes
        self.cost = 0
        if not self.genes == None:
            self.cost = self.calculate_cost()

    def mutate(self):
        """Mutation du chromosome en selectionnant une partie des gênes au hasard
        et en inversant cette portion. On l'effectue deux fois de suite, le faire
        plus de fois ne semble pas améliorer drastiquement les résultats, et on
        perd du temps.

        Il a été implémenté un mélange entre swap au hasard de gênes et inversion
        de l'ordre de séquences de gênes, mais le swap ne semble pas apporter
        d'améliorations notable"""

        # On évite de recopier uniquement la référence
        new_genes_list = list(self.genes)

        # for _ in range(0,1):
        #     index1 = random.randrange(0, len(self.genes))
        #     index2 =  random.randrange(0, len(self.genes))
        #     new_genes_list[index2], new_genes_list[index1] = new_genes_list[index1], new_genes_list[index2]

        for _ in range(0,2):
            start_index = random.randrange(0, len(self.genes))
            end_index = random.randrange(0, len(self.genes))

            if end_index < start_index:
                start_index, end_index = end_index, start_index

            part_to_reverse = new_genes_list[start_index:end_index]
            part_to_reverse.reverse()

            new_genes_list[start_index:end_index] = part_to_reverse

        return Chromosome(new_genes_list)

    def calculate_cost(self):
        """Calcul du cout du chromosome, ici la distance total vol d'oiseau
        selon l'ordre des villes"""
        nb_genes = len(self.genes)
        distance = 0

        c = cycle(self.genes)
        next(c)

        for index1, index2 in zip(self.genes, c):
            villeA = cities[index1]
            villeB = cities[index2]

            # Ces quelques lignes sont un point critique des performance de l'algorithme
            # Le changement de la méthode de calcul de la distance à vol d'oiseaux
            # Représente des variations du temps importante.

            # Utiliser la classe vec2 de pygame améliore d'un quart le temps de calcul
            # par rapport aux autres méthodes. Les autres méthodes sont laissées en
            # commentaire à titre informatif

            # dx = abs(villeA.pos.x - villeB.pos.x)
            # dy = abs(villeA.pos.y - villeB.pos.y)

            # distance += hypot(dx,dy)
            # distance += sqrt(dx**2 + dy**2)
            distance += villeA.pos.distance_to(villeB.pos)
        return distance

    def __repr__(self):
        return '[%s]' % ', '.join(map(str, self.genes)) + "] : Cost : " + str(self.cost)


################################################################################
#  Fin Classes
################################################################################


if __name__ == '__main__':
    main(sys.argv[1:])
