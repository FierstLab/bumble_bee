
### this script is used to deduce the statistics of the methylated sites ####
### this script takes the input from the output of first script
### the output of this scipt is saved in the same folder with addition of '_out' in the sample name



import os, glob
from collections import Counter as cc
import statistics as stats
import matplotlib.pyplot as plt
import numpy as np
plt.interactive(False)



grp = ['case']   #if you have more than one set of samples you can rename this according to your sample names
for group in grp:
    path = '/path/Methylated_files/'
    for filename in glob.glob(os.path.join(path, '*.dat')):
        output = os.path.basename(filename).replace('.dat', '_out.dat')
        fw = open(path+'/Freq_Num_methylated/'+output,'w')
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            cpg_sites = {}
            val = [line.split() for line in f]
            genes = [i[1] for i in val] 
        genes_list = [key[0] for key in cc(genes).items()]               #collecting the total genes for all samples here
        print(len(genes_list))
        for i in genes_list:
            numC = []
            freqC = []
            for j in val:
                if i == j[1]:
                    num_meth = (float(j[4])*float(j[5]))/100
                    numC.append(num_meth)
                    freqC.append(float(j[5]))
            if len(numC) > 1:
                numC_mean = stats.mean(numC)
                numC_stdev = stats.stdev(numC)
                freqC_mean = stats.mean(freqC)
                freqC_stdev = stats.stdev(freqC)
            else:
                numC_mean = numC[0]
                numC_stdev = 0
                freqC_mean = freqC[0]
                freqC_stdev = 0
            
            q9_num = np.quantile(numC, 0.99)
            q9_freq = np.quantile(freqC, 0.95)
            fw.write(str(i) + '\t' + str(numC_mean) + '\t' + str(numC_stdev) + '\t' + str(freqC_mean) + '\t' + str(
                freqC_stdev) +'\t' + str(q9_num) +'\t' + str(q9_freq) + '\n')


#### this part is plotting the frequency and number of the filtered methylated sites ######
            
            # fig, ax = plt.subplots(1,1)
            # data = [numC, freqC]
            # ax = fig.add_axes([0, 0, 1, 1])
            # ax.set_xticks([y for y in range(len(genes_list))], labels=genes_list)
            # ax.set_xlabel(['numC', 'freqC'])
            # ax.set_ylabel('methylation values')
            # ax.set_yticks()
            # ax.get_xaxis().tick_bottom()
            # ax.get_yaxis().tick_left()
            # bp = ax.boxplot(data)#, patch_artist=True, notch='False', vert=1)
            # colors = ['blue', 'red']
            # for patch, color in zip(bp['boxes'], colors):
            #     patch.set_facecolor(color)
            #
            # ax.set_title('Number and frequency of methylated sites')
            # plt.show()
            # imagename = os.path.basename(filename).replace('.dat', '.png')
            # plt.savefig('/home/user/folder/Methylated_files/Freq_Num_methylated/' + imagename)
        fw.close()





    # print(cpg_sites)
