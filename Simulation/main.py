import pybullet as p
import time
import pybullet_data

class Simulation:

    joint_positions = {}
    motor_speeds = {}
    revolutions_per_step = 1 / 200.0

    def setup(self) -> None:
        physics_client = p.connect(p.GUI)#or p.DIRECT for non-graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally
        p.setGravity(0,0,-10)

        # Load ground
        plane_ID = p.loadURDF("plane.urdf")

        self.joint_positions["joint_L1"] = 0.0
        self.joint_positions["joint_L2"] = 0.0
        self.joint_positions["joint_L3"] = 0.0
        self.joint_positions["joint_L4"] = 0.0
        self.joint_positions["joint_L5"] = 0.0
        self.joint_positions["joint_L6"] = 0.0
        self.motor_speeds["joint_L1"] = 0.0
        self.motor_speeds["joint_L2"] = 0.0
        self.motor_speeds["joint_L3"] = 0.0
        self.motor_speeds["joint_L4"] = 0.0
        self.motor_speeds["joint_L5"] = 0.0
        self.motor_speeds["joint_L6"] = 0.0

        # Load robot
        start_pos = [0,0,0]
        start_orientation = p.getQuaternionFromEuler([0,0,0])
        self.robot = p.loadURDF("Simulation/robot.urdf",start_pos, start_orientation)


        # Map joint names (from urdf) to index values "joint_L1" -> "joint_L6"
        self.joints = {}  

        for i in range(p.getNumJoints(self.robot)):
            joint_name = p.getJointInfo(self.robot, i)[1].decode('UTF-8') 
            self.joints[joint_name] = i


        # Zoom in w/ camera
        p.resetDebugVisualizerCamera(cameraDistance=1,
                                    cameraYaw=50,
                                    cameraPitch=-35,
                                    cameraTargetPosition=[0, 0, 0])

    def update_join_position(self, joint: int, new_position: float) -> None:
        self.joint_positions[f"joint_L{joint}"] = new_position

    def set_joint_speed(self, joint: int, speed: float) -> None:
        self.motor_speeds[f"joint_L{joint}"] = speed


    # Initial Position
    position = 0.0  

    # last_time = time.time()
    INCREMENT_INTERVAL = 0.1  # Time in seconds to wait before next increment
    POSITION_INCREMENT = 0.05  # Amount by which to increase the joint position

    def _limit_joint_position(self, joint: int) -> None:
        if joint == 1:
            if self.joint_positions[f"joint_L{joint}"] >= 2.0: self.joint_positions[f"joint_L{joint}"] = 2.0
            if self.joint_positions[f"joint_L{joint}"] <= -2.0: self.joint_positions[f"joint_L{joint}"] = -2.0
        if joint == 2:
            if self.joint_positions[f"joint_L{joint}"] >= 2.0: self.joint_positions[f"joint_L{joint}"] = 2.0
            if self.joint_positions[f"joint_L{joint}"] <= -2.0: self.joint_positions[f"joint_L{joint}"] = -2.0
        if joint == 3:
            if self.joint_positions[f"joint_L{joint}"] >= 2.0: self.joint_positions[f"joint_L{joint}"] = 2.0
            if self.joint_positions[f"joint_L{joint}"] <= -2.0: self.joint_positions[f"joint_L{joint}"] = -2.0
        if joint == 4:
            if self.joint_positions[f"joint_L{joint}"] >= 2.0: self.joint_positions[f"joint_L{joint}"] = 2.0
            if self.joint_positions[f"joint_L{joint}"] <= -2.0: self.joint_positions[f"joint_L{joint}"] = -2.0
        if joint == 5:
            if self.joint_positions[f"joint_L{joint}"] >= 2.0: self.joint_positions[f"joint_L{joint}"] = 2.0
            if self.joint_positions[f"joint_L{joint}"] <= -2.0: self.joint_positions[f"joint_L{joint}"] = -2.0
        if joint == 6:
            if self.joint_positions[f"joint_L{joint}"] >= 2.0: self.joint_positions[f"joint_L{joint}"] = 2.0
            if self.joint_positions[f"joint_L{joint}"] <= -2.0: self.joint_positions[f"joint_L{joint}"] = -2.0


    def start(self) -> None:
        # Increment all joint(s) by POSITION_INCREMENT every INCREMENT_INTERVAL
        # Bounds of rotation limited by urdf
        print(self.INCREMENT_INTERVAL)
        
        current_time = time.time()
        last_time = current_time

        while True:

            current_time = time.time()

            # Check if it's time to update the joint position
            # if current_time - last_time >= self.INCREMENT_INTERVAL:
                # position += self.POSITION_INCREMENT
                

            self.joint_positions["joint_L1"] += (self.motor_speeds["joint_L1"] * (current_time - last_time))
            self._limit_joint_position(1)
            self.joint_positions["joint_L2"] += (self.motor_speeds["joint_L2"] * (current_time - last_time))
            self._limit_joint_position(2)
            self.joint_positions["joint_L3"] += (self.motor_speeds["joint_L3"] * (current_time - last_time))
            self._limit_joint_position(3)
            self.joint_positions["joint_L4"] += (self.motor_speeds["joint_L4"] * (current_time - last_time))
            self._limit_joint_position(4)
            self.joint_positions["joint_L5"] += (self.motor_speeds["joint_L5"] * (current_time - last_time))
            self._limit_joint_position(5)
            self.joint_positions["joint_L6"] += (self.motor_speeds["joint_L6"] * (current_time - last_time))
            self._limit_joint_position(6)                

            # Increments positions of all joints
            p.setJointMotorControl2(self.robot, self.joints["joint_L1"], p.POSITION_CONTROL, targetPosition=self.joint_positions["joint_L1"])
            p.setJointMotorControl2(self.robot, self.joints["joint_L2"], p.POSITION_CONTROL, targetPosition=self.joint_positions["joint_L2"])
            p.setJointMotorControl2(self.robot, self.joints["joint_L3"], p.POSITION_CONTROL, targetPosition=self.joint_positions["joint_L3"])
            p.setJointMotorControl2(self.robot, self.joints["joint_L4"], p.POSITION_CONTROL, targetPosition=self.joint_positions["joint_L4"])
            p.setJointMotorControl2(self.robot, self.joints["joint_L5"], p.POSITION_CONTROL, targetPosition=self.joint_positions["joint_L5"])
            p.setJointMotorControl2(self.robot, self.joints["joint_L6"], p.POSITION_CONTROL, targetPosition=self.joint_positions["joint_L6"])

            last_time = current_time

            p.stepSimulation()

            # Sleep to simulate real time (this can be adjusted or removed as needed)
            time.sleep(1/180)

        p.disconnect()
