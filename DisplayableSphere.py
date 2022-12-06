"""
Define displayable cube here. Current version only use VBO
First version in 10/20/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
from typing import Optional

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
import numpy as np
import ColorType
import math

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")


class DisplayableSphere(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    radius = None
    slices = None
    stacks = None
    color = None

    def __init__(self, shaderProg,
                 radius=1,
                 slices=30,
                 stacks=30,
                 color=ColorType.BLUE):
        super(DisplayableSphere, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiated with glProgram activated
        self.ebo = EBO()

        self.generate(radius, slices, stacks, color)

    def generate(self,
                 radius: float,
                 slices: int,
                 stacks: int,
                 color: Optional[ColorType] = None):
        # If the number of slices or stacks is less than 3, set it to 3
        if slices < 3:
            slices = 3
        if stacks < 3:
            stacks = 3

        # Set the class parameters
        self.radius = radius
        self.slices = slices
        self.stacks = stacks
        self.color = color
        pi = math.pi

        # Calculate the number of vertices and indices based on the number of slices and stacks
        slices_1 = slices + 1
        stacks_1 = stacks + 1
        self.vertices = np.zeros((slices_1 * stacks_1, 11))
        self.indices = np.zeros((slices_1 * stacks_1, 6), dtype=np.uint32)

        # Loop over the slices and stacks, calculating the x, y, and z coordinates
        # of each vertex and the corresponding normal vector
        for i, phi in enumerate(np.linspace(-pi / 2, pi / 2, slices_1)):
            for j, theta in enumerate(np.linspace(-pi, pi, stacks_1)):
                x = radius * math.cos(phi) * math.cos(theta)
                y = radius * math.cos(phi) * math.sin(theta)
                z = radius * math.sin(phi)

                nx = math.cos(phi) * math.cos(theta)
                ny = math.cos(phi) * math.sin(theta)
                nz = math.sin(phi)

                # Encoding vertex order using C array order
                i_by_j = i * stacks_1 + j
                self.vertices[i_by_j] = [x, y, z, nx, ny, nz, *color, j / stacks, i / slices]

                # I've combined the two loops here so that the number of loops can be reduced.
                ip1_by_j = (i + 1) % slices_1 * stacks_1 + j
                i_by_jp1 = i * stacks_1 + (j + 1) % stacks_1
                ip1_by_jp1 = (i + 1) % slices_1 * stacks_1 + (j + 1) % stacks_1

                # Set the indices in the correct order for CCW winding
                self.indices[i_by_j] = [
                    i_by_j, ip1_by_j, i_by_jp1,
                    ip1_by_jp1, ip1_by_j, i_by_jp1]

        self.indices = self.indices.flatten("C")

    def draw(self):
        self.vao.bind()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems that don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 11)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"),
                                  stride=11, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"),
                                  stride=11, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"),
                                  stride=11, offset=6, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexTexture"),
                                  stride=11, offset=9, attribSize=2)
        self.vao.unbind()
