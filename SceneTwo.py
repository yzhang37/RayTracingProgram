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
from DisplayableCylinder import DisplayableCylinder
from DisplayableEllipsoid import DisplayableEllipsoid
from DisplayableTorus import DisplayableTorus
from SceneType import Scene
from Component import Component
from Light import Light
from Material import Material
from Point import Point

from DisplayableCube import DisplayableCube
from DisplayableSphere import DisplayableSphere
from util import vec1_to_vec2, create_flash_light, light_helper


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
    def __init__(self, shaderProg):
        super().__init__(shaderProg)

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
                               DisplayableSphere(shaderProg, 0.7, color=Ct.ColorType(
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
                                      DisplayableEllipsoid(shaderProg, 0.5, 0.5, 0.9, color=Ct.ColorType(
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
        mat_ring = Material(np.array((0.1, 0.1, 0.1, 0.1)), np.array((0.3, 0.3, 0.3, 1)),
                             np.array((0.7, 0.7, 0.7, 0.1)), 64)

        ring_colors = [Ct.BLUE, Ct.RED]
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

            for j in np.linspace(0, 2, 3):
                ring = Component(Point((0 + i * 0.8, -0.6 + j * 0.15, 1.2)),
                                 DisplayableTorus(shaderProg, 0.2, 0.26, 16, 16, color=random.choice(ring_colors)))
                ring.setMaterial(mat_ring)
                ring.setDefaultAngle(90 + random.gauss(0, 10), ring.uAxis)
                ring.setDefaultAngle(random.gauss(0, 10), ring.vAxis)
                self.addChild(ring)

        def turn_on(component):
            component.renderingRouting = "texture"

        def turn_off(component):
            component.renderingRouting = "lighting_texture"

        l0_pos = Point([0, 1, 0])
        l0 = Light(l0_pos, np.array((*Ct.WHITE, 1.0)), np.array((0, 0, 1)))
        lightCube0 = Component(l0_pos, DisplayableCube(shaderProg, 2, 0.1, 0.4, Ct.WHITE))
        lightCube0.setTexture(self.shaderProg, "assets/fluorescent.jpg")
        lightCube0.renderingRouting = "texture"
        lightCube0.setDefaultAngle(90, lightCube0.vAxis)
        lightCube0.turn_on = turn_on
        lightCube0.turn_off = turn_off
        self.addChild(lightCube0)

        v_def = Point((0, 0, 1))
        flashlight_scale = (0.35, 0.35, 0.35)
        flashlight_settings = {
            "spotRadialFactor": np.array((0.05, 0.1, 0.01)),
            "spotAngleLimit": math.cos(math.pi / 5),
            "spotExpAttenuation": 16
        }
        # add flashlight
        flash1_obj = create_flash_light(shaderProg)
        fl1_pos = Point((1.5, -0.55, 2.5))
        flash1_obj.setDefaultPosition(fl1_pos)
        flash1_obj.setDefaultScale(flashlight_scale)
        fl1_direct = Point((1, 0.15, 1))
        flash1_obj.setPreRotation(vec1_to_vec2(v_def, fl1_direct))
        self.addChild(flash1_obj)
        flash1_light = Light(fl1_pos, np.array((*Ct.WHITE, 1.0)), None,
                             spotDirection=fl1_direct, **flashlight_settings)

        flash2_obj = create_flash_light(shaderProg)
        fl2_pos = Point((-1.5, -0.55, 2.5))
        flash2_obj.setDefaultPosition(fl2_pos)
        flash2_obj.setDefaultScale(flashlight_scale)
        fl2_direct = Point((-1, 0.15, 1))
        flash2_obj.setPreRotation(vec1_to_vec2(v_def, fl2_direct))
        self.addChild(flash2_obj)
        flash2_light = Light(fl2_pos, np.array((*Ct.WHITE, 1.0)), None,
                             spotDirection=fl2_direct, **flashlight_settings)

        flash3_obj = create_flash_light(shaderProg)
        fl3_pos = Point((-2.2, -0.55, -0.2))
        flash3_obj.setDefaultPosition(fl3_pos)
        flash3_obj.setDefaultScale(flashlight_scale)
        fl3_direct = Point((-2, 0.15, 1))
        flash3_obj.setPreRotation(vec1_to_vec2(v_def, fl3_direct))
        self.addChild(flash3_obj)
        flash3_light = Light(fl3_pos, np.array((*Ct.WHITE, 1.0)), None,
                             spotDirection=fl3_direct, **flashlight_settings)

        flash4_obj = create_flash_light(shaderProg)
        fl4_pos = Point((2.4, -0.55, -2.5))
        flash4_obj.setDefaultPosition(fl4_pos)
        flash4_obj.setDefaultScale(flashlight_scale)
        fl4_direct = Point((0.5, 0, -1))
        flash4_obj.setPreRotation(vec1_to_vec2(v_def, fl4_direct))
        self.addChild(flash4_obj)
        flash4_light = Light(fl4_pos, np.array((*Ct.WHITE, 1.0)), None,
                             spotDirection=fl4_direct, **flashlight_settings)

        flash5_obj = create_flash_light(shaderProg)
        fl5_pos = Point((1.3, 0.5, -0.2))
        flash5_obj.setDefaultPosition(fl5_pos)
        flash5_obj.setDefaultScale(flashlight_scale)
        fl5_direct = Point((0.980581, -0.196116, 0))
        flash5_obj.setPreRotation(vec1_to_vec2(v_def, fl5_direct))
        self.addChild(flash5_obj)
        flash5_light = Light(fl5_pos, np.array((*Ct.WHITE, 1.0)), None,
                             spotDirection=fl5_direct, **flashlight_settings)

        self.lights = [l0, flash1_light, flash2_light, flash3_light, flash4_light, flash5_light]
        self.lightCubes = [lightCube0, flash1_obj, flash2_obj, flash3_obj, flash4_obj, flash5_obj]
        light_helper(l0, lightCube0, False)
        light_helper(flash1_light, flash1_obj, False)
        light_helper(flash2_light, flash2_obj, False)
        light_helper(flash3_light, flash3_obj, False)
        light_helper(flash4_light, flash4_obj, False)
