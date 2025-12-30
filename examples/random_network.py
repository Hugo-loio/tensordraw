import numpy as np
from scipy.stats import qmc

import tensordraw as td

# This example produces a random graph with nodes connected
# only to their near neighbours

num_nodes = 20
radius = 1/(2*num_nodes)

engine = qmc.PoissonDisk(d=2, radius=4*radius)
coords = engine.random(num_nodes) # Random 2D spaced out coordinates

node = td.Circle(radius, fc = 'blue')
fig = td.Figure()

for coord in coords:
    fig.place(node, *coord)

for i,pi in enumerate(coords):
    for j,pj in enumerate(coords[i+1:]):
        if(np.linalg.norm(pi-pj) < 8*radius):
            fig.contract(i,j+i+1)

fig.export("random_network.pdf")
