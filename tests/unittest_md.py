"""script for unit testing the code"""

import sys
import os
import unittest
import toml

from asap3 import EMT
from ase.lattice.cubic import FaceCenteredCubic

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from md import calcenergy
from create_input_file import create_input_file
from create_atoms_md import invalid_materials_EMT

atoms = FaceCenteredCubic(
    directions=[
        [1, 0, 0], [0, 1, 0], [0, 0, 1]], symbol="Cu", size=(2, 2, 2), pbc=True
)
atoms.calc = EMT()

class MdTests(unittest.TestCase):
    def test_consistent_total_energy(self):
        a, b, c = calcenergy(atoms)
        self.assertTrue(a + b == c)
    def test_invalid_materials_EMT(self):
        self.assertFalse(invalid_materials_EMT(['Al', 'Cu', 'Ag', 'Au', 'Ni', 'Pd', 'Pt'])[0])
        self.assertFalse(invalid_materials_EMT(['Al', 'Cu', 'Ag'])[0])
        self.assertTrue(invalid_materials_EMT(['Al', 'Cu', 'Ag', 'H'])[0])
        self.assertTrue(invalid_materials_EMT(['H'])[0])


class InputFileTests(unittest.TestCase):
    def test_check_input_file_types(self):
        input_file_name = 'input_data.toml'
        create_input_file(input_file_name)
        with open(input_file_name, "r") as file:
            input_data = toml.load(file)

        self.assertIsInstance(input_data["atoms"]["directions"], list)
        self.assertIsInstance(input_data["atoms"]["materials"][0], str)
        self.assertIsInstance(input_data["atoms"]["x_size"], (int, float))
        self.assertIsInstance(input_data["atoms"]["y_size"], (int, float))
        self.assertIsInstance(input_data["atoms"]["z_size"], (int, float))
        self.assertIsInstance(input_data["atoms"]["pbc"], bool)
        self.assertIsInstance(input_data["atoms"]["latticeconstant"], float)

        self.assertIsInstance(input_data["lennard_jones"]["atomic_number"][0], int)
        self.assertIsInstance(input_data["lennard_jones"]["epsilon"], (int, float))
        self.assertIsInstance(input_data["lennard_jones"]["sigma"], (int, float))
        self.assertIsInstance(input_data["lennard_jones"]["r_cut"], (int, float))
        self.assertIsInstance(input_data["lennard_jones"]["modified"], bool)

        self.assertIsInstance(input_data["temperature_K"], (int, float))
        self.assertIsInstance(input_data["time_step"], (int, float))
        self.assertIsInstance(input_data["trajectory_file_name"], str)
        self.assertIsInstance(input_data["trajectory_interval"], (int, float))

if __name__ == "__main__":
    md_tests = unittest.TestLoader().loadTestsFromTestCase(MdTests)
    input_tests = unittest.TestLoader().loadTestsFromTestCase(InputFileTests)
    testsuite = unittest.TestSuite([md_tests, input_tests])
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
