
""" Usage: 
    curve_plot.py <tableau_csv> <nom_rep_output>  
"""
#!/python3/bin/python3
# -*- coding: utf-8 -*-

import os
import docopt
import seaborn as sns
import matplotlib.pyplot as plt
import my_modules.file_repo_func as file_repo_func
from MISTIC_git.curve_rarf.my_modules.file_repo_func import import_csv_to_df
from MISTIC_git.curve_rarf.my_modules.file_repo_func import repo_check

# vérifie si répertoire existe sinon le crée
# retourne le chemin du répertoire

def barplot_pdf(df, nom_rep_output):
    # barplot with seaborn module and save as pdf

    sns.set(style="whitegrid")
    sns.set_context("paper", font_scale=1.5)
    sns.set_palette("colorblind")
    sns.set_style("ticks")
    # plot curves with seaborn module
    # curve per techno for each sampling size
    #g = sns.catplot(x="sampling_size", y="kmers_nb_distinct", hue="techno", data=df,
    #                height=6, kind="bar", palette="muted")  
    # add title
    #plt.title("Nombre de kmers distincts (kmers_nb_distinct) par taille d'échantillon")
    # save the plot as a pdf file
    #plt.savefig(nom_rep_output+"/catplot.pdf")

    # lineplot per techno for each sampling size
    l = sns.lineplot(x="sampling_size", y="kmers_nb_distinct", hue="techno", data=df,
                    palette="muted")
    # add title
    plt.title("Nombre de kmers distincts (kmers_nb_distinct) par taille d'échantillon")
    # save the plot as a pdf file
    plt.savefig(nom_rep_output+"/lineplot.pdf")


if __name__ == '__main__':
    args = docopt.docopt(__doc__)
    tableau_csv = args['<tableau_csv>'] 
    nom_rep_output = args['<nom_rep_output>']
    
    df = import_csv_to_df(tableau_csv)
    df[['techno', 'replicat', 'sampling_size']
       ] = df['bank_uri'].str.split('_', expand=True) 
    df.drop(['bank_uri'], axis=1, inplace=True)
    
    nom_rep_output = repo_check(nom_rep_output)
    barplot_pdf(df, nom_rep_output)
    
