from typing import *

from Component import Component
from GLProgram import GLProgram
from GLUtility import GLUtility
from Light import Light
from Point import Point


class Scene(Component):
    lights: List[Light] = []
    lightCubes: List[Component] = []
    shaderProg: GLProgram = None
    glutility: GLUtility = None

    def __init__(self, shaderProg: GLProgram):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility()

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
