# this script is used to extract only those CpGs which are find in the exon regions using a .bed file
# this is customized script for the specific bed files and its format. Change accordingly!


from collections import defaultdict
import os
import glob

gff_dict = defaultdict(list)

with open("/path_to/Bvos_exon.bed", 'r') as fgff:
	for line in fgff:
		parts = line.strip().split('\t')
		chrom = parts[0]
		start, end = int(parts[1]), int(parts[2])
		metadata = parts[9]
		gff_dict[chrom].append((start, end, metadata))
end1 = time.time()
print(end1-strt)
strt1 = time.time()
path = "/path_to_bedgraph_files/"

for filename in glob.glob(os.path.join(path, '*.bedGraph')):
	outfile = os.path.basename(filename).replace('.bedGraph', '.dat')
	with open(filename, 'r') as f, open(path+'MethylExons/'+outfile, 'w') as fw:
		next(f)
		for entry in f:
			val_parts = entry.strip().split('\t')
			chrom, pos = val_parts[0], int(val_parts[2])
			if chrom in gff_dict:
				for start, end, metadata in gff_dict[chrom]:
					metadata1 = metadata.split(';')
					if start <= pos <= end:
						if 'Dbxref=GeneID' in metadata1[2] and 'Genbank:' not in metadata1[2]:
							gene_id = metadata1[2].lstrip('Dbxref=GeneID:')
						elif 'Dbxref=GeneID' in metadata1[2] and 'Genbank:' in metadata1[2]:
							gene_id = metadata1[2].split(',')[0].lstrip('Dbxref=GeneID:')
						output_line = val_parts[:]
						output_line.insert(1, gene_id)
						fw.write('\t'.join(map(str, output_line))+'\n')
						break
end3=time.time()
print(end3-strt1)
