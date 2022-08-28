from configuration import BLOCK_SIZE
from .entity import Entity


class Field(Entity):

    def __init__(self, pos=..., size=(BLOCK_SIZE, BLOCK_SIZE), **kwargs):
        super().__init__(pos, **kwargs)
        self.size = size

    def update(self):
        self.update_position()
