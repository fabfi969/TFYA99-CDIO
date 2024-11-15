"""script for integration testing the code"""

import os
import os.path
import sys
import unittest

import toml

from unittest.mock import patch
from create_input_file import create_input_file
from main import run_program


class InputFileTests(unittest.TestCase):
    def check_input_file_types(self, input_file_name):
        with open(input_file_name, "r") as file:
            input_data = toml.load(file)

        self.assertIsInstance(input_data["atoms"]["directions"], list)
        self.assertIsInstance(input_data["atoms"]["materials"][0], str)
        self.assertIsInstance(input_data["atoms"]["x_size"], (int, float))
        self.assertIsInstance(input_data["atoms"]["y_size"], (int, float))
        self.assertIsInstance(input_data["atoms"]["z_size"], (int, float))
        self.assertIsInstance(input_data["atoms"]["pbc"], bool)

        self.assertIsInstance(input_data["lennard_jones"]["atomic_number"][0], int)
        self.assertIsInstance(input_data["lennard_jones"]["epsilon"], (int, float))
        self.assertIsInstance(input_data["lennard_jones"]["sigma"], (int, float))
        self.assertIsInstance(input_data["lennard_jones"]["r_cut"], (int, float))
        self.assertIsInstance(input_data["lennard_jones"]["modified"], bool)
        
        self.assertIsInstance(input_data["temperature_K"], (int, float))
        self.assertIsInstance(input_data["time_step"], (int, float))
        self.assertIsInstance(input_data["trajectory_file_name"], str)
        self.assertIsInstance(input_data["trajectory_interval"], (int, float))

    def test_create_input_test_file(self):
        input_file_name = "test_file.toml"
        create_input_file(input_file_name)
        if os.path.exists(input_file_name):
            self.assertTrue(True)
        self.check_input_file_types(input_file_name)
        os.remove(input_file_name)

    def test_input_file_exists(self):
        input_file_name = "input_data.toml"
        self.assertTrue(os.path.exists(input_file_name))
        self.check_input_file_types(input_file_name)
     

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




if __name__ == "__main__":
    input_tests = unittest.TestLoader().loadTestsFromTestCase(InputFileTests)
    system_tests = unittest.TestLoader().loadTestsFromTestCase(SystemTest)
    testsuite = unittest.TestSuite([input_tests, system_tests])
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
