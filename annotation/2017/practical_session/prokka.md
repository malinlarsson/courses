---
layout: default
title:  'Prokka exercise'
---

# Bacterial annotation using Prokka

Before running Prokka on genomes assemblies, it is a good step to start with checking the gene content of the assembly

Checking genes in the assembly

BUSCO2 provides measures for quantitative assessment of genome assembly, gene set, and transcriptome completeness. Genes that make up the BUSCO2 sets for each major lineage are selected from orthologous groups with genes present as single-copy orthologs in at least 90% of the species. It includes 1,066 genes for arthropods, 2,586 for vertebrates, 978 for metazoans, 290 for fungi, 303 for eukaryotes and for bacteria 40 universal marker genes.

You will run BUSCO on 3 bacterial assemblies provided. We will select the lineage set of bacteria.

BUSCO2 is using augustus to run, as we have no administator rights on uppmax we need to copy the config file of augustus in folder we can right in and set up de the environment.

*cp -r ~/annotation_course/course_material/augustus_path .*

AUGUSTUS_CONFIG_PATH=augustus_path

_module load bioinfo-tools_  
_module load BUSCO_  


*BUSCO -i /home/__login__/annotation\_course/course\_material/data/prokka -o 4\_dmel_busco -m geno -c 8 -l /sw/apps/bioinfo/BUSCO/v2_lineage_sets/arthropoda_obd9*
Prokka is a really easy tool to use for bacterial annotation.

we provide you with 2 genomes, one really well assembled and the other badly assembled

prokka --help

the goal of the exercise is for you to learn how to use prokka and to annotate the 2 assemblies and then visualize them in IGV.



We could now also visualise all this information using a genome browser, such as [IGV](http://www.broadinstitute.org/igv/home). 
IGV requires a genome fasta file and any number of annotation files in GTF or GFF3 format (note that GFF3 formatted file tend to look a bit weird in IGV sometimes).
