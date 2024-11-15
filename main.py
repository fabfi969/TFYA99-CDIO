"This is the main script used for running the material simulations"

import argparse

import toml

from create_input_file import create_input_file
from md import run_md
from visualisation import plotenergy

def run_program():
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
        choices=["on", "off"]
    )

    args = parser.parse_args()

    input_file_name = "input_data.toml"
    create_input_file(input_file_name)
    input_data = toml.load(input_file_name)

    run_md(args, input_data)

    if args.visualisation == "on":
        output_file = "output_data.txt"
        plotenergy(output_file)



if __name__ == "__main__":
    run_program()