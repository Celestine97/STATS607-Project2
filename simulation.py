import numpy as np
from tqdm import tqdm
from data_generation import generate_data
from statistical_methods import compute_pvalues, bonferroni_method, hochberg_method, benjamini_hochberg_method
from performance_metrics import compute_power, compute_fdr
import pandas as pd

def run_single_replication(config, rng):
    """
    Run a single replication of the simulation.
    
    Uses variance reduction trick: all methods see same data!
    
    Parameters:
    -----------
    config : dict
        Configuration dictionary
    rng : np.random.Generator
        Random number generator with fixed seed
    
    Returns:
    --------
    results : dict
        Results for this replication
    """
    # Generate data once (variance reduction!)
    data, true_nulls = generate_data(config, rng)
    
    # Compute p-values (same for all methods)
    pvalues = compute_pvalues(data)
    
    # Apply all three methods to same data
    rej_bonf = bonferroni_method(pvalues, config['alpha'])
    rej_hoch = hochberg_method(pvalues, config['alpha'])
    rej_bh = benjamini_hochberg_method(pvalues, config['alpha'])
    
    # Compute performance metrics
    results = {
        'power_bonf': compute_power(rej_bonf, true_nulls),
        'power_hoch': compute_power(rej_hoch, true_nulls),
        'power_bh': compute_power(rej_bh, true_nulls),
        'fdr_bonf': compute_fdr(rej_bonf, true_nulls),
        'fdr_hoch': compute_fdr(rej_hoch, true_nulls),
        'fdr_bh': compute_fdr(rej_bh, true_nulls)
    }
    
    return results


def run_simulation(config, show_progress=True):
    """
    Run complete simulation for a given configuration.
    
    Parameters:
    -----------
    config : dict
        Configuration dictionary
    show_progress : bool
        Whether to show progress bar
    
    Returns:
    --------
    results : dict
        Dictionary with all results arrays
    """
    # Initialize random number generator
    rng = np.random.default_rng(config['seed'])
    
    n_reps = config['n_reps']
    
    # Storage for results
    power_bonf = np.zeros(n_reps)
    power_hoch = np.zeros(n_reps)
    power_bh = np.zeros(n_reps)
    fdr_bonf = np.zeros(n_reps)
    fdr_hoch = np.zeros(n_reps)
    fdr_bh = np.zeros(n_reps)
    
    # Run replications
    iterator = range(n_reps)
    if show_progress:
        desc = f"m={config['m']}, {config['distribution']}, {config['m1']}/{config['m']} alt"
        iterator = tqdm(iterator, desc=desc)
    
    for rep in iterator:
        rep_results = run_single_replication(config, rng)
        
        power_bonf[rep] = rep_results['power_bonf']
        power_hoch[rep] = rep_results['power_hoch']
        power_bh[rep] = rep_results['power_bh']
        fdr_bonf[rep] = rep_results['fdr_bonf']
        fdr_hoch[rep] = rep_results['fdr_hoch']
        fdr_bh[rep] = rep_results['fdr_bh']
    
    # Return as dictionary
    results = {
        'config': config,
        'power_bonf': power_bonf,
        'power_hoch': power_hoch,
        'power_bh': power_bh,
        'fdr_bonf': fdr_bonf,
        'fdr_hoch': fdr_hoch,
        'fdr_bh': fdr_bh
    }
    
    return results


def get_summary_statistics(results):
    """
    Compute summary statistics from results.
    
    Parameters:
    -----------
    results : dict
        Results dictionary from run_simulation
    
    Returns:
    --------
    summary : pd.DataFrame
        Summary statistics
    """
    data = {
        'Method': ['Bonferroni', 'Hochberg', 'BH'],
        'Mean_Power': [
            np.nanmean(results['power_bonf']),
            np.nanmean(results['power_hoch']),
            np.nanmean(results['power_bh'])
        ],
        'Mean_FDR': [
            np.mean(results['fdr_bonf']),
            np.mean(results['fdr_hoch']),
            np.mean(results['fdr_bh'])
        ],
    }
    
    return pd.DataFrame(data)