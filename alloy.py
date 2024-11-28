from asap3 import EMT, LennardJones, Trajectory
from ase import units
from ase import Atoms
from ase.lattice.cubic import FaceCenteredCubic
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
from ase.build import molecule
from ase.visualize import view
from ase.lattice.cubic import BodyCenteredCubic
from ase.lattice.cubic import FaceCenteredCubicFactory
from ase.build import bulk
from ase.build.tools import sort
from ase.build.tools import cut, stack
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md.verlet import VelocityVerlet
#from md import calcenergy
from random import random


def TwoBlocks(mat1, structure1, a1, mat2, structure2, a2, size, alloy_ratio = 0, alloy = "N"):
    #Generate an two layers of atoms pressed up against each other
    bulk1 = bulk(mat1,structure1, a=a1) * (2*size, 2*size, size)
    if alloy != 0:
        bulk2 = random_alloys(mat2,structure2, a2, alloy, alloy_ratio, size)
    else:
        bulk2 = bulk(mat2,structure2, a=a2) * (2*size, 2*size, size)
    interface = stack(bulk1, bulk2,maxstrain=100)
    view(interface)
    return interface

def calcenergy(a):  # store a reference to atoms in the definition.
    """Function to calculate the potential, kinetic and total energy."""
    epot = a.get_potential_energy() / len(a)
    ekin = a.get_kinetic_energy() / len(a)
    etot = epot + ekin
    return (epot, ekin, etot)

def pseudo_random_alloys(mat1,structure1,a1,mat2,atomic_percent,size):
    #generates a singe block of material of intermittenly placed atoms of a different material
    tot_at = 4*size*size*size
    step = 1/atomic_percent
    bulk1 = bulk(mat1,structure1, a=a1) * (2*size, 2*size, size)
    next = 0
    while next < tot_at:
        place = round(next)
        bulk1.symbols[place]=mat2
        next += step
    #view(bulk1)

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

class Interface:
    def __init__(q, mat1, structure1, a1, mat2, structure2, a2, size, alloy_ratio = 0, alloy = "N"):
        q.substrate = mat1
        q.sub_struc = structure1
        q.a1 = a1
        q.film = mat2
        q.film_struc = structure2
        q.a2 = a2
        q.size = size
        q.alloy_ratio = alloy_ratio
        q.alloy_mat = alloy
        bulk1 = bulk(mat1,structure1, a=a1) * (2*size, 2*size, size)
        if alloy != 0:
            bulk2 = random_alloys(mat2,structure2, a2, alloy, alloy_ratio, size)
        else:
            bulk2 = bulk(mat2,structure2, a=a2) * (2*size, 2*size, size)
        interface = stack(bulk1, bulk2,maxstrain=100)
        q.bulk1 = bulk1
        q.bulk2 = bulk2
        q.interface = interface

    def get_atoms(q):
        return q.interface

    def get_E_int(q):
        q.bulk1.calc = EMT()
        q.bulk2.calc = EMT()
        q.interface.calc = EMT()
        epot1, ekin1, etot1 = calcenergy(q.bulk1)
        epot2, ekin2, etot2 = calcenergy(q.bulk2)
        epot3, ekin3, etot3 = calcenergy(q.interface)
        eint = (etot3 - etot2 - etot1)/3
        return eint



BeepBoop = Interface("Cu","fcc",2.54,"Au","fcc",3.4,4)
# view(BeepBoop.get_atoms())
# print(BeepBoop.get_E_int())
#TwoBlocks("Cu","fcc",2.54,"Au","fcc",3.4,4)
#random_alloys("Cu","sc",2.54,"Au",0.5,9)
#pseudo_random_alloys("Cu","sc",2.54,"Au",0.17,9)