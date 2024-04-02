import pybullet as p
import time
import pybullet_data

#new imports
import ikpy.chain

physics_client = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)

# Load ground
plane_ID = p.loadURDF("plane.urdf")

# Load robot
start_pos = [0,0,0]
start_orientation = p.getQuaternionFromEuler([0,0,0])
robot = p.loadURDF("robot.urdf",start_pos, start_orientation)

# Stick Bot to Ground *Prevents tipping
ground_joint = p.createConstraint(plane_ID, -1, 
                                  robot, -1, 
                                  jointType = p.JOINT_FIXED, 
                                  jointAxis = [0,0,0], 
                                  parentFramePosition = [-0.0274562034602567, -0.00137265400595656, 0.031237920982338], 
                                  childFramePosition = [0.0274562034602567, 0.00137265400595656, -0.031237920982338])



# Map joint names (from urdf) to index values "joint_L1" -> "joint_L6"
joints = {}

for i in range(p.getNumJoints(robot)):
    joint_name = p.getJointInfo(robot, i)[1].decode('UTF-8') 
    joints[joint_name] = i


"""
Link Activity:
-FALSE = base_link
-TRUE = link_L1
- joint_L2
-TRUE = link_L2
- joint_L2
-TRUE = link_L3
- joint_L3
-TRUE = link_L4
- joint_L4
-TRUE = link_L5
- joint_L5
-TRUE = link_L6
- joint_L6

"""


chain = ikpy.chain.Chain.from_urdf_file("robot.urdf", active_links_mask = [False, True, True, True, True, True, True])
target_pos = [0, 0, 0] # change
target_orn = [1, 0, 0] # change

# ik = chain.inverse_kinematics(target_pos, target_orn, orientation_mode = "Y") # returns list of position of each joint
ik = chain.inverse_kinematics(target_pos, target_orientation=None, orientation_mode=None)

# Zoom in w/ camera
p.resetDebugVisualizerCamera(cameraDistance=1,
                             cameraYaw=90, #50
                             cameraPitch=-35, #-35
                             cameraTargetPosition=[0, 0, 0])

# check if angle position/rotation are out of bounds
for i in ik:
    if i.item() > 2:
        print("Out of range")


# Set incrementation
joint_1_inc = ik[1].item() / 240.0
joint_2_inc = ik[2].item() / 240.0
joint_3_inc = ik[3].item() / 240.0
joint_4_inc = ik[4].item() / 240.0
joint_5_inc = ik[5].item() / 240.0
joint_6_inc = ik[6].item() / 240.0

# Final positions
final_1 = joint_1_inc
final_2 = joint_2_inc
final_3 = joint_3_inc
final_4 = joint_4_inc
final_5 = joint_5_inc
final_6 = joint_6_inc

while True:


    # if joint hasn't reached final position
    if (final_1 < ik[1].item()):

        # move joints towards position
        p.setJointMotorControl2(robot, joints["joint_L1"], p.POSITION_CONTROL, final_1)
        p.setJointMotorControl2(robot, joints["joint_L2"], p.POSITION_CONTROL, final_2)
        p.setJointMotorControl2(robot, joints["joint_L3"], p.POSITION_CONTROL, final_3)
        p.setJointMotorControl2(robot, joints["joint_L4"], p.POSITION_CONTROL, final_4)
        p.setJointMotorControl2(robot, joints["joint_L5"], p.POSITION_CONTROL, final_5)
        p.setJointMotorControl2(robot, joints["joint_L6"], p.POSITION_CONTROL, final_6)

        # update final positions
        final_1 += joint_1_inc
        final_2 += joint_2_inc
        final_3 += joint_3_inc
        final_4 += joint_4_inc
        final_5 += joint_5_inc
        final_6 += joint_6_inc

    else:
        # paste over code-- fix later
        # new position
        target_pos[0] = int(input(""))
        target_pos[1] = int(input(""))
        target_pos[2] = int(input(""))

        ik = chain.inverse_kinematics(target_pos, target_orientation=None, orientation_mode=None)

        # check if angle position/rotation are out of bounds
        for i in ik:
            if i.item() > 2:
                print("Out of range")

        # Set incrementation
        joint_1_inc = ik[1].item() / 240.0
        joint_2_inc = ik[2].item() / 240.0
        joint_3_inc = ik[3].item() / 240.0
        joint_4_inc = ik[4].item() / 240.0
        joint_5_inc = ik[5].item() / 240.0
        joint_6_inc = ik[6].item() / 240.0

        # Final positions
        final_1 = joint_1_inc
        final_2 = joint_2_inc
        final_3 = joint_3_inc
        final_4 = joint_4_inc
        final_5 = joint_5_inc
        final_6 = joint_6_inc

    p.stepSimulation()

    time.sleep(1/240)

p.disconnect()
