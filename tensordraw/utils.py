from dataclasses import dataclass

import numpy as np

@dataclass
class Position:
    x : float
    y : float
    orientation : float

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        orientation = self.orientation + other.orientation
        return Position(x, y, orientation)

def rotation(theta):
    return np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta), np.cos(theta)]])

# The line is defined by a point and a slope, y = y0 + m(x-x0)
def distance_to_line(t, path, origin, slope, rot = 0):
    R = rotation(rot)
    point = R @ path(t).T
    origin = R @ origin.T
    return np.abs(point[1] - origin[1] - slope*(point[0]-origin[0]))

# Distance from point in a parametric path to an horizontal line that 
# passes through an origin, after a rotation
def distance_to_hline(t, path, origin, rot_angle = 0):
    R = rotation(rot_angle)
    point = R @ path(t).T
    origin = R @ origin.T
    return np.abs(point[1] - origin[1])

def distance_to_point(t, path, point):
    x,y = path(t)
    return np.linalg.norm(np.array([x,y]) - point)

# Return the angle of the orientation of a 2D vector
def orientation(vector):
    if(vector[0] == 0):
        if(vector[1] > 0):
            return np.pi/2
        if(vector[1] < 0):
            return -np.pi/2
    orientation = np.arctan(vector[1]/vector[0])
    if(orientation < 0):
        orientation += 2*np.pi
    if(vector[0] < 0):
        return orientation - np.pi
    return orientation

def gradient(path, t, h):
    return (path(t+h) - path(t-h))/(2*h)
