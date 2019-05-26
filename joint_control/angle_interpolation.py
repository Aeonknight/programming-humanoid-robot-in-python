'''In this exercise you need to implement an angle interploation function which makes NAO executes keyframe motion

* Tasks:
    1. complete the code in `AngleInterpolationAgent.angle_interpolation`,
       you are free to use splines interploation or Bezier interploation,
       but the keyframes provided are for Bezier curves, you can simply ignore some data for splines interploation,
       please refer data format below for details.
    2. try different keyframes from `keyframes` folder

* Keyframe data format:
    keyframe := (names, times, keys)
    names := [str, ...]  # list of joint names
    times := [[float, float, ...], [float, float, ...], ...]
    # times is a matrix of floats: Each line corresponding to a joint, and column element to a key.
    keys := [[float, [int, float, float], [int, float, float]], ...]
    # keys is a list of angles in radians or an array of arrays each containing [float angle, Handle1, Handle2],
    # where Handle is [int InterpolationType, float dTime, float dAngle] describing the handle offsets relative
    # to the angle and time of the point. The first Bezier param describes the handle that controls the curve
    # preceding the point, the second describes the curve following the point.
'''


from pid import PIDAgent
from keyframes import *
import numpy as np


class AngleInterpolationAgent(PIDAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(AngleInterpolationAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.keyframes = ([], [], [])
        self.st = -1

    def think(self, perception):
        target_joints = self.angle_interpolation(self.keyframes, perception)
        self.target_joints.update(target_joints)
        return super(AngleInterpolationAgent, self).think(perception)

    def angle_interpolation(self, keyframes, perception):
        target_joints = {}
        # YOUR CODE HERE

        if self.st == -1:
            self.st = perception.time

        ct = perception.time - self.st

        names, times, keys = keyframes
        #go through the names
        for i in range (len(names)):
            n = names[i]

            # check for absent of names in joints
            if n in self.joint_names:
                t = times[i]
                k = keys[i]

                for j in range(len(t) - 1):
                    #normal interpolation between keyframes
                    if t[j] < ct < t[j+1]:
                        k1 = k[j][0]
                        kp1 = k1 + (k[j][2][1] * k[j][2][2])
                        k2 = k[j + 1][0]
                        kp2 = k2 + (k[j+1][1][1] * k[j+1][1][2])
                        tn = (ct - t[j]) / (t[j+1] - t[j])
                    # for the first keyframe
                    elif ct < t[0]:
                        k1 = perception.joint[n]
                        kp1 = k1
                        k2 = k [0][0]
                        kp2 = k2 + (k[j][2][1] * k[j][2][2])
                        tn = (ct - 0.0) / (t[1] - 0.0)
                    else:
                        continue
                    #formula of bezier interpolation
                    target_joints[n] = (1 - tn) ** 3 * k1 + 3 * (1 - tn) ** 2 * tn * kp1 + 3 * (1 - tn) * tn ** 2 * kp2 + tn ** 3 * k2

        return target_joints

if __name__ == '__main__':
    agent = AngleInterpolationAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
