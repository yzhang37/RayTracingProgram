"""
Define displayable Cylinder here.
"""
from typing import Optional

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
import numpy as np
import ColorType as Ct
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
                 color=Ct.WHITE):
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
                 radius_lower: float,  # The lower radius of the cylinder
                 radius_upper: float,  # The upper radius of the cylinder
                 height: float,  # The height of the cylinder
                 nsides: int,  # The number of sides of the cylinder
                 color: Optional[Ct.ColorType] = None):  # The color of the cylinder (defaults to None)
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
            # Raise an error if any of the cylinder dimensions are non-positive
            raise ValueError("Invalid cylinder parameters")

        self.radius_lower = radius_lower   # Assign the lower radius to an attribute of the Cylinder object
        self.radius_upper = radius_upper   # Assign the upper radius to an attribute of the Cylinder object
        self.height = height               # Assign the height to an attribute of the Cylinder object
        self.nsides = nsides               # Assign the number of sides to an attribute of the Cylinder object
        self.color = color                 # Assign the color to an attribute of the Cylinder object

        # Half the height of the cylinder
        hh = height / 2.0

        # The number of vertices along each edge of the cylinder,
        # there should be one more vertex than the original numbers.
        nsides_1 = nsides + 1

        # Each group of vertices (for a single side of the cylinder)
        # will contain four vertices: one for each end of the side and
        # two for the curved surface of the side
        grp_size = 4

        # The first two vertices are used to store the
        # centers of the upper and lower circles.
        self.vertices = np.zeros((nsides_1 * grp_size + 2, 11), dtype=np.float32)

        # lower circle center and upper circle center
        self.vertices[0] = [0, 0, -hh, 0, 0, -1, *color, 0.5, 0.5]
        self.vertices[1] = [0, 0, hh, 0, 0, 1, *color, 0.5, 0.5]

        # The universal offset for the later vertices other than above two
        # centers
        vOffset = 2

        self.indices = np.zeros((nsides_1, 12), dtype=np.uint32)

        pi = np.pi

        # The sine and cosine of the angle between the lower and upper radii of the cylinder
        # (used to calculate the normal vectors for the side surfaces)
        cone_sin = (radius_lower - radius_upper) / height
        cone_cos = np.sqrt(1 - cone_sin * cone_sin)
        for i, theta in enumerate(np.linspace(-pi, pi, nsides_1)):
            cos_val = np.cos(theta)
            sin_val = np.sin(theta)

            # Calculate the coordinates of the points on the lower circle of the cylinder
            x_lower = radius_lower * cos_val
            y_lower = radius_lower * sin_val
            z_lower = -hh

            # Assign the coordinates of the point on the lower circle,
            # the normal vector for the lower surface, and the texture coordinates
            # to the appropriate vertex in the vertex group
            self.vertices[vOffset + grp_size * i] = [
                x_lower, y_lower, z_lower, 0, 0, -1, *color,
                cos_val * 0.5 + 0.5, sin_val * 0.5 + 0.5]

            ip1 = (i + 1) % nsides_1
            self.indices[i, 0:3] = [0, vOffset + grp_size * i, vOffset + grp_size * ip1]

            # Calculate the coordinates of the points on the upper circle of the cylinder
            x_upper = radius_upper * cos_val
            y_upper = radius_upper * sin_val
            z_upper = hh

            # UPDATE: side surface, we have to redefine the vertices above since they have different normals
            # Assign the coordinates of the points on the upper and lower circles,
            # the normal vector for the side surface, and the texture coordinates
            # to the appropriate vertices in the vertex group
            self.vertices[vOffset + grp_size * i + 1] = [
                x_lower, y_lower, z_lower,
                cos_val * cone_cos, sin_val * cone_cos, cone_sin, *color,
                i / nsides, 0]
            self.vertices[vOffset + grp_size * i + 2] = [
                x_upper, y_upper, z_upper,
                cos_val * cone_cos, sin_val * cone_cos, cone_sin, *color,
                i / nsides, 1]
            self.indices[i, 3:9] = [
                vOffset + grp_size * i + 1, vOffset + grp_size * i + 2, vOffset + grp_size * ip1 + 2,
                vOffset + grp_size * i + 1, vOffset + grp_size * ip1 + 2, vOffset + grp_size * ip1 + 1]

            # Assign the indices of the vertices that make up the
            # triangles on the upper surface of the cylinder
            self.vertices[vOffset + grp_size * i + 3] = [
                x_upper, y_upper, z_upper, 0, 0, 1, *color,
                cos_val * 0.5 + 0.5, sin_val * 0.5 + 0.5]
            self.indices[i, 9:12] = [1, vOffset + grp_size * i + 3, vOffset + grp_size * ip1 + 3]

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
