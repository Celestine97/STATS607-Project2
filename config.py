def create_config(m, m0, distribution, L=5.0, alpha=0.05, n_reps=20000, seed=12345):
    """
    Create configuration dictionary for simulation.
    
    Parameters:
    -----------
    m : int
        Total number of hypotheses
    m0 : int
        Number of true nulls
    distribution : str
        'D' (Decreasing), 'E' (Equal), 'I' (Increasing)
    L : float
        Signal strength parameter
    alpha : float
        Significance level
    n_reps : int
        Number of simulation replications
    seed : int
        Random seed
    
    Returns:
    --------
    config : dict
        Configuration dictionary
    """
    m1 = m - m0
    assert m0 + m1 == m, "m0 + m1 must equal m"
    assert distribution in ['D', 'E', 'I'], "distribution must be D, E, or I"
    
    config = {
        'm': m,
        'm0': m0,
        'm1': m1,
        'distribution': distribution,
        'L': L,
        'alpha': alpha,
        'n_reps': n_reps,
        'seed': seed
    }
    
    return config