# SciLifeLab Courses

Public URL: https://scilifelab.github.io/courses

These are the course homepages of some of the courses given at [SciLifeLab](http://www.scilifelab.se).

http://www.scilifelab.se/education/courses/


## Editing instruction

### To keep the main folder from getting cluttered
Please create a single folder for your course and inside this folder create a folder for the current instance of the course. Ex:

```
# create a folder for the course as a whole
$ mkdir myNiceCourse

# create a folder for this instance of the course
$ mkdir myNiceCourse/November2015

# now put all the files for this course instance inside the `November2015` folder.
```

If it's a one-off course occation that will not repeat itself, please put it in the `misc` folder. 


## Developing locally
If you don't want to wait for github to build your pages after each edit, you can try this docker container that will do the building for your locally and instantly. https://github.com/Starefossen/docker-github-pages
