import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV
data_file = "blastp_runtime_data.csv"
df = pd.read_csv(data_file)

def plot_runtime(dataframe, sequence, database, output_dir="plots"):
    """
    Plots runtime vs threads for a specific sequence and database and saves as a PNG.

    Args:
        dataframe (pd.DataFrame): The dataframe containing runtime data.
        sequence (str): The sequence filename (e.g., 'ndm1.fasta').
        database (str): The database name (e.g., 'pdbaa' or 'swissprot').
        output_dir (str): Directory to save the plots.

    Returns:
        None
    """
    subset = dataframe[(dataframe['File'] == sequence) & (dataframe['Database'] == database)]
    if not subset.empty:
        plt.plot(subset['Threads'], subset['Runtime'], marker='o', label=f"{sequence} ({database})")
        plt.xlabel("Number of Threads")
        plt.ylabel("Runtime (seconds)")
        plt.title(f"Runtime vs Threads for {sequence} ({database})")
        plt.legend(loc="best")
        plt.grid(True)
        
        # Save the plot
        filename = f"{output_dir}/{sequence}_{database}_runtime.png"
        plt.savefig(filename)
        print(f"Plot saved: {filename}")
        plt.close()

def plot_all(dataframe, output_file="plots/all_runtime.png"):
    """
    Plots runtime vs threads for all combinations of sequences and databases and saves as a PNG.

    Args:
        dataframe (pd.DataFrame): The dataframe containing runtime data.
        output_file (str): Filepath to save the combined plot.

    Returns:
        None
    """
    for sequence in dataframe['File'].unique():
        for database in dataframe['Database'].unique():
            subset = dataframe[(dataframe['File'] == sequence) & (dataframe['Database'] == database)]
            if not subset.empty:
                plt.plot(subset['Threads'], subset['Runtime'], marker='o', label=f"{sequence} ({database})")
    plt.xlabel("Number of Threads")
    plt.ylabel("Runtime (seconds)")
    plt.title("Runtime vs Threads for All Sequences and Databases")
    plt.legend(loc="best")
    plt.grid(True)
    
    # Save the plot
    plt.savefig(output_file)
    print(f"Combined plot saved: {output_file}")
    plt.close()

# Example Usage
# Plot for a specific sequence and database
#plot_runtime(df, 'ndm1.fasta', 'pdbaa', output_dir="plots")

# Plot for all sequences and databases
plot_all(df, output_file="plots/all_runtime.png")
