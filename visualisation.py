import warnings
warnings.filterwarnings("ignore", message = "Unable to import Axes3D")
import matplotlib.pyplot as plt # This would give a warning without above line.
import ast

def plotenergy(output_file):
    "Plot energies."    
    f = open(output_file, "r")
    epot = ast.literal_eval(f.readline())
    ekin = ast.literal_eval(f.readline())
    etot = ast.literal_eval(f.readline())
    epot.pop(0)
    ekin.pop(0)
    etot.pop(0)

    plt.plot(epot)
    plt.plot(ekin)
    plt.plot(etot)
    plt.legend(["epot", "ekin", "etot"], loc="upper right")
    plt.xlabel("time")
    plt.ylabel("energy")
    plt.show()