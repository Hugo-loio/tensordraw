class StrokeStyle():
    def __init__(self, width, **kwargs):
        self.width = width

        #Default values
        self.color = (0,0,0,1)
        self.dashed = False
        self.dash_pattern = [2*width, width]
        self.squiggly = False
        # TODO: implement dashing

        self.set(**kwargs)

    def set(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)


    def stroke(self, context):
        context.set_source_rgba(*self.color)
        context.set_line_width(self.width)
        if(self.dashed):
            context.set_dash(self.dash_pattern)
        context.stroke()
