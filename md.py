'''Demonstrates molecular dynamics with constant energy. Is called by main'''

from asap3 import EMT, LennardJones, Trajectory # This line gives the terminal warnings.
from ase import units
from ase.lattice.cubic import BodyCenteredCubic, BodyCenteredCubicFactory, Bravais, Diamond
from ase.lattice.cubic import DiamondFactory, FaceCenteredCubic, FaceCenteredCubicFactory
from ase.lattice.cubic import SimpleCubic, SimpleCubicFactory
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase.io import read
from ase.md import Andersen
import numpy as np
from create_input_file import create_input_file
from create_atoms_md import invalid_materials_EMT, create_atoms
import toml
from calculate_properties import calcenergy, calctemperature, calcpressure
from save_data import writetofile


def run_md(args, input_data):
    '''runs the molecular dynamics simulation'''

    # Set up a crystal
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