import unittest
from unittest.mock import MagicMock
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from calculate_properties import calcenergy, calctemperature, calcpressure, calccohesiveenergy, calcbulkmodulus

class TestPropertyCalculations(unittest.TestCase):

    def setUp(self):
        # Create 50 atoms for test.
        self.mock_atoms = MagicMock()
        self.mock_atoms.__len__.return_value = 50

    def test_calcenergy(self):
        self.mock_atoms.get_potential_energy.return_value = 10
        self.mock_atoms.get_kinetic_energy.return_value = 20

        epot, ekin, etot = calcenergy(self.mock_atoms)

        self.assertAlmostEqual(epot*50, 10)
        self.assertAlmostEqual(ekin*50, 20)
        self.assertAlmostEqual(etot*50, 10+20)

    def test_calctemperature(self):
        self.mock_atoms.get_temperature.return_value = 320

        temperature = calctemperature(self.mock_atoms)

        self.assertAlmostEqual(temperature, 320)

    def test_calccohesiveenergy(self):
        self.mock_atoms.get_potential_energy.return_value = 20
        
        potential_energy_list = [self.mock_atoms.get_potential_energy()/self.mock_atoms.__len__(),\
             self.mock_atoms.get_potential_energy()/self.mock_atoms.__len__()]
        
        cohesive_energy = calccohesiveenergy(potential_energy_list)
        
        self.assertAlmostEqual(cohesive_energy, self.mock_atoms.get_potential_energy()\
             / self.mock_atoms.__len__())


if __name__ == "__main__":
    property_tests = unittest.TestLoader().loadTestsFromTestCase(TestPropertyCalculations)
    testsuite = unittest.TestSuite([property_tests])
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
