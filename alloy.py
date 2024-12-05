"""A large set of function to be used when simulating materials"""

from random import random
from asap3 import EMT
from ase.visualize import view
from ase.build import bulk
from ase.build.tools import stack
from create_input_file import create_input_file
import toml
#from md import calcenergy


def twoblocks(mat1,
              structure1,
              latticesubstrate,
              mat2, structure2,
              latticefilm,
              size,
              alloy_ratio = 0,
              alloy = "N"):
    """Generate an two layers of atoms pressed up against each other"""
    bulk1 = bulk(mat1,structure1, latticesubstrate) * (2*size, 2*size, size)
    if alloy != 0:
        bulk2 = random_alloys(mat2,structure2, latticefilm, alloy, alloy_ratio, size)
    else:
        bulk2 = bulk(mat2,structure2, latticefilm) * (2*size, 2*size, size)
    interface = stack(bulk1, bulk2,maxstrain=100)
    view(interface)
    return interface

def calcenergy(atoms):  # store a reference to atoms in the definition
    """Function to calculate the potential, kinetic and total energy."""
    epot = atoms.get_potential_energy() / len(atoms)
    ekin = atoms.get_kinetic_energy() / len(atoms)
    etot = epot + ekin
    return epot, ekin, etot

def pseudo_random_alloys(mat1,
                         structure1,
                         latticesubstrate,
                         mat2,
                         atomic_percent,
                         size):
    """generates a singe block of material of intermittenly placed atoms of a different material"""
    tot_at = 4*size*size*size
    step = 1/atomic_percent
    bulk1 = bulk(mat1,structure1, a=latticesubstrate) * (2*size, 2*size, size)
    count = 0
    while count < tot_at:
        place = round(count)
        bulk1.symbols[place]=mat2
        count += step
    #view(bulk1)

def random_alloys(mat1,
                  structure1,
                  latticesubstrate,
                  mat2,
                  atomic_percent,
                  size):
    """generates a single block of material with a randomly replaced atoms."""
    tot_at = 4*size*size*size
    bulk1 = bulk(mat1,structure1, a=latticesubstrate) * (2*size, 2*size, size)
    count = 0
    while count < tot_at:
        if random() < atomic_percent:
            bulk1.symbols[count]=mat2
        count += 1
    return bulk1
    #view(bulk1)

class Interface:
    """A class that generates objects that are interfaces between to objects"""
    def __init__(self,
                 mat1,
                 structure1,
                 latticesubstrate,
                 mat2,
                 structure2,
                 latticefilm,
                 size,
                 alloy_ratio = 0,
                 alloy = "N"):
        """The init makes the interface, represented by an atoms object
        and applies several relevant atributes."""
        input_file_name = 'input_data.toml'
        create_input_file(input_file_name)
        input_data = toml.load(input_file_name)
        self.substrate = mat1 = input_data['interface']['substrate_atoms']
        self.sub_struc = structure1 = input_data['interface']['substrate_structure']
        self.latticesubstrate = latticesubstrate = input_data['interface']['substrate_lattice']
        self.film = mat2 = input_data['interface']['film_atoms']
        self.film_struc = structure2 = input_data['interface']['film_structure']
        self.latticefilm = latticefilm = input_data['interface']['film_lattice']
        self.size = size = input_data['interface']['size']
        self.alloy_ratio = alloy_ratio = input_data['interface']['alloy_ratio']
        self.alloy_mat = alloy = input_data['interface']['alloying_atoms']
        bulk1 = bulk(mat1,structure1, a=latticesubstrate) * (2*size, 2*size, size)
        if alloy != 0:
            bulk2 = random_alloys(mat2,structure2, latticefilm, alloy, alloy_ratio, size)
        else:
            bulk2 = bulk(mat2,structure2, a=latticefilm) * (2*size, 2*size, size)
        interface = stack(bulk1, bulk2,maxstrain=100)
        self.bulk1 = bulk1
        self.bulk2 = bulk2
        self.interface = interface

    def get_atoms(self):
        """Returns the atoms objects that represents the interface"""
        return self.interface

    def get_interface_energy(self):
        """Returns the interface energy of the interface"""
        self.bulk1.calc = EMT()
        self.bulk2.calc = EMT()
        self.interface.calc = EMT()
        etot1 = calcenergy(self.bulk1)[2]
        etot2 = calcenergy(self.bulk2)[2]
        etot3 = calcenergy(self.interface)[2]
        eint = (etot3 - etot2 - etot1)/2
        eint_per_å = eint/((self.size * self.latticesubstrate)*(self.size * self.latticesubstrate))
        return eint, eint_per_å



BeepBoop = Interface("Cu","fcc",2.54,"Au","fcc",3.4,4)
view(BeepBoop.get_atoms())
print(BeepBoop.get_interface_energy())
#twoBlocks("Cu","fcc",2.54,"Au","fcc",3.4,4)
#random_alloys("Cu","sc",2.54,"Au",0.5,9)
#pseudo_random_alloys("Cu","sc",2.54,"Au",0.17,9)
