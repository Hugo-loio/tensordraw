from copy import deepcopy

import numpy as np

import tensordraw as td

# This script generates the logo of tensordraw
# Each letter is a tensor (Polygon or HoledPolygon class) 
# (doing this is not the purpose of the library, and it is quite
# laborious to define each letter in this way, but it highlights
# the versatility of this tool)

cw = 1 # Character width
ch = 1 # Character height
sw = 0.2 # Stroke width of the character (not tensor stroke width)

# Defining the coordinates for the vertices of each character
# The x origin is in the horizontal center of the character
# the y origin is at the bottom of each character

t_vertices = [[-sw/2,0], [-sw/2,ch-sw], [-cw/2,ch-sw], [-cw/2,ch],
              [cw/2,ch], [cw/2,ch-sw], [sw/2,ch-sw], [sw/2,0]]

gap = (ch-3*sw)/2 # Vertical gap between the legs of the letter E
inner_x = -cw/2+1.3*sw # x coordinate of the inner E side
e_vertices = [[-cw/2,0], [cw/2,0], [cw/2,sw], [inner_x,sw], 
              [inner_x,sw+gap], [cw/2,sw+gap], [cw/2,2*sw+gap],
              [inner_x,2*sw+gap], [inner_x,ch-sw],[cw/2,ch-sw], 
              [cw/2,ch], [-cw/2,ch]]
              
vw = 1.6*sw # Vertical width of the diagonal part
n_vertices = [[-cw/2, 0], [-cw/2, ch], [-cw/2+sw, ch], [cw/2-sw,vw],
              [cw/2-sw,ch], [cw/2,ch], [cw/2,0], [cw/2-sw,0], 
              [-cw/2+sw,ch-vw], [-cw/2+sw,0]]


s_vertices = [[-cw/2,0],[cw/2,0], [cw/2,ch/2+sw/2], 
              [-cw/2+sw,ch/2+sw/2], [-cw/2+sw,ch-sw], [cw/2,ch-sw],
              [cw/2,ch], [-cw/2,ch], [-cw/2,ch/2-sw/2], 
              [cw/2-sw, ch/2-sw/2], [cw/2-sw,sw], [-cw/2,sw]]

o_outer_vertices = [[-cw/2, 0], [-cw/2, ch], [cw/2, ch], [cw/2, 0]]
o_inner_vertices = [[-cw/2+sw, sw], [cw/2-sw, sw], 
                    [cw/2-sw, ch-sw], [-cw/2+sw, ch-sw]]

lw = 1.3*sw # Horizontal width of the right leg
r_outer_vertices = [[-cw/2,0], [-cw/2,ch], [cw/4,ch], [cw/2, ch-sw], 
                    [cw/2, ch/2], [cw/4, ch/2-sw], [cw/2, 0], [cw/2-lw, 0],
                    [cw/4-lw,ch/2-sw], [-cw/2+sw,ch/2-sw], [-cw/2+sw,0]]
inw = 1.85*sw # Width of curved part of the inner hole
r_inner_vertices = [[-cw/2+sw,ch/2], [-cw/2+sw,ch-sw], [cw/2-inw,ch-sw],
                    [cw/2-sw,ch/2 + (ch/2-sw)/2], [cw/2-inw,ch/2]]
                    
lw = 1.3*sw # Horizontal width of the legs
tw = 1.5*sw # Width of the top of the letter A
a_outer_vertices = [[-cw/2, 0], [-tw/2, ch], [tw/2, ch], [cw/2, 0], [cw/2-lw,0],
                    [tw/2, ch/2-sw], [-tw/2, ch/2-sw], [-cw/2+lw,0]]
a_inner_vertices = [[-sw/2, ch/2], [0, ch-sw], [sw/2,ch/2]]

d_outer_vertices = [[-cw/2,0], [-cw/2,ch], [cw/4,ch], [cw/2,ch-cw/4],
                    [cw/2,cw/4], [cw/4,0]]
inw = 0.33*cw # Width of curved part of the inner hole
d_inner_vertices = [[-cw/2+sw,sw], [-cw/2+sw,ch-sw], [cw/2-inw,ch-sw], 
                    [cw/2-sw,ch-inw], [cw/2-sw, inw], [cw/2-inw,sw]]

w_vertices = [[-cw/2,ch], [-cw/2,0], [cw/2,0], [cw/2,ch], [cw/2-sw,ch],
              [cw/2-sw,sw], [sw/2,sw], [sw/2,ch-sw], [-sw/2,ch-sw], 
              [-sw/2,sw], [-cw/2+sw,sw], [-cw/2+sw,ch]]

bw = sw # Base width
ih = 4*ch/7 # Inner crease height
w_vertices = [[-cw/2,ch], [-cw/2+bw,ch],  [-cw/2+bw+(cw-3*bw)/4, ch-ih],
              [-bw/2,ch], [bw/2,ch], [cw/2-bw-(cw-3*bw)/4, ch-ih], [cw/2-bw,ch],
              [cw/2,ch], [2*bw+2*(cw-2*bw)/3-cw/2,0], [bw+2*(cw-2*bw)/3-cw/2,0],
              [0, ih], [-cw/2+bw+(cw-2*bw)/3,0], [-cw/2+(cw-2*bw)/3,0]]

tensorss = td.StrokeStyle(width = 0.06, dashed = False)
kwargs = {
        'stroke_style' : tensorss,
        'corner_width' : 0.05,
        'center' : False
        }

#Create the tensor objects
t_tensor = td.Polygon(t_vertices, **kwargs, fc = 'blue')
e_tensor = td.Polygon(e_vertices, **kwargs, fc = 'yellow')
n_tensor = td.Polygon(n_vertices, **kwargs, fc = 'teal')
s_tensor = td.Polygon(s_vertices, **kwargs, fc = 'purple')
o_tensor = td.HoledPolygon(o_outer_vertices, **kwargs, fc = 'green')
o_tensor.add_hole(o_inner_vertices, center = False)
r1_tensor = td.HoledPolygon(r_outer_vertices, **kwargs, fc = 'red')
r1_tensor.add_hole(r_inner_vertices, center = False)
d_tensor = td.HoledPolygon(d_outer_vertices, **kwargs, fc = 'green')
d_tensor.add_hole(d_inner_vertices, center = False)
r2_tensor = deepcopy(r1_tensor)
a_tensor = td.HoledPolygon(a_outer_vertices, **kwargs, fc = 'orange')
a_tensor.add_hole(a_inner_vertices, center = False)
w_tensor = td.Polygon(w_vertices, **kwargs, fc = 'blue')

#Add legs to the tensors
l_open = 0.2 # Lenght of open legs
l_cont = 0.05 # Lenght of contracted legs
t_tensor.add_leg(0, length = l_cont)
t_tensor.add_leg(4, length = l_open)
t_tensor.add_leg(4, 0.2, length = l_open)
t_tensor.add_leg(4, 0.8, length = l_open)
e_tensor.add_leg(10, length = l_cont)
n_tensor.add_leg(7, length = l_cont)
n_tensor.add_leg(6, 0.3, length = l_cont)
s_tensor.add_leg(6, length = l_cont)
s_tensor.add_leg(0, 0.2, length = l_cont)
o_tensor.add_leg(0, length = l_cont)
o_tensor.add_leg(2, length = l_cont)
r1_tensor.add_leg(-2, length = l_cont)
r1_tensor.add_leg(-3, length = l_open)
r1_tensor.add_leg(4, length = l_cont)
d_tensor.add_leg(-1, length = l_cont)
d_tensor.add_leg(3, 0.7, length = l_cont)
r2_tensor.add_leg(8, 0.3, length = l_cont)
a_tensor.add_leg(-1, 0.1, length = l_cont)
w_tensor.add_leg(5, 0.7, length = l_cont)
w_tensor.add_leg(5, 0.3, length = l_open)
w_tensor.add_leg(9, length = l_cont)

# Auxilary lengths
hs = 0.1 # Horizontal spacing
vs = 0.2 # Vertical spacing
hs_ra = 0.05 # Vertical spacing between R and A
hs_aw = -0.10 # Vertical spacing between A and W
tw = 6*cw + 5*hs # Top word width
bw = 4*cw + 2*hs + hs_aw # Bottom word width

fig = td.Figure()

fig.place(t_tensor, 0, 0)
fig.place(e_tensor, (cw + hs), 0)
fig.place(n_tensor, 2*(cw + hs), 0)
fig.place(s_tensor, 3*(cw + hs), 0)
fig.place(o_tensor, 4*(cw + hs), 0)
fig.place(r1_tensor, 5*(cw + hs), 0)

fig.place(d_tensor, tw/2-bw/2, -(ch + vs))
fig.place(r2_tensor, tw/2-bw/2 + (cw + hs), -(ch + vs))
fig.place(a_tensor, tw/2-bw/2 + 2*cw + hs + hs_ra, -(ch + vs))
fig.place(w_tensor, tw/2-bw/2 + 3*cw + hs + hs_ra + hs_aw, -(ch + vs))

c1 = fig.contract(1,0,3,0, handle_lengths=[0.2,0.2])
c1.add_point((2.0*(cw+hs), 1.1*(ch+vs)))
fig.contract(2,0,2,1)
fig.contract(0,0,6,0, handle_lengths=[0.4,0.4])
fig.contract(3,1,7,0, handle_lengths=[0.1,0.05])
c2 = fig.contract(6,1,8,0, handle_lengths=[0.3,0.07])
c2.add_point((2.3*(cw+hs), -0.08*(ch+vs)), handle_lengths = [0.1,0.3])
fig.contract(9,2,4,0)
fig.contract(4,1,5,0, handle_lengths=[0.3,0.3])
fig.contract(5,2,9,0, handle_lengths=[0.3,0.7])

fig.export("logo.pdf", padding = 4)
fig.export("logo.svg", padding = 0)
