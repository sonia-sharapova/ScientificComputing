### Problem 1. Parallelize Open Reading Frame Finder with Multiprocessing
Identifying ORFs lends itself to a simple parallelization strategy to break up each reading frame into a separate process. Using the python multiprocessing package, update your implementation to utilize multiple processes to compute all six reading frames at the same time.

Note: Make use of time handling code to measure the amount of time for each process and for the entire operation.

### Parallelization:
Function: parallel_orf_finder(description, sequence)

This function finds the ORFs for the 6 reading frames in parallel by utilizing the multiprocessing Pool library:

    with Pool(processes=6) as pool:
        results = pool.map(central_dogma.find_orf_for_frame, frames)

The ORFs of the original dogma.fasta file were analyzed to maintain coonsistency and cross-reference results.

The dogma.fasta file is under the data directory.

#### Running Serial:
python3 serial.py

#### Running Parallel:
python3 parallel.py

#### Time Handling:
To track the execution time, I used python's 'time' library. The time starts before the find_orf() function and stops imediately after.

- Serial: 0.00 seconds
- Parallel: 0.13 seconds

In this case, the serial implementation ran faster. This may be due to overhead, as the dogma.fasta file is pretty small so the parallelization might actually be wasting time.

### Results:
The results are stored in the parallel_dogma.txt and serial_dogma.txt files and contain the open reading frames found for the dogma.fasta file. These results were consistent with the expected results, where both the serial and parallel implemetations gave the same output. 

#### References:
- codon table: https://gist.githubusercontent.com/juanfal/09d7fb53bd367742127e17284b9c47bf/raw/b2d8d2f450f2600d2d7a14ab2990dbd009db9fb3/gistfile1.txt
- ORF handing in python (to fix from first assignment): https://stackoverflow.com/questions/13114246/how-to-find-a-open-reading-frame-in-python
- Execution time: https://stackoverflow.com/questions/1557571/how-do-i-get-time-of-a-python-programs-execution

