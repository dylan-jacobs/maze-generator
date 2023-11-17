# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 09:24:54 2021

@author: dylan
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 21:31:49 2021

@author: dylan
"""
import pygame
import sys
import random
import math
import time
import threading
import os
import numpy as np
import skimage.measure as measure
import matplotlib.pyplot as plt

screen_width = 800
screen_height = 800
speed = 0.01 # smaller = faster
draw = True
np.set_printoptions(threshold=np.inf)
if draw:
    pygame.init()
    display = pygame.display.set_mode((screen_width, screen_height))
    display.fill((0, 0, 0))
    pygame.display.set_caption('Maze Generator')

class Maze:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.array = []
        for i in range(width * height):
            self.array.append(Cell(i))
            
    def go(self):
        index = math.floor(random.random() * self.width * self.height)
        cell1 = self.array[index]
        stack = []
        finish = False
        stack.append(cell1)
        cell1.visited = True
        while not (self.allVisited()):
            # Did the user click the window close button?
            if draw:
                for event in pygame.event.get():    
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_f:
                            finish = True
                   
            cell2 = None
            if not self.getNeighboringCell(self.array[cell1.index]) == False & (self.getNeighboringCell(self.array[cell1.index]) != None):
                cell2 = self.getNeighboringCell(self.array[cell1.index])
                stack.append(cell2)
                cell2.visited = True
                cell2.highlight = True
            else:
                cell2 = stack.pop()
                
            if (cell2 != None) & (cell1 != None):
                self.removeWall(cell1, cell2)
                if draw:
                    cell1.draw(self.width, self.height)
                    cell2.draw(self.width, self.height)
                    # Flip the display
                    pygame.display.flip()
                    cell2.highlight = False
                if not finish:
                    time.sleep(speed)
                cell1 = cell2
        
    def allVisited(self):
        for cell in self.array:
            if not cell.visited:
                return False
            
        return True
        
    def getNeighboringCell(self, cell):
        l = []
        
        topInd = cell.getTopCellIndex(self.width)
        bottomInd = cell.getBottomCellIndex(self.width, self.height)
        leftInd = cell.getLeftCellIndex(self.width, self.height)
        rightInd = cell.getRightCellIndex(self.width, self.height)
        if (topInd != None):
            if ((topInd != None) & (not self.array[cell.getTopCellIndex(self.width)].visited)):
                l.append(topInd)
        if (bottomInd != None):
            if ((bottomInd != None) & (not self.array[bottomInd].visited)):
                l.append(bottomInd)
        if (leftInd != None):
            if ((leftInd != None) & (not self.array[leftInd].visited)):
                l.append(leftInd)
        if (rightInd != None):
            if ((rightInd != None) & (not self.array[rightInd].visited)):
                l.append(rightInd)
        return self.array[random.choice(l)] if len(l) > 0 else False
            
    def draw(self):
        for cell in self.array:
            for event in pygame.event.get():
                if (event == pygame.event.QUIT):
                    sys.exit()
            cell.highlight = False
            cell.draw(self.width, self.height)            
            
    def removeWall(self, cell1, cell2):
        if cell2.index == cell1.getTopCellIndex(self.width): # top
            cell1.walls[0] = False
            
        if cell2.index == cell1.getBottomCellIndex(self.width, self.height): # bottom
            cell1.walls[1] = False
            cell2.walls[0] = False
            
        if cell2.index == cell1.getLeftCellIndex(self.width, self.height): # left
            cell1.walls[2] = False
            
        if cell2.index == cell1.getRightCellIndex(self.width, self.height): # right
            cell1.walls[3] = False
            cell2.walls[2] = False
        
    def convertToArray(self):
        new_array = np.zeros([(self.width * 2) + 1, (self.height * 2) + 1]) 
        new_array[0, :] = 1
        new_array[-1, :] = 1
        new_array[:, 0] = 1
        new_array[:, -1] = 1
        for i in range(0, len(self.array)):
            cell = self.array[i]
            if cell.topWall():                
                new_array[round(cell.getRow(self.width) * 2), (round(cell.getCol(self.width)) * 2) + 1] = 1
                new_array[round(cell.getRow(self.width) * 2), (round(cell.getCol(self.width)) * 2)] = 1
                new_array[round(cell.getRow(self.width) * 2), (round(cell.getCol(self.width)) * 2) + 2] = 1
            #if cell.bottomWall():
                #new_array[round(cell.getRow(self.width) * 2) + 2, (round(cell.getCol(self.width)) * 2)] = 1
            if cell.leftWall():                
                new_array[round(cell.getRow(self.width) * 2) + 1, (round(cell.getCol(self.width)) * 2)] = 1
                new_array[round(cell.getRow(self.width) * 2), (round(cell.getCol(self.width)) * 2)] = 1   
                new_array[round(cell.getRow(self.width) * 2) + 2, (round(cell.getCol(self.width)) * 2)] = 1                
            #if cell.rightWall():                
                #new_array[round(cell.getRow(self.width) * 2) + 1, (round(cell.getCol(self.width)) * 2) + 1] = 1        
        return new_array
        
class Cell:
    
    def __init__(self, index):
        self.index = index
        self.walls = [True, True, True, True] 
        self.visited = False
        self.highlight = False
        
    def getRow(self, width):
        return (self.index - self.getCol(width)) / width
    
    def getCol(self, width):
        return self.index % width
        
    def getTopCellIndex(self, width):
        return self.index - width if (self.index >= width) else None
    
    def getBottomCellIndex(self, width, height):
        return self.index + width if (self.index < ((width * height) - width)) else None
    
    def getLeftCellIndex(self, width, height):
        return self.index - 1 if (self.index % width != 0) else None
    
    def getRightCellIndex(self, width, height):
        return self.index + 1 if ((self.index + 1) % width != 0) else None
    
    def topWall(self):
        return self.walls[0]
    
    def bottomWall(self):
        return self.walls[1]
    
    def leftWall(self):
        return self.walls[2]
    
    def rightWall(self):
        return self.walls[3]
    
    def draw(self, width, height):
        left = (screen_width / width) * self.getCol(width)
        right = (screen_width / width) * (self.getCol(width) + 1)
        top = (self.getRow(width)) * (screen_height / height)
        bottom = (self.getRow(width) + 1) * (screen_height / height)
        if self.getRow(width) == 0:
            self.walls[0] = True
        if self.visited:
            pygame.draw.rect(display, (255, 255, 255), (left, top, (right - left), (bottom - top)))
        if self.highlight:
            pygame.draw.rect(display, (255, 0, 0), (left, top, (right - left), (bottom - top)))
        if self.topWall():
            pygame.draw.line(display, (0, 0, 0), (left, top), (right, top))
        
        if self.index >= width * (height - 1):
            self.walls[1] = True
            pygame.draw.line(display, (0, 0, 0), (left, bottom - 1), (right, bottom - 1))
        else:
            self.walls[1] = False
            
        if self.leftWall():
            pygame.draw.line(display, (0, 0, 0), (left, top), (left, bottom))
            
        if self.getCol(width) == width - 1:
            self.walls[3] = True
            pygame.draw.line(display, (0, 0, 0), (right - 1, top), (right - 1, bottom))
        else:self.walls[3] = False

def export(s):
    maze = Maze(s, s)
    maze.go()
    print("go")
    if draw:
        maze.draw()
        pygame.display.flip()
    with open('txtfile.txt', 'w') as file:
        for row in range(0, maze.convertToArray().shape[0]):
            x = (maze.convertToArray()[row, :])
            s = ''
            for i in range(0, len(x)): 
                s = s.join(str(int(x[i])))
                if (i + 1 < len(x)):
                    s = s + ' '
                file.write(s)
            file.write('\n')
            #print(x)
        #for item in maze.convertToArray():
         #   item2 = ''.join(str(item))
         #   item2 = item2.replace('.', '').replace('[', '').replace(']', '')
         #   file.write(str(item2) + '\n')
        
        file.write('\n')
        file.close()
    files = os.listdir('C:/Users/dylan/Documents/Python Scripts/Mazes')
    file_count = len(files) + 1
    string = '2D/maze' + str(file_count) + '.jpeg'
    
    if draw:
        pygame.image.save(display, string)

if __name__ == '__main__':
    if (len(sys.argv) > 1):
        export(int(sys.argv[1]))
    else:
        #export(12)
        s = 20
        maze = Maze(s, s)
        maze.go()
        if draw:
            maze.draw()
            pygame.display.flip()

