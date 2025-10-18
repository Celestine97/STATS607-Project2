import numpy as np


def generate_alternative_means(m1, L, distribution):
    """
    Generate means for false null hypotheses.
    
    Parameters:
    -----------
    m1 : int
        Number of false null hypotheses
    L : float
        Signal strength parameter
    distribution : str
        'D', 'E', or 'I'
    
    Returns:
    --------
    means : np.ndarray
        Array of means for false nulls
    """
    if m1 == 0:
        return np.array([])
    
    # Four signal levels
    levels = np.array([L/4, L/2, 3*L/4, L])
    
    if distribution == 'D':  # Decreasing
        weights = np.array([4, 3, 2, 1])
        counts = np.round(weights / weights.sum() * m1).astype(int)
        
    elif distribution == 'E':  # Equal
        counts = np.repeat(m1 // 4, 4)
        counts[:m1 % 4] += 1
        
    elif distribution == 'I':  # Increasing
        weights = np.array([1, 2, 3, 4])
        counts = np.round(weights / weights.sum() * m1).astype(int)
    
    # Adjust to ensure exact sum
    diff = m1 - counts.sum()
    if diff != 0:
        counts[-1] += diff
    
    # Create means array
    means = []
    for level, count in zip(levels, counts):
        means.extend([level] * count)
    
    return np.array(means)


def generate_data(config, rng):
    """
    Generate data for one replication.
    
    Parameters:
    -----------
    config : dict
        Configuration dictionary
    rng : np.random.Generator
        Random number generator
    
    Returns:
    --------
    data : np.ndarray
        Generated data
    true_nulls : np.ndarray
        Boolean array indicating true nulls
    """
    m = config['m']
    m0 = config['m0']
    m1 = config['m1']
    L = config['L']
    distribution = config['distribution']
    
    # Generate means
    means = np.zeros(m)
    
    if m1 > 0:
        alt_means = generate_alternative_means(m1, L, distribution)
        means[m0:] = alt_means
    
    # Generate data: X_i ~ N(mu_i, 1)
    data = rng.normal(loc=means, scale=1.0, size=m)
    
    # Track which are truly null
    true_nulls = np.arange(m) < m0
    
    return data, true_nulls