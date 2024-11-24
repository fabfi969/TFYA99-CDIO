def writetofile():
    """Save simulation data to file."""
    f = open('output_data.txt', 'w') # Open the target file. Overwrite existing file.
    epot_list, ekin_list, etot_list, temperature_list, pressure_list = ([] for i in range(5))
    epot_list.insert(0, 'epot')
    ekin_list.insert(0, 'ekin')
    etot_list.insert(0, 'etot')
    temperature_list.insert(0, 'temperature')
    pressure_list.insert(0, 'pressure')
    print(epot_list, file=f)
    print(ekin_list, file=f)
    print(etot_list, file=f)
    print(temperature_list, file=f)
    print(pressure_list, file=f)
    f.close()
    print('Simulation data saved to file: ', f.name )