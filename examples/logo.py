import numpy as np

import tensordraw as td

# This script generates the logo of tensordraw
# Each letter is a tensor (polygon class) 
# (doing this is not the purpose of the library but it just goes
# to show that there are endless possibilities of what you can create)

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

r_outer_vertices = [[-cw/2,0], [-cw/2,ch], [cw/2,ch], 
                    [cw/2,ch-sw], [-cw/2+sw,ch-sw], [-cw/2+sw,0]]

a_outer_vertices = [[-cw/2, 0], [-cw/2, ch], [cw/2, ch], [cw/2, 0]]
a_inner_vertices = [[-cw/2+sw, sw], [cw/2-sw, sw], [cw/2-sw, ch-sw], [-cw/2+sw, ch-sw]]

w_vertices = [[-cw/2,ch], [-cw/2,0], [cw/2,0], [cw/2,ch], [cw/2-sw,ch],
              [cw/2-sw,sw], [sw/2,sw], [sw/2,ch-sw], [-sw/2,ch-sw], 
              [-sw/2,sw], [-cw/2+sw,sw], [-cw/2+sw,ch]]

tensorss = td.StrokeStyle(width = 0.05, dashed = False)
kwargs = {
        'stroke_style' : tensorss,
        'corner_width' : 0.05,
        }

blue = td.FillStyle(color = (0,0,1))
green = td.FillStyle(color = (0.004, 0.851, 0))
yellow = td.FillStyle(color = (1,1,0))
orange = td.FillStyle(color = (0.949, 0.573, 0.098))
red = td.FillStyle(color = (1,0,0))
transparent = td.FillStyle(color = (0,0,0,0))

t_tensor = td.Polygon(t_vertices, **kwargs, fs = blue, center = False)
e_tensor = td.Polygon(e_vertices, **kwargs, fs = green, center = False)
n_tensor = td.Polygon(n_vertices, **kwargs, fs = orange, center = False)
s_tensor = td.Polygon(s_vertices, **kwargs, fs = red, center = False)
o_tensor_out = td.Polygon(o_outer_vertices, **kwargs, fs = blue, center = False)
o_tensor_in = td.Polygon(o_inner_vertices, **kwargs, fs = transparent, center = False, operator = "clear")
r_tensor = td.Polygon(r_vertices, **kwargs, fs = blue, center = False)
d_tensor = td.Polygon(t_vertices, **kwargs, fs = blue, center = False)
a_tensor = td.Polygon(t_vertices, **kwargs, fs = blue, center = False)
w_tensor = td.Polygon(w_vertices, **kwargs, fs = yellow, center = False)

hs = 0.1 # Horizontal spacing
vs = 0.2 # Vertical spacing

fig = td.Figure()

fig.place(t_tensor, 0, 0)
fig.place(e_tensor, (cw + hs), 0)
fig.place(n_tensor, 2*(cw + hs), 0)
fig.place(s_tensor, 3*(cw + hs), 0)
fig.place(o_tensor_out, 4*(cw + hs), 0)
fig.place(o_tensor_in, 4*(cw + hs), 0)
fig.place(r_tensor, 5*(cw + hs), 0)
fig.place(d_tensor, (cw + hs), -(ch + vs))
fig.place(r_tensor, 2*(cw + hs), -(ch + vs))
fig.place(a_tensor, 3*(cw + hs), -(ch + vs))
fig.place(w_tensor, 4*(cw + hs), -(ch + vs))
#fig.place(star, 0.6, 0, orientation = 0)
#fig.place(pentagon, 1.2, 0, orientation = np.pi/4)
#fig.place(rectangle, 1.8, 0, orientation = np.pi/3)
#fig.place(square, 0, 0.6, orientation = np.pi/3)
#fig.place(eqtriangle, 0.6, 0.54, orientation = 0)
#fig.place(isotriangle, 1.2, 0.54, orientation = 0)

fig.export("logo.pdf", padding = 4)
