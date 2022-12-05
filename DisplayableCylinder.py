"""
Define displayable Cylinder here.
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


class DisplayableCylinder(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    color = None
    nsides = None
    radius_upper = None
    radius_lower = None
    height = None

    def __init__(self, shaderProg,
                 radius_lower=1.0,
                 radius_upper=1.0,
                 height=1.0,
                 nsides=3,
                 color=ColorType.WHITE):
        super(DisplayableCylinder, self).__init__()

        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiated with glProgram activated
        self.ebo = EBO()

        self.generate(radius_lower,
                      radius_upper,
                      height,
                      nsides,
                      color)

    def generate(self,
                 radius_lower,
                 radius_upper,
                 height,
                 nsides,
                 color=None):
        # Surface parameter:
        #   x = ((0.5 + u/h) * r_lower + (0.5 - u/h) * r_upper) * cos(theta)
        #   y = ((0.5 + u/h) * r_lower + (0.5 - u/h) * r_upper) * sin(theta)
        #   z = u from -h/2 to h/2
        # Normals:
        # - On the upper surface
        #   n = (0, 0, 1)
        # - On the lower surface
        #   n = (0, 0, -1)
        # - On the side surface
        #   n = (cos(theta) * √(1 - cSin²), sin(theta) * √(1 - cSin²), cSin)
        #       where cSin = (r_lower - r_upper) / h

        if radius_lower <= 0 or radius_upper <= 0 or height <= 0:
            raise ValueError("Invalid cylinder parameters")

        self.radius_lower = radius_lower
        self.radius_upper = radius_upper
        self.height = height
        self.nsides = nsides
        self.color = color
        hh = height / 2.0

        nsides += 1
        # The first two vertices are used to store the
        # centers of the upper and lower circles.
        grp_size = 4
        self.vertices = np.zeros((nsides * grp_size + 2, 11), dtype=np.float32)
        # lower circle center and upper circle center
        self.vertices[0, 0:9] = [0, 0, -hh, 0, 0, -1, *color]
        self.vertices[1, 0:9] = [0, 0, hh, 0, 0, 1, *color]
        vOffset = 2
        self.indices = np.zeros((nsides, 12), dtype=np.uint32)

        pi = np.pi
        cone_sin = (radius_lower - radius_upper) / height
        cone_cos = np.sqrt(1 - cone_sin * cone_sin)
        for i, theta in enumerate(np.linspace(-pi, pi, nsides)):
            cos_val = np.cos(theta)
            sin_val = np.sin(theta)
            # lower surface
            x_lower = radius_lower * cos_val
            y_lower = radius_lower * sin_val
            z_lower = -hh
            self.vertices[vOffset + grp_size*i, 0:9] = [
                x_lower, y_lower, z_lower, 0, 0, -1, *color]
            ip1 = (i + 1) % nsides
            self.indices[i, 0:3] = [0, vOffset + grp_size*i, vOffset + grp_size * ip1]

            x_upper = radius_upper * cos_val
            y_upper = radius_upper * sin_val
            z_upper = hh

            # side surface, we have to redefine the vertices above since they have different normals
            self.vertices[vOffset + grp_size*i + 1, 0:9] = [
                x_lower, y_lower, z_lower, cos_val * cone_cos, sin_val * cone_cos, cone_sin, *color]
            self.vertices[vOffset + grp_size*i + 2, 0:9] = [
                x_upper, y_upper, z_upper, cos_val * cone_cos, sin_val * cone_cos, cone_sin, *color]
            self.indices[i, 3:9] = [
                vOffset + grp_size*i + 1, vOffset + grp_size*i + 2, vOffset + grp_size*ip1 + 2,
                vOffset + grp_size*i + 1, vOffset + grp_size*ip1 + 2, vOffset + grp_size*ip1 + 1]

            # upper surface
            self.vertices[vOffset + grp_size*i + 3, 0:9] = [
                x_upper, y_upper, z_upper, 0, 0, 1, *color]
            self.indices[i, 9:12] = [1, vOffset + grp_size*i + 3, vOffset + grp_size*ip1 + 3]

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
