import sys

def load_english_words(file_path):
    '''
    Function to load the set of English words from a JSON file. 
    (contained a list)
    '''
    with open(file_path, 'r') as file:
        return set(line.strip().lower() for line in file)

def load_text(file_path):
    '''
    Function to load and preprocesses text from a file.
    '''
    with open(file_path, 'r') as file:
        full_text = file.read()
        full_text = full_text.replace(" ", "").replace("\n", "").lower()
        return full_text

def extract_els_sequence(text, stride):
    '''Given a text, this function extracts characters from at a given stride'''
    sequence = ''.join([text[i] for i in range(0, len(text), stride)])
    return sequence

def find_words(sequence, english_words):
    '''Finds common English words in a given sequence.'''
    possible_words = set()
    for i in range(len(sequence)):
        for j in range(i + 2, len(sequence) + 1):  # Minimum word length of 2
            word = sequence[i:j]
            if word in english_words:
                possible_words.add(word)
    return possible_words

def run_els_algorithm(text, strides, english_words):
    results = {}
    for stride in strides:
        sequence = extract_els_sequence(text, stride)
        words_found = find_words(sequence, english_words)
        results[stride] = {
            'sequence': sequence,
            'words': sorted(words_found)
        }
    return results

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) != 3:
        print("Usage: python els_algorithm.py <text_file> <english_words_file>")
        sys.exit(1)

    # Load files from command line arguments
    text_file = sys.argv[1]
    english_words_file = sys.argv[2]

    # Load text and English words
    text = load_text(text_file)
    english_words = load_english_words(english_words_file)

    # Define strides
    strides = [2, 3, 4]

    # Run ELS algorithm and display results
    results = run_els_algorithm(text, strides, english_words)
    for stride, result in results.items():
        print(f"Stride: {stride}")
        print(f"Sequence: {result['sequence']}")
        print(f"Words: {', '.join(result['words'])}\n")
