'''file that contains the function which creates the atoms object to be used in the md
simulation'''

from ase.lattice.cubic import BodyCenteredCubic, Diamond, FaceCenteredCubic, SimpleCubic

from create_input_file import create_input_file
import toml
import re

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

def create_atoms(input_data):
    '''function which creates the atoms object to be used in the md simulation'''
    structure = input_data['atoms']['structure']
    match structure:
            case 'BodyCenteredCubic':
                return  BodyCenteredCubic(
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
            case 'Diamond':
                return  Diamond(
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
            case 'FaceCenteredCubic':
                return  FaceCenteredCubic(
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
            case 'SimpleCubic':
                return  SimpleCubic(
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

if __name__ == '__main__':
    input_file_name = 'input_data.toml'
    create_input_file(input_file_name)
    input_data = toml.load(input_file_name)
    create_atoms(input_data)
    print('created atoms object')
