import time
from multiprocessing import Pool

class CentralDogma:
    def __init__(self, description, sequence):
        self.description = description
        self.sequence = sequence.upper()

    def transcribe(self):
        '''
        Function to transcribe DNA to RNA (T -> U)
            
        Returns: 
          (str): sequence with replacements
        '''
        return self.sequence.replace('T', 'U')

    def translate(self, rna_sequence):
        '''
        This function translates RNA to Protein using a codon table.
        '''
        codon_table = {
            'CGA': 'R', 'CGC': 'R', 'CGG': 'R', 'CGU': 'R', 'AGA': 'R', 'AGG': 'R',    # Arginina
            'UCA': 'S', 'UCC': 'S', 'UCG': 'S', 'UCU': 'S', 'AGC': 'S', 'AGU': 'S',     # Serina
            'UUA': 'L', 'UUG': 'L', 'CUA': 'L', 'CUC': 'L', 'CUG': 'L', 'CUU': 'L',    # Leucina
            'GGA': 'G', 'GGC': 'G', 'GGG': 'G', 'GGU': 'G',     # Glicina
            'ACA': 'T', 'ACC': 'T', 'ACG': 'T', 'ACU': 'T',    # Treonina
            'GUA': 'V', 'GUC': 'V', 'GUG': 'V', 'GUU': 'V',    # Valina
            'GCA': 'A', 'GCC': 'A', 'GCG': 'A', 'GCU': 'A',    # Alanina
            'CCA': 'P', 'CCC': 'P', 'CCG': 'P', 'CCU': 'P',    # Prolina
            'AUA': 'I', 'AUC': 'I', 'AUU': 'I',    # Isoleucina
            'UAA': '*', 'UAG': '*', 'UGA': '*',    # Stop
            'UAC': 'Y', 'UAU': 'Y',    # Tirosina
            'UGC': 'C', 'UGU': 'C',    # Cisteina
            'CAC': 'H', 'CAU': 'H',    # Histidina
            'CAA': 'Q', 'CAG': 'Q',    # Glutamina
            'AAC': 'N', 'AAU': 'N',    # Asparagina
            'AAA': 'K', 'AAG': 'K',    # Lisina
            'GAC': 'D', 'GAU': 'D',    # Acido Aspartico
            'GAA': 'E', 'GAG': 'E',    # Acido Glutamico
            'UUC': 'F', 'UUU': 'F',    # Fenilalanina
            'UGG': 'W',    # Triptofano
            'AUG': 'M',    # Methionina
         }
        protein = []
        for i in range(0, len(rna_sequence) - 2, 3):
            codon = rna_sequence[i:i + 3]
            if codon in codon_table:
                protein.append(codon_table[codon])
        protein = ''.join(protein)
        return protein

    def find_orf_for_frame(self, frame):
        '''
        This function finds the ORFs in a specific reading frame

        Input:
            frame (int): the reading frame

        Returns: 
          (str): the open reading frames
        '''
        def reverse_complement(seq):
            complement = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G'}
            return ''.join(complement[base] for base in reversed(seq))
        
        rna_sequence = self.transcribe()
        
        # Use reverse complement for negative frames
        if frame < 0:
            sequence = reverse_complement(rna_sequence)
        else:
            sequence = rna_sequence

        abs_frame = abs(frame) - 1  # Frame indexing
        orfs = []
        start_pos = None

        for i in range(abs_frame, len(sequence) - 2, 3):
            codon = sequence[i:i + 3]
            
            if codon == 'AUG' and start_pos is None:  # New start codon found
                start_pos = i
            elif codon in ['UAA', 'UAG', 'UGA'] and start_pos is not None:  # Stop codon, but continue
                # Capture the ORF from start to current stop codon
                orf = sequence[start_pos:i + 3]
                protein_sequence = self.translate(orf)
                orfs.append((frame, start_pos + 1, i + 3, len(protein_sequence), protein_sequence))
                start_pos = None  # Reset start position for next ORF
                
        # Capture trailing ORFs at end of frame
        if start_pos is not None:
            orf = sequence[start_pos:]
            protein_sequence = self.translate(orf)
            orfs.append((frame, start_pos + 1, len(sequence), len(protein_sequence), protein_sequence))

        return orfs


def read_fasta_file(file_path):
    '''Read FASTA file and return description and sequence.'''
    description = None
    sequence = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(">"):
                description = line[1:].strip()
            else:
                sequence.append(line.strip())
    return description, ''.join(sequence)

def parallel_orf_finder(description, sequence):
    '''Find ORFs for all 6 reading frames in parallel.'''
    central_dogma = CentralDogma(description, sequence)
    frames = [-3,-2,-1,1,2,3]  # All 6 reading frames

    # Use multiprocessing Pool to parallelize ORF finding across frames
    with Pool(processes=6) as pool:
        results = pool.map(central_dogma.find_orf_for_frame, frames)

    # Flatten the results from each frame and return
    all_orfs = [orf for frame_orfs in results for orf in frame_orfs]
    return all_orfs

if __name__ == "__main__":
    fasta_file = '../data/dogma.fasta'
    output_file = 'parallel_dogma.txt'
    #fasta_file = '../data/spike.fasta'
    #output_file = 'parallel_spike.txt'

    # Read the sequence from the FASTA file
    description, sequence = read_fasta_file(fasta_file)

    # Track the time for the parallel ORF finding process
    start_time = time.time()
    orfs = parallel_orf_finder(description, sequence)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Time taken for parallel ORF finding: {total_time:.2f} seconds")

    # Write ORFs to the output file
    with open(output_file, 'w') as out_file:
        for frame, start_pos, end_pos, protein_length, protein_sequence in orfs:
            out_file.write(f"* {frame} | {start_pos} | {end_pos} | {protein_length} | {protein_sequence}\n")

    print(f"ORFs saved to {output_file}")

