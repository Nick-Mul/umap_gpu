#!/bin/sh

# This is a simple example of an batch script use the queue on the GPU node

# request  Bash shell as shell for job

#$ -S /bin/bash
# Load the python required
#$ -l gpu=1
# Set Job name
#$ -N umap-gpu

# Join std err and std out into one file
#-j y
# Set output file
#$ -o $JOB_NAME-$JOB_ID.log

# pass the variables from current working env to qsub
#$ -V
# set the current working directory
#$ -cwd
# run the job (time just a convenient way of seeing how long it took)
time python ./test.py
