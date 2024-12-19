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
            # 'SimpleCubic', 'FaceCenteredCubic', 'BodyCenteredCubic', 'Diamond'
            'structure': 'FaceCenteredCubic',
            'directions': [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            'materials': materials,
            'x_size': 10,
            'y_size': 10,
            'z_size': 10,
            'pbc': True,
            'latticeconstant': 4.09,
        },
        'structure_choices':['SimpleCubic', 'FaceCenteredCubic', 'BodyCenteredCubic', 'Diamond'],
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
            'substrate_atoms': 'Pt',
            'substrate_structure': 'fcc',
            'substrate_lattice': 3.93,
            'substrate_alloy_ratio': 0,
            'substrate_alloying_atoms': "Au",
            'film_atoms': 'Cu',
            'film_structure': 'fcc',
            'film_lattice': 3.85,
            'film_alloy_ratio': 0,
            'film_alloying_atoms': "Ag",
            'size': 10,
        },
        'temperature_K': 300,
        'time_step': 1 * units.fs,
        'trajectory_file_name': 'cu.traj',
        'trajectory_interval': 10,
        'run_time': 2000,

        'lattice_constant': {
        'Au': 4.06,
        'Ag': 4.08,
        'Cu': 3.61,
        'Al': 4.01,
        'Ni': 3.49,
        'Pd': 3.87,
        'Pt': 3.93,
        'AuAg': 4.05,
        'AuCu': 3.85,
        'AuAl': 4.05,
        'AuNi': 3.81,
        'AuPd': 3.97,
        'AuPt': 4.00,
        'AgCu': 3.85,
        'AgAl': 4.07,
        'AgNi': 3.80,
        'AgPd': 3.97,
        'AgPt': 3.98,
        'CuAl': 3.78,
        'CuNi': 3.60,
        'CuPd': 3.69,
        'CuPt': 3.85,
        'AlNi': 3.75,
        'AlPd': 4.00,
        'AlPt': 4.00,
        'NiPd': 3.71,
        'NiPt': 3.79,
        'PdPt': 3.90,
        }


    }

    filename = file_name

    with open(filename, 'w') as f:
        toml.dump(data, f)


if __name__ == '__main__':
    create_input_file('input_data.toml')
