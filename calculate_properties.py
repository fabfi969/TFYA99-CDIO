import numpy as np
from ase.eos import EquationOfState
from ase import units
from ase import Atoms
import warnings
# Set this warning to an error since it gives a bad result for bulk modulus othervise.
warnings.filterwarnings("error", message="The minimum volume of your fit is not in your volumes.*")


def calcenergy(a):  # store a reference to atoms in the definition.
    '''Function to calculate the potential, kinetic and total energy.'''
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    etot = epot + ekin
    return (epot, ekin, etot)

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

def calccohesiveenergy(epot_list, material, simulation_method):
    '''Function to calculate cohesive energy.'''
    try:
        isolated_atom = Atoms(material[0])
        isolated_atom.set_cell([10.0, 10.0, 10.0])
        isolated_atom.center()
        isolated_atom.calc = simulation_method
        e_cohesive = abs((sum(epot_list) / len(epot_list)) - isolated_atom.get_potential_energy())
        return e_cohesive
    except:
        # Cohesive energy could not be calculated. Perhaps equilibrium was not reached.
        return -1

def calcbulkmodulus(volumes, energies):
    '''Function to calculate bulk modulus.'''
    try:
        eos = EquationOfState(volumes, energies, eos = 'murnaghan')
        _, _, bulk_modulus = eos.fit()
        bulk_modulus = bulk_modulus / units.kJ * 1.0e24 # Convert eV/Angstrom^3 to GPa
        return bulk_modulus
    except:
        # Bulk modulus could not be calculated. Perhaps equilibrium was not reached.
        return -1