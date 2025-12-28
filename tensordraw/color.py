DEFAULT_COLORS = {
        'blue' : (0,0,1),
        'green' : (0,0.72,0.08),
        'red' : (1,0,0),
        'yellow' : (1,1,0),
        'orange' : (0.949, 0.573, 0.098),
        'purple' : (0.58,0,1),
        'teal' : (0,1,0.89),
        'transparent' : (0,0,0,0)
        }

class Color():
    def __init__(self, color = (0,0,1,1)):
        self.set(color)

    def set(self, val):
        if(isinstance(val, str)):
            self.color = DEFAULT_COLORS[val]
        elif(isinstance(val, tuple)):
            self.color = val
        elif(isinstance(val, Color)):
            self.color = val.color
        else:
            raise ValueError("Invalid color format")
