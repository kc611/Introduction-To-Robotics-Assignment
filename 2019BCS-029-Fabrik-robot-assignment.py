import math
import numpy as np


class fabrik_robot:
    def __init__(self, position_of_joints, tolerance: float):
        if tolerance <= 0:
            raise ValueError("Tolerance must be more than 0")
        self.joints = position_of_joints
        self.tolerance: float = tolerance
        self.length_of_link = []

        a = position_of_joints[0]
        for b in position_of_joints[1:]:
            self.length_of_link.append(np.linalg.norm(a - b))
            a = b

        if any([length <= 0 for length in self.length_of_link]):
            raise ValueError("Link lengths must be positive")

        self.lengths = self.length_of_link
        self.max_length = sum(self.length_of_link)
        self._has_moved = True
        self._angles = []
        _ = self.angles

    def as_length(self, vector, length):
        return vector * length / np.linalg.norm(vector)

    def angles(self):
        if not self._has_moved:
            return self._angles

        angles = [math.atan2(self.joints[1][1], self.joints[1][0])]
        angle_of_previous_joint: float = angles[0]
        for i in range(2, len(self.joints)):
            p = self.joints[i] - self.joints[i - 1]
            curr_angle_absolute_value: float = math.atan2(p[1], p[0])
            angles.append(curr_angle_absolute_value - angle_of_previous_joint)
            angle_of_previous_joint = curr_angle_absolute_value

        self.moved = False
        self._angles = angles
        return self._angles

    def solvable(self, target):
        return self.max_length >= np.linalg.norm(target)

    def angles_deg(self):
        angles = self.angles()
        angles = [math.degrees(val) for val in angles]
        return angles

    def move_to(self, target, try_reach=True):
        if not self.solvable(target):
            if not try_reach:
                return 0
            target = self.as_length(target, self.max_length)
        return self._iterate(target)

    def _iterate(self, target):
        curr_iteration: int = 0
        initPos = self.joints[0]
        last: int = len(self.joints) - 1

        while np.linalg.norm(self.joints[-1] - target) > self.tolerance:
            curr_iteration += 1
            self.joints[-1] = target
            for i in reversed(range(0, last)):
                next, cur = self.joints[i + 1], self.joints[i]
                len_share = self.lengths[i] / np.linalg.norm(next - cur)
                self.joints[i] = (1 - len_share) * next + len_share * cur

            self.joints[0] = initPos
            for i in range(0, last):
                next, cur = self.joints[i + 1], self.joints[i]
                len_share = self.lengths[i] / np.linalg.norm(next - cur)
                self.joints[i + 1] = (1 - len_share) * \
                    cur + len_share * next
        return curr_iteration


coordinate_1 = list(map(int, input("Enter the 1st coordinate: ").strip().split()))[:3]
coordinate_2 = list(map(int, input("Enter the 2nd coordinate: ").strip().split()))[:3]
coordinate_3 = list(map(int, input("Enter the 3rd coordinate: ").strip().split()))[:3]
coordinate_4 = list(map(int, input("Enter the 4th coordinate: ").strip().split()))[:3]
tolerance = float(input("Enter the tolerance: "))
goal_coordinate = list(map(int, input("Enter the final goal coordinates: ").strip().split()))[:3]

initial_coordinates = [np.array(coordinate_1), np.array(coordinate_2), np.array(coordinate_3), np.array(coordinate_4)]
initPos = initial_coordinates
curr_robot = fabrik_robot(initial_coordinates, tolerance)

iterations = curr_robot.move_to(np.array(goal_coordinate))

print("Number of Iterations:" + str(iterations))
print("Number of Angles: " + str(curr_robot.angles_deg()))
print("Position of Link: " + str(curr_robot.joints))
print("Final position: " + str(goal_coordinate))
