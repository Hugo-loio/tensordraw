import numpy as np
import tensordraw as td

# An example script for simple matrix-vector multiplication

matrix = td.Square(1, fc = 'blue')
vector = td.Circle(0.5, fc = 'green')
matrix.add_leg(1) # Side 1 is the left side

fig = td.Figure()

t1 = fig.place(matrix, 0, 0)
t2 = fig.place(vector, 2, 0)
fig.contract(t1, t2)

fig.export("mat_vec_mult.pdf")
