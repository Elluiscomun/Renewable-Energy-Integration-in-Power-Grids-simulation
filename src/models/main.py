import tkinter as tk
import tkinter as ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from hybrid_energy_system import HybridEnergySystem
from baseCase.EnergyVisualizer import EnergyVisualizer
from wind.wind_visualizer import WindVisualizer
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HybridEnergySystemGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hybrid Energy System Simulation")
        self.root.protocol("WM_DELETE_WINDOW", self.root.quit)

        # Input variables
        self.weeks = tk.IntVar(value=30)
        self.homes = tk.IntVar(value=15)
        self.generator_efficiency = tk.DoubleVar(value=0.9)
        self.rotor_efficiency = tk.DoubleVar(value=0.4)
        self.air_density = tk.DoubleVar(value=1.225)
        self.blade_length = tk.DoubleVar(value=5.0)
        self.number_wind_turbine = tk.IntVar(value=6)

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

        tk.Label(self.root, text="Number Wind Turbine:").grid(row=6, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.number_wind_turbine).grid(row=6, column=1)

        # Run and plot buttons
        tk.Button(self.root, text="Run Simulation", command=self.run_simulation).grid(row=7, column=0, pady=10)
        tk.Button(self.root, text="Plot Comsumption", command=self.plot_comsumption).grid(row=7, column=1, pady=10)
        tk.Button(self.root, text="Plot Energy Generation", command=self.plot_energy_generation).grid(row=7, column=2, pady=10)
        tk.Button(self.root, text="Plot Results", command=self.plot_results).grid(row=7, column=3, pady=10)

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
                rotor_efficiency=self.rotor_efficiency.get(),
                number_wind_turbine=self.number_wind_turbine.get()
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

    def create_scrollable_canvas(self):
        """Crea un canvas con scroll para incluir múltiples gráficos en una nueva ventana."""
        # Crear una nueva ventana
        new_window = tk.Toplevel(self.root)
        new_window.title("Resultados de la Simulación")
        new_window.geometry("800x600")  # Dimensiones iniciales de la ventana

        # Crear el marco principal para el canvas y el scrollbar
        frame = ttk.Frame(new_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Crear el canvas y el contenedor con scroll
        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        # Configurar el área desplazable
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Insertar el marco en el canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Ubicar los widgets en la ventana secundaria
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        return scrollable_frame

    def plot_energy_consumption(self, ax, df):
        """Subgráfica de consumo total y energía generada."""
        ax.plot(df["Semana"], df["Consumo Total (kWh)"], label="Consumo Total (kWh)", marker="o")
        ax.plot(df["Semana"], df["Energía Generada (kWh)"], label="Energía Generada (kWh)", marker="x")
        ax.set_ylabel("Energía (kWh)")
        ax.set_title("Consumo y Generación de Energía")
        ax.legend()
        ax.grid(True)

    def plot_coverage(self, ax, df):
        """Subgráfica de cobertura."""
        ax.bar(df["Semana"], df["Cobertura (%)"], alpha=0.4, label="Cobertura (%)")
        ax.set_ylabel("Cobertura (%)")
        ax.set_title("Cobertura por Semana")
        ax.legend()
        ax.grid(True)

    def plot_emissions_comparison(self, ax, df):
        """Subgráfica de comparación de emisiones por escenario."""
        wind_best_case = 9.7
        wind_worst_case = 123.7
        hydro_best_case = 3.7
        hydro_worst_case = 237.0

        total_consumption = df["Consumo Total (kWh)"]
        wind_generated = df["Energía Generada (kWh)"]
        hydro_generated = (total_consumption - wind_generated).clip(lower=0)

        wind_emissions_best = wind_generated * wind_best_case
        wind_emissions_worst = wind_generated * wind_worst_case
        hydro_emissions_best = hydro_generated * hydro_best_case
        hydro_emissions_worst = hydro_generated * hydro_worst_case

        bar_width = 0.2
        weeks = np.arange(len(df["Semana"]))

        ax.bar(weeks - bar_width, wind_emissions_best, bar_width, label="Eólica (Mejor Escenario)", color="green")
        ax.bar(weeks, hydro_emissions_best, bar_width, label="Hidroeléctrica (Mejor Escenario)", color="blue")
        ax.bar(weeks + bar_width, wind_emissions_worst, bar_width, label="Eólica (Peor Escenario)", color="orange")
        ax.bar(weeks + 2 * bar_width, hydro_emissions_worst, bar_width, label="Hidroeléctrica (Peor Escenario)", color="red")

        ax.set_xlabel("Semana")
        ax.set_ylabel("Emisiones Totales (gCO₂ eq.)")
        ax.set_title("Comparación de Emisiones por Tipo de Energía y Escenario")
        ax.set_xticks(weeks)
        ax.set_xticklabels(df["Semana"])
        ax.legend()
        ax.grid(True, linestyle="--", alpha=0.6)

    def plot_results(self):
        if self.coverage_results is None:
            messagebox.showerror("Error", "No results to plot. Please run the simulation first.")
            return

        scrollable_frame = self.create_scrollable_canvas()
        df = self.coverage_results

        fig, axs = plt.subplots(3, 1, figsize=(12, 15))

        # Generar los gráficos
        self.plot_energy_consumption(axs[0], df)
        self.plot_coverage(axs[1], df)
        self.plot_emissions_comparison(axs[2], df)

        # Ajustar diseño
        plt.tight_layout()

        # Renderizar los gráficos en el canvas
        canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def plot_comsumption(self):
        # Opción 2: Gráficos detallados con EnergyVisualizer
        if self.cost_results is not None:
            visualizer = EnergyVisualizer()
            plot_figure = visualizer.create_plots(self.hybrid_system.simulation_results, self.hybrid_system.cost_results)
            visualizer.display_gui(plot_figure)

    def plot_energy_generation(self):
        """
        Grafica la energía generada semanalmente por las turbinas eólicas.
        """
        if self.coverage_results is None:
            messagebox.showerror("Error", "No hay datos para graficar. Por favor, ejecuta la simulación primero.")
            return

        # Obtener los datos de energía generada
        generated_energy = self.coverage_results["Energía Generada (kWh)"]
        weeks = self.coverage_results["Semana"]

        # Crear la gráfica
        plt.figure(figsize=(10, 6))
        plt.plot(weeks, generated_energy, label="Energía Generada (kWh)", marker="o", color="green")
        plt.title("Energía Generada Semanalmente")
        plt.xlabel("Semana")
        plt.ylabel("Energía Generada (kWh)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Mostrar la gráfica
        plt.show()


if __name__ == "__main__":
    HybridEnergySystemGUI()
