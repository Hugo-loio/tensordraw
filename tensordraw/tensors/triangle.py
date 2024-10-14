from ._base_tensor import BaseTensor
import numpy as np

class Triangle(BaseTensor):
    def __init__(self, width, height, **kwargs):
        super().__init__(**kwargs)
        self._lengths = lengths
        self._corner_radius = np.min([widht, height])/10

    def set(self, **kwargs):
        super().set(**kwargs)
        if 'lengths' in kwargs:
            self._lengths = kwargs['lengths']
        if 'corner_radius' in kwargs:
            self._corner_radius  = kwargs['_corner_radius']
