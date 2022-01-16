import pygame

#creating a function to resize images by factors.
def resizeImage(img, factor):
    size = round(img.get_width()* factor), round(img.get_height()* factor) #this will give us a tuple of the new width and height.
    return pygame.transform.scale(img, size) #scaling the image in pygame.


#creating a function that will return a rotated image of an image based off of an angle
def blitRotate (win, image, top_Left, angle):
    rotatedImage = pygame.transform.rotate(image,angle) 
    nRectangle = rotatedImage.get_rect(center=image.get_rect(topleft=top_Left).center)  #to avoid image distortion by rotating the image without changing the x and y coords of the image on the screen
    win.blit(rotatedImage,nRectangle.topleft) 

#a function to blit/display a text 
def displayTextCentered(win, font, text):
    render = font.render(text, 1, (0, 0, 0)) #text that we want to render, 1 is for antialiasing, (0, 0, 0) is the rgb color
    win.blit(render, (win.get_width()/2 - render.get_width()/2, 220))

