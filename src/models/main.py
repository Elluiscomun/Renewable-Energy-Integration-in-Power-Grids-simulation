import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from EnergySystemSimulator import HybridEnergySystem
from baseCase.EnergyVisualizer import EnergyVisualizer


class HybridEnergySystemGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hybrid Energy System Simulation")
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

        # Input variables
        self.weeks = tk.IntVar(value=10)
        self.homes = tk.IntVar(value=15)
        self.generator_efficiency = tk.DoubleVar(value=0.9)
        self.rotor_efficiency = tk.DoubleVar(value=0.4)
        self.air_density = tk.DoubleVar(value=1.225)
        self.blade_length = tk.DoubleVar(value=50.0)

        # Predefined file paths
        self.traditional_data_path_Ni = "src/models/baseCase/data_Ni.csv"
        self.traditional_data_path_Ri = "src/models/baseCase/data_Ri.csv"
        self.wind_speed_data_path = "src/models/wind/Ni_wind.csv"

        # Simulation instance and results
        self.hybrid_system = None
        self.coverage_results = None
        self.cost_results = None  # Variable para almacenar costos
        #self.energy_visualizer = EnergyVisualizer(self.root)  # Instancia de visualizador

        self.create_widgets()
        self.root.mainloop()

    def create_widgets(self):
        # Simulation parameters
        tk.Label(self.root, text="Weeks:").grid(row=0, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.weeks).grid(row=0, column=1)

        tk.Label(self.root, text="Homes:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.homes).grid(row=1, column=1)

        tk.Label(self.root, text="Generator Efficiency:").grid(row=2, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.generator_efficiency).grid(row=2, column=1)

        tk.Label(self.root, text="Rotor Efficiency:").grid(row=3, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.rotor_efficiency).grid(row=3, column=1)

        tk.Label(self.root, text="Air Density (kg/m³):").grid(row=4, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.air_density).grid(row=4, column=1)

        tk.Label(self.root, text="Blade Length (m):").grid(row=5, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.blade_length).grid(row=5, column=1)

        # Run and plot buttons
        tk.Button(self.root, text="Run Simulation", command=self.run_simulation).grid(row=6, column=0, pady=10)
        tk.Button(self.root, text="Plot Results", command=self.plot_results).grid(row=6, column=1, pady=10)

    def run_simulation(self):
        try:
            # Create the hybrid system instance with predefined paths
            self.hybrid_system = HybridEnergySystem(
                traditional_data_path_Ni=self.traditional_data_path_Ni,
                traditional_data_path_Ri=self.traditional_data_path_Ri,
                wind_speed_data_path=self.wind_speed_data_path,
                weeks=self.weeks.get(),
                homes=self.homes.get(),
                generator_efficiency=self.generator_efficiency.get(),
                rotor_efficiency=self.rotor_efficiency.get()
            )

            # Run the system
            self.coverage_results = self.hybrid_system.run_system(
                air_density=self.air_density.get(),
                blade_length=self.blade_length.get()
            )

            # Calcula los costos de consumo
            self.cost_results = self.hybrid_system.cost_results

            messagebox.showinfo("Simulation Complete", "The simulation has completed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during the simulation: {e}")

    def plot_results(self):
        if self.coverage_results is None:
            messagebox.showerror("Error", "No results to plot. Please run the simulation first.")
            return

        # Opción 1: Gráfico simple con matplotlib
        df = self.coverage_results
        plt.figure(figsize=(10, 6))

        plt.plot(df["Semana"], df["Consumo Total (kWh)"], label="Consumo Total (kWh)", marker="o")
        plt.plot(df["Semana"], df["Energía Generada (kWh)"], label="Energía Generada (kWh)", marker="x")
        plt.bar(df["Semana"], df["Cobertura (%)"], alpha=0.4, label="Cobertura (%)")

        plt.xlabel("Semana")
        plt.ylabel("Energía (kWh) / Cobertura (%)")
        plt.title("Resultados de Consumo y Generación de Energía")
        plt.legend()
        plt.grid(True)
        plt.show()

        # Opción 2: Gráficos detallados con EnergyVisualizer
        if self.cost_results is not None:
           #self.energy_visualizer.create_plots(self.coverage_results, self.cost_results)
            #self.energy_visualizer.display_gui()
            visualizer = EnergyVisualizer()
            plot_figure = visualizer.create_plots(self.hybrid_system.simulation_results, self.hybrid_system.cost_results)
            visualizer.display_gui(plot_figure)


if __name__ == "__main__":
    HybridEnergySystemGUI()
