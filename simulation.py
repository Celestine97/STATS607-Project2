import numpy as np
from tqdm import tqdm
import pickle
import json
import os
from datetime import datetime
from statistical_methods import compute_pvalues, bonferroni_method, hochberg_method, benjamini_hochberg_method
from performance_metrics import compute_power, compute_fdr
from data_generation import generate_alternative_means


def save_simulation_results(results, config, output_dir='generated_data/'):
    """
    Save simulation results.
    
    Parameters:
    -----------
    results : dict
        Results dictionary from run_simulation
    config : dict
        Configuration dictionary
    output_dir : str
        Directory to save results
    
    Returns:
    --------
    filepath : str
        Path to saved file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Create descriptive filename
    m = config['m']
    m0 = config['m0']
    dist = config['distribution']
    L = config['L']
    n_reps = config['n_reps']
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"sim_m{m}_m0{m0}_{dist}_L{L}_n{n_reps}_{timestamp}.pkl"
    filepath = os.path.join(output_dir, filename)
    
    # Save as pickle (preserves all data)
    with open(filepath, 'wb') as f:
        pickle.dump({
            'config': config,
            'results': results
        }, f)
    
    print(f"Saved results to: {filepath}")
    return filepath



def run_simulation_with_base_data(config, base_data, show_progress=True, save_results=True):
    """
    Run simulation using pre-generated base data.
    
    This ensures the SAME random noise is used across configurations
    with the same m, implementing variance reduction.
    
    Parameters:
    -----------
    config : dict
        Configuration dictionary
    base_data : np.ndarray
        Pre-generated standard normal data (n_reps, m)
    show_progress : bool
        Whether to show progress bar
    
    Returns:
    --------
    results : dict
        Dictionary with all results arrays
    """
    
    n_reps, m = base_data.shape
    assert m == config['m'], f"Base data has m={m}, config has m={config['m']}"
    assert n_reps == config['n_reps'], f"Base data has {n_reps} reps, config has {config['n_reps']}"
    
    # Generate the means (same for all replications)
    m0 = config['m0']
    m1 = config['m1']
    means = np.zeros(m)
    
    if m1 > 0:
        alt_means = generate_alternative_means(m1, config['L'], config['distribution'])
        means[m0:] = alt_means
    
    # True nulls indicator (same for all replications)
    true_nulls = np.arange(m) < m0
    
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
        # Use the SAME base random data, just add the means!
        # data = means + base_noise
        data = means + base_data[rep, :]
        
        # Compute p-values
        pvalues = compute_pvalues(data)
        
        # Apply all three methods to same data
        rej_bonf = bonferroni_method(pvalues, config['alpha'])
        rej_hoch = hochberg_method(pvalues, config['alpha'])
        rej_bh = benjamini_hochberg_method(pvalues, config['alpha'])
        
        # Compute performance metrics
        power_bonf[rep] = compute_power(rej_bonf, true_nulls)
        power_hoch[rep] = compute_power(rej_hoch, true_nulls)
        power_bh[rep] = compute_power(rej_bh, true_nulls)
        
        fdr_bonf[rep] = compute_fdr(rej_bonf, true_nulls)
        fdr_hoch[rep] = compute_fdr(rej_hoch, true_nulls)
        fdr_bh[rep] = compute_fdr(rej_bh, true_nulls)
    
    # Return results
    results = {
        'config': config,
        'power_bonf': power_bonf,
        'power_hoch': power_hoch,
        'power_bh': power_bh,
        'fdr_bonf': fdr_bonf,
        'fdr_hoch': fdr_hoch,
        'fdr_bh': fdr_bh
    }

    # Save if requested
    if save_results:
        save_simulation_results(results, config)
    
    return results


def load_all_simulation_results(output_dir='generated_data'):
    """
    Load all simulation results from a directory.
    
    Parameters:
    -----------
    output_dir : str
        Directory containing saved results
    
    Returns:
    --------
    all_results : dict
        Dictionary with keys (m, m0, dist) and values as result dicts
    """
    from simulation import load_simulation_results
    
    # Find all .pkl files
    pattern = os.path.join(output_dir, 'sim_*.pkl')
    files = glob.glob(pattern)
    
    if not files:
        raise FileNotFoundError(f"No simulation files found in {output_dir}/")
    
    print(f"\nLoading {len(files)} simulation results...")
    
    all_results = {}
    
    for filepath in sorted(files):
        # Load individual result
        config, results = load_simulation_results(filepath)
        
        # Create key
        m = config['m']
        m0 = config['m0']
        dist = config['distribution']
        key = (m, m0, dist)
        
        # Store
        all_results[key] = results
        
        print(f"  ✓ Loaded: m={m}, m0={m0}, {dist}")
    
    print(f"\n✓ Loaded {len(all_results)} configurations")
    
    return all_results