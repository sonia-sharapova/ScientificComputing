def find_cpg_islands(sequence, window_size=200, step_size=1):
    """
    Fnction to identify CpG islands in the first third of a sequence based on GC content and Obs/Exp ratio.
    A CpG island has GC content > 50% and Obs/Exp ratio > 0.6.
    """
    cpg_islands = []
    first_third = len(sequence) // 3

    for start in range(0, first_third - window_size + 1, step_size):
        window = sequence[start:start + window_size]
        gc_content = (window.count('G') + window.count('C')) / len(window) * 100
        obs_exp_ratio = (window.count('CG') / ((window.count('C') * window.count('G')) / len(window))) if len(window) > 0 else 0

        if gc_content > 50 and obs_exp_ratio > 0.6:
            cpg_islands.append((start, start + window_size))
    
    return cpg_islands
