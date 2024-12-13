'''Demonstrates molecular dynamics with constant energy. Is called by main'''

import sys
from asap3 import EMT, LennardJones, Trajectory # This line gives the terminal warnings.
from ase import units
from ase.lattice.cubic import BodyCenteredCubic, BodyCenteredCubicFactory, Bravais, Diamond
from ase.lattice.cubic import DiamondFactory, FaceCenteredCubic, FaceCenteredCubicFactory
from ase.lattice.cubic import SimpleCubic, SimpleCubicFactory
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase.build import bulk
from ase.build.tools import sort
from ase.build.tools import cut, stack
from ase.io import read
from ase.md import Andersen
import numpy as np
from create_input_file import create_input_file
from create_atoms_md import invalid_materials_EMT_error, create_atoms
import toml
from calculate_properties import calcenergy, calctemperature, calcpressure, calccohesiveenergy, calcbulkmodulus
from save_data import writetofile
from random import random
from alloy import Interface
import statistics

"""
def TwoBlocks(mat1, structure1, a1, mat2, structure2, a2, size, film_alloy_ratio = 0, alloy = "N"):
    #Generate an two layers of atoms pressed up against each other
    bulk1 = bulk(mat1,structure1, a=a1) * (2*size, 2*size, size)
    if alloy != 0:
        bulk2 = random_alloys(mat2,structure2, a2, alloy, film_alloy_ratio, size)
    else:
        bulk2 = bulk(mat2,structure2, a=a2) * (2*size, 2*size, size)
    interface = stack(bulk1, bulk2,maxstrain=100)
    #view(interface)
    return interface


def random_alloys(mat1,structure1,a1,mat2,atomic_percent,size):
    #generates a single block of material with a randomly replaced atoms.
    tot_at = 4*size*size*size
    bulk1 = bulk(mat1,structure1, a=a1) * (2*size, 2*size, size)
    next = 0
    while next < tot_at:
        if random() < atomic_percent:
            bulk1.symbols[next]=mat2
        next += 1
    return(bulk1)
    #view(bulk1)
"""
def run_md(args, input_data):
    '''runs the molecular dynamics simulation'''

    # deletes asap3 warnings in terminal
    if not args.slurm:
        for _ in range(3):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
            sys.stdout.flush()
    print("____Starting new simulation____:")


    #command line override of lattice constant and structure
    if args.lattice_constant != -1:
        input_data['atoms']['latticeconstant'] = args.lattice_constant
    if args.structure != -1:
        input_data['atoms']['structure'] = input_data['structure_choices'][args.structure]
        print(input_data['structure_choices'][args.structure])
    #command line override for parameters for inteface simulation
    if args.simulation_method == 'Interface':
        if args.substrate_lattice != -1:
            input_data['interface']['substrate_lattice'] = args.substrate_lattice
        if args.film_lattice != -1:
            input_data['interface']['film_lattice'] = args.film_lattice
        if args.substrate_alloy_ratio != -1:
            input_data['interface']['substrate_alloy_ratio'] = args.substrate_alloy_ratio
        if args.film_alloy_ratio != -1:
            input_data['interface']['film_alloy_ratio'] = args.film_alloy_ratio
        if args.substrate_atoms != "deafult":
            input_data['interface']['substrate_atoms'] = args.substrate_atoms
        if args.substrate_alloying_atoms != "deafult":
            input_data['interface']['substrate_alloying_atoms'] = args.substrate_alloying_atoms
        if args.film_atoms != "deafult":
            input_data['interface']['film_atoms'] = args.film_atoms
        if args.film_alloying_atoms != "deafult":
            input_data['interface']['film_alloying_atoms'] = args.film_alloying_atoms

    #linear interpolation of lattice constant
    if args.lattice_interpolation and args.simulation_method == 'Interface':
        try:
            substrate_alloy_lattice = input_data['lattice_constant'][input_data['interface']['substrate_atoms']+input_data['interface']['substrate_alloying_atoms']]
        except KeyError:
            substrate_alloy_lattice = input_data['lattice_constant'][input_data['interface']['substrate_alloying_atoms']+input_data['interface']['substrate_atoms']]
        try:
            film_alloy_lattice = input_data['lattice_constant'][input_data['interface']['film_atoms']+input_data['interface']['film_alloying_atoms']]
        except KeyError:
            film_alloy_lattice = input_data['lattice_constant'][input_data['interface']['film_alloying_atoms']+input_data['interface']['film_atoms']]

        sub_alloy_ratio = input_data['interface']['substrate_alloy_ratio']
        if sub_alloy_ratio < 0.5:
            sub_atom_lat = input_data['lattice_constant'][input_data['interface']['substrate_atoms']]
            interpolated_sub_lattice = (1-2*sub_alloy_ratio)*sub_atom_lat+2*sub_alloy_ratio*substrate_alloy_lattice
        else:
            sub_alloy_atom_lat = input_data['lattice_constant'][input_data['interface']['substrate_alloying_atoms']]
            interpolated_sub_lattice = (2-2*sub_alloy_ratio)*substrate_alloy_lattice+(2*sub_alloy_ratio-1)*sub_alloy_atom_lat
        input_data['interface']['substrate_lattice'] = interpolated_sub_lattice

        film_alloy_ratio = input_data['interface']['film_alloy_ratio']
        if film_alloy_ratio < 0.5:
            film_atom_lat = input_data['lattice_constant'][input_data['interface']['film_atoms']]
            interpolated_film_lattice = (1-2*film_alloy_ratio)*film_atom_lat+2*film_alloy_ratio*film_alloy_lattice
            print(film_alloy_ratio)
            print(film_atom_lat)
            print(film_alloy_lattice)
        else:
            film_alloy_atom_lat = input_data['lattice_constant'][input_data['interface']['film_alloying_atoms']]
            interpolated_film_lattice = (2-2*film_alloy_ratio)*film_alloy_lattice+(2*film_alloy_ratio-1)*film_alloy_atom_lat
        input_data['interface']['film_lattice'] = interpolated_film_lattice

    # Set up a crystal
    # Sim = Interface("Cu","fcc",2.54,"Au","fcc",3.4,4)
    # atoms = Sim.get_atoms()
    if args.cif == '':
        atoms = create_atoms(input_data)
    else:
        atoms = read(args.cif, format='cif')

    # Describe the interatomic interactions with the Effective Medium Theory
    if args.simulation_method == 'EMT':
        invalid_materials_EMT_error(atoms.symbols)
        atoms.calc = EMT()

    elif args.simulation_method == 'Interface':
        interface_object = Interface(args, input_data)
        atoms = interface_object.get_atoms()
        atoms.calc = EMT()

    elif args.simulation_method == 'LennardJones':
        atoms.calc = LennardJones(
            input_data['lennard_jones']['atomic_number'],
            input_data['lennard_jones']['epsilon'],
            input_data['lennard_jones']['sigma'],
            input_data['lennard_jones']['r_cut'],
            modified=input_data['lennard_jones']['modified'],
        )

    # Set the momenta corresponding to T=300K
    MaxwellBoltzmannDistribution(
        atoms,
        temperature_K=input_data['temperature_K']
    )

    try:
        ensemble_mode = args.ensemble_mode
    except AttributeError:
        ensemble_mode = "energy"
    if ensemble_mode == "energy":
        # We want to run MD with constant energy using the VelocityVerlet
        # algorithm.
        dyn = VelocityVerlet(atoms, input_data['time_step'])
    elif ensemble_mode == "temperature":
        # Run MD with constant temperature instead using Andersen thermostat.
        dyn = Andersen(atoms, input_data['time_step'], input_data['temperature_K'], 1 * units.fs)

    traj = Trajectory(input_data['trajectory_file_name'], 'w', atoms)
    dyn.attach(traj.write, interval=input_data['trajectory_interval'])

    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        '''Function to print the potential, kinetic and total energy.'''
        if args.slurm:
            return
        epot, ekin, etot = calcenergy(a)
        print(
            'Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
            'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), etot)
        )
        if args.simulation_method == 'Interface':
            print(interface_object.get_interface_energy())


    f = open('output_data.txt', 'w') # Open the target file. Overwrite existing file.
    epot_list, ekin_list, etot_list, temperature_list, pressure_list, bulk_modulus = ([] for i in range(6))
    def savedata(a=atoms):
        '''Save simulation data to lists.'''
        if is_equilibrium():
            epot, ekin, etot = calcenergy(a)
            epot_list.append(epot)
            ekin_list.append(ekin)
            etot_list.append(etot)
            temperature = calctemperature(a)
            temperature_list.append(temperature)
            pressure = calcpressure(a)
            pressure_list.append(pressure)

    volumes, energies = [], []
    def volumes_and_energies(a=atoms):
        '''Vary the lattice constant to simulate different volumes to calculate bulk modulus.'''
        if is_equilibrium():
            scaling_factors = np.linspace(0.95, 1.05, 10)
            for scale in scaling_factors:
                scaled_atoms = a.copy()
                scaled_atoms.set_cell(atoms.get_cell() * scale, scale_atoms=True)
                scaled_atoms.calc = a.calc
                volumes.append(scaled_atoms.get_volume())
                energies.append(scaled_atoms.get_potential_energy())
            return volumes, energies


    equilibrium_list = [-1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000, -1000]
    def is_equilibrium(a=atoms):
        '''Function to determine if equilibrium.'''
        if ensemble_mode == 'energy':
            equilibrium_list.insert(0, a.get_temperature())
            equilibrium_list.pop(10)
            if statistics.pstdev(equilibrium_list) < 5:
                return True
            else:
                return False
        elif ensemble_mode == 'temperature':
            equilibrium_list.insert(0, (a.get_potential_energy() + a.get_kinetic_energy())/len(a))
            equilibrium_list.pop(10)
            if statistics.pstdev(equilibrium_list) < 0.01:
                return True
            else:
                return False



    # Now run the dynamics
    dyn.attach(printenergy, interval=input_data['trajectory_interval'])
    dyn.attach(savedata, interval=input_data['trajectory_interval'])

    savedata()
    printenergy()

    dyn.run(input_data['run_time'])
    cohesive_energy = calccohesiveenergy(epot_list, input_data['atoms']['materials'], atoms.calc)
    
    if args.cores == 1:
        dyn.attach(volumes_and_energies, interval=input_data['trajectory_interval'])
        volumes_and_energies()
        bulk_modulus = calcbulkmodulus(volumes, energies)
    else:
        bulk_modulus = -1


    if is_equilibrium():
        if args.slurm:

            epot, ekin, etot = calcenergy(atoms)
            slurm_cat = "Epot,Ekin,T,Etot,bulk_modulus,"
            slurm_print = f"{epot},{ekin},{ekin / (1.5 * units.kB)},{etot},{bulk_modulus},"

            if args.simulation_method == 'Interface':

                interface_energies = interface_object.get_interface_energy()
                slurm_cat_extend = 'interface_energy,substrate_alloy_ratio,film_alloy_ratio,substrate_lattice,film_lattice,Etot_substrate,Etot_film,substrate_atoms,substrate_structure,substrate_alloying_atoms,film_atoms,film_structure,film_alloying_atoms'
                slurm_print_extend = f"{interface_energies[0]},{input_data['interface']['substrate_alloy_ratio']},{input_data['interface']['film_alloy_ratio']},{input_data['interface']['substrate_lattice']},{input_data['interface']['film_lattice']},{interface_energies[2]},{interface_energies[3]},\
{input_data['interface']['substrate_atoms']},{input_data['interface']['substrate_structure']},{input_data['interface']['substrate_alloying_atoms']},{input_data['interface']['film_atoms']},{input_data['interface']['film_structure']},{input_data['interface']['film_alloying_atoms']}"
            else:
                slurm_cat_extend = 'pressure,lattice_constant,cohesive_energy,bulk_modulus,material, structure'
                try:
                    slurm_print_extend =f"{pressure_list[-1]},{input_data['atoms']['latticeconstant']},{cohesive_energy},{bulk_modulus},{input_data['atoms']['materials'][0]},{input_data['atoms']['structure']}"
                except IndexError:
                    slurm_print_extend =f"-1,{input_data['atoms']['latticeconstant']},{cohesive_energy},{bulk_modulus},{input_data['atoms']['materials'][0]},{input_data['atoms']['structure']}"

            print(slurm_cat + slurm_cat_extend)
            print(slurm_print + slurm_print_extend)

        else:
            cohesive_energy = calccohesiveenergy(epot_list, input_data['atoms']['materials'], atoms.calc)
            bulk_modulus = calcbulkmodulus(volumes, energies)
            writetofile(f, epot_list, ekin_list, etot_list, temperature_list, pressure_list, cohesive_energy, bulk_modulus)
    else:
        print("Equilibrium not reached")
    print("-----End of simulation.-----")
