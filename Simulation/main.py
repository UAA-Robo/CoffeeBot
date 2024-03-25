import pybullet as p
import time
import pybullet_data

physics_client = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
p.setGravity(0,0,-10)

# Load ground
plane_ID = p.loadURDF("plane.urdf")

# Load robot
start_pos = [0,0,0]
start_orientation = p.getQuaternionFromEuler([0,0,0])
robot = p.loadURDF("robot.urdf",start_pos, start_orientation)


# Get joints

joint_L1 = "joint_L1"  
joint_L1_index = -1
for i in range(p.getNumJoints(robot)):
    if p.getJointInfo(robot, i)[1].decode('UTF-8') == joint_L1:
        joint_L1_index = i
        break


# Check if the joint index was found
if joint_L1_index == -1:
    print("Joint not found.")
else:
    # Initial Position
    position = 0.0  

    last_time = time.time()
    INCREMENT_INTERVAL = 0.1  # Time in seconds to wait before next increment
    POSITION_INCREMENT = 0.01  # Amount by which to increase the joint position

    # Control the joint to move to the target position
    # Simulation loop
    while True:
        # Get the current time
        current_time = time.time()
        print(current_time)

        # Check if it's time to update the joint position
        if current_time - last_time >= INCREMENT_INTERVAL:
            # Update the target position
            position += POSITION_INCREMENT
            # Apply the new target position
            p.setJointMotorControl2(robot, joint_L1_index, p.POSITION_CONTROL, targetPosition=position)
            # Reset the timer
            last_time = current_time

        # Step the simulation
        p.stepSimulation()

        # Sleep to simulate real time (this can be adjusted or removed as needed)
        time.sleep(1/240)

# Disconnect when done
p.disconnect()



# for i in range (10000):
#     p.stepSimulation()
#     time.sleep(1./240.)

# cubePos, cubeOrn = p.getBasePositionAndOrientation(robot)
# print(cubePos,cubeOrn)
# p.disconnect()