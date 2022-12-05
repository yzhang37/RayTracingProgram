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
from SceneType import Scene
from Component import Component
from Light import Light
from Material import Material
from Point import Point
import GLUtility

from DisplayableCube import DisplayableCube
from DisplayableTorus import DisplayableTorus
from DisplayableSphere import DisplayableSphere

##### 1: Generate Triangle Meshes
# Requirements:
#   1. Use Element Buffer Object (EBO) to draw the cube. The cube provided in the start code is drawn with Vertex Buffer
#   Object (VBO). In the DisplayableCube class draw method, you should switch from VBO draw to EBO draw. To achieve
#   this, please first read through VBO and EBO classes in GLBuffer. Then you rewrite the self.vertices and self.indices
#   in the DisplayableCube class. Once you have all these down, then switch the line vbo.draw() to ebo.draw().
#   2. Generate Displayable classes for an ellipsoid, torus, and cylinder with end caps.
#   These classes should be like the DisplayableCube class and they should all use EBO in the draw method.
#   PS: You must use the ellipsoid formula to generate it, scaling the Displayable sphere doesn't count
#
#   Displayable object's self.vertices numpy matrix should be defined as this table:
#   Column | 0:3                | 3:6           | 6:9          | 9:11
#   Stores | Vertex coordinates | Vertex normal | Vertex Color | Vertex texture Coordinates
#
#   Their __init__ method should accept following input
#   arguments:
#   DisplayableEllipsoid(radiusInX, radiusInY, radiusInZ, slices, stacks)
#   DisplayableTorus(innerRadius, outerRadius, nsides, rings)
#   DisplayableCylinder(endRadius, height, slices, stacks)
#

##### 5: Create your scenes
# Requirements:
#   1. We provide a fixed scene (SceneOne) for you with preset lights, material, and model parameters.
#   This scene will be used to examine your illumination implementation, and you should not modify it.
#   2. Create 3 new scenes (can be static scenes). Each of your scenes must have
#      * at least 3 differently shaped solid objects
#      * each object should have a different material
#      * at least 2 lights
#      * All types of lights should be used
#   3. Provide a keyboard interface that allows the user to toggle on/off each of the lights in your scene model:
#   Hit 1, 2, 3, 4, etc. to identify which light to toggle.


class SceneTwo(Scene):
    shaderProg = None
    glutility = None

    def __init__(self, shaderProg):
        super().__init__()
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        # Add one hardwood floor
        hardwood = Component(Point((0, -1, 0)), DisplayableCube(shaderProg, 7, 0.5, 7))
        mat_hardwood = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.4, 0.4, 0.4, 1)),
                      np.array((0.4, 0.4, 0.4, 0.1)), 32)
        hardwood.setMaterial(mat_hardwood)
        hardwood.renderingRouting = "lighting_texture"
        hardwood.setTexture(self.shaderProg, "assets/hardwood.png")
        hardwood.setNormalMap(self.shaderProg, "assets/hardwood_norm.png")
        self.addChild(hardwood)

        # Add one basketball
        basketball = Component(Point((-1.2, 0, -1)),
                               DisplayableSphere(shaderProg, 0.7, color=ColorType.ColorType(
                                   155 / 255, 79 / 255, 44 / 255)))
        mat_basket = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.4, 0.4, 0.4, 1)),
                      np.array((0.4, 0.4, 0.4, 0.1)), 64)
        basketball.setMaterial(mat_basket)
        basketball.setTexture(self.shaderProg, "assets/basketball.png")
        basketball.renderingRouting = "lighting_texture"
        basketball.setNormalMap(self.shaderProg, "assets/basketball_norm.png")
        self.addChild(basketball)

        # Add one american football
        american_football = Component(Point((1.2, 0, -1)),
                                      DisplayableEllipsoid(shaderProg, 0.5, 0.5, 0.9, color=ColorType.ColorType(
                                            136 / 255, 66 / 255, 30 / 255)))
        mat_american_football = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.4, 0.4, 0.4, 1)),
                        np.array((0.4, 0.4, 0.4, 0.1)), 64)
        american_football.setMaterial(mat_american_football)
        american_football.setTexture(self.shaderProg, "assets/football.png")
        american_football.renderingRouting = "lighting_texture"
        american_football.setNormalMap(self.shaderProg, "assets/football_norm.png")
        american_football.setDefaultAngle(90, american_football.vAxis)
        american_football.setDefaultAngle(90, american_football.wAxis)
        self.addChild(american_football)

        mat_stick = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.4, 0.4, 0.4, 1)),
                             np.array((0.4, 0.4, 0.4, 0.1)), 64)
        # three sticks
        for i in np.linspace(-1, 1, 3):
            stick = Component(Point((0 + i * 0.8, -0.3, 1.2)),
                              DisplayableCylinder(shaderProg, 0.05, 0.05, 1, 36))
            stick.setDefaultAngle(90, stick.uAxis)
            stick.setMaterial(mat_stick)
            stick.renderingRouting = "lighting_texture"
            stick.setTexture(self.shaderProg, "assets/hardwood.png")
            stick.setNormalMap(self.shaderProg, "assets/hardwood_norm.png")
            self.addChild(stick)

        l0 = Light(Point([0.0, 1.5, 0.0]),
                   np.array((*ColorType.WHITE, 1.0)))
        lightCube0 = Component(Point((0.0, 1.5, 0.0)), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.WHITE))
        lightCube0.renderingRouting = "vertex"

        self.addChild(lightCube0)
        self.lights = [l0, ]
        self.lightCubes = [lightCube0, ]

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
