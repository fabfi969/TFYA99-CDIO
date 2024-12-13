'''This is a file containing examples of simulations that can be run with our program'''

import os

os.system("python3 create_input_file.py")
os.system("python3 main.py -view_atoms -visualisation on -slurm")
# theory: bulk modulus = 103.6 GPa (PH), 2.95 Ev (p50, v8, solid state physics, Kittel)

# os.system("python3 main.py -view_atoms -simulation_method LennardJones -visualisation on")

# os.system("python3 main.py -view_atoms -simulation_method Interface")
