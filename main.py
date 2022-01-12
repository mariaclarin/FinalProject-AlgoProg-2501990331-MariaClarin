import pygame
import math
import time
from tools import resizeImage

# #creating a function to resize images by factors.
# def resizeImage(img, factor):
#     size = round(img.get_width()* factor), round(img.get_height()* factor) #this will give us a tuple of the new width and height.
#     return pygame.transform.scale(img, size) #scaling the image in pygame.


#loading images into the pygame window. 
grass = resizeImage(pygame.image.load("images/grassbackground.png"), 0.9)
racetrack = resizeImage(pygame.image.load("images/racetrack.png"), 0.9)
racetrackBorder= resizeImage(pygame.image.load("images/racetrackborder.png"), 0.9)
racetrackBorderMask = pygame.mask.from_surface(racetrackBorder)
finishline = resizeImage(pygame.image.load("images/finishline.png"), 0.139)
finishlineMask = pygame.mask.from_surface(finishline)
finishlinePosition = (16.5, 208)
playerHorseImg = resizeImage(pygame.image.load("images/playerhorse.png"), 0.16)
computerHorseImg = resizeImage(pygame.image.load("images/computerhorse.png"), 0.16)


#setting up the pygame window 
width, height = grass.get_width(), grass.get_height()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Mare-a-thon")

def blitRotate (win, image, top_Left, angle):
    rotatedImage = pygame.transform.rotate(image,angle) 
    nRectangle = rotatedImage.get_rect(center=image.get_rect(topleft=top_Left).center)  #to avoid image distortion by rotating the image without changing the x and y coords of the image on the screen
    win.blit(rotatedImage,nRectangle.topleft) 

class Character :
    def __init__ (self, maxVelocity, rotationVelocity):
        self.img = self.image
        self.maxVelocity = maxVelocity
        self.velocity = 0
        self.rotationVelocity = rotationVelocity
        self.angle = 0
        self.x, self.y = self.startingPosition
        self.acceleration = 0.05
    
    def rotate(self, left = False, right = False) :
        if left :
            self.angle += self.rotationVelocity
        elif right :
            self.angle -= self.rotationVelocity
    
    def draw(self, win):
        blitRotate(win, self.img, (self.x, self.y), self.angle )
    
    #a function that allows the car to move forward 
    def moveForward(self):
        self.velocity = min(self.velocity + self.acceleration, self.maxVelocity*2)
        self.move()

    #a function that allows the car to move backward
    def moveBackward(self):
        self.velocity = max(self.velocity - self.acceleration, -self.maxVelocity/2)
        self.move()

    #a function that allows the car to move according to the x and y grid on the display of the pygame window
    def move(self):
        radians = math.radians(self.angle)
        verticalVelocity = math.cos(radians) * self.velocity
        horizontalVelocity = math.sin(radians) * self.velocity

        self.y -= verticalVelocity
        self.x -= horizontalVelocity

    #a function that reduces the speed of the car when theres no movement made by the player. Stops when the velocity = 0 / the car stops
    def reduceSpeed(self):
        self.velocity = max(self.velocity - self.acceleration / 2, 0)
        self.move()
    
    #a function that detects if the player car bumps to any mask (used for the race track border and finish line)
    def bump(self, mask, x=0, y=0):
        playerMask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        bumpPoint = mask.overlap(playerMask, offset)
        return bumpPoint

    #a function that will bounce back the car with the negative amount of velocity the car has at that time
    def bounce(self):
        self.velocity = -self.velocity/2
        self.move()
    
    #a function that resets the player car when the player car reaches the finish line 
    def resetPosition(self):
        self.x, self.y = self.startingPosition
        self.angle = 0
        self.velocity = 0

class Player(Character):
    image = playerHorseImg
    startingPosition = (80,210)

def loadImage(win, images, playerInGame):
    for img, position in images:
        win.blit(img, position)
    playerInGame.draw(window)
    pygame.display.update()

def playerMovement(playerHorse):
    #setting up keyboard keys to be used in game to do actions
    keyboardKeys = pygame.key.get_pressed()
    move = False

    #a and d key on keyboard will work on rotating the car to make turns
    if keyboardKeys[pygame.K_a]:
        playerHorse.rotate(left=True)
    if keyboardKeys[pygame.K_d]:
        playerHorse.rotate(right=True)

    #w and s key on keyboard will work on moving the car forward and backward
    if keyboardKeys[pygame.K_w]:
        move = True
        playerHorse.moveForward()
    if keyboardKeys[pygame.K_s]:
        move = True
        playerHorse.moveBackward()
    
    #if the player car stops stepping on gas (moving forward or moving backwards) the car will slowly reduce its speed (till it stop), unless player press on the gas again
    if not move :
        playerHorse.reduceSpeed()

#setting up the game loop to run the program unless the user quits
run = True
clock = pygame.time.Clock()
images = [(grass,(0,0)), (racetrack,(0,0)), (finishline, finishlinePosition), (racetrackBorder, (0,0))]
playerHorse = Player(3, 2)

while run :
    clock.tick(60) #ensure the while loop cant go faster than 60 fps, so it works synchroniously if used on other computer.
    loadImage(window, images, playerHorse)

    for event in pygame.event.get():    #if we press the quit button, we activate run = False, which exits the while loop and pygame will terminate the program and close the window
        if event.type == pygame.QUIT:
            run = False
            break

    playerMovement(playerHorse)
    if playerHorse.bump(racetrackBorderMask) != None:
        playerHorse.bounce()

    playerFinish= playerHorse.bump(finishlineMask, *finishlinePosition)
    if playerFinish != None:
        if playerFinish[1] == 0:
            playerHorse.bounce()
        else:
            playerHorse.resetPosition()

    

pygame.quit()

