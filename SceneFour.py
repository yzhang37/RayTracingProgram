"""
Define a fixed scene with rotating lights
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import math

import numpy as np

import ColorType
from Animation import Animation
from DisplayableCylinder import DisplayableCylinder
from DisplayableEllipsoid import DisplayableEllipsoid
from GLProgram import GLProgram
from Quaternion import Quaternion
from SceneType import Scene
from Component import Component
from Light import Light
from Material import Material
from Point import Point
import GLUtility

from DisplayableCube import DisplayableCube
from DisplayableTorus import DisplayableTorus
from DisplayableSphere import DisplayableSphere


class SceneFour(Scene):
    def __init__(self, shaderProg: GLProgram):
        Scene.__init__(self, shaderProg)

        # 添加一个桌子
        table = Component(Point((0, -1, 0)),
                          DisplayableCube(shaderProg, 7, 0.5, 7))
        self.addChild(table)
