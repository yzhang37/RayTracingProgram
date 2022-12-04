"""
Define a class to store Material information
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

import numpy as np
from typing import Union, Optional


class Material:
    _ambient: np.ndarray
    _diffuse: np.ndarray
    _specular: np.ndarray
    _highLight: Union[int, float]

    def __init__(self,
                 ambient: Optional[np.ndarray] = None,
                 diffuse: Optional[np.ndarray] = None,
                 specular: Optional[np.ndarray] = None,
                 highlight: Union[int, float] = 32):
        self.ambient = np.zeros(4) if ambient is None else ambient
        self.diffuse = np.zeros(4) if diffuse is None else diffuse
        self.specular = np.zeros(4) if specular is None else specular
        self.highLight = highlight

    @property
    def ambient(self) -> np.ndarray:
        return self._ambient

    @ambient.setter
    def ambient(self, ambient: np.ndarray):
        if (not isinstance(ambient, np.ndarray)) or ambient.size != 4:
            raise TypeError("ambient must be a size 4 ndarray")
        self._ambient = ambient

    @property
    def diffuse(self) -> np.ndarray:
        return self._diffuse

    @diffuse.setter
    def diffuse(self, diffuse: np.ndarray):
        if (not isinstance(diffuse, np.ndarray)) or diffuse.size != 4:
            raise TypeError("diffuse must be a size 4 ndarray")
        self._diffuse = diffuse

    @property
    def specular(self) -> np.ndarray:
        return self._specular

    @specular.setter
    def specular(self, specular: np.ndarray):
        if (not isinstance(specular, np.ndarray)) or specular.size != 4:
            raise TypeError("specular must be a size 4 ndarray")
        self._specular = specular

    @property
    def highlight(self) -> Union[int, float]:
        return self._highLight

    @highlight.setter
    def highlight(self, highLight: Union[int, float]):
        if type(highLight) != (int or float):
            print(type(highLight))
            raise TypeError("highLight must be a float/int")
        self._highLight = highLight

    def setMaterial(self,
                    ambient: np.ndarray,
                    diffuse: np.ndarray,
                    specular: np.ndarray,
                    highlight: Union[int, float]):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.highlight = highlight
