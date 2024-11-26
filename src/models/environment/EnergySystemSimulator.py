# Asegúrate de que las clases ya definidas estén correctamente importadas antes de crear la nueva clase

# Importación de las clases previamente definidas
from ..baseCase.DataManager import DataManager
from src.models.baseCase.EnergyConsumptionSimulator import EnergyConsumptionSimulator
from src.models.baseCase.EnergyVisualizer import EnergyVisualizer
from src.models.wind.WindTurbineBlade import WindTurbineBlade
from src.models.wind.Generator import Generator

class EnergySystemSimulator:
    def __init__(self, data_ri_path: str, data_ni_path: str, weeks: int, homes: int, blade_length: float, generator_efficiency: float):
        """
        Inicializa el simulador del sistema energético integrando todas las clases necesarias.
        
        :param data_ri_path: Ruta del archivo CSV con datos de variación de consumo.
        :param data_ni_path: Ruta del archivo CSV con datos de consumo inicial de energía.
        :param weeks: Número de semanas para la simulación.
        :param homes: Número de hogares en la simulación.
        :param blade_length: Longitud de la pala de la turbina de viento (en metros).
        :param generator_efficiency: Eficiencia del generador.
        """
        # Crear una instancia de cada clase para la simulación
        self.data_manager = DataManager(data_ri_path, data_ni_path)  # Carga los datos de los archivos CSV
        self.simulator = EnergyConsumptionSimulator(self.data_manager.data_ri, self.data_manager.data_ni, weeks, homes)  # Simula el consumo energético
        self.visualizer = EnergyVisualizer(self.simulator.simulate_consumption(), homes)  # Visualiza los resultados
        self.blade = WindTurbineBlade(blade_length)  # Crea una pala de turbina de viento
        self.generator = Generator(generator_efficiency)  # Crea un generador con la eficiencia especificada

    def run_simulation(self, wind_speed: float, air_density: float):
        """
        Ejecuta la simulación de consumo energético y generación de energía eólica.
        
        :param wind_speed: Velocidad del viento en metros por segundo (m/s).
        :param air_density: Densidad del aire en kg/m³.
        :return: Una figura con los gráficos de la simulación.
        """
        # Cálculo de la energía generada por la turbina eólica y el generador
        swept_area = self.blade.swept_area  # Área barrida por la turbina
        mechanical_energy = 0.5 * air_density * swept_area * (wind_speed ** 3)  # Energía mecánica generada
        electrical_energy = self.generator.convert_energy(mechanical_energy)  # Convertir energía mecánica a eléctrica
        
        print(f"Energía generada por el generador: {electrical_energy:.2f} J")

        # Crear los gráficos de visualización
        fig = self.visualizer.create_plots()
        
        return fig


# Uso del simulador

# Crear la instancia del simulador con las rutas de los archivos y parámetros
simulator = EnergySystemSimulator(
    data_ri_path="src/models/baseCase/data_Ri.csv",
    data_ni_path="src/models/baseCase/data_Ni.csv",
    weeks=10,
    homes=15,
    blade_length=50.0,  # Longitud de la pala en metros
    generator_efficiency=0.9  # Eficiencia del generador
)

# Parámetros del viento para la simulación
wind_speed = 12  # Velocidad del viento en m/s
air_density = 1.225  # Densidad del aire en kg/m³

# Ejecutar la simulación
fig = simulator.run_simulation(wind_speed, air_density)

# La figura generada (fig) se puede usar para mostrar los gráficos en una interfaz de usuario, como Tkinter.
