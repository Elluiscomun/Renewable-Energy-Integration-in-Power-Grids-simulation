from baseCase import DataManager, EnergyConsumptionSimulator, EnergyVisualizer


if __name__ == "__main__":
    # Gestión de datos (no se necesita instanciar DataManager)
    data_ri = DataManager.DataManager.shuffle_data(DataManager.DataManager.read_csv("src/models/baseCase/data_Ri.csv"))
    data_ni = DataManager.DataManager.shuffle_data(DataManager.DataManager.read_csv("src/models/baseCase/data_Ni.csv"))

    # Simulación
    simulator = EnergyConsumptionSimulator.EnergyConsumptionSimulator(data_ri, data_ni, weeks=10, homes=15)
    consumption_results = simulator.run_simulation()
    cost_results = simulator.calculate_costs(consumption_results)

    # Visualización
    visualizer = EnergyVisualizer.EnergyVisualizer()
    plot_figure = visualizer.create_plots(consumption_results, cost_results)
    visualizer.display_gui(plot_figure)
