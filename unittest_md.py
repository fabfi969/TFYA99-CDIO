"""script for unit testing the code"""

import sys
import unittest

# from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
# from ase.md.verlet import VelocityVerlet
# from asap3 import Trajectory
from asap3 import EMT

# from ase import units
from ase.lattice.cubic import FaceCenteredCubic

from md import calcenergy

atoms = FaceCenteredCubic(
    directions=[
        [1, 0, 0], [0, 1, 0], [0, 0, 1]], symbol="Cu", size=(2, 2, 2), pbc=True
)

atoms.calc = EMT()


class MdTests(unittest.TestCase):
    def test_consistent_total_energy(self):
        a, b, c = calcenergy(atoms)
        self.assertTrue(a + b == c)


if __name__ == "__main__":
    tests = unittest.TestLoader().loadTestsFromTestCase(MdTests)
    testsuite = unittest.TestSuite([tests])
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
