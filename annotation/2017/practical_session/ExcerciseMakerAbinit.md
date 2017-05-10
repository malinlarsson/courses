---
layout: default
title:  'Exercise - Running Maker with ab-initio predictions'
---

# Running Maker with ab-initio predictions

The recommended way of running Maker is in combination with one or more ab-initio profile models. Maker natively supports input from several tools, including augustus, snap and genemark. The choice of tool depends a bit on the organism that you are annotating - for example, GeneMark -ES is mostly recommended for fungi, whereas augustus and snap have a more general use.

The biggest problem with ab-initio models is the process of training them. It is usually recommended to have somewhere around 500-1000 curated gene models for this purpose. Naturally, this is a bit of a contradiction for a not-yet annotated genome.

However, if one or more good ab-initio profiles are available, they can potentially greatly enhance the quality of an annotation by filling in the blanks left by missing evidence. Interestingly, Maker even works with ab-initio profiles from somewhat distantly related species since it can create so-called hints from the evidence alignments, which the gene predictor can take into account to fine-tune the predictions.
## Create a new Maker project

In order to compare the performance of Maker with and without ab-initio predictions in a real-world scenario, we have first run a gene build without ab-initio predictions. Now, we run a similar analysis but enable ab-initio predictions through augustus.

Create a new folder for this Maker run:
```
mkdir maker_dmel_with_abinitio  
cd maker_dmel_with_abinitio
```
Now link the gff files you want to use into your folder:

 - repeatmasker.chr4.gff (coordinates of repeatmasked regions)  
 - cufflinks2genome.chr4.gff (EST hints created from assembled transcripts) 
 
You could use the stringtie gff results you created but you need to change feature types from genes/transcripts into match / match_part otherwise Maker do not recognize it, also you could use the trinity.fasta file you created with trinity but maker will take longer to run.

In addition, you will also need the genome sequence and a protein set (you can use the protein and EST sets we used earlier). Sym-link it from the the data directory created earlier:
```
ln -s /path/to/chromosome_4/chromosome/4.fa
```
This time, we do specify a reference species to be used by augustus, which will enable ab-initio gene finding and keep_preds=1 will also show abinitio prediction not supported by any evidences :

*augustus\_species=fly* #Augustus gene prediction species model  (this is where you can call the database you trained for augustus)
...  
<i>protein2genome=0</i>  
<i>est2genome=0</i>

*keep_preds=1*

With these settings, Maker will run augustus to predict gene loci, but inform these predictions with information from the protein and est alignments.
## Run Maker with ab-initio predictions

With everything configured, run Maker as you did for the previous analysis:
```
maker -c 8
```
We probably expect this to take a little bit longer than before, since we have added another step to our analysis.

## Compile the output

When Maker has finished, compile the output:
```
~/annotation_course/course_material/git/GAAS/annotation/Tools/Maker/maker_merge_outputs_from_datastore.pl --output maker_with_abinitio  
```
And again, it is probably best to link the resulting output (maker.gff) to a result folder (the same as defined in the previous exercise e.g. dmel\_results), under a descriptive name.
