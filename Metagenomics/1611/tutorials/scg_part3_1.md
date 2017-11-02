---
layout: default
title:  'Part 3: Single cell genome assembly using SPAdes'
---

# Part 3: Single cell genome assembly
---

<!-- <p class="bg-warning">If you get disconnected from Uppmax [click here](lostConnection) to know how to get back </p> -->
<div class="alert alert-info">
  <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
  <strong>Info!</strong> If you get disconnected from Uppmax <a href="lostConnection"><strong>click here</strong></a> to know how to get back to it.
</div>

## 3.1 Organizing working folder

The following set of commands are to be typed in your compute node (for example mXX - look up using ```jobinfo -u username``` command). 
Make sure you are typing them in the compute node and not log in node. Go back to [Part 1](connectToUppmax) to check how to log in to your compute node.  
Before starting the exercises, you should make a folder named *single_cell_exercises* in your home directory where the exercises will be run.
Then create 2 folders *dataset1* and *dataset2* where the raw data will be linked

```sh
mkdir ~/single_cell_exercises
cd ~/single_cell_exercises/
mkdir dataset1 dataset2
```

Next, make symbolic links of sequences in those folders:

```sh
ln -s /proj/g2015028/nobackup/single_cell_exercises/sequences/dataset1/* dataset1/
ln -s /proj/g2015028/nobackup/single_cell_exercises/sequences/dataset2/* dataset2/
```
**Please, do not edit those files**

Check that the data is present in those 2 datasets folders

```sh
ls dataset1
ls dataset2
```

You should now see 2 files per dataset, a forward fastq file ```_R1_001.fastq``` and its reverse ```_R2_001.fastq```  

Later in some commands we use the variables *sample* and *trim*, the following commands will set those variables. 
**In case you loose your connection, you will need to redo this step again.**  

#### If you assemble **Hiseq** data without trimming:
```sh
sample=Hiseq
trim=''
cd ~/single_cell_exercises/dataset1
```

#### If you assemble **Hiseq** data with trimming:
```sh
sample=Hiseq
trim=_Trimmomatic
cd ~/single_cell_exercises/dataset1
```

#### If you assemble **Miseq** data without trimming:
```sh
sample=Miseq
trim=''
cd ~/single_cell_exercises/dataset2
```

#### If you assemble **Miseq** data with merging:
```sh
sample=Miseq
trim=_Trimmomatic
cd ~/single_cell_exercises/dataset2
```

<div>
 <span style="float:left"><a class="btn btn-primary" href="scg_part3"> Previous page</a></span>
 <span style="float:right"><a class="btn btn-primary" href="scg_part3_2"> Next page</a></span>
</div>

