"""
Define displayable Ellipsoid here.
"""

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


class DisplayableEllipsoid(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    radius_x = None
    radius_y = None
    radius_z = None
    slices = None
    stacks = None
    color = None

    def __init__(self, shaderProg,
                 radius_x=1,
                 radius_y=1,
                 radius_z=1,
                 slices=30,
                 stacks=30,
                 color=ColorType.ORANGE):
        super(DisplayableEllipsoid, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiated with glProgram activated
        self.ebo = EBO()

        self.generate(radius_x, radius_y, radius_z, slices, stacks, color)

    def generate(self,
                 radius_x, radius_y, radius_z, slices, stacks,
                 color=None):
        # Ellipsoid parametric equation:
        #   x = r_x * cos(u) * sin(v)
        #   y = r_y * sin(u) * sin(v)
        #   z = r_z * cos(v)
        #   u uses slices, v uses stacks
        # Normal vector:
        #   n_x = cos(u) * sin(v) / r_x
        #   n_y = sin(u) * sin(v) / r_y
        #   n_z = cos(v) / r_z

        self.radius_x = radius_x
        self.radius_y = radius_y
        self.radius_z = radius_z

        if slices < 3:
            slices = 3
        if stacks < 3:
            stacks = 3
        self.slices = slices
        self.stacks = stacks
        self.color = color

        pi = np.pi
        slices_1 = slices + 1
        stacks_1 = stacks + 1

        self.vertices = np.zeros((slices_1 * stacks_1, 11))
        self.indices = np.zeros((slices_1 * stacks_1, 6), dtype=np.uint32)

        for i, u in enumerate(np.linspace(-pi / 2, pi / 2, slices_1)):
            for j, v in enumerate(np.linspace(-pi, pi, stacks_1)):
                vx = np.cos(u) * np.sin(v)
                vy = np.sin(u) * np.sin(v)
                vz = np.cos(v)
                x = radius_x * vx
                y = radius_y * vy
                z = radius_z * vz
                nx = vx / radius_x
                ny = vy / radius_y
                nz = vz / radius_z

                i_by_j = i * stacks_1 + j
                ip1_by_j = (i + 1) % slices_1 * stacks_1 + j
                i_by_jp1 = i * stacks_1 + (j + 1) % stacks_1
                ip1_by_jp1 = (i + 1) % slices_1 * stacks_1 + (j + 1) % stacks_1

                self.vertices[i_by_j] = [x, y, z, nx, ny, nz, *color, j / slices, i / stacks]
                self.indices[i_by_j] = [
                    i_by_j, ip1_by_j, i_by_jp1,
                    ip1_by_jp1, ip1_by_j, i_by_jp1]

        self.indices = self.indices.flatten("C")

    def draw(self):
        self.vao.bind()
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
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
