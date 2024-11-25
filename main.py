"This is the main script used for running the material simulations"

import argparse

import toml
import os

from create_input_file import create_input_file
from md import run_md
from visualisation import plotenergy

def run_program():
    '''Uses argparse to provide the MD simulation with the simulation argument required'''
    parser = argparse.ArgumentParser(description="Parses simulation parameters.")

    parser.add_argument(
        "-simulation_method",
        required = False,
        default = "EMT",
        type=str,
        choices=["EMT", "LennardJones"],
        help="Simulation method",
    )
    parser.add_argument(
        "-visualisation",
        required = False,
        default = "off",
        type=str,
        choices=["on", "off"],
        help="on if the graphs from the simulated data is to be plotted, \
off if not which is default",
    )
    parser.add_argument(
        "-cif",
        required = False,
        default = '',
        type=str,
        help="The path to the CIF-file where the specifications of the \
to be simulated atoms are defined",
    )

    parser.add_argument(
        "-ensemble_mode",
        required = False,
        default = "energy",
        type = str,
        choices = ["energy", "temperature"]
    )

    parser.add_argument(
        "-lattice_constant",
        required = False,
        default = "-1.0",
        type = float,
    )

    args = parser.parse_args()

    input_file_name = "input_data.toml"
    if os.path.isfile(input_file_name):
        pass
    else:
        create_input_file(input_file_name)
    input_data = toml.load(input_file_name)

    run_md(args, input_data)

    if args.visualisation == "on":
        output_file = "output_data.txt"
        plotenergy(output_file)

if __name__ == "__main__":
    run_program()
