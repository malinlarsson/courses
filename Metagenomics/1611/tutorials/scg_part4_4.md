---
layout: default
title:  'Part 4: Coverage plotting, chimera detection and inspection'
---

# Part 4: Coverage plotting, chimera detection and inspection
---

<!-- <p class="bg-warning">If you get disconnected from Uppmax [click here](lostConnection) to know how to get back </p> -->
<div class="alert alert-info">
  <a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>
  <strong>Info!</strong> If you get disconnected from Uppmax <a href="lostConnection"><strong>click here</strong></a> to know how to get back to it.
</div>

## 4.4 Insert size

When you’ve done your read-mapping, you can also inspect the insert-sizes, size of the actual sequenced fragments, quite easily. 
Picard-tools have a ready made tool for this called CollectInsertSizeMetrics.

```sh
java -jar /sw/apps/bioinfo/picard/1.92/milou/CollectInsertSizeMetrics.jar HISTOGRAM_FILE=G5_vs_contigs_inssizePlot.pdf INPUT=G5_vs_contigs_sorted.bam OUTPUT=G5_vs_contigs_inssize.out #[time to run = 2.5 sec]
```

You can inspect the insert size distribution by opening the pdf file in firefox.

```sh
firefox G5_vs_contigs_inssizePlot.pdf
#or Okular.
okular G5_vs_contigs_inssizePlot.pdf
```

Time to show off, here are some quick questions for you [questions](scg_part4_questions).

<div>
 <span style="float:left"><a class="btn btn-primary" href="scg_part4_3"> Previous page</a></span>
 <span style="float:right"><a class="btn btn-primary" href="scg_part4_questions"> Next page</a></span>
</div>

<!--<div>
 <span style="float:left"><a class="btn btn-primary" href="scg_part4_3"> Previous page</a></span>
 <span style="float:right"><a class="btn btn-primary" href="scg_part5"> Next page</a></span>
</div>-->
