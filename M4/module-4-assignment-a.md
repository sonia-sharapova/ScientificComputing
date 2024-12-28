# Module 4: Assignment A
-----------------------------------------------------------------------

> For each problems, please create a separate directory (eg. problem_1, problem_2, etc.).

# Problem 1. Parallelize Open Reading Frame Finder with Multiprocessing
------------------------------------------------------------------------
Identifying ORFs lends itself to a simple parallelization strategy to break up each reading frame into a separate process. Using the python `multiprocessing` package, update your implementation to utilize multiple processes to compute all six reading frames at the same time. 

Make use of time handling code to measure the amount of time for each process and for the entire operation.


# Problem 2. Parallelize Open Reading Frame Finder using Many Task Processing
-----------------------------------------------------------------------------
Apply the same approach in Problem 2 to breaking up your ORF finder into 6 tasks (one for each reading frame) that should be run as a SLURM job on the RCC. Write an `.sbatch` file that is able to execute the entire job by itself, without any manual intervention (ie. no pre-processing outside of the `.sbatch` file). 

This approach may require you to alter your ORF program to take a parameter that indicates the reading frame. For example: 

```
python orf_finder.py -sequence spike.fasta -frame 1 
python orf_finder.py -sequence spike.fasta -frame 2
python orf_finder.py -sequence spike.fasta -frame 3
python orf_finder.py -sequence spike.fasta -frame 4 
python orf_finder.py -sequence spike.fasta -frame 5
python orf_finder.py -sequence spike.fasta -frame 6
```

In this implementation, you could use set the `#SBATCH --array=1-6` and pass the `$SLURM_ARRAY_TASK_ID` as the parameter for each frame.

Provide the `.sbatch` used to compute the speedup in the repository along with the updated ORF code.


<br/>

# Problem 3. ORF Speedup
------------------------
Speedup is a metric used to assess the relative performance improvement gained by executing a program in different modes. In our case, we will compare the serial execution (a single process) of an ORF finder versus a task parallelism version.

Speedup, `S`, is defined as `S = T_Old / T_New` where `T_Old` is the time taken to execute the script without improvement (serial), and `T_New` is the time taken to execute the script with the improvement (parallel).

What is the speedup of the converting your ORF finder program to run as a multiprocessor job and a cluster job? Report your approach in a table and any/all values for the calculation.


| Approach          | T_Old    | T_New   |  S  |
| ---               | -----    |  ---    | --- |
| Serial            |   ?      |  ?      |  ?  |
| Multiprocessing   |   ?      |  ?      |  ?  |
| Many Tasks        |   ?      |  ?      |  ?  |


Are there any other approaches you can think of that will yield better performance with the goal to have the fastest time to solution? 


# Problem 4. Gene Finding
-----------------------
Update your approach to identifying ORFs to a more robust (and realistic) gene finder program. Consider the following additional criteria that is an indication an ORF is more likely to be an expressed gene:

* Must begin from a start codon
* ORF must contain at least 96 bp (32 amino acids)
* ORF must occur in a CpG island
* CpG island should appear in first third of the sequence

Implement your solution and run it against the Human [Chromosome 21](https://www.ncbi.nlm.nih.gov/nuccore/NC_000021?report=fasta). There is not yet a definitive number of protein-coding genes in Chromosome 21, but the current estimates are between 215-260. The sequence and known genes for Chromosome 21 are located in the `chromosome-21` directory.

Your program should be designed to utilized some mode of parallel programming and be capable of being run on the RCC cluster. There are many different aspects of this problem that need to be taken into consideration and you may consider using a hybrid approach. 

> Tip: For development and debugging, use a small portion of the sequence.g

Provide your program, sequence files, and `.sbatch` script in your repository, along with a `README.md` file with instructions on how to run your program.

