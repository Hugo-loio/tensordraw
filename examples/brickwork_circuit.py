import numpy as np
import tensordraw as td

# A typical brickwork circuit applied on a product state

N = 6 # Number of qubits
D = 3 # Number of layers (even and odd)

hs = 1.3 # Horizontal spacing between qubits
vs = 1.7 # Vertical spacing between layers

strokewidth = 0.15

height = 1.3 # Gate width
width  = 2  # Gate height
gate = td.Rectangle(width, height, fc = 'blue', sw = strokewidth)

qubit = td.Circle(0.5, fc = (0.5,0.5,0.5), sw = strokewidth)
# The long legs of the qubit tensors act as the physical dofs
qubit.add_leg(np.pi/2, length = (2*D+0.4)*vs)

fig = td.Figure()

# Place qubits
for i in range(N):
    fig.place(qubit, hs*i, 0)

# Place gates
for l in range(D):
    for i in range(0, N-1, 2):
        fig.place(gate, hs*i + hs/2, (2*l+1)*vs)
    for i in range(0, N-2, 2):
        fig.place(gate, hs*(i+1) + hs/2, (2*l+2)*vs)

fig.export("brickwork_circuit.pdf")
