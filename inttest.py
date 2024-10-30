"""script for integration testing the code"""

import os
import os.path
import sys
import unittest

import toml

from create_input_file import create_input_file


class InputFileTests(unittest.TestCase):
    def check_input_file_types(self, input_file_name):
        with open(input_file_name, "r") as file:
            input_data = toml.load(file)

        # TODO lägg till fler assertIsInstance
        self.assertIsInstance(input_data["material"], str)

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


if __name__ == "__main__":
    tests = [unittest.TestLoader().loadTestsFromTestCase(InputFileTests)]
    testsuite = unittest.TestSuite(tests)
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
