from abc import abstractmethod

from ._drawable import Drawable

class Placeable(Drawable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @abstractmethod
    def limits(self, R):
        pass
