Clustering of data using SC3 package, following tutorial at: <https://bioconductor.org/packages/release/bioc/vignettes/SC3/inst/doc/my-vignette.html>

Run through steps 1-5 of the manual, step 6 is more detail on the different steps of SC3, go through that as well if you find time.

For this exercise you can either run with your own data or with the example data from Treutlein paper that they provide with the package. Below is an example with human innate lympoid cells (ILCs) from Bjorklund et al. 2016.

### Load packages

``` r
suppressMessages(library(scater))
suppressMessages(library(SC3))
```

### Read data and create a scater SCESet

``` r
# read in meta data table and create pheno data
M <- read.table("data/ILC/Metadata_ILC.csv", sep=",",header=T)
pd <- new("AnnotatedDataFrame",data=M)
rownames(pd)<-M$Samples

# read rpkm values
R <- read.table("data/ILC/ensembl_rpkmvalues_ILC.csv",sep=",",header=T)

# in this case it may be wise to translate ensembl IDs to gene names to make plots with genes more understandable
TR <- read.table("data/ILC/gene_name_translation_biotype.tab",sep="\t")

# find the correct entries in TR and merge ensembl name and gene id.
m <- match(rownames(R),TR$ensembl_gene_id)
newnames <- apply(cbind(as.vector(TR$external_gene_name)[m],rownames(R)),1,paste,collapse=":")
rownames(R)<-newnames

# create the SCESet
sceset <- newSCESet(fpkmData = R, phenoData = pd, logExprsOffset = 1)
```

### QC with scater

Use scater package to calculate qc-metrics and plot a PCA

``` r
sceset <- calculateQCMetrics(sceset)
plotPCA(sceset, colour_by = "Celltype")
```

![](sc3_ilc_files/figure-markdown_github/unnamed-chunk-3-1.png)

### Run SC3

OBS! it takes a while to run (10-30mins depending on data set size), define number of clusters to test with ks parameter, testing more different k's will take longer time. You can get a hint on number of clusters you should set by running the sc3\_estimate\_k function, but it may not always give the biologically relevant clusters.

``` r
# since this step takes a while, save data to a file so that it does not have to be rerun if you execute the code again.
savefile <- "data/ILC/sc3_data_ilc_k3-6.Rdata"
if (file.exists(savefile)){
   load(savefile)
}else {
   sceset <- sc3(sceset, ks = 3:6, biology = TRUE, n_cores = 1)
   save(sceset,file=savefile)
}
```

Now you can explore the data interactively within a shiny app using command:

sc3\_interactive(sceset)

### Plot results

Instead of using the app, that sometimes is very slow, you can also create each plot with different commands, here are some example plots.

``` r
# plot PCA for 4 clusters
plotPCA(
    sceset, 
    colour_by = "sc3_4_clusters", 
    size_by = "sc3_4_log2_outlier_score"
)
```

![](sc3_ilc_files/figure-markdown_github/unnamed-chunk-5-1.png)

``` r
# plot how many high auc value genes there are per cluster
plotFeatureData(
    sceset, 
    aes(
        x = sc3_4_markers_clusts, 
        y = sc3_4_markers_auroc, 
        colour = sc3_4_markers_padj
    )
)
```

    ## Warning: Removed 46010 rows containing missing values
    ## (position_quasirandom).

![](sc3_ilc_files/figure-markdown_github/unnamed-chunk-5-2.png)

``` r
# plot consensus clusters - 4 clusters
sc3_plot_consensus(
    sceset, k = 4, 
    show_pdata = c(
        "Celltype", 
        "log10_total_features",
        "sc3_4_clusters", 
        "sc3_4_log2_outlier_score",
    "Donor" 
    )
)
```

![](sc3_ilc_files/figure-markdown_github/unnamed-chunk-5-3.png)

SC3 clearly groups the 4 main celltypes, but within celltypes there is clear separation of the donors.

``` r
# same with 6 clusters 
sc3_plot_consensus(
    sceset, k = 6, 
    show_pdata = c(
        "Celltype", 
        "log10_total_features",
        "sc3_6_clusters", 
        "sc3_6_log2_outlier_score",
    "Donor" 
    )
)
```

![](sc3_ilc_files/figure-markdown_github/unnamed-chunk-6-1.png)

The next clustering steps clearly separates the ILC3s by donor,

``` r
# plot expression of gene clusters
sc3_plot_expression(sceset, k = 4,
    show_pdata = c(
        "Celltype", 
        "log10_total_features",
        "sc3_4_clusters", 
        "sc3_4_log2_outlier_score",
    "Donor" 
    )
)
```

![](sc3_ilc_files/figure-markdown_github/unnamed-chunk-7-1.png) This plots shows cluster of genes and their expression in the different clusters.

DE genes, these are estimated using the non-parametric Kruskal-Wallis test.

``` r
# plot DE genes
sc3_plot_de_genes(sceset, k = 4,
    show_pdata = c(
        "Celltype", 
        "log10_total_features",
        "sc3_4_clusters", 
        "sc3_4_log2_outlier_score",
    "Donor" 
    )
)
```

![](sc3_ilc_files/figure-markdown_github/unnamed-chunk-8-1.png)

Marker genes - are estimated from AUC values.

``` r
# plot marker genes
sc3_plot_markers(sceset, k = 4,
    show_pdata = c(
        "Celltype", 
        "log10_total_features",
        "sc3_4_clusters", 
        "sc3_4_log2_outlier_score",
    "Donor" 
    )
)
```

![](sc3_ilc_files/figure-markdown_github/unnamed-chunk-9-1.png)
