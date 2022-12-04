"""
Define a class to store Material information
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

import numpy as np
from typing import Union, Optional
import typing


class Material:
    ambient: np.ndarray
    diffuse: np.ndarray
    specular: np.ndarray
    highLight: Union[int, float]
    useNormalMap: bool = False

    def __init__(self,
                 ambient: Optional[np.ndarray] = None,
                 diffuse: Optional[np.ndarray] = None,
                 specular: Optional[np.ndarray] = None,
                 highlight: Union[int, float] = 32,
                 useNormalMap=False):
        if ambient is not None:
            self.setAmbient(ambient)
        else:
            self.ambient = np.array((0, 0, 0, 0))

        if diffuse is not None:
            self.setDiffuse(diffuse)
        else:
            self.diffuse = np.array((0, 0, 0, 0))

        if specular is not None:
            self.setSpecular(specular)
        else:
            self.specular = np.array((0, 0, 0, 0))
        self.highLight = highlight
        self.useNormalMap = useNormalMap

    def setAmbient(self, ambient: np.ndarray):
        if (not isinstance(ambient, np.ndarray)) or ambient.size != 4:
            raise TypeError("ambient must be a size 4 ndarray")
        self.ambient = ambient

    def setDiffuse(self, diffuse: np.ndarray):
        if (not isinstance(diffuse, np.ndarray)) or diffuse.size != 4:
            raise TypeError("diffuse must be a size 4 ndarray")
        self.diffuse = diffuse

    def setSpecular(self, specular: np.ndarray):
        if (not isinstance(specular, np.ndarray)) or specular.size != 4:
            raise TypeError("specular must be a size 4 ndarray")
        self.specular = specular

    def setHighlight(self, highLight: Union[int, float]):
        if type(highLight) != (int or float):
            print(type(highLight))
            raise TypeError("highLight must be a float/int")
        self.highLight = highLight

    def setUseNormalMap(self, useNormalMap: bool):
        self.useNormalMap = useNormalMap

    def setMaterial(self,
                    ambient: np.ndarray,
                    diffuse: np.ndarray,
                    specular: np.ndarray,
                    highlight: Union[int, float],
                    useNormalMap: bool):
        self.setAmbient(ambient)
        self.setDiffuse(diffuse)
        self.setSpecular(specular)
        self.setHighlight(highlight)
        self.useNormalMap = useNormalMap
