import LSBEncoder
import sys
from PIL import Image
import numpy as np

class EnhancedLSBSteganalysis:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.pixels = np.array(self.image)
    
    def enhance_lsb(self):
        enhanced_pixels = (self.pixels & 1) * 255  # Only keep LSBs and amplify them
        enhanced_image = Image.fromarray(enhanced_pixels.astype('uint8'))
        return enhanced_image


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python LSBEncoder.py <image_path> <text> <output_path><enhanced_path>")
    else:
        image_path = sys.argv[1]
        text = sys.argv[2]
        output_path = sys.argv[3]
        enhanced_path = sys.argv[4]
        
        encoder = LSBEncoder(image_path)
        encoder.encode(text, output_path)

        # Enhance the LSBs of the encoded image
        enhancer = EnhancedLSBSteganalysis(output_path)
        enhanced_lsb_image = enhancer.enhance_lsb()
        enhanced_lsb_image.save(enhanced_path)

        print(f"Message encoded in {output_path}, enhanced image saved to {enhanced_path}\n")

        # Decode the message to verify
        decoder = LSBEncoder(output_path)
        extracted_message = decoder.decode()

        # missing last character
        print(f"\nOriginal Message:\n- {text}\n\nExtracted Message:\n- {extracted_message}\n")



