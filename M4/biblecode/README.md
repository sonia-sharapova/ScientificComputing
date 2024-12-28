### ELS Algorithm:
The Equidistant Letter Sequence (ELS) algorithm:

Used to extract and analyze sequences of characters in a text by skipping a fixed number of characters between each selected character.

#### For each text file, and for each stride value:
- Extracting the Sequence: 
Reading through the text, pick characters at step sizes of current stride (where stride is the number of characters to skip between each character selected in the sequence)
- Find Valid Words: 
A nested loop iterates through possible substrings within the extracted sequence, checking each substring to see if it forms a valid English word (we have a dictionary of common English words).
- Repeat for Multiple Strides: 
To explore different potential patterns, the 10 (as this felt like an appropriate max word length)
- Results:
For each stride and each file, valid words found in the extracted sequence are written to output files named according to the stride and source text file. This is based on the $SLURM_ARRAY_TASK_ID in the .sbatch file.

### Parallelization Strategy

Given the large size of the texts, the computational cost of processing the texts and comparing multiple strides can be reduced by implementing parallelization strategies. I tried to parallelize the program by splitting work across strides using SLURM job arrays and by using multiprocessing to further parallelize tasks within each stride on individual nodes.

#### Job Array with SLURM:

Each stride is handled as a separate job in a SLURM array, where SLURM_ARRAY_TASK_ID specifies the stride value for each job.
This setup allows each stride to be processed independently, distributing the workload across multiple jobs. Each job in the array processes all text files for a single stride value.

Using a job array is efficient because it minimizes interdependencies between jobs, allowing each one to run independently on available nodes, thereby reducing wait times and resource contention.

#### Multiprocessing within Each Job:

Within each job, Python’s multiprocessing.Pool is used to process each text file in parallel. For example, one job might process all three text files with a stride of 4, using multiple cores to handle the three files simultaneously.

Each file is treated as a separate task in the pool, enabling each core to work on extracting and analyzing sequences from different files concurrently.

#### Midway Resource Allocation:

I tested different task allocations to see how big of a difference they made:
- CPU Cores: By setting --cpus-per-task (e.g., 4 or 8 cores), each job can use multiple CPU cores to split the workload. This setup allows each job to perform word-matching and sequence extraction tasks concurrently, significantly reducing the runtime for each stride.

- Testing with Moby Dick: 8 CPU cores per task and one node per task
- Testing with War and Peace: 2 Nodes with 8 tasks per node.

#### Struggles:
- I was unable to make a directory under '/projects2/mpcs56430', it said that disk space ran out?
- My parallelization was not effective and the jobs took too long to read through and analyze the texts. I terminated the jobs because they were over 4 hours long ...
- The code worked on smaller texts, like the examples I provided for a mock text file (under small_sample)
- I was running on /scratch/midway3/ maybe it wasn't powerful enough
- I might have overlooked overhead and made the code do too many things.. I thought that splitting it up by text and removing cross referencing the 10000 most common words might help, but I didn't see any results to be able to tell :(


#### Resources:
- More Info on the ELS Algorithm: https://felcjo-ringo.medium.com/bible-codes-making-an-algorithm-to-find-hidden-word-sequences-in-text-c36e94556469
- My Sample Text: https://www.wordyard.com/large-blocks-of-uninterrupted-text-a-talk-on-blogging-and-say-everything/
- Python multiprocessing Examples: https://docs.python.org/3/library/multiprocessing.html
- Parallelizing with SLURM Tutorial: https://sciwiki.fredhutch.org/scicomputing/compute_parallel/
