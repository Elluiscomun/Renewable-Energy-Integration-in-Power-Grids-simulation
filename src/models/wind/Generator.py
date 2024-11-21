class Generator:
    """
    Class that represents an electrical generator that converts mechanical energy into electricity.
    """

    def __init__(self, efficiency: float):
        """
        Initializes the generator with an efficiency level.

        :param efficiency: Efficiency of the generator (value between 0 and 1).
        """
        if not (0 < efficiency <= 1):
            raise ValueError("Efficiency must be between 0 and 1.")
        self.efficiency = efficiency

    def convert_energy(self, mechanical_energy: float) -> float:
        """
        Converts mechanical energy into electrical energy based on the generator's efficiency.

        :param mechanical_energy: Mechanical energy provided by the rotor (in Joules or Watts).
        :return: Electrical energy generated (in Joules or Watts).
        """
        if mechanical_energy < 0:
            raise ValueError("Mechanical energy must be greater than or equal to 0.")
        return mechanical_energy * self.efficiency

    def __str__(self):
        """
        String representation of the object.
        """
        return f"Generator with {self.efficiency * 100:.2f}% efficiency"