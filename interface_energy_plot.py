import warnings
warnings.filterwarnings("ignore", message = "Unable to import Axes3D")
import matplotlib.pyplot as plt # This would give a warning without above line.
import ast
import pandas
import os

def plot_interface_energy_vs_atomic_concentration(file_name):
    '''Plot interface energy vs atomic concentration.
    Note: At the moment this plots other things.'''
    base_path = os.getcwd()  
    relative_path = os.path.join("data", "slurm_results", file_name) 
    file_path = os.path.join(base_path, relative_path)
    data = pandas.read_csv(file_path)
    x = data['film_alloy_ratio'].tolist() 
    y = data['interface_energy'].tolist()
    plt.scatter(x, y)
    plt.title('Interface energy of different mixes of AgAu on Cu.')
    plt.xlabel('Percentage Ag alloyed with Au')
    plt.ylabel('Interface energy')
    plt.show()
    

file_name = input("Type the CSV file name:")
plot_interface_energy_vs_atomic_concentration(file_name)
