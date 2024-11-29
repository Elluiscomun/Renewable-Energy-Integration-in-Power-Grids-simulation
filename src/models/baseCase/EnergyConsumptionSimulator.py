import numpy as np
import pandas as pd

class EnergyConsumptionSimulator:
    def __init__(self, data_ri, data_ni, weeks, homes):
        self.data_ri = data_ri
        self.data_ni = data_ni
        self.weeks = weeks
        self.homes = homes

    def run_simulation(self):
        """
        Realiza la simulación de consumo energético.
        """
        # Inicializar valores iniciales
        values_ni = np.array(self.data_ni[:self.homes])
        values_ri = self.data_ri[:self.homes * self.weeks]

        # Configuración inicial de consumo
        weekly_consumption = np.zeros((self.weeks, self.homes))
        weekly_consumption[0] = values_ni

        # Generar consumo semanal
        for week in range(1, self.weeks):
            variation = values_ri[(week - 1) * self.homes:week * self.homes]
            for i in range(self.homes):
                if variation[i] < 0.5:
                    weekly_consumption[week, i] = weekly_consumption[week - 1, i] + (variation[i] * 5)
                else:
                    weekly_consumption[week, i] = weekly_consumption[week - 1, i] - ((1 - variation[i]) * 5)

                # Evitar valores negativos
                weekly_consumption[week, i] = max(weekly_consumption[week, i], 0)

        # Crear DataFrame de resultados
        results = pd.DataFrame(weekly_consumption, columns=[f'Hogar {i+1}' for i in range(self.homes)])
        results.insert(0, 'Semana', range(1, self.weeks + 1))
        return results

    @staticmethod
    def calculate_costs(results, cost_per_kwh=373.92):
        """
        Calcula el promedio y costo mensual por hogar.
        """
        weekly_avg = results.iloc[:, 1:].mean(axis=0)  # Promedio semanal
        monthly_avg = weekly_avg * 4  # Promedio mensual
        monthly_cost = monthly_avg * cost_per_kwh

        cost_df = pd.DataFrame({
            'Hogar': [f'Hogar {i+1}' for i in range(len(weekly_avg))],
            'Promedio Semanal (kWh)': weekly_avg,
            'Promedio Mensual (kWh)': monthly_avg,
            'Costo Mensual ($)': monthly_cost
        })
        return cost_df
