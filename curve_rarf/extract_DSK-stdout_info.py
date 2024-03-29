"""Usage:
    extract_DSK-stdout_info.py <nom_rep_input> <output_csv>

Arguments:
    nom_rep_input     Le nom du répertoire à traiter
    output_csv  Le nom du fichier de sortie

Options:
    -h --help  Afficher ce message d'aide
    --json_file=<json_file>  Chemin vers le fichier JSON en entrée [default: keys_to_extract.json]
"""

from docopt import docopt
import csv
import json
import os

# liste file

# liste les fichiers .txt dans un repertoire


def list_text_files(repertoire):
    fichiers_texte = []
    # parcours de l'arborescence
    for dossier, sous_dossiers, fichiers in os.walk(repertoire):
        for fichier in fichiers:  # parcours des fichiers
            if fichier.endswith('.txt'):  # si le fichier est un fichier texte
                # on l'ajoute à la liste
                fichiers_texte.append(os.path.join(dossier, fichier))
    return fichiers_texte


# Fonction pour extraire les informations d'un fichier txt
# chaque ligne est stocké dans un dictionnaire
# les clés sont les noms des colonnes et les valeurs sont les valeurs de chaque ligne

def extract_info_from_txt(file_paths, keys_to_extract):
    info = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            info_line = {}
            for line in file:
                line = line.strip()
                if line:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in keys_to_extract:
                            if key == 'bank_uri':
                                value = '_'.join(file_path.replace('.txt', '').split(
                                    '/') if '/' in file_path.replace('.txt', '') else file_path.replace('.txt', '').split('\\')[-1].split('_'))
                                # parse_filename(file_path)

                            info_line[key] = value
            info.append(info_line)
    return info


def parse_filename(input_string):
    # Extraire differentiellement les parties du chemin selon les séparateurs
    parties = input_string.split(
        '/') if '/' in input_string else input_string.split('\\')[-1].split('_')

    # Initialiser les éléments du nouveau nom de fichier
    nouveau_nom_parts = []

    # Parcourir les parties pour extraire les informations requises
   # techno = parties[0]
   # subsampling = parties[1]
   # sampsize = parties[-1].replace('.fastq', '').replace(
   #     '.fasta', '').replace('.gzr', '')
   # pair = parties[2]

    for partie in parties:
        tech = ''
        if (tech == '') and (('illumina' in partie) or ('hifi' in partie)):
            parties = partie.split('_')
            tech = parties[0]
            # replace fasta or fastq
            sampsize = parties[-1].replace('.fastq',
                                           '').replace('.fasta', '').replace('.gzr', '')
        elif 'subsampling' in partie:
            subsampling = partie.split('_')[0]
    # Construire le nouveau nom de fichier en joignant les parties nécessaires
    nouveau_nom = techno+'_'+subsampling+'_'+sampsize
    print(nouveau_nom)
    return nouveau_nom


# fonction qui écrit un liste de dict dans un fichier csv
# les clés sont les noms des colonnes et les valeurs sont les valeurs de chaque lignes
# chaque élément de la liste est un ligne du fichier csv
# la première ligne et la liste de clés
def parse_listOFdico_to_csv(list_dict, output):
    with open(output, 'w', newline='') as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=list_dict[0].keys(), delimiter='\t')
        writer.writeheader()
        for dico in list_dict:
            writer.writerow(dico)


def parse_dico_toCSV(dico_info, keys_to_extract, output_file):

    if all(key in dico_info for key in keys_to_extract):
        with open(output_file, 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys_to_extract)
            writer.writerow({key: dico_info[key] for key in keys_to_extract})


if __name__ == '__main__':
    arguments = docopt(__doc__)
    nom_rep_input = arguments['<nom_rep_input>']
    output_csv = arguments['<output_csv>']

    with open('keys_to_extract.json', 'r') as f:
        keys_to_extract = json.load(f)['keys_to_extract']

    txt_liste = list_text_files(nom_rep_input)
    dico_info = extract_info_from_txt(txt_liste, keys_to_extract)

    parse_listOFdico_to_csv(dico_info, output_csv)

    print(dico_info)
