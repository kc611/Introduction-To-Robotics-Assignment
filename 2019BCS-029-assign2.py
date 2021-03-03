# Name: Kaustubh Chaudhari
# Roll Number: 2019BCS-029
import numpy as np

print("Enter coordinates of initial points : ")
initial_position = list(map(float, input( "").split()))

print("Enter angle of rotation about X axis (in degrees): ")
x_rotation_angle = float(input())
print("Enter angle of rotation about Y axis (in degrees): ")
y_rotation_angle = float(input())
print("Enter angle of rotation about Z axis (in degrees): ")
z_rotation_angle = float(input())

# We convert the list of coordinates into a 3x1 matrix
initial_position = np.array(initial_position)
initial_position = initial_position.reshape((3, 1))

# We create the rotation matrices for x, y and z
# Since numpy only accepts angle in radian we convert 
# the angles from degrees to radian
x_rotation_angle = np.deg2rad(x_rotation_angle)
x_rotation_matrix = np.array([[1, 0, 0],
                      [0, np.cos(x_rotation_angle), -np.sin(x_rotation_angle)],
                      [0, np.sin(x_rotation_angle), np.cos(x_rotation_angle)]])

y_rotation_angle = np.deg2rad(y_rotation_angle)
y_rotation_matrix = np.array([[np.cos(y_rotation_angle), 0, np.sin(y_rotation_angle)],
                      [0, 1, 0],
                      [-np.sin(y_rotation_angle), 0, np.cos(y_rotation_angle)]])

z_rotation_angle = np.deg2rad(z_rotation_angle)
z_rotation_matrix = np.array([[np.cos(z_rotation_angle),  -np.sin(z_rotation_angle), 0],
                      [np.sin(z_rotation_angle), np.cos(z_rotation_angle), 0],
                      [0, 0, 1]])

# The final rotation matrix can be created as follows:
# (@ symbol stands for matrix multiplication)
rotation_matrix= ((x_rotation_matrix @ y_rotation_matrix) @ z_rotation_matrix)

# The new coordinates can then be calculated as the matrix multiplication of 
# the final rotation matrix and the initial coordinates
new_position = rotation_matrix@initial_position

print("New coordinates of the point after rotations are: ")
print(new_position)