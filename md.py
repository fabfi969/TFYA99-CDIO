'''Demonstrates molecular dynamics with constant energy. Is called by main'''

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
from create_atoms_md import invalid_materials_EMT, create_atoms
import toml
from random import random
from alloy import Interface





def calcenergy(a):  # store a reference to atoms in the definition.
    '''Function to calculate the potential, kinetic and total energy.'''
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    etot = epot + ekin
    return (epot, ekin, etot)

def TwoBlocks(mat1, structure1, a1, mat2, structure2, a2, size, alloy_ratio = 0, alloy = "N"):
    #Generate an two layers of atoms pressed up against each other
    bulk1 = bulk(mat1,structure1, a=a1) * (2*size, 2*size, size)
    if alloy != 0:
        bulk2 = random_alloys(mat2,structure2, a2, alloy, alloy_ratio, size)
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

def calctemperature(a):
    '''Function to calculate temperature.'''
    temperature = a.get_temperature()
    return temperature

def calcpressure(a):
    '''Function to calculate internal pressure.'''

    # Get kinetic energy
    _, ekin, _ = calcenergy(a)

    # Get forces and positions.
    forces = a.get_forces()
    positions = a.get_positions()

    # Calculate the sum in formula.
    sum_of_forces_and_positions = np.sum(forces * positions)

    # Get volume.
    volume = a.get_volume()

    # Calculate pressure using formula from lecture.
    pressure = (2 * ekin * len(a) + sum_of_forces_and_positions) / (3 * volume)
    return pressure

def run_md(args, input_data):
    '''runs the molecular dynamics simulation'''

    #command line override of lattice constant
    if args.lattice_constant != -1:
        input_data['atoms']['latticeconstant'] = args.lattice_constant

    # Set up a crystal
    # Sim = Interface("Cu","fcc",2.54,"Au","fcc",3.4,4)
    # atoms = Sim.get_atoms()
    if args.cif == '':
        atoms = create_atoms(input_data)
    else:
        atoms = read(args.cif, format='cif')

    # Describe the interatomic interactions with the Effective Medium Theory
    if args.simulation_method == 'EMT':
        invalid_materials_status = invalid_materials_EMT(atoms.symbols)
        if invalid_materials_status[0]:
            print('ERROR:\n    The defined elements cannot be simulated using EMT.\n    EMT only supports \
the metals Al, Cu, Ag, Au, Ni, Pd and Pt.')
            print(f'    The defined elements are {invalid_materials_status[1]}.')
            quit()
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
    # TODO check what next line does
    dyn.attach(traj.write, interval=input_data['trajectory_interval'])

    def printenergy(a=atoms):  # store a reference to atoms in the definition.
        '''Function to print the potential, kinetic and total energy.'''
        epot, ekin, etot = calcenergy(a)
        print(
            'Energy per atom: Epot = %.3feV  Ekin = %.3feV (T=%3.0fK)  '
            'Etot = %.3feV' % (epot, ekin, ekin / (1.5 * units.kB), etot)
        )

    f = open('output_data.txt', 'w') # Open the target file. Overwrite existing file.
    epot_list, ekin_list, etot_list, temperature_list, pressure_list = ([] for i in range(5))
    def savedata(a=atoms):
        '''Save simulation data to lists.'''
        epot, ekin, etot = calcenergy(a)
        epot_list.append(epot)
        ekin_list.append(ekin)
        etot_list.append(etot)
        temperature = calctemperature(a)
        temperature_list.append(temperature)
        pressure = calcpressure(a)
        pressure_list.append(pressure)


    def writetofile():
        """Save simulation data to file."""
        epot_list.insert(0, 'epot')
        ekin_list.insert(0, 'ekin')
        etot_list.insert(0, 'etot')
        temperature_list.insert(0, 'temperature')
        pressure_list.insert(0, 'pressure')
        print(epot_list, file=f)
        print(ekin_list, file=f)
        print(etot_list, file=f)
        print(temperature_list, file=f)
        print(pressure_list, file=f)
        f.close
        print('Simulation data saved to file: ', f.name )




    # Now run the dynamics
    dyn.attach(printenergy, interval=input_data['trajectory_interval'])
    dyn.attach(savedata, interval=input_data['trajectory_interval'])
    savedata()
    printenergy()
    dyn.run(input_data['run_time'])
    writetofile()

if __name__ == '__main__':
    input_file_name = 'input_data.toml'
    create_input_file(input_file_name)
    input_data = toml.load(input_file_name)
    class arguments:
        simulation_method = 'LennardJones'
        cif = 'SrCaMg6.cif'
    args = arguments()
    run_md(args, input_data)
