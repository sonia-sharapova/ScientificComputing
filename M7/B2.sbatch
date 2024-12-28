#!/bin/bash
#BATCH --account=mpcs56430
#SBATCH --mail-user=sharapova@cs.uchicago.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=blastp_array          # Job name
#SBATCH --output=./sbatch/out/bp_array_%j.out
#SBATCH --error=./sbatch/out/bp_array_%j.err
#SBATCH --cpus-per-task=16          # Number of CPU cores per task
#SBATCH --nodes=1                  # One node per task
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH --array=0-21
#SBATCH --partition=bigmem2

# Load BLAST module 
# module load blast
# conda activate blast

# Define the query file
# QUERY=~/../../project2/mpcs56430/db/query_seq_b.fasta
QUERY=~/../../project2/mpcs56430/db/query_sequence.fasta

# Define the database prefix and fragment pattern
DB_PREFIX=~/../../project2/mpcs56430/db/refseq_protein
DB_FRAGMENT=${DB_PREFIX}.$(printf "%02d" $SLURM_ARRAY_TASK_ID)

# Define the output directory and file
OUTPUT_DIR=./assignment_b/array_output
mkdir -p $OUTPUT_DIR
OUTPUT_FILE=${OUTPUT_DIR}/blastp_${SLURM_ARRAY_TASK_ID}.out

# Run BLASTP for the current database fragment
echo "Running BLASTP for database fragment $DB_FRAGMENT..."
time -p blastp -query $QUERY -db $DB_FRAGMENT -num_threads 16 -out $OUTPUT_FILE

echo "BLASTP for database fragment $DB_FRAGMENT completed."
