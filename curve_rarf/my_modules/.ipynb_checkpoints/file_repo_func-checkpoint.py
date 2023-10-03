import pandas as pd
import os


def import_csv_to_df(csv_file):
    df = pd.read_csv(csv_file, sep='\t')
    return df


def import_dskTXTparse_to_df(csv_file):
    df = import_csv_to_df(csv_file)
    df[['techno', 'replicat', 'sampling_size']
        ] = df['bank_uri'].str.split('_', expand=True) 
    df.drop(['bank_uri'], axis=1, inplace=True)
    return df


def repo_check(nom_rep_output):
    if not os.path.exists(nom_rep_output):
        os.makedirs(nom_rep_output)
    return nom_rep_output
