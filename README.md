# Material simulation

Material simulation software description.

## Table of Contents

- [Material simulation](#material-simulation)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [How to run program](#how-to-run-program)
  - [Run on supercomputer](#run-on-supercomputer)
  - [Basic Shell instructions](#basic-shell-instructions)
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

        -cores 1/8/32
    The number of cores the simulation is run on. If not 1, make sure that you have acces to the specified number of cores of the program will crash. Note that bulk modulus will not work if the program is run on more than 1 core.

        -visualisation on/off
    This sets if the visualisation is turned on or off.

        -ensemble_mode energy/temperature
    This sets the ensemble: constant energy (NVE) or constant temperature (NVT).

        -lattice_constant float
    This overrides the lattice constant set in the input file.

        -substrate_lattice float
    Only for interface simulation. Overrides the lattice constant for the substrate.

        -film_lattice float
    Only for interface simulation. Overrides the lattice constant for the film.

        -substrate_atoms Au/Ag/Cu/Al/Ni/Pd/Pt
    Only for interface simulation. Overrides the base atoms in the substrate.

        -film_atoms Au/Ag/Cu/Al/Ni/Pd/Pt
    Only for interface simulation. Overrides the base atoms in the film.

        -substrate_alloying_atoms Au/Ag/Cu/Al/Ni/Pd/Pt
    Only for interface simulation. Overrides the alloyning atoms in the substrate.

        -film_alloying_atoms Au/Ag/Cu/Al/Ni/Pd/Pt
    Only for interface simulation. Overrides the alloyning atoms in the film.

        -substrate_alloy_ratio Au/Ag/Cu/Al/Ni/Pd/Pt
    Only for interface simulation. Overrides the ratio of materialsin the film.

        -film_alloy_ratio float
    Only for interface simulation. Overrides the ratio of materialsin the film.

        -lattice_interpolation
    If included the program will interpolate the lattice constants for the alloys based on the alloy ratio and the lattice constants for different materials and alloy in the input file. Only applicible for interface simulations. 

        -slurm
    If included the program will print in a way that the outputs in the terminal can be turned into a CSV-file.

## Run on supercomputer
1. Log in on supercomputer and move to the correct folder.
2. Run:
    ```bash
    sbatch super_comp_script.q
3. Simulation method, ensable mode, etc. can be modified by appending the corresponding option to 'python3 main.py' in the same way as when program is run in terminal, see [How to run program](#how-to-run-program).
4. The number of cores the program is running on are modified by the line 
    
        #SBATCH -n X
    in super_comp_script.q where X is the number of cores. Note that to acctly use the cores the input argument -cores needs to be used as well, see [How to run program](#how-to-run-program).
5. The maximum time the program is allowed to run is modified by the line 

        #SBATCH -t hh:mm:ss
    in super_comp_script.q where hh is the number of hours, mm is the number of minutes and ss is the number of seconds. If the program takes longer to run than the specified time it will be stoped before it is finished.
6. If further modifications are needed, note that the script is written in Schell. See [Basic Shell instructions](#basic-shell-instructions) if you are unfamiliar with Shell.
7. Output file will have name on format slurm-xxxxxxx.out
8. If code does not run properly, check if requirments are corectly installed, see [Installation](#installation).
9. If MakeParallelAtoms can't be imported run 

        source /proj/liu-compute-2024-33/software/init.sh
    in the terminal.
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

