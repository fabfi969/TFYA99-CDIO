"This is the main script used for running the material simulations"

import argparse

import toml

from create_input_file import create_input_file
from md import run_md
from visualisation import plotenergy

def run_program():
    parser = argparse.ArgumentParser(description="Parses simulation parameters.")

    parser.add_argument(
        "simulation_method",
        type=str,
        choices=["EMT", "LennardJones"],
        help="Simulation method",
    )

    parser.add_argument(
        "visualisation_onoff",
        type=str,
        nargs = "?",
        choices=["visualisation"]
    )

    args = parser.parse_args()

    input_file_name = "input_data.toml"
    create_input_file(input_file_name)
    input_data = toml.load(input_file_name)

    run_md(args, input_data)

    if args.visualisation_onoff == "visualisation":
        plotenergy()



if __name__ == "__main__":
    run_program()