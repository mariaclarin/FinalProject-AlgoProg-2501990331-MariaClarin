import pygame 

def playerMovement(playerHorse):
    #setting up keyboard keys to be used in game to do actions
    keyboardKeys = pygame.key.get_pressed()
    move = False

    #a and d key on keyboard will work on rotating the character to make turns
    if keyboardKeys[pygame.K_a]:
        playerHorse.rotate(left=True)
    if keyboardKeys[pygame.K_d]:
        playerHorse.rotate(right=True)

    #w and s key on keyboard will work on moving the character forward and backward
    if keyboardKeys[pygame.K_w]:
        move = True
        playerHorse.moveForward()
    if keyboardKeys[pygame.K_s]:
        move = True
        playerHorse.moveBackward()
    
    #if the player character stops moving the character will slowly reduce its speed (till it stop)
    if not move :
        playerHorse.reduceSpeed()


