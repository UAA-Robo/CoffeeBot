import math
import pygame

if(__name__ ==  "__main__"):
    pygame.init()  # Initialize Pygame Modules

    # Window Initialization
    SCREEN_HEIGHT = 520
    SCREEN_WIDTH = 1020
    SCREEN_WIDTH = 1525
    SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Set Window Name
    pygame.display.set_caption('Robot Simulation')
    # Set Pygame Clock
    FPS = 180
    CLOCK = pygame.time.Clock()

    l1 = 100 # Arm Segment Length
    l2 = 100

    # Base Position
    baseX = 0
    baseY = 0
    baseZ = 0
    # Elbow Position
    elbowX = 0
    elbowY = 0
    elbowZ = 0
    # End of Arm position
    handX = 50
    handY = 0
    handZ = -50

    XKey = 0
    YKey = 0
    ZKey = 0
    run = True

    def CartesianToCylindrical(x, y, z):
        #Returns p, theta, and z
        return (math.sqrt(x*x + y*y), math.atan2(y, x), z)

    def CylindricalToCartesian(p, theta, z):
        return(p * math.cos(theta), p * math.sin(theta), z)

    def RotateCartesian(x, y, z, rads):

        return (
             x * math.cos(rads) - y * math.sin(rads),
             x * math.sin(rads) + y * math.cos(rads),
             z
                )


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

        #If destination is within bounds, move the endpoint towards it
        destX = handX + XKey
        destY = handY + YKey
        destZ = handZ + ZKey

        # Move hand towards destination if destination is in range or moving to destination will bring it in range
        if( (handX - baseX) ** 2 + (handY - baseY) ** 2 + (handZ - baseZ) ** 2< (l1 + l2 - 2)**2
            or
            (destX - baseX) ** 2 + (destY - baseY) ** 2 + (destZ - baseZ) ** 2 < (l1 + l2 - 2)**2
        ):
            handX = destX
            handY = destY
            handZ = destZ

        #HandXRotated, HandYRotated, HandZRotated = handX, handY, handZ
        #elbowXRotated, elbowYRotated, elbowZRotated = elbowX, elbowY, elbowZ

        rot = CartesianToCylindrical(handX, handY, handZ)[1]
        HandXRotated, HandYRotated, HandZRotated = RotateCartesian(handX, handY, handZ, -rot)
        elbowXRotated, elbowYRotated, elbowZRotated = RotateCartesian(elbowX, elbowY, elbowZ, -rot)

        # Distance between base and hand squared
        c = baseX - HandXRotated
        p = baseZ - HandZRotated
        d = c ** 2 + p ** 2

        # Inner max is to prevent a divide by 0 error
        # Clamp the angle between the base and hand between the range of -1, 1
        a = max(-1, min(1, (d + l1**2 - l2**2) / max((2 * l1 * math.pow(d, 0.5)), 0.001)))
        # Angle from elbow to hand
        # X angle - Y angle * arm orientation
        t = math.atan2(p, c) - math.acos(a) * -1

        # Displace elbow according to angle to hand
        elbowXRotated = HandXRotated + l1 * math.cos(t)
        elbowZRotated = HandZRotated + l1 * math.sin(t)

        handX, handY, handZ = RotateCartesian(HandXRotated, HandYRotated, HandZRotated, rot)# + 0.0174532925)
        elbowX, elbowY, elbowZ = RotateCartesian(elbowXRotated, elbowYRotated, elbowZRotated, rot)# + 0.0174532925)

        AB = math.sqrt(
            (handX - baseX) ** 2 +
            (handY - baseY) ** 2 +
            (handZ - baseZ) ** 2
                       )
        if(AB > l1 + l2 + 0.0001):
            print("DANGER ARM EXCEEDED LENGTH BY :", (l1 + l2) - AB)
        ElbowWarn = math.sqrt(
            (elbowX - baseX) ** 2 +
            (elbowY - baseY) ** 2 +
            (elbowZ - baseZ) ** 2
        )
        if(ElbowWarn > l1 + 0.0001):
            print("DANGER ELBOW EXCEEDED LENGTH BY :", l1 - ElbowWarn)

        handWarn = math.sqrt(
            (handX - elbowX) ** 2 +
            (handY - elbowY) ** 2 +
            (handZ - elbowZ) ** 2
                       )
        if(handWarn > l2 + 0.0001):
            print("DANGER HAND EXCEEDED LENGTH BY :", l2 - handWarn)


        # Rendering
        SCREEN.fill((0, 0, 0))
        scaling = 1
        YOffset = (SCREEN_HEIGHT - 20) / 2
        XOffset = 265
        XHorizontalOffset = 510
        # X / Y Plane Top View
        pygame.draw.rect(SCREEN,   (50, 50, 50), (10,10,XHorizontalOffset - 15, SCREEN_HEIGHT - 20))
        pygame.draw.line(SCREEN,   (255, 255, 255), (XOffset + elbowX * scaling, elbowY * scaling + YOffset), (XOffset + handX * scaling, handY * scaling + YOffset), 2)
        pygame.draw.circle(SCREEN, (255, 0, 0), (XOffset + handX * scaling, handY * scaling + YOffset), 8)
        pygame.draw.line(SCREEN,   (255, 255, 255), (XOffset + elbowX * scaling, elbowY * scaling + YOffset), (XOffset + baseX * scaling, baseY * scaling + YOffset), 2)
        pygame.draw.circle(SCREEN, (0, 0, 255), (XOffset + baseX * scaling, baseY * scaling + YOffset), 8)
        pygame.draw.circle(SCREEN, (0, 255, 0), (XOffset + elbowX * scaling, elbowY * scaling + YOffset), 8)

        # Rotation Angle
        rotX, rotY, rotZ = CylindricalToCartesian(15, rot, 0)
        pygame.draw.line(SCREEN, (255, 255, 0), (XOffset, YOffset), (XOffset + rotX, rotY + YOffset), 2)

        # Z / Y Plane Front View
        ZYOffset = XHorizontalOffset + 265
        pygame.draw.rect(SCREEN, (50, 50, 50), (XHorizontalOffset + 5, 10, XHorizontalOffset - 15, SCREEN_HEIGHT - 20))
        pygame.draw.circle(SCREEN, (0, 0, 255), (ZYOffset + baseY * scaling, baseZ * scaling + YOffset), 8)
        pygame.draw.line(SCREEN, (255, 255, 255), (ZYOffset + elbowY * scaling, elbowZ * scaling + YOffset),(ZYOffset + handY * scaling, handZ * scaling + YOffset), 2)
        pygame.draw.circle(SCREEN, (0, 255, 0), (ZYOffset + elbowY * scaling, elbowZ * scaling + YOffset), 8)
        pygame.draw.line(SCREEN, (255, 255, 255), (ZYOffset + elbowY * scaling, elbowZ * scaling + YOffset),(ZYOffset + baseY * scaling, baseZ * scaling + YOffset), 2)
        pygame.draw.circle(SCREEN, (255, 0, 0), (ZYOffset + handY * scaling, handZ * scaling + YOffset), 8)
        # X / Z Plane Side View
        XZOffset = XHorizontalOffset * 2 + 265
        pygame.draw.rect(SCREEN, (50, 50, 50), (XHorizontalOffset * 2 , 10, XHorizontalOffset - 15, SCREEN_HEIGHT - 20))
        pygame.draw.circle(SCREEN, (0, 0, 255), (XZOffset + baseX * scaling, baseZ * scaling + YOffset), 8)
        pygame.draw.line(SCREEN, (255, 255, 255), (XZOffset + elbowX * scaling, elbowZ * scaling + YOffset), (XZOffset + handX * scaling, handZ * scaling + YOffset), 2)
        pygame.draw.circle(SCREEN, (0, 255, 0), (XZOffset + elbowX * scaling, elbowZ * scaling + YOffset), 8)
        pygame.draw.line(SCREEN, (255, 255, 255), (XZOffset + elbowX * scaling, elbowZ * scaling + YOffset), (XZOffset + baseX * scaling, baseZ * scaling + YOffset), 2)
        pygame.draw.circle(SCREEN, (255, 0, 0), (XZOffset + handX * scaling, handZ * scaling + YOffset), 8)

        pygame.display.update()  # Updates Screen

    pygame.quit()