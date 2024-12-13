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
            'x_size': 5,
            'y_size': 5,
            'z_size': 5,
            'pbc': True,
            'latticeconstant': 4.09,
        },
        'lennard_jones': {
            'atomic_number': [
                chemical_symbols.index(material) for material in materials
            ],
            'epsilon': 0.01,
            'sigma': 2,
            'r_cut': -1,
            'modified': True,
        },
        'interface': {
            'substrate_atoms': 'Cu',
            'substrate_structure': 'fcc',
            'substrate_lattice': 2.54,
            'substrate_alloy_ratio': 0.2,
            'substrate_alloying_atoms': "Ag",
            'film_atoms': 'Au',
            'film_structure': 'fcc',
            'film_lattice': 3.4,
            'film_alloy_ratio': 0.2,
            'film_alloying_atoms': "Ag",
            'size': 10,
        },
        'temperature_K': 300,
        'time_step': 1 * units.fs,
        'trajectory_file_name': 'cu.traj',
        'trajectory_interval': 10,
        'run_time': 1000,

        'lattice_constant': {
        'Au': 3.0,
        'Ag': 4.0,
        'Cu': 3.0,
        'Al': 3.0,
        'Ni': 3.0,
        'Pd': 3.0,
        'Pt': 3.0,
        'AuAg': 5.0,
        'AuCu': 3.0,
        'AuAl': 3.0,
        'AuNi': 3.0,
        'AuPd': 3.0,
        'AuPt': 3.0,
        'AgCu': 5.0,
        'AgAl': 3.0,
        'AgNi': 3.0,
        'AgPd': 3.0,
        'AgPt': 3.0,
        'CuAl': 3.0,
        'CuNi': 3.0,
        'CuPd': 3.0,
        'CuPt': 3.0,
        'AlNi': 3.0,
        'AlPd': 3.0,
        'AlPt': 3.0,
        'NiPd': 3.0,
        'NiPt': 3.0,
        'PdPt': 3.0,
        }


    }

    filename = file_name

    with open(filename, 'w') as f:
        toml.dump(data, f)


if __name__ == '__main__':
    create_input_file('input_data.toml')