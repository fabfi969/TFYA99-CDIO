"""script for integration testing the code"""

import os
import os.path
import sys
import unittest

import toml

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import patch
from create_input_file import create_input_file
from main import run_program
from md import run_md

class inputFileTests(unittest.TestCase):

    def test_create_input_test_file(self):
        input_file_name = "test_file.toml"
        create_input_file(input_file_name)
        if os.path.exists(input_file_name):
            self.assertTrue(True)
        os.remove(input_file_name)

    def test_input_file_exists(self):
        input_file_name = "input_data.toml"
        self.assertTrue(os.path.exists(input_file_name))

    def test_structure_parameter(self):
        input_file_name = "input_data.toml"
        create_input_file(input_file_name)
        input_data = toml.load(input_file_name)

        structure_list = ['BodyCenteredCubic', 'Diamond', 'FaceCenteredCubic', 'SimpleCubic']
        for structure in structure_list:
            for simul_method in ['EMT', 'LennardJones']:
                input_data['atoms']['structure'] = structure
                class arguments:
                    simulation_method = simul_method
                    lattice_constant = -1
                    structure = -1
                    cif = ''
                    slurm = False
                    lattice_interpolation = False
                    view_atoms = False
                args = arguments()
                run_md(args, input_data)
                self.assertTrue(True)

class SystemTest(unittest.TestCase):
    def test_program_running_EMT(self):
        with unittest.mock.patch('sys.argv', ["run_program.py" ,"-simulation_method", "EMT"]):
            run_program()
            self.assertTrue(True)

    def test_program_running_LennardJones(self):
        with unittest.mock.patch('sys.argv', ["run_program.py", "-simulation_method", "LennardJones"]):
            run_program()
            self.assertTrue(True)

    def test_program_running_LennardJones_with_visualisation(self):
        with unittest.mock.patch('sys.argv', ["run_program.py", "-simulation_method", "LennardJones", \
            "-visualisation", "on"]):
            run_program()
            self.assertTrue(True)

    def test_program_running_EMT_with_visualisation(self):
        with unittest.mock.patch('sys.argv', ["run_program.py", "-simulation_method", "EMT", \
            "-visualisation", "on"]):
            run_program()
            self.assertTrue(True)

    def test_program_running_without_arguments(self):
        with unittest.mock.patch('sys.argv', ["run_program.py"]):
            run_program()
            self.assertTrue(True)

    def test_program_with_thermostat(self):
        with unittest.mock.patch('sys.argv', ["run_program.py", "-ensemble_mode", "temperature"]):
            run_program()
            self.assertTrue(True)

    def test_program_running_with_cif(self):
        with unittest.mock.patch('sys.argv', ["run_program.py" ,"-cif", "Al.cif"]):
            run_program()
            self.assertTrue(True)

if __name__ == "__main__":
    system_tests = unittest.TestLoader().loadTestsFromTestCase(SystemTest)
    input_file_tests = unittest.TestLoader().loadTestsFromTestCase(inputFileTests)
    testsuite = unittest.TestSuite([system_tests, input_file_tests])
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
