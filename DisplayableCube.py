"""
Define displayable cube here. Current version only use VBO
First version in 10/20/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
import numpy as np
import ColorType as Ct

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


class DisplayableCube(Displayable):
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

    def __init__(self, shaderProg,
                 length: float = 1,
                 width: float = 1,
                 height: float = 1,
                 color: Ct.ColorType = Ct.BLUE,
                 texture_stretch: bool = True,
                 texture_x_unit: float = 1.0,
                 texture_y_unit: float = 1.0):
        super(DisplayableCube, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiated with glProgram activated
        self.ebo = EBO()

        self.generate(length, width, height, color,
                      texture_stretch, texture_x_unit, texture_y_unit)

    def generate(self,
                 length: float = 1,
                 width: float = 1,
                 height: float = 1,
                 color: Ct.ColorType = None,
                 texture_stretch: bool = True,
                 texture_x_unit: float = 1.0,
                 texture_y_unit: float = 1.0):

        if not texture_stretch and texture_x_unit <= 0 or texture_y_unit <= 0:
            raise ValueError("Texture unit must be positive")

        self.length = length
        self.width = width
        self.height = height
        self.color = color

        hl, hw, hh = length / 2, width / 2, height / 2
        l, w, h = length, width, height

        # Define the order of the vertices of the 6 edges
        # as well as the order of the triangles.

        # It must be ensured that the order satisfies the same law
        # so that the texture direction is the same for each face after the texture is added.
        self.vertices = np.array([
            # back face
            hl, -hw, -hh, 0, 0, -1, *color, 0, 0,
            -hl, -hw, -hh, 0, 0, -1, *color, 1, 0,
            -hl, hw, -hh, 0, 0, -1, *color, 1, 1,
            hl, hw, -hh, 0, 0, -1, *color, 0, 1,
            # front face
            -hl, -hw, hh, 0, 0, 1, *color, 0, 0,
            hl, -hw, hh, 0, 0, 1, *color, 1, 0,
            hl, hw, hh, 0, 0, 1, *color, 1, 1,
            -hl, hw, hh, 0, 0, 1, *color, 0, 1,
            # left face
            -hl, -hw, -hh, -1, 0, 0, *color, 0, 0,
            -hl, -hw, hh, -1, 0, 0, *color, 1, 0,
            -hl, hw, hh, -1, 0, 0, *color, 1, 1,
            -hl, hw, -hh, -1, 0, 0, *color, 0, 1,
            # right face
            hl, -hw, hh, 1, 0, 0, *color, 0, 0,
            hl, -hw, -hh, 1, 0, 0, *color, 1, 0,
            hl, hw, -hh, 1, 0, 0, *color, 1, 1,
            hl, hw, hh, 1, 0, 0, *color, 0, 1,
            # top face
            -hl, hw, hh, 0, 1, 0, *color, 0, 0,
            hl, hw, hh, 0, 1, 0, *color, 1, 0,
            hl, hw, -hh, 0, 1, 0, *color, 1, 1,
            -hl, hw, -hh, 0, 1, 0, *color, 0, 1,
            # bot face
            -hl, -hw, -hh, 0, -1, 0, *color, 0, 0,
            hl, -hw, -hh, 0, -1, 0, *color, 1, 0,
            hl, -hw, hh, 0, -1, 0, *color, 1, 1,
            -hl, -hw, hh, 0, -1, 0, *color, 0, 1,
        ]).reshape((-1, 11))

        if not texture_stretch:
            self.vertices[0, 9:11] = [0, 0]
            self.vertices[1, 9:11] = [l / texture_y_unit, 0]
            self.vertices[2, 9:11] = [l / texture_y_unit, w / texture_x_unit]
            self.vertices[3, 9:11] = [0, w / texture_x_unit]

            self.vertices[4, 9:11] = [0, 0]
            self.vertices[5, 9:11] = [l / texture_y_unit, 0]
            self.vertices[6, 9:11] = [l / texture_y_unit, w / texture_x_unit]
            self.vertices[7, 9:11] = [0, w / texture_x_unit]

            self.vertices[8, 9:11] = [0, 0]
            self.vertices[9, 9:11] = [h / texture_y_unit, 0]
            self.vertices[10, 9:11] = [h / texture_y_unit, w / texture_x_unit]
            self.vertices[11, 9:11] = [0, w / texture_x_unit]

            self.vertices[12, 9:11] = [0, 0]
            self.vertices[13, 9:11] = [h / texture_y_unit, 0]
            self.vertices[14, 9:11] = [h / texture_y_unit, w / texture_x_unit]
            self.vertices[15, 9:11] = [0, w / texture_x_unit]

            self.vertices[16, 9:11] = [0, 0]
            self.vertices[17, 9:11] = [l / texture_y_unit, 0]
            self.vertices[18, 9:11] = [l / texture_y_unit, h / texture_x_unit]
            self.vertices[19, 9:11] = [0, h / texture_x_unit]

            self.vertices[20, 9:11] = [0, 0]
            self.vertices[21, 9:11] = [l / texture_y_unit, 0]
            self.vertices[22, 9:11] = [l / texture_y_unit, h / texture_x_unit]
            self.vertices[23, 9:11] = [0, h / texture_x_unit]

        indices_def = np.array([
            # back face
            0, 1, 2, 0, 2, 3,
            # front face
            4, 5, 6, 4, 6, 7,
            # left face
            8, 9, 10, 8, 10, 11,
            # right face
            12, 13, 14, 12, 14, 15,
            # top face
            16, 17, 18, 16, 18, 19,
            # bot face
            20, 21, 22, 20, 22, 23,
        ])

        self.indices = np.array(indices_def)

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
