import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from save_data import writetofile

class TestSaveData(unittest.TestCase):
    
    def setUp(self):
        # First create temporary test file.
        self.testfile = "temp_testfile.txt"

    def tearDown(self):
        # Remove the temporary file.
        if os.path.exists(self.testfile):
            os.remove(self.testfile)

    def test_writetofile(self):
        epot_list = [1, 2]
        ekin_list = [3, 4]
        etot_list = [4, 6]
        temperature_list = [220, 225]
        pressure_list = [10, 15]
        cohesive_energy = 5
        bulk_modulus = 7
        with open(self.testfile, "w") as f:
            writetofile(f, epot_list, ekin_list, etot_list, \
                temperature_list, pressure_list, cohesive_energy, bulk_modulus)
        with open(self.testfile, "r") as f:
            contents = f.readlines()
        
        expected_contents = [
            "['epot', 1, 2]\n",
            "['ekin', 3, 4]\n",
            "['etot', 4, 6]\n",
            "['temperature', 220, 225]\n",
            "['pressure', 10, 15]\n",
            "Cohesive energy:  5 eV/atom\n",
            "Bulk modulus:  7 unit..?\n"
        ]

        self.assertEqual(contents, expected_contents)

if __name__ == "__main__":
    savedata_tests = unittest.TestLoader().loadTestsFromTestCase(TestSaveData)
    testsuite = unittest.TestSuite([savedata_tests])
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())