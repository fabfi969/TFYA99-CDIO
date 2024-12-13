'''file that contains the function which creates the atoms object to be used in the md
simulation'''

from ase.lattice.cubic import BodyCenteredCubic, Diamond, FaceCenteredCubic, SimpleCubic

from create_input_file import create_input_file
import toml
import re
from asap3 import MakeParallelAtoms


def invalid_materials_EMT_error(atoms_symbols):
    invalid_materials_status = invalid_materials_EMT(atoms_symbols)
    if invalid_materials_status[0]:
        print('ERROR:\n    The defined elements cannot be simulated using EMT.\n    EMT only supports \
the metals Al, Cu, Ag, Au, Ni, Pd and Pt.')
        print(f'    The defined elements are {invalid_materials_status[1]}.')
        quit()

def invalid_materials_EMT(materials_list):
    '''checks if the given materials can be used for EMT (effective-medium theory)
    calculations. It only supports the standard EMT metals: Al, Cu, Ag, Au, Ni, Pd and Pt

    Parameters:
    material_list (list): a list of the chemical elements which are to be simulated

    Returns:
    bool: returns True if the elements cannot be used for EMT simulations, False if they can
    '''
    materials_list = set([re.sub(r'\d+', '', material) for material in materials_list])

    valid_elements = ['Al', 'Cu', 'Ag', 'Au', 'Ni', 'Pd', 'Pt']
    return not(all(element in valid_elements for element in materials_list)), materials_list

def create_atoms(args, input_data):
    '''function which creates the atoms object to be used in the md simulation'''
    structure = input_data['atoms']['structure']
    if structure == 'BodyCenteredCubic':
        atoms = BodyCenteredCubic(
                    directions=input_data['atoms']['directions'],
                    symbol=input_data['atoms']['materials'][0],
                    size=(
                        input_data['atoms']['x_size'],
                        input_data['atoms']['y_size'],
                        input_data['atoms']['z_size'],
                        ),
                    pbc=input_data['atoms']['pbc'],
                    latticeconstant=input_data['atoms']['latticeconstant'],
                    )
    elif structure == 'Diamond':
        atoms = Diamond(
                    directions=input_data['atoms']['directions'],
                    symbol=input_data['atoms']['materials'][0],
                    size=(
                        input_data['atoms']['x_size'],
                        input_data['atoms']['y_size'],
                        input_data['atoms']['z_size'],
                        ),
                    pbc=input_data['atoms']['pbc'],
                    latticeconstant=input_data['atoms']['latticeconstant'],
                    )
    elif structure == 'FaceCenteredCubic':
        atoms = FaceCenteredCubic(
                    directions=input_data['atoms']['directions'],
                    symbol=input_data['atoms']['materials'][0],
                    size=(
                        input_data['atoms']['x_size'],
                        input_data['atoms']['y_size'],
                        input_data['atoms']['z_size'],
                        ),
                    pbc=input_data['atoms']['pbc'],
                    latticeconstant=input_data['atoms']['latticeconstant'],
                    )
    elif structure == 'SimpleCubic':
        atoms = SimpleCubic(
                    directions=input_data['atoms']['directions'],
                    symbol=input_data['atoms']['materials'][0],
                    size=(
                        input_data['atoms']['x_size'],
                        input_data['atoms']['y_size'],
                        input_data['atoms']['z_size'],
                        ),
                    pbc=input_data['atoms']['pbc'],
                    latticeconstant=input_data['atoms']['latticeconstant'],
                    )
    if args.cores == 1:
        return atoms
    elif args.cores == 8:
        cpulayout = (2,2,2)
        return MakeParallelAtoms(atoms, cpulayout, cell=None, pbc=None, distribute=True)