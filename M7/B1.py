import subprocess



query = '~/../../project2/mpcs56430/db/query_sequence.fasta'

bd_path = '~/../../project2/mpcs56430/db/refseq'

command = f"time -p blastp -query {query} -db {bd_path} -num_threads 16 -out problem1.out"
result = subprocess.run(command, shell=True)
print(result)

