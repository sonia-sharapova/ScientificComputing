'''
Note: made changes to the global (separated from local) because the scores were not being computed correctly.
'''

import argparse
import numpy as np

# Scoring matrices from the uploaded file
from matrices import PAM250, BLOSUM62

def read_fasta(filename):
    '''
    This function reads in a fasta file but removing the header line (that starts with ">")

    Input:
        filename (str): the fasta file

    Returns:
        sequence (str): the sequence
    '''
    sequence = ''
    with open(filename, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if not line.startswith('>'): # checks header
                sequence+=line.strip()
    return sequence

def global_alignment(seq1, seq2, scoring_matrix=False, match_score=1, mismatch_score=-1, gap_penalty=-3):
    '''
    This function creates a score matrix for Needleman-Wunsch (global) algorithm

    Input:
        seq1, seq2 (str): your sequences
        scoring_matrix (bool): use of a scoring matrix

    Returns:
        aligned_seq1, aligned_seq2 (str): the optimal alignment of the sequences
        score_matrix: A 2D list (matrix). each cell contains the alignment score for the best possible alignment up to that point
    '''

    if scoring_matrix:
        match_score = scoring_matrix.get(seq1[i-1], {}).get(seq2[j-1], gap_penalty)

    rows = len(seq1) + 1
    cols = len(seq2) + 1

    # Initialize the output matrices
    score_matrix = [[0] * cols for _ in range(rows)]
    traceback_matrix = [[None] * cols for _ in range(rows)]


    # Create scoring matrix

    # Initialize first row and column using gap penalty
    for i in range(rows):
        score_matrix[i][0] = gap_penalty * i
        traceback_matrix[i][0] = 'up'
    for j in range(cols):
        score_matrix[0][j] = gap_penalty * j
        traceback_matrix[0][j] = 'left'

    # Fill the matrix using the recursion
    for i in range(1, rows):
        for j in range(1, cols):
            match = score_matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_score)
            gap1 = score_matrix[i - 1][j] + gap_penalty
            gap2 = score_matrix[i][j - 1] + gap_penalty
            score_matrix[i][j] = max(match, gap1, gap2)

    # Traceback
    aligned_seq1 = ""
    aligned_seq2 = ""
    i, j = rows-1, cols-1
    while i > 0 or j > 0:
        if i > 0 and j > 0 and score_matrix[i][j] == score_matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_score):
            aligned_seq1 = seq1[i - 1] + aligned_seq1
            aligned_seq2 = seq2[j - 1] + aligned_seq2
            i -= 1
            j -= 1
        elif i > 0 and score_matrix[i][j] == score_matrix[i - 1][j] + gap_penalty:
            aligned_seq1 = seq1[i - 1] + aligned_seq1
            aligned_seq2 = "-" + aligned_seq2
            i -= 1
        else:
            aligned_seq1 = "-" + aligned_seq1
            aligned_seq2 = seq2[j - 1] + aligned_seq2
            j -= 1

    return aligned_seq1, aligned_seq2, score_matrix


def create_score_matrix(seq1, seq2, scoring_matrix, gap_penalty, local=False):
    '''
    This function creates a score matrix for Needleman-Wunsch (global) or Smith-Waterman (local).

    Input:
        seq1, seq2 (str): your sequences
        scoring_matrix: PAM250 or BLOSUM62
        gap_penalty (int): the gap penalty you want to use
        local (bool): type of alignemnt (local or global)

    Returns:
        score_matrix: A 2D list (matrix). each cell contains the alignment score for the best possible alignment up to that point
        traceback_matrix: A 2D list (matrix) that stores the directions for reconstructing the optimal alignment. 
        max_pos: tuple (i, j) representing the position of the highest scoring cell in the score matrix. 
    '''
    
    rows = len(seq1) + 1
    cols = len(seq2) + 1

    # Initialize the output matrices
    score_matrix = [[0] * cols for _ in range(rows)]
    traceback_matrix = [[None] * cols for _ in range(rows)]

    # Initialize first row and column
    for i in range(1, rows):
        score_matrix[i][0] = score_matrix[i-1][0] + gap_penalty
        traceback_matrix[i][0] = 'up'
    for j in range(1, cols):
        score_matrix[0][j] = score_matrix[0][j-1] + gap_penalty
        traceback_matrix[0][j] = 'left'

    max_score = 0
    max_pos = (0, 0)
    for i in range(1, rows):
        for j in range(1, cols):
            # Score based on gap, match, or mismatch
            if seq1[i-1] == '-' or seq2[j-1] == '-':
                match = score_matrix[i-1][j-1] + gap_penalty
            else:
                match = score_matrix[i-1][j-1] + scoring_matrix.get(seq1[i-1], {}).get(seq2[j-1], gap_penalty)

            delete = score_matrix[i-1][j] + gap_penalty
            insert = score_matrix[i][j-1] + gap_penalty

            score = max(match, delete, insert)
            if local:
                score = max(0, score)
            score_matrix[i][j] = score

            if local and score > max_score:
                max_score = score
                max_pos = (i, j)

            if score == match:
                traceback_matrix[i][j] = 'diag'
            elif score == delete:
                traceback_matrix[i][j] = 'up'
            else:
                traceback_matrix[i][j] = 'left'
            if local and score == 0:
                traceback_matrix[i][j] = None

    print(score_matrix)
    return score_matrix, traceback_matrix, max_pos


def traceback(seq1, seq2, traceback_matrix, local=False, max_pos=None):
    '''
    This function computes the traceback in the matrices
    '''
    aligned_seq1 = []
    aligned_seq2 = []
    
    if local:
        i, j = max_pos
    else:
        i, j = len(seq1), len(seq2)

    # check global vs local
    while i > 0 or j > 0:
        if traceback_matrix[i][j] == 'diag':
            aligned_seq1.append(seq1[i-1])
            aligned_seq2.append(seq2[j-1])
            i -= 1
            j -= 1
        elif traceback_matrix[i][j] == 'up':
            aligned_seq1.append(seq1[i-1])
            aligned_seq2.append('-')
            i -= 1
        elif traceback_matrix[i][j] == 'left':
            aligned_seq1.append('-')
            aligned_seq2.append(seq2[j-1])
            j -= 1
        else:
            break  # if local: stop when we reach a cell with score 0
    
    return ''.join(reversed(aligned_seq1)), ''.join(reversed(aligned_seq2))

def calculate_identity(aligned_seq1, aligned_seq2):
    '''
    This function calculates the sequence identity. This is to tell how similar the sequences are
    '''
    matches = sum(1 for a, b in zip(aligned_seq1, aligned_seq2) if a == b and a != '-')
    total_residues = sum(1 for a, b in zip(aligned_seq1, aligned_seq2) if a != '-' and b != '-')
    return matches / total_residues * 100 if total_residues > 0 else 0

def main():
    # parse the arguments
    parser = argparse.ArgumentParser(description="Sequence alignment using dynamic programming")
    parser.add_argument('--seq1', required=True, help="FASTA file for sequence 1")
    parser.add_argument('--seq2', required=True, help="FASTA file for sequence 2")
    parser.add_argument('--type', required=True, choices=['global', 'local'], help="Type of alignment: global or local")
    parser.add_argument('--matrix', required=True, choices=['blosum62', 'pam250'], help="Scoring matrix to use")
    parser.add_argument('--gap_penalty', required=True, type=int, help="Gap penalty (negative integer)")
    args = parser.parse_args()

    seq1 = read_fasta(args.seq1)
    seq2 = read_fasta(args.seq2)

    scoring_matrix = BLOSUM62 if args.matrix == 'blosum62' else PAM250

    if args.type == 'global':
        aligned_seq1, aligned_seq2, score_matrix = global_alignment(seq1, seq2, gap_penalty=args.gap_penalty)
    else:
        score_matrix, traceback_matrix, max_pos = create_score_matrix(seq1, seq2, scoring_matrix, args.gap_penalty, local=True)
        aligned_seq1, aligned_seq2 = traceback(seq1, seq2, traceback_matrix, local=True, max_pos=max_pos)

    if args.type == 'global':
        alignment_score = score_matrix[len(seq1)][len(seq2)]
    else:
        alignment_score = score_matrix[max_pos[0]][max_pos[1]]

    identity = calculate_identity(aligned_seq1, aligned_seq2)

    print(f"Alignment:\n{aligned_seq1}\n{aligned_seq2}")
    print(f"Alignment Score: {alignment_score}")
    print(f"Sequence Identity: {identity:.2f}%")

if __name__ == "__main__":
    main()

