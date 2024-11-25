import numpy as np

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