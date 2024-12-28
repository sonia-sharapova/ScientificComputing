from scipy.stats import entropy
import numpy as np
from PIL import Image
import sys
from problem1 import LSBEncoder

class LSBSteganalysis:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.pixels = np.array(self.image)

    def extract_lsb_matrix(self):
        '''
        For each pixel, keep only the least significant bit (LSB) and ignore the other bits. Use this to create a binary matrix. 
        '''
        lsb_matrix = self.pixels & 1
        avg = lsb_matrix.mean(axis=2)  # Averaging across color channels
        return avg

    def compute_metrics(self, lsb_matrix):
        '''
        Calculate statistical metrics that can indicate non-random patterns within the LSB matrix. 
        '''
        flat_lsb = lsb_matrix.flatten()
        
        # Entropy
        lsb_entropy = entropy(np.bincount(flat_lsb.astype(int)))

        # Mean
        lsb_mean = np.mean(flat_lsb)
        
        # Variance
        lsb_variance = np.var(flat_lsb)

        return lsb_mean, lsb_variance, lsb_entropy

    def analyze_blocks(self, lsb_matrix, block_size=8):
        '''
        Divide the LSB matrix into blocks and compute frequencies of 1s and 0s.
        '''
        h, w = lsb_matrix.shape
        block_frequencies = []
        
        for i in range(0, h, block_size):
            for j in range(0, w, block_size):
                block = lsb_matrix[i:i+block_size, j:j+block_size]
                freq = np.mean(block)
                block_frequencies.append(freq)
        
        return np.mean(block_frequencies), np.var(block_frequencies)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python problem3.py <image_path>")
    else:
        image_path = sys.argv[1]

        # Get image
        steganalysis = LSBSteganalysis(image_path)

        # Extract LSB Matrix
        lsb_matrix = steganalysis.extract_lsb_matrix()

        # Compute Metrics
        lsb_mean, lsb_variance, lsb_entropy = steganalysis.compute_metrics(lsb_matrix)
        block_mean, block_variance = steganalysis.analyze_blocks(lsb_matrix)

        print(f"LSB Mean: {lsb_mean}, LSB Variance: {lsb_variance}, LSB Entropy: {lsb_entropy}")
        # if lsb_entropy < 0.9 or abs(lsb_mean - 0.5) > 0.1 or lsb_variance < 0.02:
        #abs(lsb_mean - 0.5) > 0.05 or lsb_variance < 0.01
        if abs(lsb_mean - 0.5) > 0.05 or lsb_variance < 0.01:
            print("LSB Steganography Detected")
        else:
            print("No LSB Steganography Detected")

