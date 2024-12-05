'''script to create the TOML input file'''

import toml
from ase import units
from ase.data import chemical_symbols

def create_input_file(file_name):
    '''
    function to create the TOML input file
    '''

    materials = ['Ag']

    data = {
        'atoms': {
            # 'BodyCenteredCubic', 'Diamond', 'FaceCenteredCubic', 'SimpleCubic'
            'structure': 'FaceCenteredCubic',
            'directions': [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            'materials': materials,
            'x_size': 10,
            'y_size': 10,
            'z_size': 10,
            'pbc': True,
            'latticeconstant': 10.0,
        },
        'lennard_jones': {
            'atomic_number': [
                chemical_symbols.index(material) for material in materials
            ],
            'epsilon': 0.01,
            'sigma': 0.8,
            'r_cut': -1,
            'modified': True,
        },
        'interface': {
            'substrate_atoms': 'Cu',
            'substrate_structure': 'fcc',
            'substrate_lattice': 2.54,
            'film_atoms': 'Au',
            'film_structure': 'fcc',
            'film_lattice': 3.4,
            'size': 10,
            'alloy_ratio': 0.2,
            'alloying_atoms': "Ag",
        },
        'temperature_K': 300,
        'time_step': 1 * units.fs,
        'trajectory_file_name': 'cu.traj',
        'trajectory_interval': 10,
        'run_time': 20,
        
    }

    filename = file_name

    with open(filename, 'w') as f:
        toml.dump(data, f)


if __name__ == '__main__':
    create_input_file('input_data.toml')
