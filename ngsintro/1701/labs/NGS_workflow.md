---
layout: default
title:  'NGS workflow'
---


# NGS workflow

The data we will work with comes from the 1000 Genomes Project.
Because whole human genomes are time consuming to work, with on account of their size, we will use only a small portion of the human genome. To be more precise about a megabase from chromosome 17.
Samtools has been used to extract this region of the data from the 1000 Genomes ftp site. It is a whole genome shotgun sequence from all of the individuals from the CEU (CEPH Europeans from Utah) population whose samples had low coverage (2-4x average).
We have 81 low coverage Illumina sequences, 63 Illumina exomes and 15 low coverage 454 samples.
55 of the samples exist in more than one datatype.

Much like the corresponding lecture, we will go through alignment, deduplication, base quality score recalibration, variant calling and variant filtering.

But first, lets book a node and set up the programs that we will be using.

## Book your own node

We have reserved half a node for each student during this course.
By now, you are probably already familiar with the procedure:

```bash
salloc -A g2016035 -t 04:00:00 -p core -n 8 --no-shell --reservation=g2016035_3 &
```

Make sure you only do this once, otherwise other course participants will have a hard time booking theirs!
Once your job allocation has been granted you can connect to the node you got using ssh, just like in the [Uppmax Introduction exercise](uppmax-intro) yesterday.

I.e. use
```bash
squeue -u <username>
```

to find out the name of your node, and then
```bash
ssh -Y <nodename>
```

To connect to the node.

## Accessing programs

First, we're going to run several programs that are installed in the module system.
To access the bioinformatics modules you first need to load the bioinfo-tools module:

```bash
module load bioinfo-tools
```
This makes it possible to load the individual programs we need:

```bash
module load bwa
module load samtools
module load GATK/3.7
module load picard/2.0.1
```
Picard and GATK are java programs, which means that we need to explicitly invoke java each time we run them and we need to know the path to the program file. Luckily, UPPMAX has a variable set when you load their modules. Notice the $GATK_HOME and $PICARD_HOME when we run those programs later on.

## Accessing data and creating a workspace

You need to know where your input data is and where your output will go.

All input data for the first steps of the exercises is located in the folder:

```bash
/sw/courses/ngsintro/gatk
```

Since we're all sharing the same data, we've made these files read-only. This prevents someone accidentally deleting or writing over the raw data or someone else's output.

Instead, you are going to write your output to your home directory.
Remember that your home directory can be represented by the '~' character.
(It is not good practice to keep large amounts of data in your home directory, usually you would work in your designated projects storage space.)

<!-- This creates some complexity, because your input data and your output data are not in the same place.
This is a common data processing problem, and one you should get used to dealing with.
It does mean that you'll need to type a lot.

Here are some tips for dealing with this:

1. Remember where you are (your current working directory, `pwd`) and use relative or absolute paths as necessary to type the least.
This is a quick but sloppy solution, and error prone, but if you are only doing something once, it works.
We all do it sometimes.
1. Use the full paths to everything, regardless of where you are actually working.
This is the most time consuming, and requires that you remember where everything is, but it is also the safest, because you always know that you are telling the computer exactly where you want to read and write.
This method is not dependent on keeping track of your current directory, because there are no relative paths, and you are much less likely to write output data to the wrong place by mistake.
Any time you get to the point of writing code or batch scripts to automate your data processing, you should do this.
For purposes of these exercises, it does not really matter which of these you do.
This is part of learning to work on the command line.
In the examples the full paths will be given, but there will be places where only the general syntax of the command will be given, and you will have to find the correct input for the situation.

Also, remember that tab completion can be very helpful in typing paths to files, not just because it saves keystrokes but also because it validates that you have typed a valid path (if the file is not there, tab completion will not work). -->

So that we don't clutter up the top level of our home folder we will make a subdirectory

```bash
mkdir ~/ngsworkflow
```

##Running commands

Throughout the exercises, we will illustrate commands in the format:

```bash
command <parameter1> <parameter2> ...
```

This signifies that you should replace &lt;parameter&gt; with the correct parameter type, for example your input file name, output file name, directory name, etc.
If you don't know what parameter you should supply, please ask.

## General tips

1. Use tab completion
1. Running a command without parameters will, usually, return a default help message on how to run the command.
1. Copying and pasting commands from the exercise to terminal can result in formatting errors. You will learn more by typing anyway :).
1. To be more strict, use the complete path to files you are using.
1. Once a command has resulted in successful completion, save it! You will redo the procedure again with another sample and this will save time.
1. If you book a new node or log out of the node you will need to reload the tool modules.
1. Check that the output file exists and is a reasonable size after a command is completed as a quick way to see that nothing is wrong. A common mistake people make is to attempt to load input files that do not exist or create output files where they cannot write.
1. Google errors, someone in the world has run into EXACTLY the same problem you had and asked about it on a forum somewhere.

<!-- We do this for two reasons.
First, as you all work, not everyone will create files with exactly the same names, so there is no way to make standard instructions for everyone.
Second, you need to learn how to figure out what goes into these spaces.
Usually, if you type a command without input parameters the documentation of the tool including possible input parameters will be displayed on the screen.

That brings us to copying and pasting.
It is possible to copy some of the commands out of this wiki and paste them into your terminal and make them work.
This is not recommended.
First, there can be formatting differences (especially how return characters are handled) between the browser and the terminal that make these commands not work properly.
Second, and more important, when you are doing this on your own data, there will be no cutting and pasting.
You will learn more by typing.
Remember that tab completion will help you with this.

NOTE - one you have typed the command for a step in the exercise below and seen that it works with your specifications, we recommend you to save the command in a plain text file. Plain text format will not cause formatting errors. You will perform the same procedure for at least two samples, so storing the commands in a text file will make the second analysis much faster.

We will align our data to the reference using BWA, a popular aligner based on the Burrows-Wheeler transform. -->

## Indexing the reference genome

Before we can align our sample we need a reference genome, and we need to perform the Burrows-Wheeler transform on the reference to build the associated files that the aligner expects. You will only need to create these files once, wether running on one sample or a million.
For our exercises, we'll use only human chromosome 17.
You can copy this from the project directory to your workspace.
(Normally copying you would not copy the reference, but this is so that everyone can see the full BWA process.)

```bash
cp /sw/courses/ngsintro/gatk/refs/human_17_v37.fasta ~/ngsworkflow
```

Check to see that this worked.

```bash
ls -l ~/ngsworkflow
```

which should show you something similar to:

```bash
-rwxrwxr-x 1 zberg uppmax 82548517 Jan 25 14:00 human_17_v37.fasta
```

except with your username. The size of the file in bytes is the number before the date.

<!-- If your file is not there or if it's the wrong size, something went wrong with your copy and you need to figure out what before you move on.
Checking the existence and size of files from each step in a process before performing the next step is a good practice that saves a lot of time.
A common mistake people make is to attempt to load input files that do not exist or create output files where they cannot write. -->

Now we need to build the Burrows-Wheeler transform

```bash
bwa index -a bwtsw ~/ngsworkflow/human_17_v37.fasta
```

BWA is a single program that takes a series of different commands as the first argument.
This command says to index the specified reference and use the bwtsw algorithm (BWA also has another indexing method for small genomes that we will not use).

This command will take about 2 minutes to run and should create 5 new files in your ngsworkflow directory with the same base name as the reference and different extensions.

While we are at it we will also build two different sequence dictionaries for the reference, which just lists the names and lengths of all the chromosomes.
Other programs will need these as input later and they are used to make sure the headers are correct.

```bash
samtools faidx ~/ngsworkflow/human_17_v37.fasta
```

```bash
java -Xmx16g -jar $PICARD_HOME/picard.jar CreateSequenceDictionary R=~/ngsworkflow/human_17_v37.fasta O=~/ngsworkflow/human_17_v37.dict
```


![](files/NGS_workflow/wf_align.png)

## Aligning the reads

We are skipping the quality control and trimming of reads for this exercise due to the origin of the data.

Let's start with aligning a chunk of whole genome shotgun data from individual NA06984. The command used is bwa mem, the ```-t 8``` signifies that we want it to use 8 threads/cores, which is what we have booked. This is followed by our reference genome and the forward and reverse read fastq files.

Learn more about[bwa mem](http://bio-bwa.sourceforge.net/bwa.shtml) if you are interested.

```bash
bwa mem -t 8 ~/ngsworkflow/human_17_v37.fasta /sw/courses/ngsintro/gatk/fastq/wgs/NA06984.ILLUMINA.low_coverage.17q_1.fq /sw/courses/ngsintro/gatk/fastq/wgs/NA06984.ILLUMINA.low_coverage.17q_2.fq > ~/ngsworkflow/NA06984.ILLUMINA.low_coverage.17q.sam
```

<!-- ```bash
bwa aln ~/ngsworkflow/human_17_v37.fasta /sw/courses/ngsintro/gatk/fastq/wgs/NA06984.ILLUMINA.low_coverage.17q_1.fq > ~/ngsworkflow/NA06984.ILLUMINA.low_coverage.17q_1.sai
``` -->

Note that you have to use a file redirect ( &gt;) for your output, otherwise bwa will print the output directly to stdout, i.e. your screen.

While that's running, take a minute to look at the input files paths.
They are fastq files, so I placed them in a directory called fastq.
It is from whole genome shotgun sequencing, so it is in a subdirectory called wgs.
The file name has 6 parts, separated by . or \_:

1. NA06984 - this is the individuals name
1. ILLUMINA - these reads came from the Illumina platform
1. low_coverage - these are low coverage whole genome shotgun reads
1. 17q - I have sampled these reads from one region of 17q
1. 1 - these are the forward reads in their paired sets
1. 2 - these are the reverse reads in their paired sets
1. fq - this is a fastq file

<!-- Now we need to do this again for the second read file.
Everything is that same except with 2s instead of 1s.
Don't forget to change your output file also! -->

Before we go on to the next step, take a minute and look at the fastq files and understand the format and contents of these files.
Use

```bash
less
```

to read one of those .fq files in the project directory.

<!-- ## Merging Alignments and Making SAM Files

The sai files are a binary format internal to BWA.
We now need to process those into something we can use.
For paired ends, this is done with the sampe function of BWA.
(Note that if you ever forget the syntax for a function, you can just type

```bash
bwa <function>
```

and it will list the parameters and options.
Run it for your files:

```bash
bwa sampe <ref> <sai1> <sai2> <fq1> <fq2> > ~/ngsworkflow/<sample>.sam
```

The sampe function takes a lot of arguments.
It needs the reference and the reads, because the sai files just have the definitions of the alignments, not the sequences.
It needs the sai files to get the alignments.
It outputs a SAM format file.
I would suggest that you give it the same name prefix as the others, but if you are getting tired of typing that, pick something shorter.
Retain the sample name and the fact that it is the 17q low coverage data. -->

## Creating a BAM file and adding Read Group information

SAM files are nice, but bulky, so there is a compressed binary format, BAM.
We want to convert our SAM into BAM before proceeding downstream.

Typically the BAM has the same name as the SAM but with the .sam extension replaced with .bam.

We need to add something called read groups which defines information about the sequencing run to our BAM file, because GATK is going to need this information.
Normally, you would do this one sequencing run at a time, but because of the way this data was downloaded from 1000 Genomes, our data is pulled from multiple runs and merged.
We will pretend that we have one run for each sample, but on real data, you should not do this.

We will use Picard to add read group information.
As a benefit, it turns out that Picard is a very smart program, and we can start with the SAM file and ask it to simultaneously add read groups, sort the file, and output as BAM.

```bash
java -Xmx16g -jar $PICARD_HOME/picard.jar AddOrReplaceReadGroups INPUT=<sam file> OUTPUT=<bam file> SORT_ORDER=coordinate RGID=<sample>-id RGLB=<sample>-lib RGPL=ILLUMINA RGPU=<sample>-01 RGSM=<sample>
```

Note that the arguments to Picard are parsed (read by the computer) as single words, so it is important that there is no whitespace between the upper case keyword, the equals, and the value specified, and that you quote ('write like this') any arguments that contain whitespace.

We specify the INPUT, the OUTPUT (assumed to be BAM), the SORT_ORDER, meaning we want Picard to sort the reads according to their genomic coordinates, and a lot of sample information.
The &lt;sample&gt; names for each of these 1000 Genomes runs is the Coriell identifier which is made up of the two letters and five numbers at the start of the file names (e.g., NA11932). This is sufficient to add for our read groups with suffixes such as -id and -lib as shown above.
Here is a more strict explanation of the read groups components:

* RGID is the group ID. This is usually derived from the combination of the sample id and run id, or the SRA/EBI id.
* RGLB is the group library. This will come from your library construction process. You may have multiple read groups per library if you did multiple sequencing runs, but you should only have one library per read group.
* RGPL is the platform. It is a restricted vocabulary. These reads are ILLUMINA.
* RGPU is the run identifier. It would normally be the barcode of your flowcell. You may have multiple read groups per run, but only one run per read group. We will just fake it as &lt;sample&gt;-01.
* RGSM is the sample name. You can have multiple read groups, libraries, runs, and even platforms per sample, but you can only have one sample per read group. (If you are pooling samples without barcoding, there is no way to separate them later, so you should just designate the pool itself as a sample, but downstream analyses like SNP calling will be blind to that knowledge.)

Lastly, we need to index this BAM, so that programs can randomly access the sorted data without reading the whole file.
This creates a index file similarly named to the input BAMfile, except with a .bai extension.
If you rename one the BAM and not the bai or vice versa you will cause problems for programs that expect them to be in sync.

```bash
java -Xmx16g -jar $PICARD_HOME/picard.jar BuildBamIndex INPUT=<bam file>
```

![](files/NGS_workflow/wf_localRealign.png)

## Local Realignment

Now, we want to use the Genome Analysis Toolkit (GATK) to perform local realignments.

First, we'll realign locally around potential indels.
This is done in two steps.
First, we identify possible sites to realign using the GATK tool RealignerTargetCreator:

```bash
java -Xmx16g -jar $GATK_HOME/GenomeAnalysisTK.jar -I <input bam file> -R <reference> -T RealignerTargetCreator -o <intervals file>
```

The &lt;bam file&gt; should be your sorted and indexed BAM with read groups added from before.
<!-- Note that the option flag preceding the input bam is a capital I (as in Input), not a lower case l. -->
The &lt;reference&gt; is the reference you used for alignment, and the &lt;intervals file&gt; is an output text file that will contain the regions GATK thinks should be realigned.
Give it the extension ".intervals".
Note that there is an additional option we are not using, which is to specify a list of known indels that might be present in the data (i.e., are known from other sequencing experiments).
Using this speeds up the process of identifying potential realignment sites, but because our data set is so small, we won't use it.

Now we feed our intervals file back into a different GATK tool called IndelRealigner to perform the realignments:

```bash
java -Xmx16g -jar $GATK_HOME/GenomeAnalysisTK.jar -I <input bam> -R <reference> -T IndelRealigner -o <realigned bam> -targetIntervals <intervals file>
```

Note that we need to give it the intervals file we just made, and also specify a new output BAM (&lt;realigned bam&gt;).
GATK is also clever and automatically indexes that BAM for us (you can type ls and look at the list of files to verify this).

![](files/NGS_workflow/wf_markdup.png)

##Marking and viewing duplicates

Next, we're going to go back to Picard and mark duplicate reads:

```bash
java -Xmx16g -jar $PICARD_HOME/picard.jar MarkDuplicates INPUT=<input bam> OUTPUT=<marked bam> METRICS_FILE=<metrics file>
```

The &lt;input bam&gt; should now be your realigned BAM from before, and you need to specify an output, the &lt;marked bam&gt; which will be a new file used in the following steps.
There is also the output of &lt;metrics file&gt; that contains some statistics such as how many reads were marked as duplicates.

Picard does not automatically index the .bam file so you need to do that before proceeding.

```bash
java -Xmx16g -jar $PICARD_HOME/picard.jar BuildBamIndex INPUT=<bam file>
```

Now we can look at the duplicates we marked with Picard, using a filter on the bit flag.
The mark for duplicates is the bit for 1024, we can use samtools view to look at them.

```bash
samtools view -f 1024 <bam file> | less
```

If we just want a count of the marked reads, we can use the -c option.

```bash
samtools view -f 1024 -c <bam file>
```

Before we move forward, ask yourelf why we used samtools to look at the BAMfile? Could we have looked at it with just less?

![](files/NGS_workflow/wf_bqsr.png)

## Base quality score recalibration

Next we want to perform quality recalibration with GATK.
We do this last, because we want all the data to be as clean as possible at at this point.
Like the local realignment this is performed in two steps.
First, we compute all the covariation of quality with various other factors using BaseRecalibrator:

```bash
java -Xmx62g -jar $GATK_HOME/GenomeAnalysisTK.jar -T BaseRecalibrator -I <input bam> -R <reference> -knownSites /sw/courses/ngsintro/gatk/ALL.chr17.phase1_integrated_calls.20101123.snps_indels_svs.genotypes.vcf -o <calibration table>
```

Note: This can take about 20 minutes.

As usual we give it our latest BAM file and the reference file.
Additionaly we supply a list of known sites.
If we had not done this GATK will think all the real SNPs in our data are errors since we are using low coverge calls from 1000 Genomes.
If you are sequencing an organism with few known sites, you could try variant calling once before base quality score recalibration and then using the most confident variants as known sites (which should remove most of the non-erroneous bases).
Failure to supply known SNPs to the recalibration will result in globally lower quality scores.

The calibration table output file has the covariation data written to it.
It is used in the next step where we use GATKs PrintReads to apply the recalibration:

```bash
java -Xmx16g -jar $GATK_HOME/GenomeAnalysisTK.jar -T PrintReads -BQSR <calibration table> -I <input bam> -R <reference> -o <output bam>
```

The &lt;input bam&gt; in this step is the same as the last step. As we have not changed the latest created BAM file. The &lt;output bam&gt; is new and will have the recalibrated qualities.
The &lt;calibration table&gt; is the file we created in the previous step using BaseRecalibrator.

![](files/NGS_workflow/wf_varcall.png)

## Variant Calling

Now we'll run the GATK HaplotypeCaller on our BAM and output a gVCF file that will later be used for joint genotyping.

```bash
java -Xmx16g -jar $GATK_HOME/GenomeAnalysisTK.jar -T HaplotypeCaller -R <reference> -I <input bam> --emitRefConfidence GVCF --variant_index_type LINEAR --variant_index_parameter 128000 -o <output>
```

The &lt;reference&gt; is our reference fasta again.
The &lt;input bam&gt; is the output from the recalibration step.
The output file is &lt;filename.g.vcf&gt;.
It needs to have a .g.vcf extension because it is a gvcf file.
The filename prefix should be identifiable as associated with your BAM file name (like the name root you use before the .bam) so you can tell later which vcf file came from which BAM). The --variant_index_type LINEAR and --variant_index_parameter 128000 sets the correct index strategy for the output gVCF.

Rerun the mapping and variant calling steps for at least one more sample from the course directory ```/sw/courses/ngsintro/gatk/fastq/wgs``` before continuing with the next step. Make sure it is also 17q.

# Joint genotyping

Now you will call variants on all the gvcf-files produced in the previous step by using GenotypeGVCFs. This takes the output from the Haplotypecaller that was run on each sample to create raw SNP and indel VCFs.

```bash
java -Xmx16g -jar $GATK_HOME/GenomeAnalysisTK.jar -T GenotypeGVCFs -R <ref file> --variant <sample1>.g.vcf --variant <sample2>.g.vcf ... -o <output>.vcf
```

As an alternative try to run the same thing but with all the gVCF for all low_coverage files in the course directory. A gVCF file where these have been merged can be found in the course directory, /sw/courses/ngsintro/gatk/vcfs/ILLUMINA.low_coverage.17q.g.vcf. In the next step when viewing the data in IGV, look at both and try to see if there is a difference for a your sample.

```bash
java -Xmx16g -jar $GATK_HOME/GenomeAnalysisTK.jar -T GenotypeGVCFs -R <ref file> --variant /sw/courses/ngsintro/gatk/vcfs/ILLUMINA.low_coverage.17q.g.vcf -o <output>
```

## Filtering Variants

The last thing we will do is filter variants.
We do not have enough data that the VQSR technique for training filter thresholds on our data is likely to work, so instead we're going to use the [best practices](http://www.broadinstitute.org/gatk/guide/topic?name=best-practices) parameters suggested by the GATK team at Broad.

The parameters are slightly different for SNPs and indels, but we have called ours together.
Why do you think that some of these parameters are different between the two types of variants?

An example command line with SNP filters is:

```bash
java -Xmx16g -jar $GATK_HOME/GenomeAnalysisTK.jar -T VariantFiltration -R <reference> -V <input vcf> -o <output vcf> --filterExpression "QD<2.0" --filterName QDfilter --filterExpression "MQ<40.0" --filterName MQfilter --filterExpression "FS>60.0" --filterName FSfilter
```

Note two things:
1. Each filterName option has to immediately follow the filterExpression it matches.
This is an exception to the rule that options can come in any order.
However, the order of these pairs, or their placement relative to other arguments, can vary.
1. The arguments to filterExpression are in quotation marks (").
Why is that?

Once you have the filtered calls, open your filtered VCF with less and page through it.
It still has all the variant lines, but the FILTER column that was blank before is now filled in, indicating that the variant on that line either passed filtering or was filtered out, with a list of the filters it failed.
Note also that the filters that were run are described in the header section.

## Look at Your Data with IGV

Next, we want to know how to look at these data.
For that, we will use IGV (Integrative Genomics Viewer).
We will launch IGV from our desktops because it runs faster that way.
Go to your browser window and Google search for IGV.
Find the downloads page.
You will be prompted for an email address.
If you have not already downloaded IGV from that email address, it will prompt you to fill in some information and agree to a license.
When you go back to your own lab, you can just type in your email and download the software again without agreeing to the license.

Now launch the viewer through webstart.
The 1.2 Gb version should be sufficient for our data.
It will take a minute or two to download IGV and start it up.
While that's going on, we need to download some data to our local machines so the viewer can find it (IGV can also look at web hosted data, but we are not going to set that up for our course data).
When it prompts you to save the IGV program, if you are working on a Mac put it in the Applications folder, otherwise just save it in your home directory.

Open a new terminal or xterm _on your local machine_ (i.e., do not log in to UPPMAX again).
You should be in your home directory.
Now we're going to use the command scp (secure copy) to get some data copied down:

We will start with the merged BAM files.
We want to get both the BAMs and bais for the low coverage and exome data.

```bash
scp <username>@milou.uppmax.uu.se:/sw/courses/ngsintro/gatk/processed/MERGED.illumina.\* ./
```

Because your UPPMAX user name is different than the user name on the local machine, you have to put your UPPMAX user name in front of the @ in the scp so that it knows you want to log in as your UPPMAX user, not as macuser.
After the colon, we give the path to the files we want.
The wildcard (*) character indicates that we want all the files that start with "MERGED.illumina".
However, in this case, we need to add a backslash ('\') in front of the wildcard ('*').
This is known as "escaping", because ordinarily your local shell would try to expand the wildcard in your local directory, but we want it expanded on the remote machine.
The './' means copy the files to your current directory.

It will prompt you for your UPPMAX password, then it should download four files.

We will also want to load the vcfs into IGV, so you can look at what calls got made.

```bash
scp <username>@milou.uppmax.uu.se:/sw/courses/ngsintro/gatk/vcfs/MERGED.illumina.\* ./
```

Do the same thing for the vcf that you have created in your home directory.

By now, IGV should be launching.
The first thing we want to do is make sure we have the right reference.
In IGV, go to the popup menu in the upper left and set it to "Human 1kg (b37+decoy)".
This is the latest build of the human genome (also known as GRCh37).

Now, go under the Tools menu and selection "Run igvtools..." Change the command to "Count" and then use the Browse button next to the Input File line to select the BAMs (not the bai) that you just downloaded.
It will autofill the output file.
Now hit the Run button.
This generates a .tdf file for each BAM.
This allows us to see the coverage value for our BAM file even at zoomed at views.
(We could also do this offline using a standalone version of igvtools.)

Now close the igvtools window and go back to the File menu, select "Load from File..." and select your BAMs (not the .bai or the .tdf).
They should appear in the tracks window.
Click on chromosome 17 to zoom in to there.
You can now navigate with the browser to look at some actual read data.
If you want to jump directly to the region we looked at, you can type MAPT in the text box at the top and hit return.
This will jump you to one of the genes in the region.

Let's look at a few features of IGV.

Go under the View menu and select Preferences.
Click on the Alignments tab.
There are a number of things we can configure.
Feel free to play with them.
Two important ones for our data are near the top.
Because we have multiple samples and the exome coverage is very deep, we want to turn off downsampling (upper left).
However, this will cause us to load more reads, so we want to reduce the visible range threshold (top).
I would suggest 5 kb.

Next, we want to look at some of the track features.
If you control-click (or right click for PCs or multi-button mice on Macs) on the track name at the left, you will get a popup menu with several options.
For example, click the gene track and play with the view (collapsed, squished, expanded).
I would suggest squished for our purposes.

If you go to a read alignment track, you can control some useful features of the display.
One is how you color the reads (by sample is an interesting one here).
Another is the grouping.
Group by sample is again useful (having grouped by sample, we could then use color for something else).

You can look at just the calls you made, or you can look at the calls from the full set, where you may see more of a difference between different types and depths of sequencing and between the calls with and without filtering. (IGV displays the filtered variant site in lighter shades, so you only need to load the filtered file).
You can even load these data all together.
Are there calls that were made using only one or two samples that were not made in the full data set or vice versa?

Try to browse around in your data and get a feeling for the called variants. Can you find a variant that have an allele frequency of exactly 0.5? A variant that have calls for all individuals? Exonic variants?


## [Extra labs](resequencing-extra)

If you have more time there are a couple of extra exercises where you will perform downstream analysis of the called variants in your .vcf file. [Extra labs](resequencing-extra)

## More info Quality Scores
Here is a technical documentation of Illumina Quality Scores: [technote_Q-Scores.pdf](technote_Q-Scores.pdf)

