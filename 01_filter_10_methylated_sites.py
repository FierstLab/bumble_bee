
### this script filters the sites based on the given threshold of methylation
### the output of this script is saved in the folder Methylated_files as samplename_methylated.dat
import matplotlib.pyplot as plt
import os
import glob



path = '/path/with/methylkit_files/'          # this folder contains the methylkit files (you can edit as per your folder names)
for filename in glob.glob(os.path.join(path, '*.methylKit')):
	with open(os.path.join(os.getcwd(), filename), 'r') as f: # these files contain 7 colums. Columns 6 and 7 are freqC and freqT
		val = [line.split() for line in f]
		print(filename.strip(path))
		coverage = []
		freqT = []
		freqC = []
		thresh = 10.0   # set threshold
		wfilename = filename.strip(path).rstrip('_methyldackel_CpG.methylK')+str('_methylated.dat')
		fw = open(path+'Methylated_files/'+wfilename,'w')
		for i in val[1:]:
			if float(i[5]) > thresh:            # taking only those sites which are more than 10% methylated (column freqC)
				fw.write(str(i[0])+'\t'+str(i[1])+'\t'+str(i[2])+'\t'+str(i[3])+'\t'+str(i[4])+'\t'+str(i[5])+'\t'+str(i[6])+'\n')
				coverage.append(int(i[4]))
				freqC.append(float(i[5]))
				freqT.append(float(i[6]))
		fw.close()
	f.close()



### this part of the script is used to plot the histogram of the coverage or frequency of T or C for a given sample   ########


# fn = open('/home/user/folder/Methylated_files/samplename_methylated.dat','r')
# val = [line.split() for line in fn]
# freqC = []
# for i in val:
# 	freqC.append(float(i[5]))
#
# plt.hist(freqC)
# plt.show()


#plt.hist(coverage)
#plt.show()
#plt.hist(freqC)
#plt.ylim(0, 10000)
#plt.ylim(0,2500)
# plt.hist(freqC)
#plt.savefig("/home/user/folder/temp/histT.png")
#plt.close()

