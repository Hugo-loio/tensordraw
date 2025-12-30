from dataclasses import dataclass

import numpy as np
from scipy.signal import argrelmin

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

def pos_to_point(position):
    return np.array([position.x, position.y])

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

# Return the angle of the orientation of a 2D vector in [0, 2*pi]
def orientation(vector):
    if(vector[0] == 0):
        if(vector[1] > 0):
            return np.pi/2
        if(vector[1] < 0):
            return 3*np.pi/2
    orientation = np.arctan(vector[1]/vector[0])
    if(vector[0] < 0):
        return orientation - np.pi
    if(orientation < 0):
        orientation += 2*np.pi
    return orientation

def gradient(path, t, h):
    return (path(t+h) - path(t-h))/(2*h)

# Find the intersection parameters between a parametric path [0,1] -> R^2
# And a straight line passing through an origin with a certain inclination
def path_line_intersection(path, origin, inclination, res):
    ts = np.linspace(0, 1, res)
    steps = [np.linalg.norm(path(ts[i]) - path(ts[i+1])) for i,_ in enumerate(ts[:-1])]
    adjacent_dists = np.empty(res)
    adjacent_dists[0] = steps[0]
    adjacent_dists[-1] = steps[-1]
    adjacent_dists[1:-1] = np.max([steps[:-1], steps[1:]], axis = 0)
    dists = np.array([distance_to_hline(t, path, origin, -inclination) for t in ts])
    argmins = argrelmin(dists, mode = 'wrap')[0]
    dists_min = dists[argmins]
    argmins = argmins[dists_min < adjacent_dists[argmins]]
    if(len(argmins) == 0):
        raise RuntimeError("Intersection of leg with tensor not found")
    return ts[argmins] 

# TODO: Find an analytical exact solution to the previous function
