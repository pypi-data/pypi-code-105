from gym import Env
from gym import error, spaces, utils
from gym.utils import seeding
from gym.spaces import Discrete, Box

import numpy as np
import random
import pybullet as p
import pybullet_data
import math
import os


class ThormangEnv(Env):


    def __init__(self):
        p.connect(p.GUI) # Connect to pybullet
        self.action_space = Box(np.array([-1]*33), np.array([1]*33))
        self.observation_space = Box(np.array([-1]*33), np.array([1]*33))
        # self.state = 38 + random.randint(-3,3)


    def step(self, action): 

        p.configureDebugVisualizer(p.COV_ENABLE_SINGLE_STEP_RENDERING) # For bettter rendering
        orientation = p.getQuaternionFromEuler([0.,-math.pi,math.pi/2.]) # Convert the angles to Quaternion variables
        dv = 0.005 # For smoother inverse kinematics output
        dx = action[0] * dv
        dy = action[1] * dv
        dz = action[2] * dv

        currentPose = p.getLinkState(self.thormang3, 11) # Read the current Cartesian position
        currentPosition = currentPose[0]
        newPosition = [currentPosition[0] + dx,
                       currentPosition[1] + dy,
                       currentPosition[2] + dz]

        jointPoses = p.calculateInverseKinematics(self.thormang3, 11, newPosition, orientation) # Calculating target joint variables

        p.setJointMotorControlArray(self.thormang3, list(range(7))+[9,10], p.POSITION_CONTROL, list(jointPoses)+2*[fingers]) # Apply those joint variables
        p.stepSimulation() # run the environment for one time step

        state_robot = p.getLinkState(self.thormang3, 11)[0]
        
        # Calculate reward
        
        # Check if is done
  
        # Apply  noise

        
        info = {} # Set placeholder for info
        observation = state_robot

        return observation, reward, done, info # Return step information


    def render(self, mode='human'):
        # Implement viz
        pass
    

    def reset(self):
        p.resetSimulation()
        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,0) # 0: Disable 1: Enable the rendering 
        p.setGravity(0,0,-10)
        urdfRootPath=pybullet_data.getDataPath()
        # thormang3 = p.loadURDF("thormang3.urdf", useFixedBase=False)
        self.thormang3 = p.loadURDF(os.path.join(urdfRootPath, "thormang3.urdf"), useFixedBase=False)

        # rest_poses = [0,-0.215,0,-2.57,0,2.356,2.356,0.08,0.08]
        # p.resetJointState(self.thormang3, i, rest_poses[i]) # Set initial position of the joints

        state_robot = p.getLinkState(self.thormang3)[0]
        observation = state_robot

        p.configureDebugVisualizer(p.COV_ENABLE_RENDERING,1)

        return observation


    def close(self):
        p.disconnect()