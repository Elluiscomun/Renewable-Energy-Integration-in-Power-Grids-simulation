import math
from typing import List


class WindTurbineBlade:
    """
    Class representing a wind turbine blade.
    """

    def __init__(self, length: float):
        """
        Initializes the WindTurbineBlade object with a specific length.
        
        :param length: Length of the blade in meters.
        """
        if length <= 0:
            raise ValueError("The blade length must be greater than 0.")
        self.length = length
    
    @property
    def swept_area(self) -> float:
        """
        Calculates the swept area of the blade.
        
        :return: Swept area (m²).
        """
        return math.pi * (self.length ** 2)
    
    def __str__(self):
        """
        String representation of the object.
        """
        return f"Blade of {self.length} m - Swept area: {self.swept_area:.2f} m²"
