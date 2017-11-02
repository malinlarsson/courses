#! /usr/bin/env python

import sys, re, math, random
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

if len(sys.argv)<3:
    print "Usage: %s <vcffile> <outfile> \n\n<vcffile> = Input vcf\n<outfile> = root name of output file\n\nCreates a pdf file with plots of alternative allele frequency (based on read counts) distributions for samples in a VCF file.\n\n" %sys.argv[0]
    sys.exit(0)


vcffile = sys.argv[1]
out = sys.argv[2]

#Extract sample names from VCF file
sample_name=[]
for line in open(vcffile, 'r'):
    line=line.strip()
    if line.startswith("#CHROM"):
        info=line.split("\t")
        for col in range(9, len(info)):
            sample_name.append(info[col])
        break

#extract allele frequencies for every sample and SNV in VCF file
allele_freq=np.zeros(len(sample_name))
for snp in open(vcffile, 'r'):
    snp=snp.strip()
    if not snp.startswith("#"):
        snp_info=snp.split("\t")
        this_site_freqs=np.zeros(len(sample_name))
        for col in range(9, len(snp_info)):
            if  snp_info[col] == ".":
                this_site_freqs[col-9]=0
            else:
                genotype_info=snp_info[col].split(":")
                #Format of snp_info is GT:BQ:DP:FA:SS:AD where FA=Alt allele frequency based on read counts
                this_site_freqs[col-9]=float(genotype_info[3])
    
        #include this_site_freqs in allele_freq matrix
        allele_freq=np.vstack((allele_freq, this_site_freqs))


#Create plots and print to PDF file
pp = PdfPages(out+'.pdf')
#Boxplot
x=range(1, len(sample_name)+1)
plt.boxplot(allele_freq)
plt.xticks(x, sample_name, rotation=45)
plt.title('Alt allele frequency distributions in '+vcffile+'\n')
plt.ylabel('Alt allele frequency based on read depths')
plt.margins(0.1)
plt.subplots_adjust(bottom=0.3)
plt.savefig(pp, format='pdf')
plt.clf()

#Histogram
n, bins,patches=plt.hist(allele_freq, label=sample_name)
plt.legend()
plt.xlabel('Alt allele freq based on read depths')
plt.ylabel('Counts (SNVs)')
plt.title('Alt allele frequency distributions in '+vcffile+'\n')
plt.savefig(pp, format='pdf')
#plt.show()
pp.close()

print 'printed results to '+out+'.pdf'
