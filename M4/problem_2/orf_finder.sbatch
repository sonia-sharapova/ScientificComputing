#!/bin/bash
#SBATCH --account=mpcs56430
#SBATCH --job-name=ORF_Finder          # Job name
#SBATCH --mail-type=ALL               # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=sharapova@uchicago.edu    # Where to send mail
#SBATCH --ntasks=1                    # Run on a single CPU
#SBATCH --output=%j.orf_finder.out
#SBATCH --error=%j.orf_finder.err
#SBATCH --array=1-6

#
# Run with command:
#    sbatch orf_finder.sbatch
#

# Set the output log file for the timing information
time_log="slurm_time_log.txt"

# Run the ORF finder with time command and redirect timing output to log file
{ time python3 orf_finder.py -sequence ../data/dogma.fasta -frame $SLURM_ARRAY_TASK_ID ; } 2>> $time_log

# Frame info
echo "Frame $SLURM_ARRAY_TASK_ID completed" >> $time_log
