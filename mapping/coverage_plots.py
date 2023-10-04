#! bin/python3

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

run1_reads = pd.read_csv("/kwak/hub/25_cbelliardo/MISTIC/Salade_I/mapping_SR_LR_reads/cleaned_run1__vs__hifireads.bam.sorted.coverage", sep="\t", header=None)
run1_assembly = pd.read_csv("/kwak/hub/25_cbelliardo/MISTIC/Salade_I/mapping_SR_LR_assembly/cleaned_run1__vs__hifi_assembly.bam.sorted.coverage",  sep="\t", header=None)


# boxplot of num reads per contig
sns.boxplot(x=run1_reads[2])
plt.show()

print(run1_assembly.head())