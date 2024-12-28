import sys
import os
import json
from multiprocessing import Pool

def load_words_json(file_path):
    '''
    Function to load the set of English words from a JSON file. 
    (contained a list)
    '''    
    with open(file_path, 'r') as file:
        words_list = json.load(file)
    return set(words_list)  # Convert the list directly to a set

def load_common_words(file_path):
    '''Loads a set of common English words from a text file.'''
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

def find_common_words(sequence, english_words, common_words):
    '''Finds common English words in a given sequence.'''
    possible_words = set()
    for i in range(len(sequence)):
        for j in range(i + 2, len(sequence) + 1):  # Minimum word length of 2
            word = sequence[i:j]
            if word in english_words and word in common_words:
                possible_words.add(word)
    return possible_words

def process_stride(args):
    '''Processes a single stride and writes results to a file.'''
    text, stride, english_words, common_words, output_path = args
    sequence = extract_els_sequence(text, stride)
    words_found = find_common_words(sequence, english_words, common_words)

    # Write results to a file in the specified output path
    with open(output_path, 'w') as f:
        f.write("Stride: {}\n".format(stride))
        f.write("Sequence: {}\n".format(sequence))
        f.write("Common Words: {}\n".format(', '.join(sorted(words_found))))

    return "Results for {} written to {}".format(output_path, output_path)

def create_output_path(stride, file_name):
    '''Creates the output file path based on the stride and text file name.'''
    base_dir = "./strides"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    # Map file name to shorter, descriptive suffix
    if file_name == "moby-dick.txt":
        suffix = "moby"
    elif file_name == "war-and-peace.txt":
        suffix = "warandpeace"
    elif file_name == "kjb-bible.txt":
        suffix = "bible"
    else:
        suffix = os.path.splitext(file_name)[0]

    return os.path.join(base_dir, "stride-{}-{}.txt".format(stride, suffix))

if __name__ == "__main__":
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python els_parallel.py <stride>")
        sys.exit(1)

    # Load files from command line arguments
    stride = int(sys.argv[1])

    # Define paths for text files and the word dictionary
    word_dict_file = "../data/books/words_dictionary.json"
    text_files = [
        "../data/books/moby-dick.txt",
        "../data/books/war-and-peace.txt",
        "../data/books/kjb-bible.txt"
    ]

    # Load English words from the JSON dictionary and common words
    english_words = load_words_json(word_dict_file)
    common_words_file = '../data/books/google-10000-english-usa.txt'
    common_words = load_common_words(common_words_file)

    # Set up multiprocessing pool to process each file combination with the given stride
    tasks = []
    for text_file in text_files:
        # Load the text
        text = load_text(text_file)
        
        # Create tasks for each file with the provided stride
        output_path = create_output_path(stride, os.path.basename(text_file))
        tasks.append((text, stride, english_words, common_words, output_path))

    # Run tasks in parallel
    pool = Pool()
    results = pool.map(process_stride, tasks)
    pool.close()
    pool.join()

    # Print completion messages
    for result in results:
        print(result)
