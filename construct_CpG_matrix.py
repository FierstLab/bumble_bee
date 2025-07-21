# this script is to create a matrix of samples and common CpGs with the methylation percentage values (5th column of BedGraph file) for each CpG 
# rows are genes and columns are samples

import glob, os
import csv


groups = ['High_altitude', 'Low_altitude', 'TMin', 'TMax', 'TCtrl']
path2 = "/path_to_common_entries_file/"

#print(samples)
for grps in groups:
    path1 = "/methylexons/"+str(grps)+"/"           # this contains the files with CpGs present in exons created from the extract_exon_cpgs.py
    samples = [f for f in os.listdir(path1) if f.endswith(".dat")]
    with open(path2+"common_entries.txt", "r") as fc:
        reader1 = csv.reader(fc, delimiter="\t")  
        main_keys = [tuple(row[:2]) for row in reader1]  
#print(main_keys)
    result_dict = {key: [""] * len(samples) for key in main_keys} 


    for file_index, file in enumerate(samples):
        file_path = os.path.join(path1, file)
        print(file_path)
        with open(file_path, "r") as fs:
            reader2 = csv.reader(fs, delimiter='\t')
            #print([roww[1:5] for roww in reader2])
            file_data = {tuple(row1[1:3]): row1[4] for row1 in reader2}    # 1, 2, 3 and 4 are gene name, strt position, end position and methylation percentage, respectively.
            #print("filedata:", file_data)
            for key in main_keys:
                #print(key)
                if key in file_data:
#                print(file_data[key])
                    result_dict[key][file_index] = file_data[key]
    #print(result_dict.items())
    output_file = os.path.join(path1, "CpG_matrix_correct.csv")
    with open(output_file, "w", newline="") as fw:
        writer = csv.writer(fw)
        writer.writerow(["Gene", "CpG_locus"] + samples)
        for (key1,key2), values in result_dict.items():
            #print([key1, key2], values)
            writer.writerow([key1, key2] + values)

    print(f"Matrix saved to {output_file}")
