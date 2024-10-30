"""script to create the TOML input file"""

import toml
from ase import units
from ase.data import atomic_numbers, chemical_symbols


def create_input_file(file_name):
    """
    function to create the TOML input file
    """

    materials = ["Ag"]

    data = {
        "atoms": {
            "directions": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
            "materials": materials,
            "x_size": 10,
            "y_size": 10,
            "z_size": 10,
            "pbc": True,
        },
        "lennard_jones": {
            "atomic_number": [
                chemical_symbols.index(material) for material in materials
            ],
            "epsilon": 0.010323,
            "sigma": 3.40,
            "r_cut": -1,
            "modified": True,
        },
        "temperature_K": 300,
        "time_step": 1 * units.fs,
        "trajectory_file_name": "cu.traj",
        "trajectory_interval": 10,
    }

    filename = file_name

    with open(filename, "w") as f:
        toml.dump(data, f)

    print(f"Created {filename}")


if __name__ == "__main__":
    create_input_file("input_data.toml")
