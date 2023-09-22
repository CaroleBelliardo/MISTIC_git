"""Usage:
    extract_DSK-stdout_info.py <nom_rep_input> <output.txt>

Arguments:
    nom_rep_input     Le nom du répertoire à traiter
    output.txt  Le nom du fichier de sortie

Options:
    -h --help  Afficher ce message d'aide
    --json_file=<json_file>  Chemin vers le fichier JSON en entrée [default: keys_to_extract.json]
"""

from docopt import docopt
import csv
import json
import os

# liste file


def list_text_files(repertoire):
    fichiers_texte = []
    for dossier, sous_dossiers, fichiers in os.walk(repertoire):
        for fichier in fichiers:
            if fichier.endswith('.txt'):
                fichiers_texte.append(os.path.join(dossier, fichier))
    return fichiers_texte


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
                if key == 'bank_uri':
                    value = parse_filename(value)
                info[key] = value
            else:
                current_section = line.strip()
    return info


def extract_info_from_txt_list(txt_liste):
    dico_result = {}
    for txt in txt_liste:
        dico_info = extract_info_from_txt(txt)
        dico_result.update(dico_info)
        print('______________________________')
        print(len(dico_result), len(dico_info))
    return dico_result


def parse_filename(input_string):
    # Séparer le chemin en répertoires et le nom de fichier
    chemin, nom_fichier = os.path.split(input_string)

    # Extraire les parties du nom de fichier
    parties = nom_fichier.split('/')

    # Initialiser les éléments du nouveau nom de fichier
    nouveau_nom_parts = []

    # Parcourir les parties pour extraire les informations requises
    for partie in parties:
        if 'illumina' in partie:
            nouveau_nom_parts.append(partie)
        elif 'hifi' in partie:
            nouveau_nom_parts.append(partie)
        elif partie.startswith('subsampling'):
            subsampling_parts = partie.split('_')
            if len(subsampling_parts) >= 2:
                nouveau_nom_parts.append(subsampling_parts[0])
                version_part = subsampling_parts[1].split(
                    '.')[0]  # Retirer l'extension le cas échéant
                nouveau_nom_parts.append(version_part)

    # Construire le nouveau nom de fichier en joignant les parties nécessaires
    nouveau_nom = '_'.join(nouveau_nom_parts)

    # Retirer les extensions ".fasta" et ".fastq" en fin de fichier s'ils existent
    nouveau_nom = nouveau_nom.replace('.fasta', '').replace('.fastq', '')

    return nouveau_nom


def parse_dico_toCSV(dico_info, keys_to_extract, output_file):

    if all(key in dico_info for key in keys_to_extract):
        with open(output_file, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys_to_extract)
            writer.writerow({key: dico_info[key] for key in keys_to_extract})


if __name__ == '__main__':
    arguments = docopt(__doc__)
    nom_rep_input = arguments['<nom_rep_input>']
    output = arguments['<output.txt>']

    with open('keys_to_extract.json', 'r') as f:
        keys_to_extract = json.load(f)['keys_to_extract']

    txt_liste = list_text_files(nom_rep_input)
    dico_info = extract_info_from_txt_list(txt_liste)
    parse_dico_toCSV(dico_info, keys_to_extract, output)

    # bug == parcours des fichiers txt et ecrase les info -> ecrire a la voler ou faire une meta structure
    # ajouter l'entete du fichier csv
