import time
import pygame
import sys

#setting up the game information class
class GameInfoBasics: 
    levels = 5 #there are 5 levels to the game
    def __init__(self, level=1): 
        self.level = level  
        self.startGame = False
        self.levelStartTimer = 0  

    #a function for leveling up by incrementing level by 1
    def nextLevel (self):
        self.level += 1
        self.startGame = False #game wont immediately start when we level up

    #a function that will end the game and quit the game
    def endGame(self):   
        pygame.quit()
        sys.exit(0)  
    
    #a function to finish the game when all the levels are passed.
    def finishGame(self):
        return self.level > self.levels #if the current level is more than the amount of levels there are to the game, the game is finished

    #a function to initiate the levels.
    def startLevel(self):
        self.startGame = True 
        self.levelStartTimer = time.time() #to keep track when the level has started.

    #a function that returns the calculated time of the level in process
    def getLevelTimer(self):
        if not self.startGame :
            return 0 # if the game hasnt started, the timer will return 0 as the time
        return round(time.time() - self.levelStartTimer )