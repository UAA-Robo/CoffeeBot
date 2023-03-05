import math
import pygame
from ikscreen import IKScreen
from model import Model

if (__name__ == "__main__"):
    pygame.init()  # Initialize Pygame Modules

    ikscreen = IKScreen()
    model = Model()

    # Variables Needed for controls and runtime loop
    XKey = 0
    YKey = 0
    ZKey = 0
    run = True
    while run:
        # Ensures the simulation runs no faster than FPS

        # Handle Keypresses
        for event in pygame.event.get():  # Keypresses
            if event.type == pygame.QUIT:  # If the exit button is pressed this will cause the game to quit
                run = False
            if event.type == pygame.KEYUP:  # If a key is released do stuff.
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    ZKey = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    XKey = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    YKey = 0
            if event.type == pygame.KEYDOWN:  # If a key is pressed down do stuff.
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    ZKey = -1 if event.key == pygame.K_w else 1
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    XKey = -1 if event.key == pygame.K_a else 1
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    YKey = -1 if event.key == pygame.K_LEFT else 1

        # If destination is within bounds, move the endpoint towards it
        model.destX = model.handX + XKey
        model.destY = model.handY + YKey
        model.destZ = model.handZ + ZKey
        model.update()

        # and render the screen
        ikscreen.render(model)

    pygame.quit()
