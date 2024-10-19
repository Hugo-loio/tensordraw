class StrokeStyle():
    def __init__(self, **kwargs):
        #Default values
        self.width = 1
        self.color = (0,0,0,1)
        self.dashed = False
        self.dash_pattern = [2*self.width, self.width]
        self.squiggly = False
        self.default = {key : True for key in self.__dict__.keys()}

        self.set(**kwargs)

    def set(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                self.default[key] = False


    def stroke(self, context):
        context.set_source_rgba(*self.color)
        context.set_line_width(self.width)
        if(self.dashed):
            context.set_dash(self.dash_pattern)
        context.stroke()
