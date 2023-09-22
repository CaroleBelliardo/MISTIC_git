import os
import csv

# Fonction pour extraire les informations d'un fichier txt
def extract_info_from_txt(file_path):
    info = {}
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    current_section = None
    for line in lines:
        line = line.strip()
        if line:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                info[key] = value
            else:
                current_section = line.strip()
    
    return info

# Fonction pour parcourir les répertoires et extraire les informations
def process_directories(input_list_file, output_csv_file):
    with open(input_list_file, 'r') as list_file:
        directories = list_file.read().splitlines()

    with open(output_csv_file, 'w', newline='') as csv_file:
        fieldnames = ['bank_uri', 'kmers_nb_distinct', 'kmers_nb_weak', 'kmers_percent_weak', 'kmers_nb_solid']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for directory in directories:
            for root, _, files in os.walk(directory):
                for file in files:
                    if file.endswith('.txt'):
                        file_path = os.path.join(root, file)
                        info = extract_info_from_txt(file_path)
                        if 'bank_uri' in info and 'kmers_nb_distinct' in info and 'kmers_nb_weak' in info and 'kmers_percent_weak' in info and 'kmers_nb_solid' in info:
                            writer.writerow({
                                'bank_uri': info['bank_uri'],
                                'kmers_nb_distinct': info['kmers_nb_distinct'],
                                'kmers_nb_weak': info['kmers_nb_weak'],
                                'kmers_percent_weak': info['kmers_percent_weak'],
                                'kmers_nb_solid': info['kmers_nb_solid']
                            })

# Appel de la fonction pour traiter les répertoires
process_directories('input_list_repo.txt', 'output.csv'
