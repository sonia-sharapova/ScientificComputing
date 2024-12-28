#!/bin/bash

#SBATCH --account=mpcs56430
#SBATCH --mail-user=sharapova@cs.uchicago.edu
#SBATCH --mail-type=ALL
#SBATCH --job-name=benchmark_full
#SBATCH --output=./slurm/out/%j.%N.stdout
#SBATCH --error=./slurm/out/%j.%N.stderr
#SBATCH --chdir=/home/sharapova/sci_final/benchmark # modify if needed

#SBATCH --cpus-per-task=8                # Number of CPU cores per task (increased for parallel processing)
#SBATCH --nodes=1                        # One node per task
#SBATCH --time=02:00:00                  # Time limit hrs:min:sec
#SBATCH --mem=16GB                       # Memory limit per node

# Print some information about the job
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_JOB_NODELIST"
echo "CPUs per task: $SLURM_CPUS_PER_TASK"
date

# Load necessary modules (adjust these based on your cluster's configuration)
module load opencv/4.8.0

# Create output directory for results
mkdir -p benchmark_results_${SLURM_JOB_ID}

# Set environment variable for number of CPUs to use
export NUM_CPUS=$SLURM_CPUS_PER_TASK

# Run the benchmark script
# Note: Make sure correct path to input data
python src/benchmark.py data/smallerData/

# Print completion time
echo "Job completed at:"
date
