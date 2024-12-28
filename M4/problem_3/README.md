### Problem 3. ORF Speedup
Compare the performance of the ORF finder in serial vs. parallel.

Speedup measures performance improvement. 
Speedup, S, is defined as 
    
    S = T_Old / T_New  

- T_Old: serial script execution time (s)
- T_New: parallel script execution time (s)

#### Speedup Table:

| Approach    | T_Old (s) | T_New (s) | S |
| -------- | ------- | ------- | ------- |
| Serial  | 2.29   | 2.29s (baseline) | 1  |
| Multiprocessing | 2.29s   |0.13     | 17.62 |
| Many Tasks    | 2.29s  |  0.072    |  31.81  |


This table demonstrates that we have a significant performance improvement with the parallel approaches when compared to serial. As expected, running parallel jobs on RCC clusters gave the best speedup.



#### Other Approaches:
The methods used only utilized CPUs, but implementing a hybrid solution that distributes tasks across nodes while also leveraging GPU acceleration for individual sequence processing tasks could potentially give a higher speedup - especially if the datasets read are very large. 

GPUs can handle thousands of parallel computations efficiently, and combining this with distributed processing allows large workloads to be divided across both nodes and cores. This speedup most likely wouldn't be visible on such a small dataset, but if we have a very large sequence (or many sequences), this approach could be useful. 

#### References:
- GPUs and SLURM: https://researchcomputing.princeton.edu/support/knowledge-base/gpu-computing
- GPU breakdown and analysis: https://www.weka.io/learn/glossary/ai-ml/gpu-acceleration/
- Speedup and Parallel crashcourse: https://ekatsevi.github.io/statistical-computing/hpc-basics.html