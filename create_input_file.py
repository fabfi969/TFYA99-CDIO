"""script to create the TOML input file"""

import toml

def create_input_file(file_name):
    """
    function to create the TOML input file
    """
    data = {
        'material': '',
        'parameters': {
            'energy': 0,
            'temperature': 0,
        },
        'other_parameters': {
            'potential': 0,
        }
    }

    filename = file_name

    with open(filename, 'w') as f:
        toml.dump(data, f)

    print(f"Created {filename}")

if __name__ == "__main__":
    create_input_file('input_data.toml')
