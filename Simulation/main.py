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

# Stick Bot to Ground
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
target_pos = [2, 2, 2] # change
target_orn = [-1, 0, 0]  # change

ik = chain.inverse_kinematics(target_pos, target_orn, orientation_mode = "X") # returns list of position of each joint




# Zoom in w/ camera
p.resetDebugVisualizerCamera(cameraDistance=1,
                             cameraYaw=50,
                             cameraPitch=-35,
                             cameraTargetPosition=[0, 0, 0])


# Set incrementation
joint_1_inc = ik[1].item() / 10.0
joint_2_inc = ik[2].item() / 10.0
joint_3_inc = ik[3].item() / 10.0
joint_4_inc = ik[4].item() / 10.0
joint_5_inc = ik[5].item() / 10.0
joint_6_inc = ik[6].item() / 10.0

while True:

    # move joints towards position
    # p.setJointMotorControl2(robot, joints["joint_L1"], p.POSITION_CONTROL, joint_1_inc)
    # p.setJointMotorControl2(robot, joints["joint_L2"], p.POSITION_CONTROL, joint_2_inc)
    # p.setJointMotorControl2(robot, joints["joint_L3"], p.POSITION_CONTROL, joint_3_inc)
    # p.setJointMotorControl2(robot, joints["joint_L4"], p.POSITION_CONTROL, joint_4_inc)
    # p.setJointMotorControl2(robot, joints["joint_L5"], p.POSITION_CONTROL, joint_5_inc)
    # p.setJointMotorControl2(robot, joints["joint_L6"], p.POSITION_CONTROL, joint_6_inc)


    p.setJointMotorControl2(robot, joints["joint_L1"], p.POSITION_CONTROL, ik[1].item())
    p.setJointMotorControl2(robot, joints["joint_L2"], p.POSITION_CONTROL, ik[2].item())
    p.setJointMotorControl2(robot, joints["joint_L3"], p.POSITION_CONTROL, ik[3].item())
    p.setJointMotorControl2(robot, joints["joint_L4"], p.POSITION_CONTROL, ik[4].item())
    p.setJointMotorControl2(robot, joints["joint_L5"], p.POSITION_CONTROL, ik[5].item())
    p.setJointMotorControl2(robot, joints["joint_L6"], p.POSITION_CONTROL, ik[6].item())

    p.stepSimulation()

    time.sleep(1/50)

p.disconnect()
