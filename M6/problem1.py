import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import sys

class LSBEncoder:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.pixels = np.array(self.image)
        self.height, self.width, _ = self.pixels.shape

    def text_to_bits(self, text):
        '''
        This function converts a string of text into a sequence of binary bits.

        Input: 
            text (str): The message to be encoded

        Returns:
            binary_text (str): the text in binary
        '''
        in_bin = [format(ord(c), '08b') for c in text]
        binary_text = ''.join(in_bin)
        return binary_text

    def bits_to_text(self, bits):
        '''
        This function converts a sequence of binary bits back into readable text.

        Input: 
            bits (str): The binary bits to be converted back to text.

        Returns:
            text (str): the readable text
        '''
        chars = [chr(int(bits[i:i+8], 2)) for i in range(0, len(bits), 8)] # reads every 8 bits as one char and converts to ASCII
        text = ''.join(chars)
        return text

    def encode(self, text, output_path):
        '''
        This function encodes a given text message into the image’s least significant bits and saves the modified image.
        
        Inputs:
            text (str): The message to hide within the image.
            output_path (str): The file path where the new encoded image will be saved.
        
        Returns:
            output_path: encoded image.
        '''
        # Convert the text to binary bits.
        bits = self.text_to_bits(text) + '00000000'  # Add a null byte as a terminator
        required_pixels = len(bits) + 1

        # Check if there’s enough space in the image to store the message.
        if required_pixels > self.width * self.height * 3:
            raise ValueError("Image does not contain enough bytes to encode the data.")
        
        flat_pixels = self.pixels.flatten().astype(np.uint8)  # Ensure uint8 type for each pixel value

        # Encode each bit of the message into the LSB of each pixel.
        for i, bit in enumerate(bits):
            # Cast each pixel as an int to avoid overflow, modify LSB, then cast back to uint8
            pixel_value = int(flat_pixels[i]) & ~1 | int(bit)
            flat_pixels[i] = np.uint8(pixel_value)  # Safely cast back to uint8
        
        encoded_pixels = flat_pixels.reshape(self.pixels.shape)
        encoded_image = Image.fromarray(encoded_pixels.astype('uint8'))
        encoded_image.save(output_path) # Save modified image to output_path.
        return output_path


    def decode(self):
        '''
        This function extracts the hidden text message from the LSBs of the image.
         
        Returns:
            message (str): The encoded message
        '''
        # Read each pixel’s LSB to reconstruct the hidden binary bits.
        flat_pixels = self.pixels.flatten()
        bits = ''.join([str(flat_pixels[i] & 1) for i in range(self.width * self.height * 3)])

        # Stop reading at a null byte (end of the message)
        null_terminator = bits.find('00000000')
        if null_terminator != -1:
            bits = bits[:null_terminator]

        # Converts the binary bits back into readable text 
        message = self.bits_to_text(bits)
        return message

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python LSBEncoder.py <image_path> <text> <output_path>")
    else:
        image_path = sys.argv[1]
        text = sys.argv[2]
        output_path = sys.argv[3]
        
        encoder = LSBEncoder(image_path)
        encoder.encode(text, output_path)
        print(f"Message encoded in {output_path}")

        # Decode the message
        decoder = LSBEncoder(output_path)
        extracted_message = decoder.decode()

        print(f"\nOriginal Message:\n- {text}\n\nExtracted Message:\n- {extracted_message}\n")


