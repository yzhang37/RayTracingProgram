"""
Define displayable cube here. Current version only use VBO
First version in 10/20/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
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


class DisplayableSphere(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    length = None
    width = None
    height = None
    color = None

    def __init__(self, shaderProg, radius=1, color=ColorType.BLUE):
        super(DisplayableSphere, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(radius, color)

    def generate(self, radius=1, color=None, slices=30, stacks=30):
        # self.length = length
        # self.width = width
        # self.height = height
        self.color = color
        pi = math.pi

        slices_1 = slices + 1
        stacks_1 = stacks + 1
        # sphere_vertices = np.zeros([slices + 1, stacks + 1, 3])
        # sphere_normals = np.zeros([slices + 1, stacks + 1, 3])
        sphere_vbo_data = np.zeros((slices_1 * stacks_1, 9))
        sphere_indices = np.zeros((slices_1 * stacks_1, 6), dtype=np.uint32)

        for i, phi in enumerate(np.arange(-pi / 2, pi / 2 + pi / slices, pi / slices)):
            for j, theta in enumerate(np.arange(-pi, pi + pi / (stacks / 2), pi / (stacks / 2))):
                x = radius * math.cos(phi) * math.cos(theta)
                y = radius * math.cos(phi) * math.sin(theta)
                z = radius * math.sin(phi)

                x_normal = math.cos(phi) * math.cos(theta)
                y_normal = math.cos(phi) * math.sin(theta)
                z_normal = math.sin(phi)

                # sphere_vertices[i][j] = [x, y, z]
                # sphere_normals[i][j] = [x_normal, y_normal, z_normal]

                # Encoding vertex order using C array order
                i_by_j = i * stacks_1 + j
                sphere_vbo_data[i_by_j] = [x, y, z, x_normal, y_normal, z_normal, *color]

                # I've combined the two loops here so that the number of loops can be reduced.
                i_1 = (i + 1) % slices_1
                j_1 = (j + 1) % stacks_1
                sphere_indices[i_by_j] = [
                    i_by_j, i * stacks_1 + j_1, i_1 * stacks_1 + j_1,
                    i_by_j, i_1 * stacks_1 + j, i_1 * stacks_1 + j_1]

        # triangle_list = []
        # for i in range(slices):
        #     for j in range(stacks):
        #         i_1 = (i + 1) % (slices + 1)
        #         j_1 = (j + 1) % (stacks + 1)
        #         triangle_list.append(np.array([*sphere_vertices[i][j], *sphere_normals[i][j], *color]))
        #         triangle_list.append(np.array([*sphere_vertices[i][j_1], *sphere_normals[i][j_1], *color]))
        #         triangle_list.append(np.array([*sphere_vertices[i_1][j_1], *sphere_normals[i_1][j_1], *color]))
        #
        #         triangle_list.append(np.array([*sphere_vertices[i][j], *sphere_normals[i][j], *color]))
        #         triangle_list.append(np.array([*sphere_vertices[i_1][j], *sphere_normals[i_1][j], *color]))
        #         triangle_list.append(np.array([*sphere_vertices[i_1][j_1], *sphere_normals[i_1][j_1], *color]))
        # new_vl = np.stack(triangle_list)

        self.vertices = np.zeros([len(sphere_vbo_data), 11])
        self.vertices[0:len(sphere_vbo_data), 0:9] = sphere_vbo_data

        self.indices = sphere_indices.flatten("C")

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
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()
