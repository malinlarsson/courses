---
layout: default
title:  'Exercise - Comparing and evaluating annotations'
---

# Comparing and evaluating annotations

In this exercise you will take the three annotations you have created for Drosophila - one with augustus, one without ab-initio predictions and the other with ab-initio. First, we will count the features annotated in each of them and compare that number against the existing reference annotation. Next, we will perform a proper feature-level comparison to obtain a proper estimate of congruency.

## Evaluating annotation quality

Evaluating an annotation can be done in three ways - running busco but with the proteins obtained from the annotation, in comparison with another annotation or in reference to the evidence alignments. The former isn't so much a quality check as a measure of congruency - i.e. the resulting numbers don't tell you which of the two gene builds is more correct. On the other hand, a comparison with evidence alignments is what Maker uses internally to select gene models. After synthesizing and annotating loci, the resulting model will be ranked against the filtered evidence alignments. The more congruent these two points of information are, the lower the 'annotation edit distance' (AED) will be. The AED score can be used to e.g. check an annotation for problematic models that may then be subjected to manual curation.

### BUSCO2

BUSCO is run before annotating to check if the assembly is good and therefore if the annotation will be good. It is also run after the structural annotation to then compare if we indeed find a number of genes corresponding of the first run of busco.

You will need to link the protein file created by maker on the run with the ab-initio
```
module load BUSCO

ln -s ~/PATH/maker_dmel_with_annotation/maker_with_abinition/annotations.proteins.fa   

BUSCO -i annotations.proteins.fa -o dmel_maker_abinitio -m prot -c 8 -l /sw/apps/bioinfo/BUSCO/v2_lineage_sets/arthropoda_odb9 -o dmel_maker_abinitio  
```
- if you compare with you first busco results what do you see?

## Comparing annotations

As with many tasks within bioinformatics, it is always a great idea to first look around for existing solutions. In the case of comparing annotations, there are in fact options already out there. One such example is genometools, which we have briefly used before.

First you need to write the path of libraries,  you will need,  in the bash\_profile to perform the following analyses.
```
~/annotation_course/course_material/lib/install_perllib_missing.sh

source ~/.bash_profile
```
If it isn't loaded anymore, reload it:
```
module load BioPerl/1.6.924_Perl5.18.4
```
### Preparing the input files
First you have to be situated in a folder containing the two maker annotations (with and without ab initio) and the augustus annotation. Then, copy or sym-link the EnsEMBL reference annotation that we provided you. Hint: The EnsEMBL annotation for chromosome 4 should be located in the folder course\_material/data/dmel/chromosome\_4/annotation.  
Now we have to do a couple of things: convert the EnsEMBL reference annotation from GTF format to GFF3 and then sort any GFF3-formatted annotation in a way that genometools accepts.
```
~/annotation_course/course_material/git/GAAS/annotation/Tools/Converter/gxf_to_gff3.pl -g drosophila_melanogaster.chr4.gtf -o drosophila_melanogaster.gff*
```
you need to unload Bioperl to be able to load GenomeTools 
```
module unload BioPerl/1.6.924_Perl5.18.4

module load GenomeTools/1.3.5

gt gff3 -sort maker_no_abinitio.gff > maker_no_abinitio.sorted.gff 
```
Repeat the command for the other gff files

### Counting features

Next, we get the feature counts for the three annotations and the reference from EnsEMBL:
```
gt stat maker_no_abinitio.gff
```
(or whatever you decided to name the file(s). The use of the sorted file or the original one changes nothing here)

As you will note, there are some differences - and of course, this is expected, since we used quite different approaches to generate the two gene builds. EnsEMBL on the other hand is originally imported from FlyBase. Obviously, a lot of manual labor and much more data has been put into the FlyBase annotation - and this highlights a common limitation of any computational pipeline. You will simply never reach the same level of quality and detail as seen in a manually curated reference annotation.

### Pairwise comparison of features

But feature counts alone can't really give you a clear measure of overlap/differences between any two annotations. In order to properly compare them, we can use another function included in genometools.

With the sorted files, we can now perform a comparison:
```
gt eval drosophila_melanogaster.sorted.gff maker_no_abinitio.sorted.gff  
```
This will create a long list of measures for all relevant sequence features with respect to both the 'sensitivity' and 'specificity' - as a measure of how close the annotation comes to a reference. As a reminder, 'specificity' measures the fraction of a reference overlapping a prediction whereas 'sensitivity' measures the fraction of a prediction overlapping a reference.

Note that the measures employed by genometools function in a all-or-nothing fashion. If the overlap is not 100%, it doesn't count (which is why you are unlikely to find gene-level congruencies between your gene builds and the reference annotation).  

From the comparison of your annotations to the Ensembl annotation, which one **seems** to be the most comprehensive to you ?

## Visualising annotations

**Note:** The following section overlaps with some of the exercises you have done earlier (comparing augustus predictions against the reference annotation).

In the previous tasks, we have looked at the overlap between different gene builds. While this gives us an indication of how similar two annotations are, **it doesn't really allow us to judge the overall quality and similarity of annotations**. Remember, sensitivity and specificity are 'all-or-nothing' - two annotations may be considered very different, but provide similar information, biologically. By that, we mean that two gene models don't need to be 100% identical in their coordinates to tell the scientist that a gene indeed exists in a given location and what it's product looks like.

We therefore need to visually inspect and compare the gene builds. This is a crucial step in any annotation project - gene build pipelines use a set of defined rules, but human pattern recognition is needed to spot potential systematic errors. For example, a pipeline like Maker will simply take all your input and try to synthesize it into an annotation, but it doesn't do too much checks on the data itself. What if you RNA-seq data is messier than you thought? What if your protein data set includes to many 'predicted' proteins that are in clear conflict with the other data?

There exist a number of 'annotation viewers' - IGV, Argo and Apollo, to name a few. A common choice for annotators is the web-based version of Apollo, WebApollo, mostly for its curation capabilities.

### Using WebApollo to view annotations
Transfer your maker annotation files to your computer using the scp command.  
Then, jump to [WebApollo](http://annotation-prod.scilifelab.se:8080/NBIS_gp1/) and upload your annotation track. [Here find the WebApollo instruction](UsingWebapollo)  
Along with your own gene builds, there are a number of other tracks already available - including a BAM track obtained from an RNA-seq sample as well as the reference annotation from FlyBase /EnsEMBL. You can now compare your gene builds against this reference. Some questions to ask yourself:

- Do my gene builds recover all the genes found in the reference?  
- What sort of differences are most common?  
- Do my gene builds reflect the patterns found in the RNA-seq data?
