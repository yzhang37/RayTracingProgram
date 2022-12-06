"""
Define a fixed scene with rotating lights
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import math

import numpy as np

import ColorType as Ct
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


class SceneThree(Scene):
    def __init__(self, shaderProg: GLProgram):
        Scene.__init__(self, shaderProg)

        # add a table
        table = Component(Point((0, -1, 0)), DisplayableCube(
            shaderProg, 6, 0.5, 3, Ct.WHITE,
            False, 2, 2
        ))
        table.setTexture(shaderProg, "assets/checker_table.png")
        table.renderingRouting = "texture"
        table.setNormalMap(shaderProg, "assets/table_cloth_normal.jpg")
        self.addChild(table)

        # four legs of the table, using cylinder
        for i in (-2, 2):
            for j in (-1, 1):
                leg = Component(Point((i, -1 - 1.8 / 2, j)), DisplayableCylinder(
                    shaderProg, 0.2, 0.2, 1.8, 20, Ct.WHITE
                ))
                leg.setDefaultAngle(90, leg.uAxis)
                leg.setTexture(shaderProg, "assets/hardwood.png")
                leg.renderingRouting = "texture"
                leg.setNormalMap(shaderProg, "assets/hardwood_norm.png")
                self.addChild(leg)

        # two present boxes
        box1 = Component(Point((2.4, (0.5 + 0.7) / 2, 0.15)), DisplayableCube(
            shaderProg, 0.7, 0.7, 0.7, Ct.WHITE))
        box1.setDefaultAngle(-10, box1.vAxis)
        box1.setTexture(shaderProg, "assets/box_b.png")
        box1.renderingRouting = "texture"

        box2 = Component(Point((1.7, (0.5 + .9) / 2, -0.85)), DisplayableCube(
            shaderProg, .9, .9, .9, Ct.WHITE))
        box2.setDefaultAngle(10, box2.vAxis)
        box2.setTexture(shaderProg, "assets/box_a.png")
        box2.renderingRouting = "texture"

        table.addChild(box1)
        table.addChild(box2)

        # two plates

