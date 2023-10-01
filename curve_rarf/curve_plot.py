
""" Usage: 
    curve_plot.py <tableau_csv> <nom_rep_output>  
"""
#!/python3/bin/python3
# -*- coding: utf-8 -*-

import docopt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def import csv_to_df(csv_file):
    df = pd.read_csv(csv_file, sep='\t')
    return df

def main():
    df = import_csv_to_df(arguments['<tableau_csv>'])
    df['techno', 'replicat', 'sampling_size'] = df['bank_uri'].str.split('_', expand=True)
    print(df)

if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)
    main()
