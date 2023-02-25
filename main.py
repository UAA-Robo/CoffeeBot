import math
import pygame

if(__name__ ==  "__main__"):
    pygame.init()  # Initialize Pygame Modules

    # Window Initialization
    SCREEN_HEIGHT = 520
    SCREEN_WIDTH = 1020
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Set Window Name
    pygame.display.set_caption('Robot Simulation')
    # Set Pygame Clock
    FPS = 180
    CLOCK = pygame.time.Clock()

    l1 = 100 # Arm Segment Length
    l2 = 100

    # Base Position
    baseX = 260
    baseY = 260
    baseZ = 0
    # Elbow Position
    elbowX = 0
    elbowY = 0
    elbowZ = 0
    # End of Arm position
    handX = 270
    handY = 270
    handZ = 0

    XKey = 0
    YKey = 0
    ZKey = 0
    run = True
    while run:
        # Ensures the simulation runs no faster than FPS
        CLOCK.tick(FPS)
        mousePos = pygame.mouse.get_pos()

        # Handle Keypresses
        for event in pygame.event.get():  # Keypresses
            if event.type == pygame.QUIT:  # If the exit button is pressed this will cause the game to quit
                run = False
            if event.type == pygame.KEYUP:  # If a key is released do stuff.
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    YKey = 0
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    XKey = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ZKey = 0
            if event.type == pygame.KEYDOWN:  # If a key is pressed down do stuff.
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    YKey = -1 if event.key == pygame.K_w else 1
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    XKey = -1 if event.key == pygame.K_a else 1
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    ZKey = -1 if event.key == pygame.K_LEFT else 1

        #If destination is within bounds, move the endpoint towards it
        destX = handX + XKey
        destY = handY + YKey
        destZ = handZ + ZKey
        # Move hand towards destination if destination is in range
        if( (handX - baseX) ** 2 + (handY - baseY) ** 2 + (handZ - baseZ) ** 2< (l1 + l2 - 2)**2
            or
            (destX - baseX) ** 2 + (destY - baseY) ** 2 + (destZ - baseZ) ** 2 < (l1 + l2 - 2)**2
        ):
            handX = destX
            handY = destY
            handZ = destZ

        # Distance between base and hand squared
        c = baseX - handX
        p = baseY - handY
        d = c ** 2 + p ** 2

        # Inner max is to prevent a divide by 0 error
        # Clamp the angle between the base and hand between the range of -1, 1
        a = max(-1, min(1, (d + l1**2 - l2**2) / max((2 * l1 * math.pow(d, 0.5)), 0.001)))
        # Angle from elbow to hand
        # X angle - Y angle * arm orientation
        t = math.atan2(p, c) - math.acos(a) * -1

        # Displace elbow according to angle to hand
        elbowX = handX + l1 * math.cos(t)
        elbowY = handY + l1 * math.sin(t)







        # Rendering
        SCREEN.fill((0, 0, 0))
        scaling = 1
        # X / Y Plane
        pygame.draw.rect(SCREEN,   (50, 50, 50), (10,10,SCREEN_WIDTH/2 - 15, SCREEN_HEIGHT - 20))
        pygame.draw.line(SCREEN,   (255, 255, 255), (elbowX * scaling, elbowY * scaling), (handX * scaling, handY * scaling), 2)
        pygame.draw.circle(SCREEN, (255, 0, 0), (handX * scaling, handY * scaling), 8)
        pygame.draw.line(SCREEN,   (255, 255, 255), (elbowX * scaling, elbowY * scaling), (baseX * scaling, baseY * scaling), 2)
        pygame.draw.circle(SCREEN, (0, 0, 255), (baseX * scaling, baseY * scaling), 8)
        pygame.draw.circle(SCREEN, (0, 255, 0), (elbowX * scaling, elbowY * scaling), 8)
        # Z / Y Plane
        ZYOffset = SCREEN_WIDTH/2 + 265
        pygame.draw.rect(SCREEN, (50, 50, 50), (SCREEN_WIDTH/2 + 5, 10, SCREEN_WIDTH/2 - 15, SCREEN_HEIGHT - 20))
        pygame.draw.circle(SCREEN, (0, 0, 255), (ZYOffset + baseZ * scaling, baseY * scaling), 8)
        pygame.draw.line(SCREEN, (255, 255, 255), (ZYOffset + elbowZ * scaling, elbowY * scaling),(ZYOffset + handZ * scaling, handY * scaling), 2)
        pygame.draw.circle(SCREEN, (0, 255, 0), (ZYOffset + elbowZ * scaling, elbowY * scaling), 8)
        pygame.draw.line(SCREEN, (255, 255, 255), (ZYOffset + elbowZ * scaling, elbowY * scaling),(ZYOffset + baseZ * scaling, baseY * scaling), 2)
        pygame.draw.circle(SCREEN, (255, 0, 0), (ZYOffset + handZ * scaling, handY * scaling), 8)

        pygame.display.update()  # Updates Screen

    pygame.quit()