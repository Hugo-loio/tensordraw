import numpy as np
import tensordraw as td

# A typical brickwork circuit applied on a product state

N = 6 # Number of qubits
D = 3 # Number of layers (even and odd)

hs = 1.3 # Horizontal spacing between qubits
vs = 1.7 # Vertical spacing between layers
vs0 = 1.7 # Vertical spacing between the qubits and the first layer

strokewidth = 0.15

gate = td.Rectangle(2, 1.3, fc = 'blue', sw = strokewidth)
qubit = td.Circle(0.5, fc = (0.5,0.5,0.5), sw = strokewidth)
qubit.add_leg(np.pi/2)

fig = td.Figure()

# Place qubits
for i in range(N):
    fig.place(qubit, hs*i, 0)

for l in range(D):
    for i in range(0, N-1, 2):
        fig.place(gate, hs*i + hs/2, vs0 + 2*l*vs)
    for i in range(0, N-2, 2):
        fig.place(gate, hs*(i+1) + hs/2, vs0 + 2*l*vs + vs)



fig.export("brickwork_circuit.pdf")
