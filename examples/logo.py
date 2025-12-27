import numpy as np

import tensordraw as td

# This script generates the logo of tensordraw
# Each letter is a tensor (polygon class) 
# (doing this is not the purpose of the library but it just goes
# to show that the possibilities for creating diagrams are endless)

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

tensorss = td.StrokeStyle(width = 0.05, dashed = False)
kwargs = {
        'stroke_style' : tensorss,
        'corner_width' : 0.05,
        }

blue = td.FillStyle(color = (0,0,1))
green = td.FillStyle(color = (0,0.72,0.08))
yellow = td.FillStyle(color = (1,1,0))
orange = td.FillStyle(color = (0.949, 0.573, 0.098))
red = td.FillStyle(color = (1,0,0))
purple = td.FillStyle(color = (0.58,0,1))
teal = td.FillStyle(color = (0,1,0.89))
transparent = td.FillStyle(color = (0,0,0,0))

t_tensor = td.Polygon(t_vertices, **kwargs, fs = blue, center = False)
e_tensor = td.Polygon(e_vertices, **kwargs, fs = yellow, center = False)
n_tensor = td.Polygon(n_vertices, **kwargs, fs = teal, center = False)
s_tensor = td.Polygon(s_vertices, **kwargs, fs = purple, center = False)
o_tensor_out = td.Polygon(o_outer_vertices, **kwargs, fs = green, center = False)
o_tensor_in = td.Polygon(o_inner_vertices, **kwargs, center = False, operator = "clear")
r_tensor_out = td.Polygon(r_outer_vertices, **kwargs, fs = red, center = False)
r_tensor_in = td.Polygon(r_inner_vertices, **kwargs, center = False, operator = "clear")
d_tensor_out = td.Polygon(d_outer_vertices, **kwargs, fs = green, center = False)
d_tensor_in = td.Polygon(d_inner_vertices, **kwargs, center = False, operator = "clear")
a_tensor_out = td.Polygon(a_outer_vertices, **kwargs, fs = orange, center = False)
a_tensor_in = td.Polygon(a_inner_vertices, **kwargs, center = False, operator = "clear")
w_tensor = td.Polygon(w_vertices, **kwargs, fs = blue, center = False)

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
fig.place(o_tensor_out, 4*(cw + hs), 0)
fig.place(o_tensor_in, 4*(cw + hs), 0)
fig.place(r_tensor_out, 5*(cw + hs), 0)
fig.place(r_tensor_in, 5*(cw + hs), 0)

fig.place(d_tensor_out, tw/2-bw/2, -(ch + vs))
fig.place(d_tensor_in, tw/2-bw/2, -(ch + vs))
fig.place(r_tensor_out, tw/2-bw/2 + (cw + hs), -(ch + vs))
fig.place(r_tensor_in, tw/2-bw/2 + (cw + hs), -(ch + vs))
fig.place(a_tensor_out, tw/2-bw/2 + 2*cw + hs + hs_ra, -(ch + vs))
fig.place(a_tensor_in, tw/2-bw/2 + 2*cw + hs + hs_ra, -(ch + vs))
fig.place(w_tensor, tw/2-bw/2 + 3*cw + hs + hs_ra + hs_aw, -(ch + vs))
#fig.place(star, 0.6, 0, orientation = 0)
#fig.place(pentagon, 1.2, 0, orientation = np.pi/4)
#fig.place(rectangle, 1.8, 0, orientation = np.pi/3)
#fig.place(square, 0, 0.6, orientation = np.pi/3)
#fig.place(eqtriangle, 0.6, 0.54, orientation = 0)
#fig.place(isotriangle, 1.2, 0.54, orientation = 0)

fig.export("logo.pdf", padding = 4)
