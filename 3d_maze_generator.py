# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 16:58:37 2021

@author: dylan
"""

import maze_generator
import txt_to_3d
import os
import sys

def removeFiles():
    
    dir_name = "C:/Users/dylan/Documents/Python Scripts/Mazes/3D"
    test = os.listdir(dir_name)
    for item in test:
        if item.endswith(".mtl"):
            os.remove(os.path.join(dir_name, item))

def go(dif):
    removeFiles()
    maze_generator.export(dif)
    txt_to_3d.go()
    removeFiles()
    
if __name__ == '__main__':
    if (len(sys.argv) > 1):
        go(int(sys.argv[1]))
    else:      
        for i in range(15, 22):
            go(i)
            go(i)
            go(i)