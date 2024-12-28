### Problem 2. Parallelize Open Reading Frame Finder using Many Task Processing
Break up your ORF finder into 6 tasks (one for each reading frame) that should be run as a SLURM job on the RCC. 

Write an .sbatch file that is able to execute the entire job by itself, without any manual intervention (ie. no pre-processing outside of the .sbatch file).

In this implementation, you could use set the #SBATCH --array=1-6 and pass the $SLURM_ARRAY_TASK_ID as the parameter for each frame.

### Usage:

Run with command:

    sbatch orf_finder.sbatch

### Timing:
Run the ORF finder with time command to keep track of run times. I redirected the timing output to a time log file.

#### Running the file in .sbatch:
{ time python3 orf_finder.py -sequence ../data/dogma.fasta -frame $SLURM_ARRAY_TASK_ID ; } 2>> $time_log

### Parallelization:
The parallelization is smilar to Problem1, but 

Each task will process one reading frame, log the results in its respective file in the 'frame_log' directory, and time taken in the slurm_time_log.txt file. This setup enables easy tracking and analysis of the time taken for each frame.

#### Time Handling:
If each frame is processed independently, the total execution time is roughly the time taken by the longest-running frame. Based on the results, the longest running time was 0.072s, faster than the multiprocessor parallel implementation alone (which took 0.13 seconds).


### Results:
frame_logs (dircectory): hold the ORFs found by the program for each frame
slurm_time_log.txt: Times each task took to execute

The open reading frames found were consistent with the expected results for the dogma.fasta file. We also observe a sleep-up from the parallel implementation of about 1.8, so the time is almost halved. 

#### References:
- multiprocessing with Pool on cluster: https://stackoverflow.com/questions/67975328/slurm-and-python-multiprocessing-pool-on-a-cluster
- timing in bash: https://unix.stackexchange.com/questions/52313/how-to-get-execution-time-of-a-script-effectively
- More SLURM info: https://slurm.schedmd.com/overview.html
- Guide on SBATCH: https://blogs.oracle.com/research/post/a-beginners-guide-to-slurm
