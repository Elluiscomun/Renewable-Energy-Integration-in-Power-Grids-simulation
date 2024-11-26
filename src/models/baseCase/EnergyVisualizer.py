import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

class EnergyVisualizer:
    @staticmethod
    def create_plots(results, cost_df):
        """
        Crea gráficos de consumo y costos.
        """
        fig, axs = plt.subplots(3, 1, figsize=(12, 18))

        # Gráfico 1: Consumo por semana
        for col in results.columns[1:]:
            axs[0].plot(results['Semana'], results[col], label=col)
        axs[0].set_title("Caminata Aleatoria: Consumo Energético por Hogar")
        axs[0].set_xlabel("Semana")
        axs[0].set_ylabel("Consumo (kWh)")
        axs[0].legend(loc="upper right", fontsize="small")
        axs[0].grid()

        # Gráfico 2: Costo mensual
        axs[1].bar(cost_df['Hogar'], cost_df['Costo Mensual ($)'], color='skyblue')
        axs[1].set_title("Costo Mensual de Electricidad por Hogar")
        axs[1].set_xlabel("Hogar")
        axs[1].set_ylabel("Costo Mensual ($)")
        axs[1].tick_params(axis='x', rotation=45)
        axs[1].grid()

        # Tabla de Resumen
        axs[2].axis('tight')
        axs[2].axis('off')
        axs[2].table(cellText=cost_df.values, colLabels=cost_df.columns, loc='center', cellLoc='center')

        plt.tight_layout()
        return fig

    @staticmethod
    def display_gui(fig):
        """
        Muestra la interfaz gráfica con los gráficos.
        """
        root = tk.Tk()
        root.title("Simulación Energética")
        root.geometry("1240x800")

        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=1)

        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        canvas.configure(yscrollcommand=scrollbar.set)

        second_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=second_frame, anchor="nw")

        canvas_fig = FigureCanvasTkAgg(fig, second_frame)
        canvas_fig.get_tk_widget().pack()

        root.mainloop()
