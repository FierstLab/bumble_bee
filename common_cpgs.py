# this script is to generate the common CpGs among all the samples

import os, glob

path="/path_to_filtered_files/"
common_entries = None
for filename in glob.glob(os.path.join(path, '*.dat')):
	#outfile = os.path.basename(filename).replace('.bedGraph', '.dat') #one can do this from the begGraph files as well
	print(filename)
	with open(filename, 'r') as f:
		entries = set('_'.join(line.split('\t')[1:3]) for line in f)    #the second part is 
	if common_entries is None:
		common_entries = entries
	else:
		common_entries.intersection_update(entries)
	if not common_entries:
		break

with open(path+"common_entries.txt", "w") as output_file:
	for j in common_entries:
		k = j.split('_')
		output_file.write(str(k[0])+'\t'+str(k[1])+'\n')
