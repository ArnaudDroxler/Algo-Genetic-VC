# -*- coding: utf-8 -*-

import DroxlerRoy

def main():
    file = "data/pb020.txt"
    gui = False
    maxtime = 5
   
    result = DroxlerRoy.ga_solve(file,gui,maxtime)
    
    print(result[0])
   

if __name__ == '__main__':
    main()