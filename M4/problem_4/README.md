### Problem 4. Gene Finding
Creating a robust gene finder program for Human Chromosome 21.

Additional Criteria:
- Must begin from a start codon
- ORF must contain at least 96 bp (32 amino acids)
- ORF must occur in a CpG island
- CpG island should appear in first third of the sequence

### Updates:
#### Identify CpG Islands:
Searches for regions meeting the following criteria:
-  GC content > 50%, 
- Obs/Exp ratio > 0.6 in the first third of the sequence.


#### Find Open Reading Frames (ORFs):

Search for ORFs in all six frames [-3, -2, -1, 1, 2, 3].
Ensure each ORF starts with a start codon (AUG), has at least 96 base pairs (32 amino acids), and falls within identified CpG islands.

#### Parallel Processing:

Process different reading frames, or different sections of the chromosome in parallel. 

#### Files:

- chr21.sbatch:

    SLURM job script. Deploys the gene finder program across multiple tasks on the RCC cluster, utilizing parallel processing where possible.

- gene_finder.py:

    Identify ORFs that meet the gene criteria and filter them based on the presence in CpG islands.

- cpg_island_finder.py:

    Fnction to locate CpG islands in the sequence.

- valid_genes.txt:
    ORFs meeting gene criteria saved here.

#### Example Usage (frames are executed in parallel otherwise):

    python3 gene_finder.py --sequence ../data/chromosome-21/chr21.fasta --frame 1 --output ./valid_genes.txt

#### References:
- Identifying CPG Islands: https://github.com/lucasnell/TaJoCGI
- Previously given: https://www.genscript.com/sms2/cpg_islands.html

