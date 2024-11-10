def plotenergy():
    import matplotlib.pyplot as plt # This gives a warning.
    import ast
    
    f = open("output_data.txt", "r")
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