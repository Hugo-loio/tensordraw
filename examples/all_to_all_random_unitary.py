import numpy as np
import tensordraw as td

# An all_to_all random unitary gate applied to N qubits
# (a simple example with latex integration)

N = 5 # Number of qubits

strokewidth = 0.15

radius = 0.5 # Qubit radius
qubit = td.Circle(radius, fc = (0.5,0.5,0.5), sw = strokewidth)

width = N*3*radius  # Gate height
gate = td.Square(width, fc = 'blue', sw = strokewidth)
qubit.add_leg(0, length = width + 2*radius)
label = td.Latex("oi")

fig = td.Figure()

# Place qubits
for i in range(N):
    fig.place(qubit, 0, i*3*radius)
# Place gate
fig.place(gate, 1 + width/2,  (width-3*radius)/2)
fig.place(label, 1 + width/2,  (width-3*radius)/2)


fig.export("all_to_all_random_unitary.pdf")
