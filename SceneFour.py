"""
Define a fixed scene with rotating lights
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import math
import random

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
from util import light_helper


# function that generates a random angle value in the range [-90.0, 90.0].
def get_random_degree() -> float:
    return random.random() * 180.0 - 90.0


# sets a random rotation for the given component object along the x, y, and z axes.
# The function takes the component object, as well as the x, y, and z rotation values,
# and applies a random offset to each of these values using get_random_degree()
def set_random_rotation(component: Component, x, y, z):
    component.setDefaultAngle(x + 0.6 * get_random_degree(), component.uAxis)
    component.setDefaultAngle(y + 0.6 * get_random_degree(), component.vAxis)
    component.setDefaultAngle(z + 0.6 * get_random_degree(), component.wAxis)


class SceneFour(Scene):
    def __init__(self, shaderProg: GLProgram):
        Scene.__init__(self, shaderProg)
        self.lights.clear()
        self.lightCubes.clear()

        mat_table = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.5, 0.5, 0.5, 1)),
                             np.array((0.1, 0.1, 0.1, 0.1)), 16)
        # add the pool table
        table = Component(Point((0, -1, 0)), DisplayableCube(
            shaderProg, 7, 0.5, 7, Ct.SEAGREEN,
            False, 1, 1
        ))
        table.setTexture(shaderProg, "assets/pool.png")
        table.setNormalMap(shaderProg, "assets/pool_norm.png")
        table.renderingRouting = "lighting_texture"
        table.setMaterial(mat_table)
        self.addChild(table)

        # material for the ball
        mat_ball = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.7, 0.7, 0.7, 1)),
                            np.array((0.9, 0.9, 0.9, 0.1)), 12)

        c_x = 1.35
        c_y = 0
        c_z = 0
        # add balls 1 - 15
        ball_radius = 0.2
        height = ball_radius * 2 * 4 * math.sqrt(3) / 2
        ball_count = 0
        for i, pa in enumerate(np.linspace(-2/3, 1/3, 5)):
            base_x = pa * height
            for j in range(0, i + 1):
                pb = j - i / 2
                base_z = -pb * ball_radius * 2
                ball = Component(Point((c_x + base_x, c_y + 0.5 / 2 + ball_radius, c_z + base_z)), DisplayableSphere(
                    shaderProg, ball_radius, 16, 16, Ct.WHITE
                ))
                ball_count += 1
                filename = f"assets/billiard_{ball_count:02d}.png"
                print(filename)
                ball.setTexture(shaderProg, filename)
                ball.renderingRouting = "lighting_texture"
                ball.setMaterial(mat_ball)
                set_random_rotation(ball, 0, -90, 0)
                table.addChild(ball)
        # add #0 ball
        ball = Component(Point((c_x - 2.5, c_y + 0.5 / 2 + ball_radius, c_z)), DisplayableSphere(
            shaderProg, ball_radius, 16, 16, Ct.WHITE
        ))
        ball.setTexture(shaderProg, f"assets/billiard_00.png")
        ball.renderingRouting = "lighting_texture"
        ball.setMaterial(mat_ball)
        set_random_rotation(ball, 0, -90, 0)
        table.addChild(ball)

        # add the frame of the balls, it's radius should be 2/3 * height
        inner = height * 2/3 + ball_radius * 2
        thickness = 0.4
        frame = Component(Point((c_x, c_y + (0.5 + thickness) / 2, c_z)), DisplayableTorus(
            shaderProg, inner, inner + thickness, 3, 15, Ct.ORANGE
        ))
        frame.setDefaultAngle(90, frame.uAxis)
        frame.renderingRouting = "texture_lighting"
        frame.setTexture(shaderProg, "assets/hardwood.png")
        frame.setNormalMap(shaderProg, "assets/hardwood_norm.png")
        mat_frame = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.4, 0.4, 0.4, 1)),
                             np.array((0.4, 0.4, 0.4, 0.1)), 64)
        frame.setMaterial(mat_frame)
        table.addChild(frame)

        # add the cue

        def turn_on(component):
            component.renderingRouting = "texture"

        def turn_off(component):
            component.renderingRouting = "lighting_texture"

        fluo_dark_material = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.2, 0.2, 0.2, 1)),
                                      np.array((0.9, 0.9, 0.9, 0.1)), 20)
        fluo0_pos = Point([-0.5, 2, 0])
        fluo0_light = Light(fluo0_pos, np.array((*Ct.WHITE, 1.0)), np.array((0, 0, 1)))
        fluo0_obj = Component(fluo0_pos, DisplayableCube(shaderProg, 2, 0.1, 0.4, Ct.WHITE))
        fluo0_obj.setTexture(self.shaderProg, "assets/fluorescent.jpg")
        fluo0_obj.renderingRouting = "texture"
        fluo0_obj.setDefaultAngle(90, fluo0_obj.vAxis)
        fluo0_obj.turn_on = turn_on
        fluo0_obj.turn_off = turn_off
        fluo0_obj.setMaterial(fluo_dark_material)
        self.lights.append(fluo0_light)
        self.lightCubes.append(fluo0_obj)
        self.addChild(fluo0_obj)

        fluo1_pos = Point([0.5, 2, 0])
        fluo1_light = Light(fluo1_pos, np.array((*Ct.WHITE, 1.0)))
        fluo1_obj = Component(fluo1_pos, DisplayableCube(shaderProg, 2, 0.1, 0.4, Ct.WHITE))
        fluo1_obj.setTexture(self.shaderProg, "assets/fluorescent.jpg")
        fluo1_obj.renderingRouting = "texture"
        fluo1_obj.setDefaultAngle(90, fluo1_obj.vAxis)
        fluo1_obj.turn_on = turn_on
        fluo1_obj.turn_off = turn_off
        fluo1_obj.setMaterial(fluo_dark_material)
        self.lights.append(fluo1_light)
        self.lightCubes.append(fluo1_obj)
        self.addChild(fluo1_obj)

        light_helper(fluo0_light, fluo0_obj, False)
