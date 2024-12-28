import argparse
from multiprocessing import Pool
from cpg_island_finder import find_cpg_islands

class GeneFinder:
    def __init__(self, description, sequence):
        self.description = description
        self.sequence = sequence.upper()
        self.cpg_islands = find_cpg_islands(self.sequence)

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
        return ''.join(protein)

    def is_in_cpg_island(self, pos):
        for start, end in self.cpg_islands:
            if start <= pos <= end:
                return True
        return False

    def find_orf_for_frame(self, frame):
        rna_sequence = self.transcribe()
        orfs = []
        start_pos = None
        sequence = rna_sequence if frame > 0 else rna_sequence[::-1]
        abs_frame = abs(frame) - 1

        for i in range(abs_frame, len(sequence) - 2, 3):
            codon = sequence[i:i + 3]
            if codon == 'AUG':
                start_pos = i
            elif codon in ['UAA', 'UAG', 'UGA'] and start_pos is not None:
                if i - start_pos + 3 >= 96 and self.is_in_cpg_island(start_pos):
                    orf = sequence[start_pos:i + 3]
                    protein_sequence = self.translate(orf)
                    orfs.append((frame, start_pos + 1, i + 3, len(protein_sequence), protein_sequence))
                start_pos = None
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

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Find ORFs that meet gene criteria in Human Chromosome 21.")
    parser.add_argument("--sequence", type=str, required=True, help="Path to the FASTA file.")
    parser.add_argument("--frame", type=int, required=True, help="Reading frame (1-6).")
    parser.add_argument("--output", type=str, required=True, help="Path to the output file.")
    args = parser.parse_args()

    # Read the sequence from the FASTA file
    description, sequence = read_fasta_file(args.sequence)
    gene_finder = GeneFinder(description, sequence)

    # Get the frame index from input
    frames = [-3,-2,-1,1,2,3] # all 6 reading frames
    frame = frames[args.frame - 1]

    # Find ORFs in the specified frame
    orfs = gene_finder.find_orf_for_frame(frame)

    # Append ORFs to the output file
    with open(args.output, 'a') as out_file:
        for frame, start_pos, end_pos, protein_length, protein_sequence in orfs:
            out_file.write(f"* {frame} | {start_pos} | {end_pos} | {protein_length} | {protein_sequence}\n")

    print(f"ORFs meeting gene criteria appended to {args.output}")

if __name__ == "__main__":
    main()
