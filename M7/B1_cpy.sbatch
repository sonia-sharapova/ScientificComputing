#!/bin/bash
#BATCH --account=mpcs56430
#SBATCH --mail-user=sharapova@cs.uchicago.edu
#SBATCH --mail-type=ALL

#SBATCH --job-name=b_problem1_cpy         # Job name
#SBATCH --output=./sbatch/out/%j.B1_cpy.out
#SBATCH --error=./sbatch/out/%j.B1_cpy.err
#SBATCH --cpus-per-task=8          # Number of CPU cores per task
#SBATCH --nodes=4                  # One node per task
#SBATCH --partition=bigmem2
#
#
# Load necessary modules
module load blast

# Paths to query and database
QUERY=~/../../project2/mpcs56430/db/query_sequence.fasta
DB_PATH=~/../../project2/mpcs56430/db/refseq_protein

# Array of thread counts
THREADS=(1 2 4 6 8 16 32)

# Output file for times
TIMES_FILE="blastp_times_bigmem.txt"
echo "Threads Runtime" > $TIMES_FILE

# Loop through thread counts and run BLASTP
for THREAD in "${THREADS[@]}"
do
    echo "Running BLASTP with $THREAD threads..."
    OUTPUT_FILE="tmp_out/blastp_${THREAD}_threads.out"
    
    # Run BLASTP and capture runtime
    { time -p blastp -query $QUERY -db $DB_PATH -num_threads $THREAD -out $OUTPUT_FILE ; } 2> temp_time.txt
    
    # Extract runtime
    RUNTIME=$(grep "real" temp_time.txt | awk '{print $2}')
    
    # Save thread count and runtime to file
    echo "$THREAD $RUNTIME" >> $TIMES_FILE
done

# Cleanup
rm temp_time.txt

echo "All BLASTP runs completed. Times saved in $TIMES_FILE."