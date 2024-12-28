#!/bin/bash
#SBATCH --account=mpcs56430
#SBATCH --job-name=els_war          # Job name
#SBATCH --mail-type=ALL               # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=sharapova@uchicago.edu    # Where to send mail
#SBATCH --output=%j.orf_finder_.out
#SBATCH --error=%j.orf_finder_.err
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH --array=2-10               # Array job for strides 2 through 10

#
# Run with command:
#    sbatch war.sbatch
#

# Run the Python script with command line arguments for text and words file
# python els_parallel.py ../../../../../project2/mpcs56430/bible_code/words_english.txt
# $SLURM_ARRAY_TASK_ID corresponds to the stride value
python els_war.py $SLURM_ARRAY_TASK_ID
