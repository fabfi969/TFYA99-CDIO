'''this will parse a slurm file'''

import os
import csv

def slurm_to_csv():
    '''this parses the slurm files in data/slurms and creates CSV-files out of them located in data/slurm_results'''

    root_path = (os.getcwd()).split('TFYA99-CDIO')[0] + 'TFYA99-CDIO'
    RES_PATH = f'{root_path}/data/slurm_results'

    if not os.path.exists(RES_PATH):
        os.makedirs(RES_PATH)

    for slurm_name in os.listdir(f'{root_path}/data/slurms'):
        print(slurm_name)

        with open(f'{RES_PATH}/{slurm_name}.csv', mode='w', newline='', encoding='UTF-8') as file:
            writer = csv.writer(file)

            with open(f'{root_path}/data/slurms/{slurm_name}', 'r', encoding='UTF-8') as f:
                lines = f.readlines()

            # These are the categories written to the CSV
            # TODO: ADD CATEGORIES THAT DIFFERENTIATE THE RUNS ON THE NEXT LINE, AKA thickness or material combination or something
            csv_categories = 'Epot,Ekin,T,Etot'
            if len(lines[2].split(',')) > 4:
                csv_categories = csv_categories + ',interface_E'
            writer.writerow((csv_categories).split(','))

            for line in lines:
                if (line[0]).isdigit():
                    csv_file_line = line[:-1]
                elif line[0] == '-':
                    # only write the values when the system has stabilized
                    writer.writerow(csv_file_line.split(','))

if __name__ == '__main__':
    slurm_to_csv()
