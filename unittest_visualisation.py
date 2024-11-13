import unittest
import sys
import os
from visualisation import plotenergy
import matplotlib.pyplot as plt 

class VisualisationTests(unittest.TestCase):

    def setUp(self):
        # First create temporary test file.
        self.testfile = "temp_testfile.txt"
        f = open(self.testfile, "w")
        print(["epot", 1,2,3], file = f)
        print(["ekin", 4,5,6], file = f)
        print(["etot", 7,8,9], file = f)
        f.close()

    def tearDown(self):
        # Remove the temporary file.
        if os.path.exists(self.testfile):
            os.remove(self.testfile)


    def test_nr_of_data_types(self):
        with open("temp_testfile.txt", "r") as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 3) 

    def test_plot_created(self):
        plotenergy("temp_testfile.txt")
        fig = plt.gcf()
        self.assertIsNotNone(fig)
        
        

if __name__ == "__main__":
    tests = unittest.TestLoader().loadTestsFromTestCase(VisualisationTests)
    testsuite = unittest.TestSuite([tests])
    result = unittest.TextTestRunner(verbosity=0).run(testsuite)
    sys.exit(not result.wasSuccessful())
    