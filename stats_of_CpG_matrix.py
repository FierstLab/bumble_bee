# this script calculates the statistics of the CpGs across all the samples for each environmental categories
import numpy as np
import csv
path ="/path_to_CpG_matrix_correct.csv/"
groups = ['High_altitude', 'Low_altitude', 'TCtrl', 'TMax', 'TMin']
for grp in groups:
    print(grp)
    with open(path+str(grp)+"/CpG_matrix_correct.csv",'r') as f, open(path+str(grp)+"/CpG_matrix_correct_stats.csv", 'w') as fw:
        lines = f.readlines()
        writer = csv.writer(fw)
        headline = lines[0].strip()+","+"mean"+","+"stdev"+","+"var"
        writer.writerow(headline.split(","))
        for line in lines[1:]:
            line = line.strip().split(',')
            #print(line)
            new_line = list(map(int, line[2:]))
            # new_line = [i/100 for i in new_line]
            # print(new_line)
            mean = np.mean(new_line)
            stdev = np.std(new_line)
            var = np.var(new_line)
            line.append(str(mean))
            line.append(str(stdev))
            line.append(str(var)]
            writer.writerow(line)
