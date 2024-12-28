import argparse
import time
import sys
import os

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
    """Read FASTA file and return description and sequence."""
    description = None
    sequence = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(">"):
                description = line[1:].strip()
            else:
                sequence.append(line.strip())
    return description, ''.join(sequence)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Find ORFs in a specific reading frame.")
    parser.add_argument("-sequence", type=str, required=True, help="Path to the FASTA file.")
    parser.add_argument("-frame", type=int, required=True, help="Reading frame (1-6).")
    args = parser.parse_args()

    # Read the sequence from the FASTA file
    description, sequence = read_fasta_file(args.sequence)
    central_dogma = CentralDogma(description, sequence)

    # Get the frame index from input
    frames = [-3,-2,-1,1,2,3] # all 6 reading frames
    frame = frames[args.frame - 1]

    # Track the time for the ORF finding process for this frame
    start_time = time.time()
    orfs = central_dogma.find_orf_for_frame(frame)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Time taken for frame {args.frame}: {total_time:.2f} seconds")

    # Write ORFs to the output file
    base_dir = "frame_logs"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    output = "frame_logs/frame_{}_log.txt".format(args.frame)
    with open(output, 'w') as out_file:
        for frame, start_pos, end_pos, protein_length, protein_sequence in orfs:
            out_file.write(f"* {frame} | {start_pos} | {end_pos} | {protein_length} | {protein_sequence}\n")
