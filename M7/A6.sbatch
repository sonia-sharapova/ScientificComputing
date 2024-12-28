#!/bin/bash
#BATCH --account=mpcs56430
#SBATCH --mail-user=sharapova@cs.uchicago.edu
#SBATCH --mail-type=ALL

#SBATCH --job-name=A6          # Job name
#SBATCH --output=./sbatch/out/%j.A6.out
#SBATCH --error=./sbatch/out/%j.A6.err
#SBATCH --cpus-per-task=4          # Number of CPU cores per task
#SBATCH --nodes=1                  # One node per task
#SBATCH --partition=bigmem2
#
#
# Run with command:
#    sbatch els.sbatch
#


python3 blast_opt.py