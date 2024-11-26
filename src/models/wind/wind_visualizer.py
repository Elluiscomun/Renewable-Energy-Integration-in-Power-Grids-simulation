import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class WindVisualizer:
    @staticmethod
    def create_plots(generator_results, wind_speed_values):
        """
        Crea gráficos de energía generada para diferentes velocidades del viento.
        """
        fig, axs = plt.subplots(2, 1, figsize=(12, 12))

        # Gráfico: Energía generada por velocidad del viento
        axs[0].plot(wind_speed_values, generator_results, label="Energía Generada (kWh)", marker="x", color='orange')
        axs[0].set_title("Energía Generada vs Velocidad del Viento (m/s)")
        axs[0].set_xlabel("Velocidad del Viento (m/s)")
        axs[0].set_ylabel("Energía Generada (kWh)")
        axs[0].legend(loc="upper right", fontsize="small")
        axs[0].grid()

        # Tabla de Resultados
        axs[1].axis('tight')
        axs[1].axis('off')
        results_df = pd.DataFrame({
            "Velocidad del Viento (m/s)": wind_speed_values,
            "Energía Generada (kWh)": generator_results
        })
        axs[1].table(cellText=results_df.values, colLabels=results_df.columns, loc='center', cellLoc='center')

        plt.tight_layout()
        return fig

    @staticmethod
    def display_gui(fig):
        """
        Muestra la interfaz gráfica con los gráficos.
        """
        root = tk.Tk()
        root.title("Simulación Energética del Generador")
        root.geometry("1240x600")

        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=1)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        canvas.configure(yscrollcommand=scrollbar.set)

        second_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=second_frame, anchor="nw")

        # Agregar los gráficos al segundo frame
        canvas_fig = FigureCanvasTkAgg(fig, second_frame)
        canvas_fig.get_tk_widget().pack()

        # Actualizar la región de desplazamiento después de agregar el contenido
        second_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

        root.mainloop()


# Ejemplo de uso
if __name__ == "__main__":
    # Crear los datos de ejemplo para los gráficos
    wind_speed_values = np.linspace(3, 25, 10)  # Velocidad del viento (en m/s)

    # Simulación de la energía generada por el generador
    generator_results = wind_speed_values ** 2 * 0.5  # Ejemplo simple de generación (proporcional al cuadrado de la velocidad)

    # Crear gráficos
    fig = WindVisualizer.create_plots(generator_results, wind_speed_values)

    # Mostrar la interfaz gráfica
    WindVisualizer.display_gui(fig)
