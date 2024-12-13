"""A large set of function to be used when simulating materials"""

from random import random
from asap3 import EMT
from ase.visualize import view
from ase.build import bulk
from ase.build.tools import stack
from create_input_file import create_input_file
import toml

from asap3 import MakeParallelAtoms
#from md import calcenergy


def twoblocks(mat1,
              structure1,
              latticesubstrate,
              mat2, structure2,
              latticefilm,
              size,
              film_alloy_ratio = 0,
              alloy = "N"):
    """Generate an two layers of atoms pressed up against each other"""
    bulk1 = bulk(mat1,structure1, latticesubstrate) * (2*size, 2*size, size)
    if alloy != 0:
        bulk2 = random_alloys(mat2,structure2, latticefilm, alloy, film_alloy_ratio, size)
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
    def __init__(self, args, input_data):
        """The init makes the interface, represented by an atoms object
        and applies several relevant atributes."""

        self.substrate = substrate_mat = input_data['interface']['substrate_atoms']
        self.sub_struc = substrate_structure = input_data['interface']['substrate_structure']
        self.latticesubstrate = latticesubstrate = input_data['interface']['substrate_lattice']
        self.substrate_alloy_ratio = substrate_alloy_ratio = input_data['interface']['substrate_alloy_ratio']
        self.substrate_alloy_mat = substrate_alloy = input_data['interface']['substrate_alloying_atoms']

        self.film = film_mat = input_data['interface']['film_atoms']
        self.film_struc = film_struct = input_data['interface']['film_structure']
        self.latticefilm = latticefilm = input_data['interface']['film_lattice']
        self.film_alloy_ratio = film_alloy_ratio = input_data['interface']['film_alloy_ratio']
        self.alloy_mat = film_alloy = input_data['interface']['film_alloying_atoms']

        self.size = size = input_data['interface']['size']

        if substrate_alloy != 0:
            substrate_bulk = random_alloys(substrate_mat, substrate_structure, latticefilm, substrate_alloy, substrate_alloy_ratio, size)
        else:
            substrate_bulk = bulk(substrate_mat, substrate_structure, a=latticefilm) * (2*size, 2*size, size)

        if film_alloy != 0:
            film_bulk = random_alloys(film_mat, film_struct, latticefilm, film_alloy, film_alloy_ratio, size)
        else:
            film_bulk = bulk(film_mat, film_struct, a=latticefilm) * (2*size, 2*size, size)

        interface = stack(substrate_bulk, film_bulk,maxstrain=100)

        if args.cores == 1:
            self.substrate_bulk = substrate_bulk
            self.film_bulk = film_bulk
            self.interface = interface
        elif args.cores == 8:
            cpulayout = (2,2,2)
            self.substrate_bulk = MakeParallelAtoms(substrate_bulk, cpulayout, cell=None, pbc=None, distribute=True)
            self.film_bulk = MakeParallelAtoms(film_bulk, cpulayout, cell=None, pbc=None, distribute=True)
            self.interface = MakeParallelAtoms(interface, cpulayout, cell=None, pbc=None, distribute=True)

    def get_atoms(self):
        """Returns the atoms objects that represents the interface"""
        return self.interface

    def get_interface_energy(self):
        """Returns the interface energy of the interface"""

        

        self.substrate_bulk.calc = EMT()
        self.film_bulk.calc = EMT()
        self.interface.calc = EMT()
        etot1 = calcenergy(self.substrate_bulk)[2]
        etot2 = calcenergy(self.film_bulk)[2]
        etot3 = calcenergy(self.interface)[2]
        eint = (etot3 - etot2 - etot1)/2
        eint_per_å = eint/((self.size * self.latticesubstrate)*(self.size * self.latticesubstrate))
        return eint, eint_per_å, etot1, etot2


if __name__ == "__main__":
    BeepBoop = Interface()
    view(BeepBoop.get_atoms())
    print(BeepBoop.get_interface_energy())
    #twoBlocks("Cu","fcc",2.54,"Au","fcc",3.4,4)
    #random_alloys("Cu","sc",2.54,"Au",0.5,9)
    #pseudo_random_alloys("Cu","sc",2.54,"Au",0.17,9)