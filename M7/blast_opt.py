import os
import subprocess
import re
import pandas as pd
#import matplotlib.pyplot as plt

# Define threads and files
threads = [1, 2, 4, 6, 8, 16, 32]
files = ['ndm1.fasta', 'spike.fasta', 'protein1.fasta']

# Data storage
runtime_data = {
    "Database": [],
    "File": [],
    "Threads": [],
    "Runtime": []
}

# Function to parse `real` time from the command output
def parse_time(output):
    match = re.search(r"real\s+(\d+)m([\d.]+)s", output)
    if match:
        minutes = int(match.group(1))
        seconds = float(match.group(2))
        return minutes * 60 + seconds
    match_seconds = re.search(r"real\s+([\d.]+)", output)
    if match_seconds:
        return float(match_seconds.group(1))
    return None

# Run BLAST and capture runtime
for fts in files:
    #print(f"Running for {fts}:")
    for i in threads:
        for db in ['pdbaa', 'swissprot']:
            #print(f"Running for {db} with {i} threads:")
            
            # Prepare command with /usr/bin/time to ensure the output is captured
            command = f"/usr/bin/time -p blastp -query assets/{fts} -db db/{db} -num_threads {i} -out blast_out/{db}/{fts}_{i}.out"
            
            # Run command and capture output
            result = subprocess.run(command, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
            
            # Debug: print stderr to see the output of /usr/bin/time
            #print("Command STDERR:", result.stderr)
            
            # Extract runtime from stderr
            runtime = parse_time(result.stderr)
            #print(f"Parsed Runtime: {runtime}")  # Debugging the parsed runtime
            if runtime is not None:
                runtime_data["Database"].append(db)
                runtime_data["File"].append(fts)
                runtime_data["Threads"].append(i)
                runtime_data["Runtime"].append(runtime)


# Convert data to DataFrame
df = pd.DataFrame(runtime_data)

# Save data to CSV for future use
df.to_csv("blastp_runtime_data.csv", index=False)



#~/../../project/mpcs56430/bioinformatics/pdbaa/pdbaa.fasta
# time blastp -query '~/../../project/mpcs56430/bioinformatics/swissprot/swissprot.fasta' -db '~/../../project2/mpcs56430/db/swissprot' -num_threads 1 -out problem_1/swiss_1.out

#pdbaa_file = '~/../../project/mpcs56430/bioinformatics/pdbaa/pdbaa.fasta'
#swissprot_file = '/project/mpcs56430/bioinformatics/swissprot/swissprot.fasta'

#sp = '../../../../../../project/mpcs56430/bioinformatics/swissprot/swissprot.fasta'
#db = '../../../../../../project2/mpcs56430/db/swissprot'
#out = 'problem_1/swiss_1.out'
#_file = 'downloads/pdbaa.fasta'
#s_file = 'downloads/swissprot.fasta'
