from typing import List

from .WindTurbineBlade import WindTurbineBlade


class Rotor:
    """
    Class that represents a wind turbine rotor composed of multiple blades.
    """

    def __init__(self, blades: List[WindTurbineBlade]):
        """
        Initializes the rotor with a list of blades.
        
        :param blades: List of WindTurbineBlade objects.
        """
        if len(blades) < 1:
            raise ValueError("The rotor must have at least one blade.")
        self.blades = blades
    
    @property
    def total_swept_area(self) -> float:
        """
        Calculates the total swept area of the rotor.
        
        :return: Total swept area (m²).
        """
        # Since the blades rotate around the same axis, the swept area is the same as that of one blade.
        return self.blades[0].swept_area if self.blades else 0
    
    def generated_energy(self, air_density: float, wind_speed: float, efficiency: float) -> float:
        """
        Calculates the total energy generated by the rotor.
        
        Formula: P = 0.5 * air_density * A * v³ * efficiency
        
        :param air_density: Air density (kg/m³), typically 1.225 kg/m³.
        :param wind_speed: Wind speed (m/s).
        :param efficiency: System efficiency (value between 0 and 1).
        :return: Total energy generated by the rotor (W).
        """
        max_recoverable_efficiency_Betz = 0.6  # Betz limit
        if not (0 < efficiency <= 1):
            raise ValueError("Efficiency must be between 0 and 1.")
        if wind_speed <= 0:
            raise ValueError("Wind speed must be greater than 0.")
        
        return 0.5 * air_density * self.total_swept_area * (wind_speed ** 3) * efficiency
    
    def __str__(self):
        """
        String representation of the object.
        """
        return f"Rotor with {len(self.blades)} blades - Total swept area: {self.total_swept_area:.2f} m²"