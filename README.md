# Material simulation

Material simulation software description.

## Table of Contents

- [Material simulation](#material-simulation)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [How to run program](#how-to-run-program)
  - [Run on supercomputer](#run-on-supercomputer)
  - [Edit README](#edit-readme)

## Features

- Can do simple material simulations using an input file.

## Installation

1. pip install --upgrade pip
2. Create a virtual environment:
    ```bash
    python3 -m venv venv  # only has to be run once
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Make sure that your Python version is at least Python 3.9.18 with
    ```bash
    python3 -V
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt  # run when requirements.txt has been updated

## How to run program

1. Open terminal in program folder.
2. Type:

        python3 main.py
    This will run the code with EMT, without visualisation and in constant energy mode.
3.  There are a few optional flags that can be set. Those should be typed seperated by a space after main.py. Only one value for each flag can be set. The values are seperated by "/" below. The flags are the following:

        -simulation_method EMT/LennardJones
    This sets the method that should be used for the integrator.

        -visualisation on/off
    This sets if the visualisation is turned on or off.

        -ensemble_mode energy/temperature
    This sets the ensemble: constant energy (NVE) or constant temperature (NVT).

        -lattice_constant float
    This overrides the lattice constant set in the input file.

        -slurm
    This will tell the program to print in a way that the outputs in the terminal can be turned into a CSV-file.

## Run on supercomputer
1. Run:
    ```bash
    sbatch super_comp_script.q
2. Simulation method, ensable mode, etc. can be modified by appending the corresponding option to 'python3 main.py' in the same way as when program is run in terminal, see [How to run program](#how-to-run-program).
3. Output file will have name on format slurm-xxxxxxx.out
4. If code does not run properly, check if requirments are corectly installed, see Installation.

## Results from Supercomputer
1. Push up the slurm-file to data/slurms
2. On a local computer run:
    ```bash
    python3 slurm_to_csv.py
3. Use pandas to read the CSV into Python


## Edit README
1. open README
3. use 'Ctrl+k v' to see the compiled file in VSCode
