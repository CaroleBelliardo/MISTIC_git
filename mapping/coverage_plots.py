#! bin/python3

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import samtools_func as sf
import bedtools_func as bf



run1_reads = pd.read_csv("/kwak/hub/25_cbelliardo/MISTIC/Salade_I/mapping_SR_LR_readscleaned_run1__vs__hifireads.bam.sorted.coverage", sep="\t", header=None)