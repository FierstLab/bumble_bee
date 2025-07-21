

#### this script is used for the second filter of the methylated sites based on the statistics calculated in the previous code #####
#### this cript uses two input files from the 1st and 2nd scripts
#### the output of this file is saved in a new folder named as "Significant_genes_2sd" in a '*.csv format'
import os as os


path = "/path/"
#f = open(path+"files_ID.dat",'r')           # this file contains the name/id of all the samples

#filename = [line.split() for line in f]
if (not os.path.exists(path+"Methylated_files/Significant_genes_2sd")):
    os.mkdir(path+"Methylated_files/Significant_genes_2sd/")

for i in ['V01341', 'V01344']:
    print(i)
    site_file = i+'_methylated.dat'
    stat_file = i+'_methylated_out.dat'
    if os.path.isfile(path+"Methylated_files/"+site_file):
        f1 = open(path+"Methylated_files/"+site_file+"", 'r')
        f2 = open(path+"Methylated_files/Freq_Num_methylated/"+stat_file+"",'r')
        meth_sites = [line.split() for line in f1]
        stats_sites = [line.split() for line in f2]
        outputfile = i+'_significant_meth_2sd.csv'
        fw = open(path+"Methylated_files/Significant_genes_2sd/"+outputfile+"", 'w')
        for k in stats_sites:
           # print(k)
            musd_num_add = float(k[1]) + 2*(float(k[2]))
            musd_num_sub = float(k[1]) - 2*(float(k[2]))
            musd_freq_add = float(k[3]) + 2*(float(k[4]))
            musd_freq_sub = float(k[3]) - 2*(float(k[4]))
            for j in meth_sites:
                num_meth = (float(j[5])*float(j[6]))/100
                # for l in gff: j[1] == l[0] and int(j[2]) <= int(l[4]) and int(j[2]) >= int(l[3]) and l[1] != 'RefSeq' and
                if j[1] == k[0] and num_meth <= musd_num_add and num_meth >= musd_num_sub and float(j[6]) <=  musd_freq_add and float(j[6]) >= musd_freq_sub:
                    fw.write(str(j[0])+'\t'+str(j[1])+'\t'+str(j[2])+'\t'+str(j[3])+'\t'+str(j[4])+'\t'+str(j[5])+'\t'+str(j[6])+'\n')
                
        f1.close()
        f2.close()
        fw.close()
        print('done')
    else:
        continue
