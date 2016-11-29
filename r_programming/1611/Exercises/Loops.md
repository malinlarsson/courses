---
layout: default
title:  'Repeats in R'
---
# Repeats in R
<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#orgheadline2">1. Introduction</a>
<ul>
<li><a href="#orgheadline1">1.1. Exercises: Loop structures</a></li>
</ul>
</li>
</ul>
</div>
</div>

# Introduction<a id="orgheadline2"></a>

In programming languages loop structures, either with or without
conditions, are used to repeat commands over multiple entities. For
and while loops as well as if-else statements are also often used in
R, but not as often as in many other programming languages. The reason
for this is that many needs of the loops are addressed using
vectorization or via apply functions.

This means that we can multiply all values in a vector in R by two, just
call:

    vec.a <- c(1, 2, 3, 4)
    vec.a * 2

    [1] 2 4 6 8

In many other and languages as well as in R you can also create this
with a loop instead

    for (i in vec.a) {
        v[i] <- vec.a[i] * 2
        }
    vec.a

    [1] 2 4 6 8

As you saw in the lecture this is far less efficient and not by any
means easier to type and we hence tend avoid loops when possible. 

## Exercises: Loop structures<a id="orgheadline1"></a>

1.  Create a 100000 by 10 matrix with the numbers 1:1000000. Make a
    for-loop that calculates the median for each row of the
    matrix. Verify that your results are consistent with what you
    obtain with the apply function to calculate row means as well as
    with the built-in rowSums function. These functions were discussed
    in the lecture "Elements of the programming language - part 2"
	<details>
	<summary>:key: Click to see how</summary>
	<pre>
        X <- matrix(1:1000000, nrow = 100000, ncol = 10)
        for.sum <- vector()
        # Note that this loop is much faster if you outside the loop create an empty vector of the right size.
        # rwmeans <- vector('integer', 100000)
        for (i in 1:nrow(X)) {
            for.sum[i] <- sum(X[i,])
        }
        head(for.sum)
    
        [1] 4500010 4500020 4500030 4500040 4500050 4500060
    
        app.sum <- apply(X, MARGIN = 1, sum)
        head(app.sum)
    
        [1] 4500010 4500020 4500030 4500040 4500050 4500060
    
        rowSums.sum <- rowSums(X)
        head(rowSums.sum)
    
        [1] 4500010 4500020 4500030 4500040 4500050 4500060
    
        identical(for.sum, app.sum)
        identical(for.sum, rowSums.sum)
        identical(for.sum, as.integer(rowSums.sum))
    
        [1] TRUE
        [1] FALSE
        [1] TRUE
	</pre>
	</details>
<br>

2.  Another common loop structure that is used is the while loop, which
    functions much like a for loop, but will only run as
    long as a test condition is TRUE. Modify your for loop from
    exercise 1 and make it into a while loop.
	<details>
	<summary>:key: Click to see how</summary>
	<pre>
        x <- 1
        while.sum <- vector("integer", 100000)
        while (x < 100000) {
            while.sum[x] <- sum(X[x,])
            x <- x + 1
            }
        head(while.sum)
    
        [1] 4500010 4500020 4500030 4500040 4500050 4500060

	</pre>
	</details>
<br>
3.  Create a data frame that contains 3 columns, 2 numeric and 1
    character vector. The length of the vectors does not matter. Make a
    loop structure that have the ability to report without you giving
    the column numbers report the total number of characters if the it
    is a character vector and report the mean if it is a numeric vector.
	<details>
	<summary>:key: Click to see how</summary>
	<pre>
        #df1 <- data.frame(c(letters[1:5], LETTERS[1:5], 1:5, 1:5))
        vector1 <- 1:10
        vector2 <- c("Odd", "Loop", letters[1:8])
        vector3 <- rnorm(10, sd = 10)
        df1 <- data.frame(vector1, vector2, vector3, stringsAsFactors = FALSE)
        sum.vec <- vector()
        for (i in 1:ncol(df1)) {
            if (is.numeric(df1[,i])) {
                sum.vec[i] <- mean(df1[,i])
            } else {
                sum.vec[i] <- sum(nchar(df1[,i]))
            }
        }
        sum.vec
    
        [1]  5.500000 15.000000  2.727954
	</pre>
	</details>
<br>
4.  Convert the code to count characters and estimate means that you
    created under question 3. The function should take a single data
    frame as argument.
	<details>
	<summary>:key: Click to see how</summary>
	<pre>
        df.info <- function(df) {
        sum.vec <- vector()
        for (i in 1:ncol(df)) {
            if (is.numeric(df[,i])) {
                sum.vec[i] <- mean(df[,i])
            } else {
                sum.vec[i] <- sum(nchar(df[,i]))
            }
        }
        sum.vec
        }
	</pre>
	</details>
<br>
5.  In all loops that we tried out we have created the  variable where
    the output is saved outside the loop. Why is this?
