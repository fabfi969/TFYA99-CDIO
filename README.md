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

        -simulation_method EMT/LennardJones/Interface
    This sets the method that should be used for the integrator. Interface uses EMT but simulates an interface between two materials.

        -visualisation on/off
    This sets if the visualisation is turned on or off.

        -ensemble_mode energy/temperature
    This sets the ensemble: constant energy (NVE) or constant temperature (NVT).

        -lattice_constant float
    This overrides the lattice constant set in the input file.

        -substrate_lattice
    Only for interface simulation. Overrides the lattice constant for the substrate.

        -film_lattice
    Only for interface simulation. Overrides the lattice constant for the film.

        -alloy_ratio
    Only for interface simulation. Overrides the ratio of materialsin the film.

        -slurm
    This will tell the program to print in a way that the outputs in the terminal can be turned into a CSV-file.

## Run on supercomputer
1. Run:
    ```bash
    sbatch super_comp_script.q
2. Simulation method, ensable mode, etc. can be modified by appending the corresponding option to 'python3 main.py' in the same way as when program is run in terminal, see [How to run program](#how-to-run-program).
3. If further modifications are needed, note that the script is written in Schell. See [Basic Shell instructions](#basic-shell-instructions) if you are unfamiliar with Shell.
4. Output file will have name on format slurm-xxxxxxx.out
5. If code does not run properly, check if requirments are corectly installed, see Installation.

## Basic Shell instructions
The following instructions is to allow people who have no experience in Shell to make modifications to super_comp_script.q to be able to run their desierd calculations.
### Variables
A variable is declered by writing

    var=value
It is important that that there are no spaces between the variable name, the equal sign and the value since this will return errors. The following exampels will not work:

    var= value
    var =value
    var = value
To accsess the value of a variable put '$' in fron of it. For example:

    $var
### For Loops
A for loop is declered in the following way:

    for i in {1..3}
    do
        [insert code here]
    done
This example will excecute the code in the loop for i=1, i=2 and i=3.

### Floating Point Operations
Shells normal arithmetic opperations do not suport floating point numbers. Insted a expression on the following form is requiered.

    $(bc <<<"scale=2;[expression]")
where [expression] should be replaced by the desierd mathamatical expression.
Scale is a varable that determains the number of decimals in the float.

### Example Submit Script
The following is an example of an extract from super_comp_script.q demonstrating the instructions above.

    for i in {2..4}
    do
        j=$(bc <<<"scale=2;2+$i*0.1")
        python3 main.py -lattice_constant $j
    done

The script will run the program with lattice constant 2.2, 2.3 and 2.4.

## Results from Supercomputer
1. Push up the slurm-file to data/slurms
2. On a local computer run:
    ```bash
    python3 slurm_to_csv.py
3. To visualize the result, run: 
    ```bash
    python3 interface_energy_plot.py
When requested, enter the csv file name.
## Edit README
1. open README
3. use 'Ctrl+k v' to see the compiled file in VSCode

