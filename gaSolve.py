# -*- coding: utf-8 -*-

import DroxlerRoy

def main():
    file = "data/pb050.txt"
    gui = False
    maxtime = 30

    result = DroxlerRoy.ga_solve(file,gui,maxtime)

    print(result)


if __name__ == '__main__':
    main()
