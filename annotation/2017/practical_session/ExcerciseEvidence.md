---
layout: default
title:  'Exercise Evidence'
---

# Preparing evidence data for annotation

This exercise is meant to get you acquainted with the type of data you would normally encounter in an annotation project. You will get an idea of where to download protein sequences, and also try out some programs that are often used. We will for all exercises use data for the fruit fly, Drosophila melanogaster, as that is one of the currently best annotated organisms and there is plenty of high quality data available.

## 1. Obtaining data

<u>**Swissprot:**</u> Uniprot is an excellent source for high quality protein sequences. The main site can be found at [http://www.uniprot.org](http://www.uniprot.org). This is also the place to find Swissprot, a collection of manually curated non-redundant proteins that cover a wide range of organisms while still being manageable in size.

**_Exercise 1_ - Swissprot:**  
Navigate the Uniprot site to find the download location for Swissprot in fasta-format. You do not need to download the file, just find it. In what way does Swissprot differ from Uniref (another excellent source of proteins, also available at the same site)?

<u>**Uniprot:**</u> Even with Swissprot available, you also often want to include protein sequences from organisms closely related to your study organism. An approach we often use is to concatenate Swissprot with a few protein fasta-files from closely related organisms and use this in our annotation pipeline.

**_Exercise 2_ - Uniprot:**  
Use Uniprot to find (not download) all protein sequences for all the complete genomes in the family Drosophilidae. How many complete genomes in Drosophilidae do you find?

<u>**Refseq:**</u> Refseq is another good place to find non-redundant protein sequences to use in your project. The sequences are to some extent sorted by organismal group, but only to very large and inclusive groups. The best way to download large datasets from refseq is using their ftp-server at [ftp://ftp.ncbi.nlm.nih.gov/refseq/](ftp://ftp.ncbi.nlm.nih.gov/refseq/).

**_Exercise 3_ - Refseq:**  
Navigate the Refseq ftp site to find the invertebrate collection of protein sequences. You do not need to download the sequences, just find them. The files are mixed with other types of data, which files include the protein sequences?

<u>**Ensembl:**</u> The European Ensembl project makes data available for a number of genome projects, in particular vertebrate animals, through their excellent webinterface. This is a good place to find annotations for model organisms as well as download protein sequences and other types of data. They also supply the Biomart interface, which is excellent if you want to download data for a specific region, a specific gene, or create easily parsable file with gene names etc.

**_Exercise 4_ - Ensembl Biomart:**  
Go to Biomart at [http://www.ensembl.org/biomart/martview](http://www.ensembl.org/biomart/martview) and use it to download all protein sequences for chromosome 4 in Drosophila melanogaster. Once you have downloaded the file, use some command line magic to figure out how many sequences are included in the file. Please ask the teachers if you are having problems here.

## 2. Running an ab initio gene finder

<u>**Setup:**</u> For this exercise you need to be logged in to Uppmax. Follow the [UPPMAX login instructions](LoginInstructions).

*cd annotation_course*

*mkdir practical2* 

*cd practical2*  


We have made a genome browser called Webapollo available for you on the address [http://annotation-prod.scilifelab.se:8080/NBIS_gp1/](http://annotation-prod.scilifelab.se:8080/NBIS_gp1/)  called drosophila\_melanogaster\_course.
This browser can already has a number of tracks preloaded for you, but you can also load data you have generated yourself using the ‘file” menu and then ‘open’ and ‘local files’. First time you go there you need to log in using the email adress provided to register the course and your last name as password (lower case and if more than one last name separated by _ eg: lastname1_lastname2)(if you already have access to our webapollo please use the password that have been previously provided to you).

<u>**Ab initio gene finders:**</u> These methods have been around for a very long time, and there are many different programs to try. We will in this exercise focus on the gene finder Augustus. These gene finders use likelihoods to find the most likely genes in the genome. They are aware of start and stop codons and splice sites, and will only try to predict genes that follow these rules. The most important factor here is that the gene finder needs to be trained on the organism you are running the program on, otherwise the probabilities for introns, exons, etc. will not be correct. Luckily, these training files are available for Drosophila.

**_Exercise 5_ - Augustus:**

First you need to write the libraries path you will need in .bash_profile to perform the following analyses. 

*/home/__login__/annotation_course/course_material/lib/install_perllib_missing.sh*

*source ~/.bash\_profile*

Second load the needed modules using:  
_module load bioinfo-tools_  
_module load augustus_

Run Augustus on your genome file using:  
*augustus -\-species=fly /home/__login__/annotation\_course/course\_material/data/dmel/chromosome\_4/chromosome/4.fa > augustus\_drosophila.gtf*

Take a look at the result file using ‘less augustus\_drosophila.gtf’. What kinds of features have been annotated? Does it tell you anything about UTRs?

The gff-format of Augustus is non-standard (looks like gtf) so to view it in a genome browser you need to convert it. You can do this using genometools which is available on Uppmax.

Do this to convert your Augustus-file:

_module load perl_  
_module load perl_modules_  
_module load BioPerl/1.6.924_Perl5.18.4_  

*~/annotation\_course/course\_material/git/GAAS/annotation/Tools/Converter/gxf_to_gff3.pl -g augustus_drosophila.gtf -o augustus_drosophila.gff3 --gff_version 2*

Transfer the augustus\_drosophila.gff3 to your computer using scp:    
*scp __login__@milou.uppmax.uu.se:/home/__login__/annotation\_course/practical2/augustus\_drosophila.gff3 .*  

Load the file in [Webapollo](http://annotation-prod.scilifelab.se:8080/NBIS_gp1/). [Here find the WebApollo instruction](UsingWebapollo)
<br/>Load the Ensembl annotation available in  ~/annotation\_course/course\_material/data/dmel/chromosome\_4/annotation
How does the Augustus annotation compare with the Ensembl annotation? Are they identical?

**_Exercise 6 -_ Augustus with yeast models:**  
Run augustus on the same genome file but using settings for yeast instead (change species to Saccharomyces).

Load this result file into Webapollo and compare with your earlier results. Can you based on this draw any conclusions about how a typical yeast gene differs from a typical Drosophila gene?

## 3. Checking the gene space of your assembly.

Cegma is a program that includes sequences of 248 core proteins. These proteins are conserved and should be present in all eukaryotes. Cegma will try to align these proteins to your genomic sequence and report to you the number of proteins that are successfully aligned. This percentage can be used as a measure of how complete your assembly is. 

BUSCO2 provides measures for quantitative assessment of genome assembly, gene set, and transcriptome completeness. Genes that make up the BUSCO2 sets for each major lineage are selected from orthologous groups with genes present as single-copy orthologs in at least 90% of the species. It includes 1,066 genes for arthropods, 2,586 for vertebrates, 978 for metazoans, 290 for fungi, 303 for eukaryotes and for bacteria 40 universal marker genes.

***Note:*** In a real-world scenario, this step should come first and foremost. Indeed, if the result is under your expectation you might be required to enhance your assembly before to go further. As running Cegma is taking a while, you should also open a new tab and launch BUSCO. If this is too long to run, you can find the results of Cegma in ~/annotation\_course/course\_material/data/dmel/chromosome\_4/.  


**_Exercise 7_ - Cegma -:**  

Here you will try Cegma on Chromosome 4 of Drosophila melanogaster.First, load cegma by typing 'module load cegma'. The problem is that the file ‘4.fa’ has fasta-headers that are only numbers, and Cegma won’t accept that. Can you figure out how to change the fasta header to ‘chr4’ rather than just ‘4’ using the linux command sed? Ask the teachers if you are having problems, or cheat by using the already parsed file 4_parsed.fa. :)

_module load cegma_   
*cegma -g /home/__login__/annotation\_course/course\_material/data/dmel/chromosome\_4/chromosome/4\_parsed.fa -T 8*

When done, check the output.completeness_report. How many proteins are reported as complete? Does this sound reasonable?

**_Exercise 8_ - BUSCO -:**

You will run BUSCO on chromosome 4 of Drosophila melanogaster. We will select the lineage set of arthropoda.

As said yesterday, BUSCO2 is using augustus to run so please use the path you copied ~/annotation_course/course_material/augustus_path into.

AUGUSTUS_CONFIG_PATH=PATH/augustus_path

_module load bioinfo-tools_  
_module load BUSCO_  


*BUSCO -i /home/__login__/annotation\_course/course\_material/data/dmel/chromosome\_4/chromosome/4.fa -o 4\_dmel_busco -m geno -c 8 -l /sw/apps/bioinfo/BUSCO/v2_lineage_sets/arthropoda_obd9*

When done, check the short\_summary\_4\_dmel\_busco. How many proteins are reported as complete? Does this sound reasonable?



## 4. Assembling transcripts based on RNA-seq data

Rna-seq data is in general very useful in annotation projects as the data usually comes from the actual organism you are studying and thus avoids the danger of introducing errors caused by differences in gene structure between your study organism and other species.

Important remarks to remember before starting working with RNA-seq:
- Check if RNAseq are paired or not. Last generation of sequenced short reads (since 2013) are almost all paired. Anyway, it is important to check that information, which will be useful for the tools used in the next steps.
- Check if RNAseq are stranded. Indeed this information will be useful for the tools used in the next steps. (In general way we recommend to use stranded RNAseq to avoid transcript fusion during the transcript assembly process. That gives more reliable results. )
- Left / L / forward / 1 are identical meaning. It is the same for Right / R /Reverse / 2

**_Exercise 9_ - RNA-seq assembly genome based:**  

### Checking encoding version and fastq quality score format

To check the technology used to sequences the RNAseq and get some extra information we have to use fastqc tool.

_module load bioinfo-tools_  
_module load FastQC/0.11.5_  

*mkdir fastqc_reports*

*fastqc ~/annotation_course/course_material/data/dmel/chromosome_4/raw_computes/ERR305399.left.fastq.gz -o fastqc_reports/*

scp the html file resulting of fastqc (cf. exercise 4), what kind of result do you have?

Checking the fastq quality score format

*~/annotation_course/course_material/git/GAAS/annotation/Tools/Util/fastqFormatDetect.pl ~/annotation_course/course_material/data/dmel/chromosome_4/raw_computes/ERR305399.left.fastq.gz*

In the normal mode, it differentiates between Sanger/Illumina1.8+ and Solexa/Illumina1.3+/Illumina1.5+.
In the advanced mode, it will try to pinpoint exactly which scoring system is used.

More test can be made and should be made on RNA-seq data before doing the assembly, we have not time to do all of them during this course. have a look [here](https://en.wikipedia.org/wiki/List_of_RNA-Seq_bioinformatics_tools)

### Trimmomatic/Tophat/Stringtie (mapping reads to genome)

#### Trimmomatic

[Trimmomatic](http://www.usadellab.org/cms/?page=trimmomatic) performs a variety of useful trimming tasks for illumina paired-end and single ended data.The selection of trimming steps and their associated parameters are supplied on the command line.

*mkdir trimmomatic*  
_module load bioinfo-tools_  
_module load trimmomatic/0.36_  

The following command line will perform the following:  
	• Remove adapters (ILLUMINACLIP:TruSeq3-PE.fa:2:30:10)  
	• Remove leading low quality or N bases (below quality 3) (LEADING:3)  
	• Remove trailing low quality or N bases (below quality 3) (TRAILING:3)  
	• Scan the read with a 4-base wide sliding window, cutting when the average quality per base drops below 15 (SLIDINGWINDOW:4:15)  
	• Drop reads below the 36 bases long (MINLEN:36)  

*java -jar /sw/apps/bioinfo/trimmomatic/0.32/milou/trimmomatic-0.32.jar PE -threads 8 ~/annotation_course/2017/course_material/data/dmel/chromosome_4/raw_computes/ERR305399.left.fastq.gz ~/annotation_course/2017/course_material/data/dmel/chromosome_4/raw_computes/ERR305399.right.fastq.gz trimmomatic/ERR305399.left_paired.fastq.gz trimmomatic/ERR305399.left_unpaired.fastq.gz trimmomatic/ERR305399.right_paired.fastq.gz trimmomatic/ERR305399.right_unpaired.fastq.gz ILLUMINACLIP:/sw/apps/bioinfo/trimmomatic/0.32/milou/adapters/TruSeq3-PE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36*

#### Tophat

Once the reads have been trimmed, we use [tophat](https://ccb.jhu.edu/software/tophat/index.shtml) to align the RNA-seq reads to a genome in order to identify exon-exon splice junctions. It is built on the ultrafast short read mapping program [Bowtie](http://bowtie-bio.sourceforge.net/index.shtml).

*mkdir tophat*

*module load tophat/2.0.11*  
*module load bowtie2/2.2.3*  
*module load samtools/0.1.19*  
*module load perl*  
*module load perl_modules*  

*tophat --library-type=fr-firststrand chr4 trimmomatic/ERR305399.left_paired.fastq.gz trimmomatic/ERR305399.right_paired.fastq.gz*

This step will take a really long time so you can use the bam file located here ~/annotation_course/course_material/data/dmel/chromosome_4/RNAseq/tophat/accepted_hits.bam

#### Stringtie

StringTie is a fast and highly efficient assembler of RNA-Seq alignments into potential transcripts. It uses a novel network flow algorithm as well as an optional de novo assembly step to assemble and quantitate full-length transcripts representing multiple splice variants for each gene locus. Its input can include not only the alignments of raw reads used by other transcript assemblers, but also alignments longer sequences that have been assembled from those reads.

*module load bioinfo-tools*  
*module load StringTie*  

stringtie accepted_hits.bam -o outdir/transcripts.gtf

When done you can find your results in the directory ‘outdir’. The file transcripts.gtf includes your assembled transcripts.
As Webapollo doesn't like the gtf format file you should convert it in gff3 format (cf. Exercise 5). Then, transfer the gff3 file to your computer and load it into [Webapollo](http://annotation-prod.scilifelab.se:8080/NBIS_gp1/). How well does it compare with your Augustus results? Looking at your results, are you happy with the default values of Stringtie (which we used in this exercise) or is there something you would like to change?

**_Exercise 10_ - RNA-seq de-novo assembly:**  

### Trinity (de-novo assembly)

Trinity assemblies can be used as complementary evidence, particularly when trying to polish a gene build with Pasa. Before you start, check how big the raw read data is that you wish to assemble to avoid unreasonably long run times.

*module load bioinfo-tools*  
*module load perl*  
*module load perl_modules*  
*module load trinity/2.0.6*  
*module load java/sun_jdk1.7.0_25*  
*module load samtools*  

*Trinity --seqType fq --max_memory 64G --left ~/annotation_course/2017/course_material/data/dmel/chromosome_4/raw_computes/ERR305399.left.fastq --right ~/annotation_course/2017/course_material/data/dmel/chromosome_4/raw_computes/ERR305399.right.fastq --CPU 8 --output trinity_result --SS_lib_type RF* 


Trinity takes a long time to run if you want to have a look at the results, look in ~/annotation_course/course_material/data/dmel/chromosome_4/RNAseq/ the output that will be used later on for the annotation will be Trinity.fasta


You have now successfully retrieve most data useful to do an annotation! 
