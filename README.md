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
## General flags 
There are a few optional flags that can be set. Those should be typed seperated by a space after main.py. Only one value for each flag can be set. The values are seperated by "/" below. The flags are the following:

    -simulation_method EMT/LennardJones/Interface
This sets the method that should be used for the integrator. Interface uses EMT but simulates an interface between two materials.

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
This will tell the program to print in a way that the outputs in the terminal can be turned into a CSV-file.

### Supercomputer specific flags
The following flags should only be run when using the script to submit the code on the supersomputer.

    -sc
Enables use of all flags listed below. Must be run if the program is to use different parameteres on different core. 

    -sc_lattice_offset float
Makes the program run with different lattice constants for the non-interface simulation on different cores. The constants are evenly spaced with spacing equal to the inputed parameter. The lowest lattice constant will have the value specified by the flag -lattice_constant or if it is not used the value from the input file. 

    -sc_film_lattice_offset float
Only for interface simulation. Makes the program run with different lattice constants for the film in the interface simulation on different cores. The constants are evenly spaced with spacing equal to the inputed parameter. The lowest lattice constant will have the value specified by the flag -film_lattice or if it is not used the value from the input file. 

    -sc_substrate_lattice_offset float
Only for interface simulation. Makes the program run with different lattice constants for the substrate in the interface simulation on different cores. The constants are evenly spaced with spacing equal to the inputed parameter. The lowest lattice constant will have the value specified by the flag -substrate_lattice or if it is not used the value from the input file. 

    -sc_film_alloy_ratio_offset float
Only for interface simulation. Makes the program run with different alloy ratio for the film in the interface simulation on different cores. The alloy ratios are evenly spaced with spacing equal to the inputed parameter. The lowest alloy ratio will have the value specified by the flag -film_alloy_ratio or if it is not used the value from the input file. 

    -sc_substarte_alloy_ratio_offset float
Only for interface simulation. Makes the program run with different alloy ratio for the substrate in the interface simulation on different cores. The alloy ratios are evenly spaced with spacing equal to the inputed parameter. The lowest alloy ratio will have the value specified by the flag -substrate_alloy_ratio or if it is not used the value from the input file. 

## Run on supercomputer
1. Log in on supercomputer and move to the correct folder.
2. Run:

        source /proj/liu-compute-2024-33/software/init.sh
3. To submit to supercomputer, run:
    

        sbatch super_comp_script.q
    The file super_comp_script.q can be modified to change what is run which is disscussed in deatial below. 
3. 
        mpprun python3
    in the file super_comp_script.py will start a number of processes equal to the number of avilible cores. The nuber of cores can be changed by modifiyng the line

        #SBATCH -n 32
    in super_comp_script.py. If x cores are to be used where x>32 change the line 

        #SBATCH -N 1
    to the smallest integer value larger than x/32. 
4. Simulation method, ensable mode, etc. can be modified by appending the corresponding option to 'mpprun python3 supercomp_main.py' in super_comp_script.py in the same way as when program is run in terminal, see [How to run program](#how-to-run-program).
5. Running different simulations methods on different core uses the flags described in [Supercomputer specific flags](#supercomputer-specific-flags) and are appended to 'mpprun python3 supercomp_main.py' in super_comp_script.py in the same way as normal flags.
6. The program will run for a maximum amount of time specified by the line 
    
        #SBATCH -t hh:mm:ss
    in super_comp_script.py where hh is the number of hours, mm is the number of minutes and ss is the number of seconds. If the code is not finshed when the time is up the program will be stopped.
7. If further modifications are needed, note that the script is written in Schell. See [Basic Shell instructions](#basic-shell-instructions) if you are unfamiliar with Shell.
8. Output file will have name on format slurm-xxxxxxx.out
9. If code does not run properly, check if requirments are corectly installed, see Installation.

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

    #SBATCH -A liu-compute-2024-33
    #SBATCH --reservation devel
    #SBATCH -t 00:05:00
    #SBATCH -N 1
    #SBATCH -n 32
    #SBATCH --exclusive
    #
    export NSC_MODULE_SILENT=1
    export OPENBLAS_NUM_THREADS=1
    export MKL_NUM_THREADS=1
    export NUMEXPR_NUM_THREADS=1
    export OMP_NUM_THREADS1

    j=$(bc <<<"scale=2;0.01")
    for i in {0..2}
    do
        k=$(bc <<<"scale=2;4+32*$j*$i")
        mpprun python3 supercomp_main.py -slurm -lattice_constant $k -sc_lattice_offset $j -sc
    done

    echo "job completed"


The script will run the program with lattice constants (4.0, 4.01 ... 4.95).

Note that all flags should be on the same line as 'mpprun python3 supercomp_main.py', it may not look that way depending on how this document is displayed.

## Results from Supercomputer
1. Push up the slurm-file to data/slurms
2. On a local computer run:
    
        python3 slurm_to_csv.py
3. To visualize the result, run:
    
        python3 interface_energy_plot.py
    When requested, enter the csv file name.
    
    Note that minor modifications need to be done to the script to changed what is plotted or to change the legend.

## Edit README
1. open README
3. use 'Ctrl+k v' to see the compiled file in VSCode

