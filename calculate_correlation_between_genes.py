# to calculate the correlation between each gene across all the samples of each group
# we used parallel processing for this calculation
# we used this code with a HPC code
# the output file contains the gene1, gene2 and correlation value between them

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import time
from  joblib import Parallel, delayed
import os 

num_cores = os.cpu_count()
groups = ['High_altitude','TMax','Low_altitude']

def compute_correlations(i):
    results = []
    istat = data[i]
    key_i = keys[i]
    for j in range(i+1, n):
        jstat = data[j]
        key_j = keys[j]

        cor, pval = spearmanr(istat, jstat)
        if pval < 0.05:
            results.append(f"{key_i}\t{key_j}\t{cor}")
    return results

for grp in groups:
    print(f"Processing group: {grp}", flush=True)       #
    path = "/grp/"
    df = pd.read_csv(path + "CpG_gene_matrix_correct_filtered.csv", delimiter='\t')
    data = df.iloc[:, 1:].values
    keys = df.iloc[:, :1].astype(str).agg('_'.join, axis=1).values
    results = []
    print("starting the pairwise calculation", flush=True)
    n = len(data)
    results = Parallel(n_jobs=num_cores)(delayed(compute_correlations)(i) for i in range(n))
    flattened_results = [ele for elements in results for ele in elements]

    with open(path + "gene_correlation_correct.csv", 'w') as fw:
        batch_size = 500
        batch = []
        for i in range(0, len(flattened_results), batch_size):
            fw.write("\n".join(flattened_results[i:i + batch_size])+"\n")
