from typing import *

from Component import Component
from Light import Light
from Point import Point


class Scene(Component):
    lights: List[Light] = []
    lightCubes: List[Component] = []

    def __init__(self):
        super().__init__(Point((0, 0, 0)))
