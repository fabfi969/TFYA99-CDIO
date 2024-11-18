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
from random import random


def TwoBlocks(mat1,structure1,a1,mat2,structure2,a2,size):
    #Generate an two layers of atoms pressed up against each other
    bulk1 = bulk(mat1,structure1, a=a1) * (2*size, 2*size, size)
    bulk2 = bulk(mat2,structure2, a=a2) * (2*size, 2*size, size)
    interface = stack(bulk1, bulk2,maxstrain=9000000)
    view(interface)

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
    view(bulk1)

def random_alloys(mat1,structure1,a1,mat2,atomic_percent,size):
    #generates a single block of material with a randomly replaced atoms.
    tot_at = 4*size*size*size
    bulk1 = bulk(mat1,structure1, a=a1) * (2*size, 2*size, size)
    next = 0
    while next < tot_at:
        if random() < atomic_percent:
            bulk1.symbols[next]=mat2
        next += 1
    view(bulk1)

#Twoblocks("Cu","fcc",2.54,"Au","fcc",3.4,10)
#random_alloys("Cu","sc",2.54,"Au",0.5,9)
#pseudo_random_alloys("Cu","sc",2.54,"Au",0.17,9)