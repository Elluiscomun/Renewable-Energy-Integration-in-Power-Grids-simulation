import pandas as pd
import numpy as np
from baseCase.DataManager import DataManager
from baseCase.EnergyConsumptionSimulator import EnergyConsumptionSimulator
from wind.Generator import Generator


class HybridEnergySystem:
    def __init__(self, traditional_data_path_Ni: str, traditional_data_path_Ri: str, wind_speed_data_path: str, weeks: int, homes: int, generator_efficiency: float, rotor_efficiency: float, number_wind_turbine = 1):
        """
        Initializes the hybrid energy system.

        :param traditional_data_path_Ni: Path to the CSV file with traditional consumption data (initial values).
        :param traditional_data_path_Ri: Path to the CSV file with traditional consumption variation data.
        :param wind_speed_data_path: Path to the CSV file with wind speed data.
        :param weeks: Number of weeks for the simulation.
        :param homes: Number of homes in the simulation.
        :param generator_efficiency: Efficiency of the generator (value between 0 and 1).
        """
        # Load and shuffle data
        self.data_ri = DataManager.shuffle_data(DataManager.read_csv(traditional_data_path_Ri))
        self.data_ni = DataManager.shuffle_data(DataManager.read_csv(traditional_data_path_Ni))
        self.wind_speed_data = DataManager.shuffle_data(DataManager.read_csv(wind_speed_data_path))
        self.rotor_efficiency = rotor_efficiency
        self.number_wind_turbine = number_wind_turbine

        # Create instances
        self.simulator = EnergyConsumptionSimulator(self.data_ri, self.data_ni, weeks, homes)
        self.generator = Generator(generator_efficiency)

        # Variables to store results
        self.simulation_results = None
        self.cost_results = None
        self.generated_energy = None

    def simulate_traditional_consumption(self):
        """
        Simulates traditional energy consumption.
        """
        self.simulation_results = self.simulator.run_simulation()
        self.cost_results = self.simulator.calculate_costs(self.simulation_results)

    def simulate_wind_generation(self, air_density: float, blade_length: float):
        """
        Simulates wind energy generation.

        :param air_density: Air density (kg/m³).
        :param blade_length: Length of the turbine blade (meters).
        """
        self.generated_energy = []

        counter = 1
        energy = []
        for wind_speed in self.wind_speed_data[:len(self.simulation_results)*7]:
            electrical_energy = self.generator.generate_energy(
                length_bade=blade_length,
                air_density=air_density,
                wind_speed=wind_speed,
                rotor_efficiency=self.rotor_efficiency
            )
            energy.append(electrical_energy*self.number_wind_turbine)
            if(counter>=7):
                energy_adding = 0
                for i in energy:
                    energy_adding = energy_adding+i
                self.generated_energy.append(energy_adding)
                counter=0
                energy=[]
            counter = counter+1

        self.generated_energy = pd.Series(self.generated_energy, name="Energía Generada (kWh)")

    def analyze_coverage(self):
        """
        Analyzes if the wind-generated energy covers 50% of the traditional consumption.

        :return: DataFrame comparing consumption and generation.
        """
        if self.simulation_results is None or self.generated_energy is None:
            raise ValueError("Simulation has not been fully executed.")
        print('Consumos Casas')
        print(self.simulation_results.iloc[:, 1:])
        total_consumption = self.simulation_results.iloc[:, 1:].sum(axis=1)  # Total weekly consumption
        coverage = (self.generated_energy / total_consumption) * 100  # Coverage percentage

        comparison_df = pd.DataFrame({
            "Semana": range(1, len(self.generated_energy) + 1),
            "Consumo Total (kWh)": total_consumption,
            "Energía Generada (kWh)": self.generated_energy,
            "Cobertura (%)": coverage
        })
        return comparison_df

    def run_system(self, air_density: float, blade_length: float):
        """
        Executes the complete hybrid system simulation.

        :param air_density: Air density (kg/m³).
        :param blade_length: Length of the turbine blade (meters).
        """
        print("Simulating traditional consumption...")
        self.simulate_traditional_consumption()

        print("Simulating wind generation...")
        self.simulate_wind_generation(air_density, blade_length)

        print("Analyzing energy coverage...")
        coverage_results = self.analyze_coverage()

        print("\nAnalysis Results:")
        print(coverage_results)
        
        return coverage_results

