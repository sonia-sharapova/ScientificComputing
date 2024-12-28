#!/bin/bash
#SBATCH --account=mpcs56430
#SBATCH --job-name=els_moby          # Job name
#SBATCH --mail-type=ALL               # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=sharapova@uchicago.edu    # Where to send mail
#SBATCH --output=%j.orf_finder_.out
#SBATCH --error=%j.orf_finder_.err
#SBATCH --cpus-per-task=8          # Number of CPU cores per task
#SBATCH --nodes=1                  # One node per task
#SBATCH --array=2-10               # Array job for strides 2 through 10

#
# Run with command:
#    sbatch moby.sbatch
#

# Run the Python script with stride value as argument
# $SLURM_ARRAY_TASK_ID corresponds to the stride value (from 2 to 10)
python els_moby.py $SLURM_ARRAY_TASK_ID
