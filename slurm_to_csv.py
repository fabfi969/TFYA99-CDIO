'''this will parse a slurm file'''

import os
import csv

csv_categories = ['Epot,Ekin,T,Etot']

RES_PATH = 'data/slurm_results'
if not os.path.exists(RES_PATH):
    os.makedirs(RES_PATH)

for slurm_name in os.listdir('data/slurms'):
    print(slurm_name)

    if not os.path.exists(f'{RES_PATH}/{slurm_name}'):
        os.makedirs(f'{RES_PATH}/{slurm_name}')

    with open(f'data/slurms/{slurm_name}', 'r', encoding='UTF-8') as f:
        lines = f.readlines()

    SIMUL_NR = 1
    csv_file_lines = csv_categories[:]
    for line in lines:

        if (line[0]).isdigit():
            csv_file_lines.append(line[:-1])

        elif line[0] == '-':

            with open(f'{RES_PATH}/{slurm_name}/simulation_{SIMUL_NR}.csv',
                        mode='w', newline='', encoding='UTF-8') as file:
                writer = csv.writer(file)
                for line in csv_file_lines:
                    writer.writerow(line.split(','))
            SIMUL_NR += 1
            csv_file_lines = csv_categories[:]
