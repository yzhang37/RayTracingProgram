"""
Define a fixed scene with rotating lights
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import math
from typing import Tuple, Optional

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


_material_donut = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.4, 0.4, 0.4, 1)),
                           np.array((0.4, 0.4, 0.4, 0.1)), 64)


def get_donut(shaderProg, pos=Point((0, 0, 0))) -> Component:
    donut = Component(pos, DisplayableTorus(
        shaderProg, 0.3, 0.1, 16, 16, Ct.WHITE))
    donut.setTexture(shaderProg, "assets/donut.jpg")
    donut.renderingRouting = "lighting_texture"
    donut.setMaterial(_material_donut)
    return donut


_material_candle = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.4, 0.4, 0.4, 1)),
                            np.array((0.4, 0.4, 0.4, 0.1)), 64)


def get_candle(shaderProg,
               pos=Point((0, 0, 0)),
               candle_texture: Optional[str] = "assets/white_candle.jpg",
               use_texture: bool = True) -> Component:
    candle_line = Component(pos, DisplayableCylinder(
        shaderProg, 0.01, 0.01, 0.08, 3, Ct.WHITE))
    candle_line.renderingRouting = "vertex"
    candle_line.setDefaultAngle(-90, candle_line.uAxis)
    candle_base = Component(Point((0, 0, -(0.4 + 0.08) / 2)), DisplayableCylinder(
        shaderProg, 0.05, 0.05, 0.4, 8, Ct.WHITE))
    candle_base.setMaterial(_material_candle)
    if use_texture and candle_texture is not None:
        candle_base.setTexture(shaderProg, candle_texture)
        candle_base.renderingRouting = "lighting_texture"
    else:
        candle_base.renderingRouting = "lighting"
    candle_line.addChild(candle_base)

    def turn_on(component):
        component.displayObj = DisplayableCylinder(shaderProg, 0.01, 0.01, 0.08, 3, Ct.WHITE)
        component.displayObj.initialize()

    def turn_off(component):
        component.displayObj = DisplayableCylinder(shaderProg, 0.01, 0.01, 0.08, 3, Ct.BLACK)
        component.displayObj.initialize()

    candle_line.turn_on = turn_on
    candle_line.turn_off = turn_off
    return candle_line


class SceneThree(Scene):
    def __init__(self, shaderProg: GLProgram):
        Scene.__init__(self, shaderProg)

        # add a table
        table = Component(Point((0, -1, 0)), DisplayableCube(
            shaderProg, 6, 0.5, 3, Ct.WHITE,
            False, 2, 2
        ))
        mat_table = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.4, 0.4, 0.4, 1)),
                             np.array((0.4, 0.4, 0.4, 0.1)), 64)
        table.setMaterial(mat_table)
        table.setTexture(shaderProg, "assets/checker_table.png")
        table.renderingRouting = "lighting_texture"
        table.setNormalMap(shaderProg, "assets/table_cloth_normal.jpg")
        self.addChild(table)

        # four legs of the table, using cylinder
        for i in (-2, 2):
            for j in (-1, 1):
                leg = Component(Point((i, -1 - 1.8 / 2, j)), DisplayableCylinder(
                    shaderProg, 0.2, 0.2, 1.8, 20, Ct.WHITE
                ))
                leg.setMaterial(mat_table)
                leg.setDefaultAngle(90, leg.uAxis)
                leg.setTexture(shaderProg, "assets/hardwood.png")
                leg.renderingRouting = "lighting_texture"
                leg.setNormalMap(shaderProg, "assets/hardwood_norm.png")
                self.addChild(leg)

        # two present boxes
        mat_box = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.4, 0.4, 0.4, 1)),
                        np.array((0.4, 0.4, 0.4, 0.1)), 64)
        box1 = Component(Point((2.4, (0.5 + 0.7) / 2, 0.15)), DisplayableCube(
            shaderProg, 0.7, 0.7, 0.7, Ct.WHITE))
        box1.setMaterial(mat_box)
        box1.setDefaultAngle(-10, box1.vAxis)
        box1.setTexture(shaderProg, "assets/box_b.png")
        box1.renderingRouting = "lighting_texture"

        box2 = Component(Point((1.7, (0.5 + .9) / 2, -0.85)), DisplayableCube(
            shaderProg, .9, .9, .9, Ct.WHITE))
        box2.setMaterial(mat_box)
        box2.setDefaultAngle(10, box2.vAxis)
        box2.setTexture(shaderProg, "assets/box_a.png")
        box2.renderingRouting = "lighting_texture"

        table.addChild(box1)
        table.addChild(box2)

        # two plates
        mat_plate = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.4, 0.4, 0.4, 1)),
                             np.array((0.4, 0.4, 0.4, 0.1)), 64)
        plate1 = Component(Point((0.2, (0.5 + 0.05) / 2, 0)), DisplayableCylinder(
            shaderProg, 0.9, 0.9, 0.05, 36, Ct.WHITE))
        plate1.setMaterial(mat_plate)
        plate1.setDefaultAngle(-90, plate1.uAxis)
        plate1.renderingRouting = "lighting"
        table.addChild(plate1)

        plate2 = Component(Point((-1.9, (0.5 + 0.05) / 2, 0.3)), DisplayableCylinder(
            shaderProg, 1, 1, 0.05, 36, Ct.WHITE))
        plate2.setMaterial(mat_plate)
        plate2.setDefaultAngle(-90, plate2.uAxis)
        plate2.renderingRouting = "lighting"
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

        # add one cake (cylinder) to plate1
        mat_cake = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.4, 0.4, 0.4, 1)),
                            np.array((0.4, 0.4, 0.4, 0.1)), 64)
        cake = Component(Point((0, 0, (0.05 + 0.4) / 2)), DisplayableCylinder(
            shaderProg, 0.65, 0.65, 0.35, 16, Ct.YELLOW))
        cake.setMaterial(mat_cake)
        cake.setTexture(shaderProg, "assets/chocoside.jpg")
        cake.renderingRouting = "lighting_texture"
        plate1.addChild(cake)

        mat_choco = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.4, 0.4, 0.4, 1)),
                            np.array((0.4, 0.4, 0.4, 0.1)), 64)
        cake_top = Component(Point((0, 0, (0.35 + 0.15) / 2)), DisplayableCylinder(
            shaderProg, 0.67, 0.67, 0.15, 24, Ct.PURPLE))
        cake_top.setMaterial(mat_choco)
        cake_top.setTexture(shaderProg, "assets/chocotop.png")
        cake_top.renderingRouting = "lighting_texture"
        cake.addChild(cake_top)

        # add candles, using a cylinder
        l1_pos = Point((0, 1, 0))
        l1 = Light(l1_pos, np.array((*Ct.WHITE, 1.0)))
        cl1 = get_candle(shaderProg, l1_pos)
        self.addChild(cl1)

        self.lights = [l1]
        self.lightCubes = [cl1]