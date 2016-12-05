import pygame
from pygame.locals import *

import sys

def ga_solve(file = None, gui=True, maxtime=0):
    return true

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

    LEFTCLICK = 1                     # Défini ainsi dans pygame
    WHITE = (255,255,255)
    POINTSIZE = 5

    if len(sys.argv) > 2:
        print('ok')
    else:
        print(main.__doc__)

    window = pygame.display.set_mode((500, 500))

    continued = True

    while continued:
        for event in pygame.event.get():
            # On est obligé de faire en deux lignes car les événements parcourus peuvent retourner false.
            # On gère la fermeture via ESCAPE ou via la croix de la fenêtre
            if (event.type == KEYDOWN and event.key == K_ESCAPE) or (event.type == QUIT):
            	continued = False

            # Gestion des événements souris
            if event.type == MOUSEBUTTONDOWN and event.button == LEFTCLICK:
                pygame.draw.rect(window, WHITE, (event.pos[0],event.pos[1],POINTSIZE,POINTSIZE))

        pygame.display.update()

if __name__ == '__main__':
    main()
