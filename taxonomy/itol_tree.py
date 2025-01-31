import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from ete3 import Tree

from scipy import stats

from scipy.stats import zscore
from scipy.spatial.distance import pdist, squareform
from scipy.stats import chi2_contingency

def import_qt_files(directory):
    all_files = [f for f in os.listdir(directory) if f.endswith('.taxo')]
    df_list = []
    
    for file in all_files:
        file_path = os.path.join(directory, file)
        df = pd.read_csv(file_path, sep='\t')  # Assuming the .qt files are in CSV format
        df['source_file'] = file.strip('.taxo')
        df_list.append(df)
    
    combined_df = pd.concat(df_list, ignore_index=True)
    return combined_df

# Example usage
directory = '/kwak/hub/25_cbelliardo/paper_v2/4_MAGs_data'
df = import_qt_files(directory)

df.source_file=df.source_file.str.lstrip('LR_').str.lstrip('SR_')

df_cp = df.copy()   
df_cp.classification=df_cp.classification.str.rstrip('s__').str.rstrip('g__').str.rstrip('f__').str.rstrip('o__').str.rstrip('c__').str.rstrip('p__')

df_cp.classification = df_cp.classification.str.replace('d__','')
df_cp.classification = df_cp.classification.str.replace('p__','')
df_cp.classification = df_cp.classification.str.replace('c__','')
df_cp.classification = df_cp.classification.str.replace('o__','')
df_cp.classification = df_cp.classification.str.replace('f__','')
df_cp.classification = df_cp.classification.str.replace('g__','')
df_cp.classification = df_cp.classification.str.replace('s__','')

df_cp[['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']] = df_cp['classification'].str.split(';', expand= True )

# Construire un arbre
root = Tree()  # Racine de l'arbre
for lineage in df_cp.classification.unique():
    levels = lineage.split(";")
    node = root
    for level in levels:
        if level:  # Si non vide
            child = node&level if node.search_nodes(name=level) else node.add_child(name=level)
            node = child

# Exporter en Newick
newick_str = root.write(format=1)
print("Arbre au format Newick :", newick_str)

# Sauvegarder dans un fichier
with open("arbre_phylogenetique.newick", "w") as f:
    f.write(newick_str)


###

# rename df.source_file array(['sequel_revio_SR', 'illumin', 'sequel_SR', 'sequel_revi', 'revi', 'sequel', 'revio_SR'], dtype=object) into 'illumina', 'sequel', 'sequel_SR', 'revio', 'revio_SR', 'sequel_revio', 'sequel_revio_SR']
df.source_file = df.source_file.replace({
    'illumin': 'Illumina',
    'sequel_revi': 'sequel_revio',
    'revi': 'revio'
})
# Capitalise the first letter
df.source_file = df.source_file.str.capitalize()

df_cp.source_file = df_cp.source_file.replace({
    'illumin': 'Illumina',
    'sequel_revi': 'sequel_revio',
    'revi': 'revio'
})

df_cp.source_file = df_cp.source_file.str.capitalize()

order = ['illumina', 'sequel', 'sequel_SR', 'revio',   'revio_SR', 'sequel_revio', 'sequel_revio_SR']
# capitalise order
order = [x.capitalize() for x in order]
df.source_file = pd.Categorical(df_cp.source_file, order)
df_cp.source_file = pd.Categorical(df_cp.source_file, order)
dfg = df.groupby(['source_file', 'classification']).size().reset_index(name='count')

###
dfg = df.groupby(['source_file', 'classification']).size().reset_index(name='count')
dfg = dfg.reset_index().pivot(index='classification', columns='source_file', values='count').fillna(0)

df_cpg = df_cp.groupby(['source_file', 'classification']).size().reset_index(name='count')
df_cpg = df_cpg.reset_index().pivot(index='classification', columns='source_file', values='count').fillna(0)

df_cpg.reset_index(inplace=True)
df_cpg.columns.name = None 
df_cpg.to_csv('itol_dataset.csv', index=False,sep=',')
###

# divide all data of df_cpg by 12 and multiply by 5, keeping the classification name
df_cpg.iloc[:, 1:] = round(df_cpg.iloc[:, 1:] / 12 * 5)
df_cpg.to_csv('itol_dataset_shape.csv', index=False, sep=',')

###
def generate_itol_annotation(df, output_file):
    """
    Génère un fichier d'annotation iTOL au format DATASET_MULTIBAR pour des barplots basés sur un DataFrame.
    
    :param df: DataFrame contenant les colonnes ['source_file', 'classification', 'count'].
    :param output_file: Chemin du fichier de sortie.
    """
    # Obtenir les champs pour le dataset
    source_files = df['source_file'].unique()
    classifications = df['classification'].unique()
    
    # Générer les couleurs pour chaque source_file (une couleur par source_file)
    color_map = {
        source_files[i]: f"#{i:02x}{(i*50)%256:02x}{(255-i*10)%256:02x}" 
        for i in range(len(source_files))
    }
    
    with open(output_file, 'w') as file:
        # Entête du fichier iTOL
        file.write("DATASET_MULTIBAR\n")
        file.write("#=================================================================#\n")
        file.write("#                    MANDATORY SETTINGS                           #\n")
        file.write("#=================================================================#\n")
        file.write("SEPARATOR TAB\n")
        file.write("DATASET_LABEL\tBarplot by Source File\n")
        file.write("COLOR\t#ff0000\n")  # Couleur principale
        file.write(f"FIELD_COLORS\t{','.join(color_map.values())}\n")
        file.write(f"FIELD_LABELS\t{','.join(source_files)}\n")
        file.write("#=================================================================#\n")
        file.write("#       Actual data follows after the \"DATA\" keyword              #\n")
        file.write("#=================================================================#\n")
        file.write("DATA\n")
        
        # Calcul des valeurs par classification
        for classification in classifications:
            # Récupérer les valeurs pour chaque source_file
            classification = classification.split(';')
            classification.reverse()
            classification = [i for i in classification if i != ''][0] 
            values = []
            for source_file in source_files:
                value = df[
                    (df['classification'] == classification) & 
                    (df['source_file'] == source_file)
                ]['count'].sum()  # Total des occurrences
                values.append(value)
            # Écriture dans le fichier
            file.write(f"{classification}\t" + '\t'.join(map(str, values)) + "\n")

# Vérifier la structure et regrouper par source_file et classification
df_grouped = df_cp.groupby(['source_file', 'classification']).size().reset_index(name='count')

# Générer le fichier d'annotation iTOL
output_annotation_file = "itol_annotation_multibar.txt"
generate_itol_annotation(df_grouped, output_annotation_file)

print(f"Fichier d'annotation iTOL généré : {output_annotation_file}")

###
df_grouped = df_cp.groupby(['source_file', 'classification']).size().reset_index(name='count')
df.groupby(['source_file', 'classification']).size().reset_index(name='count')





