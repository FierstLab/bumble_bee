# cpg to gene matrix, we calculated an average value for each gene such as sum(CpGs) for a given sample by number of times a gene appears in that sample.

import collections
import pandas as pd


##this code is calculating the average of cpgs present in each gene
groups = ['High_altitude', 'Low_altitude', 'TMax', 'TMin', 'TCtrl']
path = "/"
for grp in groups:
    df = pd.read_csv(path+str(grp)+"/CpG_matrix_correct_stats_filtered.csv", delimiter=',', header=0)
    gene_sites = collections.defaultdict(lambda: [0] * (df.shape[1] - 5))
    gene_counts = collections.defaultdict(int)
    for _, row in df.iterrows():
        gene = row[0] #gene name
        sample_values = row[2:-3].tolist() #samples
        gene_counts[gene] += 1
        gene_sites[gene] = [gene_sites[gene][i] + val for i, val in enumerate(sample_values)]

    gene_avg_sites = {
        gene: [val / gene_counts[gene] for val in values]
        for gene, values in gene_sites.items()
    }
    output_df = pd.DataFrame.from_dict(gene_avg_sites, orient='index', columns=[df.columns[2:-3]])
    output_df.insert(0, 'Gene', output_df.index)  # adding gene column back
    output_df.reset_index(drop=True, inplace=True)
    output_df.to_csv(path+str(grp)+"/CpG_gene_matrix_correct_filtered.csv", sep='\t', index=False)
