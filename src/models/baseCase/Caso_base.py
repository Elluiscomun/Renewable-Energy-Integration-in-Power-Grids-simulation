import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import random
import csv

# Función para leer datos desde un archivo CSV
def read_csv(csvFile):
    with open(csvFile, "r") as f:
        reader = csv.reader(f)
        next(reader)
        numbers = [float(num[0]) for num in reader]
    return numbers

# Leer datos de los archivos
data_Ri = read_csv("src/models/baseCase/data_Ri.csv")
data_Ni = read_csv("src/models/baseCase/data_Ni.csv")

# Mezclar los datos para aleatoriedad
random.shuffle(data_Ri)
random.shuffle(data_Ni)

# Configuración para la caminata aleatoria
weeks = 10  # Total de semanas
sample = 15  # Total de hogares

# Obtener valores iniciales para los hogares
values_Ni = np.array(data_Ni[:sample])
values_Ri = data_Ri[:sample * weeks]

homes_num = len(values_Ni)
weekly_consumption = np.zeros((weeks, homes_num))

# Inicializar el consumo para la primera semana
weekly_consumption[0] = values_Ni

# Generar la caminata aleatoria
for week in range(1, weeks):
    variation = values_Ri[(week - 1) * homes_num:week * homes_num]  # Variación para cada hogar

    for i in range(homes_num):
        if variation[i] < 0.5:
            # Si la variación es menor que 0.5, + consumo
            weekly_consumption[week, i] = weekly_consumption[week - 1, i] + (variation[i] * 5)
        else:
            # Si la variación es mayor que 0.5, - consumo
            weekly_consumption[week, i] = weekly_consumption[week - 1, i] - ((1 - variation[i]) * 5)

        # Asegurarse de que el consumo no sea negativo
        weekly_consumption[week, i] = max(weekly_consumption[week, i], 0)

# Guardar los resultados de consumo en un DataFrame
results = pd.DataFrame(weekly_consumption, columns=[f'Hogar {i+1}' for i in range(homes_num)])
results.insert(0, 'Semana', range(1, weeks + 1))

# Calcular el promedio semanal y mensual por hogar
weekly_avg = results.iloc[:, 1:].mean(axis=0)  # Promedio por hogar (columnas)
monthly_avg = weekly_avg * 4  # Promedio mensual (4 semanas por mes)

# Calcular el costo mensual por hogar
cost_per_kwh = 12.08  # $/kWh
monthly_cost = monthly_avg * cost_per_kwh

# Crear un DataFrame con los resultados de costos
cost_df = pd.DataFrame({
    'Hogar': [f'Hogar {i+1}' for i in range(homes_num)],
    'Promedio Semanal (kWh)': weekly_avg,
    'Promedio Mensual (kWh)': monthly_avg,
    'Costo Mensual ($)': monthly_cost
})

# Crear gráficos en Matplotlib
def create_plots():
    fig, axs = plt.subplots(3, 1, figsize=(12, 18))

    # Gráfico 1: Caminata Aleatoria - Consumo por Semana
    for i in range(homes_num):
        axs[0].plot(results['Semana'], results[f'Hogar {i+1}'], label=f'Hogar {i+1}')
    axs[0].set_title("Caminata Aleatoria: Demanda Energética por Hogar")
    axs[0].set_xlabel("Semana")
    axs[0].set_ylabel("Consumo (kWh)")
    axs[0].legend(loc="upper right", bbox_to_anchor=(1.15, 1), fontsize="small")
    axs[0].grid()

    # Gráfico 2: Costo Mensual por Hogar
    axs[1].bar(cost_df['Hogar'], cost_df['Costo Mensual ($)'], color='skyblue')
    axs[1].set_title("Costo Mensual de Electricidad por Hogar")
    axs[1].set_xlabel("Hogar")
    axs[1].set_ylabel("Costo Mensual ($)")
    axs[1].tick_params(axis='x', rotation=45)
    axs[1].grid()

    # Tabla de Resumen
    axs[2].axis('tight')
    axs[2].axis('off')
    table_data = cost_df.values
    table_columns = cost_df.columns
    axs[2].table(cellText=table_data, colLabels=table_columns, cellLoc='center', loc='center')

    # Ajustar diseño
    plt.tight_layout()

    return fig

def on_closing():
    root.destroy()  # Cierra la ventana principal
    root.quit()  # Finaliza el bucle principal de tkinter


# Crear la ventana principal
root = tk.Tk()
root.title("Simulación caso base de Consumo Energético")
root.geometry("1240x600")

# Crear un frame para la barra de desplazamiento
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=1)

# Crear un canvas para colocar gráficos y habilitar scroll
canvas = tk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Configurar el canvas para que use el scrollbar
canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Crear un frame dentro del canvas para colocar los gráficos
second_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=second_frame, anchor="nw")

# Agregar los gráficos al frame
fig = create_plots()
canvas_fig = FigureCanvasTkAgg(fig, second_frame)
canvas_fig.get_tk_widget().pack()

# Iniciar la interfaz gráfica
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
