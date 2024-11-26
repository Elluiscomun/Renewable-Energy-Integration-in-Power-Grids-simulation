import csv
import random
import numpy as np

class DataManager:
    @staticmethod
    def read_csv(file_path):
        """
        Lee un archivo CSV y devuelve una lista de números flotantes.
        """
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            next(reader)
            data = [float(row[0]) for row in reader]
        return data

    @staticmethod
    def shuffle_data(data):
        """
        Mezcla los datos para aleatoriedad.
        """
        random.shuffle(data)
        return data
