import numpy as np
import tensordraw as td

# An example script for simple matrix-vector multiplication

matrix = td.Square(1, fc = 'blue')
vector = td.Circle(0.5, fc = 'green')
matrix.add_leg(1) # Side 1 is the left side
l1 = matrix.add_leg(3) # Side 3 is the right side
l2 = vector.add_leg(np.pi) # angle np.pi points to the left

fig = td.Figure()

t1 = fig.place(matrix, 0, 0)
t2 = fig.place(vector, 2, 0)
fig.contract(t1, l1, t2, l2)
#c.add_point([1.4, 1.8])

fig.export("mat_vec_mult.pdf", padding = 0)
