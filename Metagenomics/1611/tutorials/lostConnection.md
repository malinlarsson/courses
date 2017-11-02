---
layout: default
title:  'What to do when you are disconnected from Uppmax?'
---

# What to do when you are disconnected from Uppmax?  
---

It happens from time to time that you get disconnected from Uppmax after loosing the connection to the network for example.
Here, we summarize the steps you have to repeat before continuing doing your work.

Type the following command but replace *username* with your login name.  

1. Connect to Uppmax:

```sh
ssh -X username@milou.uppmax.uu.se
```

2. Type the following command to see the node you are affected to: 

```sh
squeue -u username
```

3. The *nodelist* column gives you the name of the node that has been reserved for you.  
To log in to compute node run the following command (replace *mXX* with the actual compute node you are assigned to)  

```sh
ssh -X mXX
```
4. Make sure that you can launch graphical tools in your node by typing this command:  

```sh
xclock
```

If you see the clock then you should be able to launch GUI-based tools. Close the clock.

5. Load all necessary softwares to complete all exercices
```sh
source /proj/g2015028/nobackup/single_cell_exercises/scripts/modules_load
```

Now we can check that all softwares have been correctly loaded, please type the following command in your terminal and check that all element of the list below is listed **contact the teachers if not**.  

```sh
module list
```

* bioinfo-tools
* trimmomatic/0.32
* spades/3.1.1
* IDBA/1.1.1-384
* quast/2.3
* prodigal/2.60
* blast/2.2.29+
* bwa/0.7.5a
* picard/1.92
* artemis/15.0.0
* MEGAN/4.70.4
* Ray/2.3.1-mpiio



### If you have reached the **part 3: Single cell genome assembly**, continue with the next steps

Since we use the variables *sample* and *trim*, the following commands will set those variables. 
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
 <span style="float:left"><a class="btn btn-primary" onclick="javascript:history.go(-1)"> Previous page</a></span>
</div>
