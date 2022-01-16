import pygame
import math
import sys
from gameinfo import GameInfoBasics
from imagetools import resizeImage, blitRotate, displayTextCentered
from movementtools import playerMovement

#initializing all pygame modules
pygame.init()

#music settings 
music = pygame.mixer.music.load("music/music.mp3")  
pygame.mixer.music.play(-1) #plays background music

#load sound effects for specific uses
bumpSound = pygame.mixer.Sound("music/bonk.mp3") #sound effect whenever we bump on the track border
poopSound = pygame.mixer.Sound("music/poop.mp3") #sound effect whenever we step over the poop 
rainbowSound = pygame.mixer.Sound("music/wow.mp3")  #sound effect whenever we step on the rainbow lane
booSound = pygame.mixer.Sound("music/boo.mp3") #sound effect when we lose the game
winSound = pygame.mixer.Sound("music/win.mp3") #sound effect whenever we win a level

#loading images into the pygame window. 
#resizeImage function is defined in imagetools.py
grass = resizeImage(pygame.image.load("images/grass.png"), 0.9)
racetrack = resizeImage(pygame.image.load("images/racetrack.png"), 0.9)
racetrackBorder= resizeImage(pygame.image.load("images/racetrackborder.png"), 0.9)
racetrackBorderMask = pygame.mask.from_surface(racetrackBorder)
finishline = resizeImage(pygame.image.load("images/finishline.png"), 0.139)
finishlineMask = pygame.mask.from_surface(finishline)
finishlinePosition = (16.5, 208)
poop = resizeImage(pygame.image.load("images/poop.png"), 0.3)
poopMask = pygame.mask.from_surface(poop)
poopPosition1 = (1090, 300)
poopPosition2 = (670, 600)
poopPosition3 = (30, 360)
rainbow = resizeImage(pygame.image.load("images/rainbow.png"), 0.35)
rainbowMask = pygame.mask.from_surface(rainbow)
rainbowPosition1 = (950, 890)
rainbowPosition2 = (400, 110)
rainbowPosition3 = (260, 500)
playerHorseImg = resizeImage(pygame.image.load("images/playerhorse.png"), 0.16)
computerHorseImg = resizeImage(pygame.image.load("images/computerhorse.png"), 0.16)


#setting up the pygame window 
width, height = grass.get_width(), grass.get_height() #the width and the height of the pygame window will be the width and the height of the grass background image
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mare-a-thon")
gameFont = pygame.font.SysFont("comicsans", 30) 

#a list containing tuples of coordinates for the computer car to use as a route/path
path = [(55, 139.360), (273, 75), (714, 76), (1040, 77), (1150, 234) , (1150, 419), (1114, 679), (1092, 882), (735, 824), (723, 500), (673, 369), (484, 383), (396, 538), (102, 535), (30,0)]

#parent class (abstract type) for the game characters (will be divided into the computer and the player)
class Character :
    def __init__ (self, maxVelocity, rotationVelocity):
        self.img = self.image
        self.maxVelocity = maxVelocity
        self.velocity = 0
        self.rotationVelocity = rotationVelocity
        self.angle = 0
        self.x, self.y = self.startingPosition
        self.acceleration = 0.05
    
    #a function to rotate the image of the character to be able to move and turn right and left
    def rotate(self, left = False, right = False) :
        if left :
            self.angle += self.rotationVelocity
        elif right :
            self.angle -= self.rotationVelocity
    
    #a function that displays the rotated image of the character 
    #blitRotate is defined in the imagetools.py file
    def draw(self, win):
        blitRotate(win, self.img, (self.x, self.y), self.angle )
    
    #a function that allows the character to move forward 
    def moveForward(self):
        self.velocity = min(self.velocity + self.acceleration, self.maxVelocity*2)
        self.move()

    #a function that allows the character to move backward
    def moveBackward(self):
        self.velocity = max(self.velocity - self.acceleration, -self.maxVelocity/2)
        self.move()

    #a function that allows the character to move according to the x and y grid on the display of the pygame window
    def move(self):
        radians = math.radians(self.angle)
        verticalVelocity = math.cos(radians) * self.velocity
        horizontalVelocity = math.sin(radians) * self.velocity

        self.y -= verticalVelocity
        self.x -= horizontalVelocity

    #a function that reduces the speed of the character when theres no movement made by the player. Stops when the velocity = 0 / the car stops
    def reduceSpeed(self):
        self.velocity = max(self.velocity - self.acceleration / 2, 0)
        self.move()
    
    #a function that detects if the player bumps to any mask (used for the obstacles, boundaries, and boosts)
    def bump(self, mask, x=0, y=0):
        playerMask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        bumpPoint = mask.overlap(playerMask, offset)
        return bumpPoint

    #a function that allows the character to activate an acceleration boost by incrementing the self.acceleration 
    def accelerationBoost(self):
        self.acceleration += 0.1
        self.move()

    #a function that will bounce back the character with the negative amount of velocity the character has at that time
    def bounce(self):
        self.velocity = -self.velocity
        self.move()
    
    #a function that resets the player character to the starting condition
    def resetPosition(self):
        self.x, self.y = self.startingPosition
        self.angle = 0
        self.velocity = 0

#child class for the player character (concrete type) that inherits the parent class
class Player(Character):
    image = playerHorseImg
    startingPosition = (80,210)

#child class for the computer character (concrete type) that inherits the parent class
class Computer(Character):
    image = computerHorseImg
    startingPosition = (40,210)
    
    def __init__(self, maxVelocity, rotationVelocity, path =[]):
        super().__init__(maxVelocity, rotationVelocity)
        self.path = path
        self.currentPoint = 0
        self.velocity = maxVelocity
    
    #function tools i use to find the pathway coordinates for the computer character
    def drawPoints(self, win):
        for point in self.path:
            pygame.draw.circle(win, (255, 0, 0), point, 5) #draws a circle on our window, rgb 255 0 0, point as center of drawing, and circle radius of 5
    
    def draw(self, win):
        super().draw(win)
        # self.drawPoints(win) #this function draws the dots indicating the path of the computer horse
    
    #a function that calculates the angle for our computer horse to move to in the direction of.
    def calculateAngle(self):
        desiredX, desiredY = self.path[self.currentPoint] #calculate the displacement of the x and y coords between the next point and the current computer horse position
        xDifference = desiredX - self.x
        yDifference = desiredY - self.y

        if yDifference == 0: #avoid zero division errors
            desiredRadianAngle = math.pi/2 
        else:
            desiredRadianAngle = math.atan(xDifference/yDifference) #calculation of the angle formula
        
        if desiredY > self.y: #if the next point is lower on the screen than the current point (lower y coords) we need to make sure that we have to add a whole 180 degrees to the angle to ensure the character is facing down.
            desiredRadianAngle += math.pi 
        
        angleDifference = self.angle = math.degrees(desiredRadianAngle) #finding the difference of angles of our current angle and the desired angle to move to and based on whether the number is negative or positive,
        if angleDifference >= 180:                                      #we will find out whether the computer horse will move right or left.
            angleDifference -= 360 #if the difference of angle is larger than 180 degrees, we have to decrease the angle with 360 to make sure we have the right direction.

        if angleDifference > 0:
            self.angle -= min(self.rotationVelocity, abs(angleDifference)) #to avoid potentially passing over the desired angle if in an instance our rotation velocity is bigger than the angle we use the min()
        else:
            self.angle += min(self.rotationVelocity, abs(angleDifference))
    
    #a function that checks whether or not we move to the next point when we collide with the current point.
    def updatePathPoint(self):
        target = self.path[self.currentPoint]
        rectangle = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        if rectangle.collidepoint(*target):
            self.currentPoint += 1

    #a function to allow the computer horse to move to a specific point
    def move(self):
        if self.currentPoint >= len(self.path):  #ensuring that we have a point to move to, this avoids errors of our computer horse moving to a non existent point
            return
        
        self.calculateAngle()  #calling the function so we can shift the computer horse according to the calculated angle
        self.updatePathPoint()
        super().move() #call the move method from the parent class
    
    #a function used to set level settings for the computer horse for everytime we level up
    def levelUp(self, level):
        self.resetPosition()
        self.velocity = self.maxVelocity + (level-1) * 0.5 #increase the maximum velocity of the computer horse faster by 0.5 x (the current level -1)
        self.currentPoint = 0


#creating a function to display images in the pygame window
def loadImage(win, images, playerHorse, computerHorse, gameplay):
    for img, position in images:
        win.blit(img, position)

    #displaying the current level info in the bottom left corner of the pygame display
    levelinfo = gameFont.render(f"Level {gameplay.level}", 1, (0,0,0))
    win.blit(levelinfo, (40, height - levelinfo.get_height() -100)) 

    #displaying the time info in the bottom left corner of the pygame display
    timerinfo = gameFont.render(f"Time : {gameplay.getLevelTimer()} s", 1, (0,0,0))
    win.blit(timerinfo, (40, height - timerinfo.get_height() -70)) 

    #displaying the speed info in the bottom left corner of the pygame display
    speedinfo = gameFont.render(f"Speed : {round(playerHorse.velocity, 1)}", 1, (0,0,0))
    win.blit(speedinfo, (40, height - speedinfo.get_height() -40)) 

    playerHorse.draw(window)
    computerHorse.draw(window)
    pygame.display.update()

#a function to take care of every bumps/boost activation
def bumpsAndBoosts(playerHorse, computerHorse, gameplay):
    #if the player hits/bumps into the racetrack borders, the player will bounce back with the negative amount of the same velocity as when he initially bumped.
    if playerHorse.bump(racetrackBorderMask) != None:
        playerHorse.bounce()
        bumpSound.play()

    #Finishline setups
    #1. If player finishes first
    playerFinish= playerHorse.bump(finishlineMask, *finishlinePosition)
    if playerFinish != None:
        # print(playerFinish)    #the tool i use to get the position/coordinate of the top of the finish line
        if playerFinish[1] == 43:
            playerHorse.bounce()    #to prevent the player from cheating and just reversing to the finishline, they will bounce back and it wont count as a finish
        else:
            gameplay.nextLevel()    #increment the level by 1
            playerHorse.resetPosition()
            computerHorse.levelUp(gameplay.level) #when the player hits the finishline and finishes the lap, the player and the computer will both reset the position to the initial position 
            winSound.play()
    # 2. If the computer finishes first
    computerFinish = computerHorse.bump(finishlineMask, *finishlinePosition)
    if computerFinish != None:
        booSound.play()
        displayTextCentered(window, gameFont, "GAME OVER! Better luck next time :P")
        pygame.display.update()
        pygame.time.wait(5000)
        gameplay.endGame()

    #Obstacle Setups
    #if the player hits the poop obstacle, they will bounce back with the negative amount of the same velocity as when he initially bumped
    playerPoopHit= playerHorse.bump(poopMask, *poopPosition1)
    if playerPoopHit != None:
        playerHorse.bounce()    #setup for position 1 of the poop
        poopSound.play()
    playerPoopHit= playerHorse.bump(poopMask, *poopPosition2)
    if playerPoopHit != None:
        playerHorse.bounce()    #setup for position 2 of the poop
        poopSound.play()
    playerPoopHit= playerHorse.bump(poopMask, *poopPosition3)
    if playerPoopHit != None:
        playerHorse.bounce()    #setup for position 3 of the poop
        poopSound.play()        

    #Boost Setups 
    #if the player steps on the rainbow dash square, they will receive an acceleration boost.
    playerRainbowBoost= playerHorse.bump(rainbowMask, *rainbowPosition1)
    if playerRainbowBoost != None:
        playerHorse.accelerationBoost() #setup for position 1 of the boost
        rainbowSound.play()
    playerRainbowBoost= playerHorse.bump(rainbowMask, *rainbowPosition2)
    if playerRainbowBoost != None:
        playerHorse.accelerationBoost() #setup for position 2 of the boost
        rainbowSound.play()
    playerRainbowBoost= playerHorse.bump(rainbowMask, *rainbowPosition3)
    if playerRainbowBoost != None:
        playerHorse.accelerationBoost() #setup for position 3 of the boost
        rainbowSound.play()

#setting up the game loop to run the program 
run = True
clock = pygame.time.Clock()
images = [(grass,(0,0)), (racetrack,(0,0)), (finishline, finishlinePosition), (racetrackBorder, (0,0)), (poop, poopPosition1), 
(poop, poopPosition2), (poop, poopPosition3), (rainbow, rainbowPosition1), (rainbow, rainbowPosition2), (rainbow, rainbowPosition3)]
playerHorse = Player(4, 2)
computerHorse = Computer(3.5,2, path)
gameplay = GameInfoBasics() 

while run :

    clock.tick(60) #ensure the while loop cant go faster than 60 fps, so it works synchronously if used on other computer.
    loadImage(window, images, playerHorse, computerHorse, gameplay)

    #a while loop that is active when the level hasn't started
    while not gameplay.startGame:
        displayTextCentered(window, gameFont, f"Press any key to start! Current level is {gameplay.level}")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)               #if player quits the window before they start the game, it will quit the game 
            if event.type == pygame.KEYDOWN:
                gameplay.startLevel() #if player press any key down, the game will start the level, thus exiting this while loop 

    for event in pygame.event.get():    #if we press the quit button, we activate run = False, which exits the while loop and pygame will terminate the program and close the window
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit(0)  #if player quits the window when the game has started, it will quit the game 
    
        if event.type == pygame.MOUSEBUTTONDOWN:   #this is the function i use to find coordinates of the computer path and after i just print(computerCar.path) to my terminal and copas it to my path =[]
            pos = pygame.mouse.get_pos()
            computerHorse.path.append(pos)

    playerMovement(playerHorse)
    computerHorse.move()
    bumpsAndBoosts(playerHorse, computerHorse, gameplay)

    #if the player has completed all 5 levels, they win, so this is the if statement to check if thats the case
    if gameplay.finishGame():
        displayTextCentered(window, gameFont, "YOU WIN !!! Thanks for playing!")
        pygame.display.update()
        pygame.time.wait(5000) 
        gameplay.endGame()

# print(computerHorse.path)  #function to print path added alongside the other functions to find the path for the computer horse
print("Thank you for playing Mare-a-thon")
pygame.quit()

