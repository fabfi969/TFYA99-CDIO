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
        print("Code check 1")
        with open(input_file_name, "r") as file:
            input_data = toml.load(file)

        # TODO lägg till fler assertIsInstance
        self.assertIsInstance(input_data["atoms"]["materials"][0], str)

    def test_create_input_test_file(self):
        print("Code check 2")
        input_file_name = "test_file.toml"
        create_input_file(input_file_name)
        if os.path.exists(input_file_name):
            self.assertTrue(True)
        self.check_input_file_types(input_file_name)
        os.remove(input_file_name)

    def test_input_file_exists(self):
        print("Code check 3")
        input_file_name = "input_data.toml"
        self.assertTrue(os.path.exists(input_file_name))
        self.check_input_file_types(input_file_name)

     

class SystemTest(unittest.TestCase):
    def test_program_running(self):
        print("Code check 4")
        with unittest.mock.patch('sys.argv', ['-a', "EMT"]):
            run_program()
            self.assertTrue(True)


if __name__ == "__main__":
    input_tests = unittest.TestLoader().loadTestsFromTestCase(InputFileTests)
    system_tests = unittest.TestLoader().loadTestsFromTestCase(SystemTest)
    testsuite = unittest.TestSuite([input_tests, system_tests])
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
