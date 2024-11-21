# Material simulation

Material simulation software description.

## Table of Contents

- [Material simulation](#material-simulation)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [How to run program](#how-to-run-program)
  - [Edit README](#edit-readme)

## Features

- Can do simple material simulations using an input file.

## Installation

1. pip install --upgrade pip
2. Create a virtual environment:
    ```bash
    python3 -m venv venv  # only has to be run once
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. Make sure that your Python version is at least Python 3.10.12 with
    ```bash
    python3 -V
4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt  # run when requirements.txt has been updated

## How to run program

1. Open terminal in program folder.
2. type: python3 main.py
This will run the code with EMT and without visualisation.
3. To change simulation method, also type the following in terminal when running program: -simulation_method LennardJones
4. To enable visualisation, also type the following when running program: -visualisation on

## Edit README

1. open README
3. use 'Ctrl+k v' to see the compiled file in VSCode

## Run on supercomputer
1. Run 'sbatch super_comp_script.q'
2. Output will have name on format slurm-xxxxxxx.out
3. If code does not run properly, check if requirments are corectly installed, see Installation.
