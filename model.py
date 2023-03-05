import math

""" 
helper functions to do some math for us convenientyl
"""


def cartesian_to_cylindrical(x, y, z):
    # Converts Cartesian Coordiantes to Crylindrical coordinates Returns p, theta, and z
    return math.sqrt(x * x + y * y), math.atan2(y, x), z


def cylindrical_to_cartesian(p, theta, z):
    # Converts cylindrical coordinates to cartesian coordinates
    return p * math.cos(theta), p * math.sin(theta), z


def rotate_cartesian(x, y, z, rads):
    # Rotates a point around 0,0 using radians
    return (x * math.cos(rads) - y * math.sin(rads),
            x * math.sin(rads) + y * math.cos(rads),
            z)


class Model:

    def __init__(self,
                 # Arm Segment Length
                 l1=100,  # Base to Elbow
                 l2=100,  # Elbow to Hand

                 # Base Position
                 baseX=0,
                 baseY=0,
                 baseZ=0,
                 # Elbow Position
                 elbowX=25,
                 elbowY=0,
                 elbowZ=25,
                 # End of Arm position
                 handX=50,
                 handY=0,
                 handZ=-50,
                 ):
        # Arm Segment Length
        self.l1 = l1  # Base to Elbow
        self.l2 = l2  # Elbow to Hand

        # Base Position
        self.baseX = baseX
        self.baseY = baseY
        self.baseZ = baseZ
        # Elbow Position
        self.elbowX = elbowX
        self.elbowY = elbowY
        self.elbowZ = elbowZ
        # End of Arm position
        self.handX = handX
        self.handY = handY
        self.handZ = handZ

        self.destX = self.handX
        self.destY = self.handY
        self.destZ = self.handZ

    def update(self):
        # Move hand towards destination if destination is in range or moving to destination will bring it in range
        if (
                (self.handX - self.baseX) ** 2 + (self.handY - self.baseY) ** 2 + (self.handZ - self.baseZ) ** 2 < (
                self.l1 + self.l2 - 2) ** 2
                or
                (self.destX - self.baseX) ** 2 + (self.destY - self.baseY) ** 2 + (self.destZ - self.baseZ) ** 2 < (
                self.l1 + self.l2 - 2) ** 2
        ):
            self.handX = self.destX
            self.handY = self.destY
            self.handZ = self.destZ

        # Get rotations of elbow relative to the Y plane and hand relative to base
        rotHand = cartesian_to_cylindrical(self.handX, self.handY, self.handZ)[1]
        rotElbow = cartesian_to_cylindrical(self.elbowX, self.elbowY, self.elbowZ)[1]

        # Rotate the points to be 0 on the Y plane
        HandXRotated, HandYRotated, HandZRotated = rotate_cartesian(self.handX, self.handY, self.handZ, -rotHand)
        elbowXRotated, elbowYRotated, elbowZRotated = rotate_cartesian(self.elbowX, self.elbowY, self.elbowZ, -rotElbow)

        # Distance between base and hand squared
        c = self.baseX - HandXRotated
        p = self.baseZ - HandZRotated
        d = c ** 2 + p ** 2

        # Inner max is to prevent a divide by 0 error
        # Clamp the angle between the base and hand between the range of -1, 1
        a = max(-1, min(1, (d + self.l1 ** 2 - self.l2 ** 2) / max((2 * self.l1 * math.pow(d, 0.5)), 0.001)))

        # Angle from elbow to hand
        # X angle - Y angle * arm orientation
        t = math.atan2(p, c) - math.acos(a) * -1

        # Displace elbow according to angle to hand
        elbowXRotated = HandXRotated + self.l1 * math.cos(t)
        elbowZRotated = HandZRotated + self.l1 * math.sin(t)

        # Rotate the arm back out the Y plane and back into its proper rotation
        # Commented out values make the arm spin in a circle, they are the equivalent to one degree in radians.
        self.handX, self.handY, self.handZ = rotate_cartesian(HandXRotated, HandYRotated, HandZRotated,
                                                              rotHand)  # + 0.0174532925)
        self.elbowX, self.elbowY, self.elbowZ = rotate_cartesian(elbowXRotated, elbowYRotated, elbowZRotated,
                                                                 rotElbow + (rotHand - rotElbow))  # + 0.0174532925)

        # Warnings for when the simulation doesn't work properly
        # Distance from Base to hand Exceeds total arm length
        ArmLengthWarn = math.sqrt(
            (self.handX - self.baseX) ** 2 +
            (self.handY - self.baseY) ** 2 +
            (self.handZ - self.baseZ) ** 2
        )
        if ArmLengthWarn > self.l1 + self.l2 + 0.00001:
            print("DANGER! ARM EXCEEDED LENGTH BY :", (self.l1 + self.l2) - ArmLengthWarn)
        # Distance from base to elbow is exceeded
        ElbowWarn = math.sqrt(
            (self.elbowX - self.baseX) ** 2 +
            (self.elbowY - self.baseY) ** 2 +
            (self.elbowZ - self.baseZ) ** 2
        )
        if ElbowWarn > self.l1 + 0.00001:
            print("DANGER! ELBOW EXCEEDED LENGTH BY :", self.l1 - ElbowWarn)
        # Distance from elbow to hand is exceeded
        handWarn = math.sqrt(
            (self.handX - self.elbowX) ** 2 +
            (self.handY - self.elbowY) ** 2 +
            (self.handZ - self.elbowZ) ** 2
        )
        if handWarn > self.l2 + 0.00001:
            print("DANGER! HAND EXCEEDED LENGTH BY :", self.l2 - handWarn)
