# Metagenomics Course, Fall 2017

## Learning goals :

We have  number of goals for this course:
* Understand and recognise basic datatypes involved in metagenomics (fasta, fastq, sam/bam, otu-tables, gff...)
* Understand the differences between the types of molecular data (reaads, paired-reads, contigs, genomes...)
* Basic usage of High Performance Computing (HPC) clusters, e.g. UPPMAX (module system, running tools interactively, running things in a queue, installing new tools...)
* Understand and replicate the presented workflows in metagenomics
* Familiarise yourself with manuals and online ressources


## UPPMAX :

All the exercices here will be done using UPPMAX (https://www.uppmax.uu.se/) more specifically the Rackham cluster.

The rackham-cluster of uppmax is a distributed HPC cluster, meaning it is a lot of powerful computers networked together. It has 4 login-nodes and many more computing nodes.

[MAKE A FIGURE]

We will use `ssh` (Secure SHell) to connect to this cluster, use you ssh-client of choice. To start, we have to log into the login node.

```bash
ssh -X MY_USERNAME@rackham.uppmax.uu.se
```

The first time you do this (we should not be the case this time) there might be a few questions, but eventually you will be asked for your password, enter it. When you type your password nothing will be shown on the screen. This a security feature, not a bug.

We will not spend much time on the login node. we just want to know which computer is booked for each of us.

> Optional question: what does the `-X` in the command do.

Rackham, as most UPPMAX computer systems, runs a queuing tool called SLURM (Simple Linux Utility for Resource Management, https://slurm.schedmd.com/). This tool is used to distribute computing ressources to all users. A computer has been booked for each participant, SLURM knows 'it's name'.

On Rackham, to know which ressources you have requested (or somenoe else requested for you) the `jobinfo` command is used.

> Use the jobinfo command to find the name of your dedicated computer

Once you have the name of the computer (something looking like r123), you can log directly onto that computer. That name is the name of the computer in the local network of rackham, so you can simply connect with :

```bash
ssh -X r123
```

You are now on the computer that you can call `$HOME` for the next 3 days.

As you might/will notice, the wifi connection in this room is a bit 'dodgy' sometimes, `ssh` does not like bad connections, when the connection is broken while a program is running the programs stop, which can be very annoying for long computations. To alleviate this we will use a tool called `screen`. This will start a terminal that does not stop running when the connection is broken or the terminal is closed.

To start `screen` you just run the command:

```bash
screen
```

You can leave the 'screen' without closing it by doing `ctrl-A ctrl-D` (careful doing `ctrl-D` closes the 'screen' completly). With this you are back to the normal terminal. To reconnect to your screen, you first need to find out the name of the screen, `screen -list` will give you a list of screens available on this computer (yes, you can have many screens), and to reconnect simply run `screen -r NAME_OF_SCREEN` or if there is only one detached screen `screen -r`.

Now that we are comfortably in our screen and nothing can happen to anything running lets start.

The data we are gonna use for this course is in our common project folder, e.g. `/proj/g2017026/`), more specifically in  `/proj/g2017026/raw_data`.

> How many fastq-files can you find in this folder, and list all of them?!

> INTERNET INTERUPTIONNNNNNNNNN

Rackham uses a module system for programs (http://www.uppmax.uu.se/resources/software/installed-software/), so many bioinformatic programs are available without installing anything. We will use this as much as possible during this course. You can list all available module with `module list`. Let's load the `bioinfo-tools`-module:

```bash
module load bioinfo-tools
```

## Data-types

### FASTQ-files

Sequencing facilty might provide data from different technologies in a variety of formats, but most probably one of the formats the data will be delivered in will be the FASTQ format. We will start this tutorial with data in this format. It is a wide text-based format for sequencesm, they are related to the FASTA format which will see too.

A FASTQ-file can contain many many sequences, each sequence is represented by two data-types, the actual sequence and the quality scores:

```
@an_example_sequence_in_a_fastq_file
ACACATATATACACACATACACACACATATACACACACATATAAACACATATATACATTTATATGCATATATTAATACATATATATTTAAGTTGATGGAGAGTATAACAGAGTTAGGCTGCTTATT
+
BBBBBFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFBFFF/FFFBFFBFFFFFFFFFFFFFFFFFFFFFFBFFFF//FFFFFFFF<FFFF/FFFFFB/FFF<BF//<</BFFFFF
```

Normally each entry in a FASTQ-file is composed of exactly four lines.

The quality scores are related the quality of sequencing. They are `Q = -10 log<sub>10</sub> p` where `p`is the probabilty of a wrong base-call, and each letter corresponds to an integer value of Q. These letter can differ a bit depending on the sequencing platform, for recent illumina we have this correspondance table (courtecy of wikipedia):

```
  BCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
   |     |                               |
   3.....9...............................41
 ```


 As mentioned, the raw-data we will use is available in the `/proj/g2017026/raw_data`. This is publicly availble data from a number of microbioal saples from a single subject of the human microbiome project (https://hmpdacc.org/).

 > Use the linux commanda `ls`, `wc`, and `du` :
 >
 > What is the content of this folder?
 >
 > Optional : What is the difference between the files in the two folders?

 I preprocessed some of these files a little bit already, so now each file corresponds to one sample (I simply concatenated some files together as they where from the same samples). For each samples (library) we have two files, this is due to the way the illumina technology sequences, it would be different for PacBio for example.

 [FIND A FIGURE]

 > Using `wc`, the bash redirect (e.g. `wc -l my_lib.fastq > txt_file `, for example), combined with your data manipulation tool of choice (`R`, `python`, `bash`, `excel`, `pen&paper`)
 >
 > Make a table with the number of reads for each library
 >
 > Optional : Is there a relationship between number of reads and sampling-site or sampling-time (the number in the file is a the number of the visit)
> Very optional : Anything to say about the diversity of the reads in the libraries?

A very common tool to analyse reads is `fastqc`.

> load `fastqc` using UPPMAX' `module load`
>
> run `fastqc` for one of the shotgun and one of the amplicon `libraries`
>
> What can you learn from the returned report?!

Do not worry to much about fastqc reports in general, metagenomic data has a tendency to fail many things, as fastqc is made for nice clean genomes, so many of the warnings/errors will be due to actual biological effects or PCR-artefacts.

### FASTA-files

FASTA-files are the mother of all sequence data-types. It is a very simply text base file type compose of one or multiple entries. Each entry is composed of two type parts: A description part, which is a single line starting with `>` containing text information about the following sequence; and a data-part containing sequence data as plain text, this can be spread over multiple lines. FASTQ-files can be easily transformed to FASTA-files by removing the qualities and the `+`-line and replacing `@` by `>`, e.g:

```
>an_example_sequence_in_a_fasta_file
ACACATATATACACACATACACACACATATACACACACATATAAACACATATATACATTT
ATATGCATATATTAATACATATATATTTAAGTTGATGGAGAGTATAACAGAGTTAGGCTG
CTTATT
```

## AMPLICON-ANALYSES

### Tools

General amplicon processing and more:
* QIIME
* MOTHUR
* usearch (used in this course, mostly because of convinience)
* dada2 (bioconductor)

Quantification:
* phyloseq (bioconductor)
* metagenomeseq (bioconductor)
* DEseq2 (bioconductor)

Other:
* PiCRUST
* Phylotyping

### Processing the amplicon

Most analyses of 16s rRNA gene amplicons rely on an OTU-table, e.g. a table of counts of microbial-types in your samples. For this we need to cluster the reads into 'OTUs' (Operational Taxonomical Units), these are then counted.

We will use the `usearch` software to do the necessary computations (https://www.drive5.com/usearch/manual/). We are going to be fancy and we are going to use the latest version of `usearch` which is not on uppmax. We have it however locally in our project folder in `/proj/g2017026/bin/` (as well as some other software we will use later). For ease of use we will put this folder in our `PATH` environment variable (this contains all the folders which have excutables readily available).

```bash
PATH=/proj/g2017026/bin/:$PATH
```

> Optional : which other folders are in the `PATH`

From now one for a few exercice you will pic one of the amplicon libraries to process. We will call it MY_LIBRARY for the next few questions!

#### Merging reads

As we saw, each library has pairs of reads. In the case of a well designed amplicon the PCR product should be shorter than the lengths of the two reads added, in which case they will overlap, and the two pairs can be merged into one longer pseudo-read which will improve the quality of the analyses. This is the case for this dataset.

> Using the `usearch10` program with the `-fastq_mergepairs` option
>
> Merge the pairs of MY_LIBRARY
>
> Optional : play with the parameters to increase/decrease merging rate

<!-- One sample is nice and fine, but for a good analysis of the data we will need to analyse all the reads as one. If we just concatenate the files we will lose the information of which samples the reads came for. Luckily `usearch` can make our life a bit easier!

> Using the `--relabel` and `-fastq_mergepairs` options of `usearch10`
>
> Merge all the libraries.
> How many reads got lost in the merging
>
> Optional : any relationship between the merging rate and some of the sampling-parameters -->

#### QC-ing the reads

The reads have now been merged into pseudo-reads, but we have not done any quality-check yes. For merged paired reads it is convinient to do it after merging, as the mergin can increase the quality of the overlapping bases! In all sequencing runs there will be some bad reads, this can be due to many reasons, but usually mostly to the quality of the DNA, e.g. extraction and PCRs, or interactions between spots on the sequencing array. We will use the quality scores from the fastq files to remove reads below as certain quality.

> Using the `-fastq_filter` option of `usearch10`
>
> Remove from MY_LIBRARY the reads with more than one expected error and output it as a FASTA-file
>
> Optional: How does the loss of reads vary with the expected error.


#### Dereplicating

All clustering algorithms can be sensistive to the number of reads, however amplicon data has huge amounts of duplicates du to the PCRs, so one way to help the clustering is to remove these duplicates. Also, as there it is very reasonable to expect duplicates, any reads that appear only once is probably due to either PCR- or sequencing errors. In `usearch` both of these steps are done together.

> Using the `-fastx_uniques` option of `usearch10`
>
> Dereplicate MY_LIBRARY and remove singletons

> Optional: How does the count distribution of the reads look like?

#### Clustering

We are finally ready to do the clustering. The clustering heuristic of `usearch` is pretty fast and incorporates chimera detection as well. Please note that one of the keys of the heuristic is that the reads are aligned, as they are in an illumina amplicon, but might not be in other cases where you'd like to run this tool for!

> Using the `-cluster_otus` option of `usearch10`

> Compute 97% similarity sequence-clusters in MY_LIBRARY

> Optional: vary the identity cutoff, also what happens if you run the clustering without removing the singletons in the previous step

#### Mapping back

Now the whole data of MY_LIBRARY has been reduced to a small number of sequence-clusters (OTUs). Each of them represented by the most abundand read of that cluster. However the information of the total amount of reads has been lost along the way. For this reason we need to map the reads back to the OTUs, which means we need to find for each read the OTU that matches it best and that is more similar then the identity threshold. This will also allow us to recruit back reads lost during QC!

> Using the `-usearch_global` option of `usearch`
> Get some help from : https://www.drive5.com/usearch/manual/cmd_otutab.html
> Map the merged reads to the representative sequences of the clusters, and make an otu-table

> Optional : what are the reads that did not map?

#### Putting it all together

Well, this is all nice and fine,  but this is only one sample, so not really a table, just a vector. We could run the same thing for every sample seperatley but we would just get many separate vectors, we could not connect the OTUs easily to each other. What we need to do is to run the clustering step with all the reads of all the sample at the same time!

> Using all the options of `usearch10` that you have used until now,
> Have a look at the `-relabel` option of the `-fastq_mergepairs` function

> Make an OTU-table with all the samples, e.g. run the merging, QC for every sample seperately, concatenate the resulting FASTA-files, and follow then with the rest of the script.

> Optional : quantify the read-losses. Are there any experimental factors influencing the loss of reads?

#### New Age Clustering

In recent years there have been many discussions about OTUs and there meaning and the issues linked to them. Hence new modern methods of clustering amplicon reads have been developped. Much talked about recently has been the `dada2`-tool running with `R`, this tool does not use sequence identity to cluster reads, but build a noise model to clean reads from variation that is not biologically relevant. `usearch` also released recenlty a similar heuristic, the `unoise` algorithm.

> Using the `-unoise3` option of `usearch10`

> redo the OTU-table

> Optional : compare the mapping rates between the two methods


#### Taxonomical Annotation

We have not a table with OTUs and their abundances in each samples, as well as representative reads for all the OTUs. To learn more about our data we want also to annotate the reads. In the case of amplicon, we want to annotate for taxonomy, as we normally know exactly what genes we already have. For 16s rRNA amplicon there are many tools and databases. For sake of simplicity we will use a tool also provided by the `usearch` software, the `sintax`-tool.

> Let's split the class in two using the two OTU-tables

> Using the `-sintax` option of `usearch10`
> and the taxonomy/16s database found in /proj/g2017026/data/rdp_16s_v16_sp.udb

> Give all the OTUs taxonomical classifications.

> Optional : play with the cutoff, and try to install/use an other database.

### Let's make some plots : or where the real game starts!

Now you have the data in a good shape to start doing some proper data-analysis.

[TBD]


## Shotgun Data

Shotgun amplicon data is much more diverse and versatile than amplicon data. For this tutrial, we will run together a number of more or less complicated workflows using the 4 shotgun libraries we have in store for us on `/proj/g2017026/raw_data/shotgun`.

As mentioned before, the principal of shotgunm metagenomics is pretty straight forward. Take a sample, extract all the DNA, sequence the hell out of it. This leaves us often with a lot of data and many things we might want to know.

### Pre-processing

Some analyses are general to whatever biological question, they are linked to general NGS-methods.

#### Some Quality Control

Getting good libraries for shotgun sequencing can be difficult as the samples used normally are not as friendly as other types of biological samples (I am looking at you people doing cell-cultures). This can often result in lower quality of sequencing. A common tool used to judge quality of NGS-data is `FastQC`. This is only an analysis-tool, and only generate reports, it will not actually do any cleaning, but it might give us some insight into the data, and possible issues.

> Let's each first pic a sample of choice

> Using the `module`-system of UPPMAX load `FastQC`

> Generate a `FastQC`-report for your library of choice

> Optional : try to understand the FastQC-reports, and why we get so many warnings/errors

#### Read trimming and QC

[MultiQC]

Once we have some idea of problematic libraries, and potential issues, we can use some tools to clean the libraries a bit reduce noise and increase quality

A very commonly used tool for this is `trimmomatic`, it can do a large variety of operations on reads.

> Load `trimmomatic` with UPMMAX's `module`-system

> Clean the reads!

> Optional : re-run `FastQC` on the cleaned libraries and discuss


### Read-based analysis

#### Minhash-ing!

Raw libraries are large and clunky, and hard to handle really, mostly if we have many. Also they can be very complicated to compare directly. However, computer scientist are clever apparently, and developed methods to comapare large amount of text, which turn out work pretty well for sequence data as well. For texts, it is based on words but in sequences it is based on k-mers, meaning 'nucleotide-words' of length 'k'. It uses these words in hash-functions  (http://mccormickml.com/2015/06/12/minhash-tutorial-with-python-code/) to compute a very-compressed vector representation of your sequence data that can be used to compute distances!

The `Mash` tool has been developed to compute MinHashes and MinHash distances for genomic data, interestingly it can also be used for other things than reads. But here we will use it for our metagenomic libraries!

> Use the `mash` command

> Compute the MinHash set for your library
> Exchange these with other students so you have the set for each library
> Compute the MinHash distance between the libraries

> Optional : run MinHash some more libraries in [FOLDER] and then use my script [SCRIPT] to make a pretty plot.

#### Taxonomic annotation

We have all these reads now, but who are they from?! This is much more complicated then for 16s amplicons. Many tools have been developped, and most have the problem that they are only as good as the database they use, and as raw reads can be very numerous, often databases are limited to make computations tractable.

One recent tool that deserves mention is `kaiju`. The interesting aspect is that it uses a `blast`-index to do the classification, this is reasonably compact and easy to compute meaning that a much more exhaustive database can be used to classify as opposed to other methods.

> Get `kaiju` from github, compile it
> Using `kaiju` and the `krona` tools (available through `module`)
>
> Make a Krona plot of the taxonomies of your library of choice using with the database found in [/proj/g2017026/data/]

> Optional : Compare the taxonomy results with the 16s rRNA data of the same sample
> Super-optional : Make a new database for kaiju using which also includes a human reference and reannotate


#### Functional annotation

What is meant by functional annotation, name the reads base on known genes, or funtional ontongenies. For example, assign them PFAMs or EC-numbers. Functional annotation for reads is often mapping-based, meaning the reads are aligned to a reference database which has 'known'-functional annotations.

Most of these tools are pretty slow, so we will at first subset our libraries.

> Subset your library of choice to 500000 reads

Then we will use a tool called HUMAnN2 to annotate our reads.

> Install `HUMAnN2`, setting it us with the database in [/proj/g2017026/data/]
>
> Using HUMAn2

> Annotate the subset of your library of choice!

> What proportion of your data has been actually annotated?!

> Optional : run `HUMAnN2` on your whole library in an other `screen` using half of your processors

#### Compiling the data

The taxonomic and functional annotations here have now been done for each sample separatly, however if we want to compare the samples, we need to compile these to be able to compare them.

> Using your data-processing tools of choice

> Share the runs with each other and compile it into two tables, one for taxonomy and one for functions.

> Optional : Use some multi-dimensional scaling to visualize the distance between the samples, compare it to the results of Mash, and of the same samples in the 16s amplicon

### Assembly

The other road for analysis of metagenomic data is to assemble the reads into longer continguous pieces of DNA (contigs). This will simplify annotation of the sequences with the downside of risking chimeric sequences (e.g. assembling things that do not belong to each other). Assembling (meta)genomes can be a 

#### Assemble

We will start with an ob


