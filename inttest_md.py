import os.path
import sys
import unittest

import md

md.run_md()


class MdTests(unittest.TestCase):
    def test_file_exist(self):
        if os.path.exists("cu.traj"):
            self.assertTrue(True)


if __name__ == "__main__":
    tests = [unittest.TestLoader().loadTestsFromTestCase(MdTests)]
    testsuite = unittest.TestSuite(tests)
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
