#!/bin/bash
#SBATCH --job-name=gene_finder
#SBATCH --output=%j.gene_finder_.out
#SBATCH --error=%j.gene_finder_.err
#SBATCH --mail-type=ALL               # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=sharapova@uchicago.edu    # Where to send mail
#SBATCH --ntasks=1                    # Run on a single CPU
#SBATCH --output=%j.orf_finder.out
#SBATCH --error=%j.orf_finder.err
#SBATCH --array=1-6

mkdir -p './logs'
output_file="./logs/gene_finder_frame_${SLURM_ARRAY_TASK_ID}.txt"

{ time python3 gene_finder.py --sequence ../data/chromosome-21/chr21-genes.fasta --frame $SLURM_ARRAY_TASK_ID --output ./valid_genes.txt ; } 2>> $output_file


# Frame info
echo "Frame $SLURM_ARRAY_TASK_ID completed" >> $output_file