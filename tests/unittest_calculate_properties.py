import unittest
from unittest.mock import MagicMock, patch
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from calculate_properties import calcenergy, calctemperature, calcpressure, calccohesiveenergy, calcbulkmodulus
from ase.build import bulk
from main import run_program
import re

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

    @patch('main.toml.load')
    def test_calccohesiveenergy(self, mock_toml_load):
        # Simulate gold input data.
        mock_input_data = {
            'temperature_K': 300,
            'time_step': 0.09822694788464063,
            'trajectory_file_name': "Au.traj",
            'trajectory_interval': 10,
            'run_time': 1200,
            'atoms': {
                'structure': 'FaceCenteredCubic',
                'directions': [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                'materials': ['Au'],
                'x_size': 10,
                'y_size': 10,
                'z_size': 10,
                'pbc': True,
                'latticeconstant': 4.08
            },
            'lennard_jones': {
                'atomic_number': [79],
                'epsilon': 0.01,
                'sigma': 0.8,
                'r_cut': -1,
                'modified': True
            }
        }
        mock_toml_load.return_value = mock_input_data
        run_program()
        with open('output_data.txt', 'r') as file:
            data = file.read()
        match = re.search(r"Cohesive energy:\s+([\d.]+)\s+eV/atom", data)
        cohesive_energy = float(match.group(1))
        # Expected value: 3,81 eV/atom.
        self.assertGreaterEqual(cohesive_energy, 3.70)
        self.assertLessEqual(cohesive_energy, 3.90)
    
    @patch('main.toml.load')
    def test_calcbulkmodulus(self, mock_toml_load):
        # Simulate gold input data.
        mock_input_data = {
            'temperature_K': 300,
            'time_step': 0.09822694788464063,
            'trajectory_file_name': "Au.traj",
            'trajectory_interval': 10,
            'run_time': 1200,
            'atoms': {
                'structure': 'FaceCenteredCubic',
                'directions': [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                'materials': ['Au'],
                'x_size': 10,
                'y_size': 10,
                'z_size': 10,
                'pbc': True,
                'latticeconstant': 4.08
            },
            'lennard_jones': {
                'atomic_number': [79],
                'epsilon': 0.01,
                'sigma': 0.8,
                'r_cut': -1,
                'modified': True
            }
        }
        mock_toml_load.return_value = mock_input_data
        run_program()
        with open('output_data.txt', 'r') as file:
            data = file.read()
        match = re.search(r"Bulk modulus:\s+([\d.]+)\s+GPa", data)
        bulk_modulus = float(match.group(1))
        self.assertGreaterEqual(bulk_modulus, 148)
        self.assertLessEqual(bulk_modulus, 180)



if __name__ == "__main__":
    property_tests = unittest.TestLoader().loadTestsFromTestCase(TestPropertyCalculations)
    testsuite = unittest.TestSuite([property_tests])
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
