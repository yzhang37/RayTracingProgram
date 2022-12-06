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


def get_donut(shaderProg, pos=Point((0, 0, 0))) -> Component:
    donut = Component(pos, DisplayableTorus(
        shaderProg, 0.3, 0.1, 16, 16, Ct.WHITE))
    donut.setTexture(shaderProg, "assets/donut.jpg")
    donut.renderingRouting = "texture"
    return donut


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
        plate1 = Component(Point((0.2, (0.5 + 0.05) / 2, 0)), DisplayableCylinder(
            shaderProg, 0.9, 0.9, 0.05, 36, Ct.WHITE))
        plate1.setDefaultAngle(90, plate1.uAxis)
        plate1.renderingRouting = "vertex"
        table.addChild(plate1)

        plate2 = Component(Point((-1.9, (0.5 + 0.05) / 2, 0.3)), DisplayableCylinder(
            shaderProg, 1, 1, 0.05, 36, Ct.WHITE))
        plate2.setDefaultAngle(-90, plate2.uAxis)
        plate2.renderingRouting = "vertex"
        table.addChild(plate2)

        pi = np.pi
        # add twenty donuts
        # 1st layer
        donut = get_donut(shaderProg, Point((0, 0, 0.1)))
        plate2.addChild(donut)
        for i, theta in enumerate(np.linspace(-pi, pi, 9)):
            if i == 0:
                continue
            donut = get_donut(shaderProg, Point((0.7 * math.cos(theta), 0.7 * math.sin(theta), 0.1)))
            plate2.addChild(donut)
        # 2nd layer
        for i, theta in enumerate(np.linspace(-pi, pi, 8)):
            if i == 0:
                continue
            donut = get_donut(shaderProg, Point((0.55 * math.cos(theta), 0.55 * math.sin(theta), 0.1 + 0.2)))
            plate2.addChild(donut)
        # 3rd layer
        for i, theta in enumerate(np.linspace(-pi, pi, 5)):
            if i == 0:
                continue
            donut = get_donut(shaderProg, Point((0.4 * math.cos(theta), 0.4 * math.sin(theta), 0.1 + 0.2 * 2)))
            plate2.addChild(donut)
