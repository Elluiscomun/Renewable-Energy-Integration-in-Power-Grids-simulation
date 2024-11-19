import math

class AspaAerogenerador:
    """
    Clase que representa un aspa de un aerogenerador.
    """

    def __init__(self, longitud: float):
        """
        Inicializa el objeto AspaAerogenerador con una longitud específica.
        
        :param longitud: Longitud del aspa en metros.
        """
        if longitud <= 0:
            raise ValueError("La longitud del aspa debe ser mayor que 0.")
        self.longitud = longitud
    
    @property
    def area_barrida(self) -> float:
        """
        Calcula el área barrida por el aspa.
        
        :return: Área barrida (m²).
        """
        return math.pi * (self.longitud ** 2)
    
    def energia_generada(self, densidad_aire: float, velocidad_viento: float, eficiencia: float) -> float:
        """
        Calcula la energía generada por el aspa según la fórmula de potencia eólica.
        
        Fórmula: P = 0.5 * densidad_aire * A * v³ * eficiencia
        
        :param densidad_aire: Densidad del aire (kg/m³), típico: 1.225 kg/m³.
        :param velocidad_viento: Velocidad del viento (m/s).
        :param eficiencia: Eficiencia del sistema (valor entre 0 y 1).
        :return: Potencia generada (W).
        """
        if velocidad_viento <= 0 or eficiencia <= 0 or eficiencia > 1:
            raise ValueError("Velocidad del viento y eficiencia deben ser mayores que 0 y eficiencia menor o igual a 1.")
        
        return 0.5 * densidad_aire * self.area_barrida * (velocidad_viento ** 3) * eficiencia
    
    def __str__(self):
        """
        Representación en cadena del objeto.
        """
        return f"Aspa de {self.longitud} m - Área barrida: {self.area_barrida:.2f} m²"
