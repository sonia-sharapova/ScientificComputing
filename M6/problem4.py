import os
import sys
import numpy as np
from scipy.stats import chi2
from PIL import Image
import matplotlib.pyplot as plt

class Steganalysis:
    '''
    A class to analyze if an image has been modified  using LSB steganography.
    '''
    def __init__(self, image_path):
        self.image = Image.open(image_path).convert("RGB")  # Use RGB channels
        self.pixels = np.array(self.image)
        
    def extract_lsb_matrix(self):
        '''
        Extract the LSBs of each color channel in the image.
        '''
        red_lsb = self.pixels[:, :, 0] & 1
        green_lsb = self.pixels[:, :, 1] & 1
        blue_lsb = self.pixels[:, :, 2] & 1
        return red_lsb, green_lsb, blue_lsb

    def visualize_lsb(self, output_path):
        '''
        Create an enhanced visualization of LSBs
         - set LSB=1 to 255 and LSB=0 to 0.
        '''
        red_lsb, green_lsb, blue_lsb = self.extract_lsb_matrix()
        enhanced_image = np.stack([red_lsb * 255, green_lsb * 255, blue_lsb * 255], axis=-1)
        
        lsb_image = Image.fromarray(enhanced_image.astype(np.uint8))
        lsb_image.save(output_path)  # Save enhanced LSB visualization

    def chi_square_test(self):
        '''
        Perform a Chi-square test on the LSBs of each color channel.
        '''
        red_lsb, green_lsb, blue_lsb = self.extract_lsb_matrix()
        
        chi_square_stat, p_values = [], []
        
        for lsb_matrix in [red_lsb, green_lsb, blue_lsb]:
            observed_freq = np.bincount(lsb_matrix.flatten(), minlength=2)
            expected_freq = np.array([observed_freq.sum() / 2] * 2)
            chi_stat = np.sum((observed_freq - expected_freq) ** 2 / expected_freq)
            p_value = chi2.sf(chi_stat, df=1)
            chi_square_stat.append(chi_stat)
            p_values.append(p_value)
        
        return chi_square_stat, p_values

    def is_encoded(self):
        '''
        Determine if the image is likely encoded using Chi-square and entropy threshold.
        '''
        chi_square_stat, p_values = self.chi_square_test()
        encoded = all(p < 0.05 for p in p_values)  # Threshold: significant at p < 0.05
        return encoded, chi_square_stat, p_values

def analyze_images(directory_path, output_file, enhanced_output_dir):
    
    results = []
    
    # Ensure the enhanced output directory exists
    os.makedirs(enhanced_output_dir, exist_ok=True)

    for file_name in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file_name)
        if file_name.lower().endswith('.png'):
            try:
                steganalysis = Steganalysis(file_path)
                
                # Save the enhanced LSB image
                enhanced_output_path = os.path.join(enhanced_output_dir, f"{file_name}_enhanced_lsb.png")
                steganalysis.visualize_lsb(enhanced_output_path)
                
                # Perform chi-square analysis
                encoded, chi_square_stat, p_values = steganalysis.is_encoded()
                
                # Append results
                result = "true" if encoded else "false"
                results.append((file_name, result))
                
                print(f"{file_name}: Encoded={encoded}, Chi-Square Stats={chi_square_stat}, p-values={p_values}")
            
            # Ensure the program does not crash on error
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
                results.append((file_name, "error"))

    # Write results to output file
    with open(output_file, 'w') as f:
        for file_name, encoded in results:
            f.write(f"{file_name} | {encoded}\n")

if __name__ == "__main__":
    # Set the directory path and output file
    directory_path = "./project/2024_steganography"
    output_file = "steganography_results.csv"
    enhanced_output_dir = "images/project_images"

    # local:
    # directory_path = "images/og"
    # utput_file = "images/results/steganography_results.csv"
    # enhanced_output_dir = "images/enhanced_lsb_images"

    # Analyze images and write results
    analyze_images(directory_path, output_file, enhanced_output_dir)

