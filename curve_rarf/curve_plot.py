
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


def main():
    df = pd.read_csv(arguments['<tableau_csv>'], sep='\t')
    print(df)


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__)
    main()
