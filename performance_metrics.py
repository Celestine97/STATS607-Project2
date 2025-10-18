import numpy as np


def compute_power(rejections, true_nulls):
    """
    Compute average power.
    
    Parameters:
    -----------
    rejections : np.ndarray
        Boolean array of rejections
    true_nulls : np.ndarray
        Boolean array of true nulls
    
    Returns:
    --------
    power : float
        Average power
    """
    false_nulls = ~true_nulls
    n_false_nulls = false_nulls.sum()
    
    if n_false_nulls == 0:
        return np.nan
    
    true_positives = (rejections & false_nulls).sum()
    power = true_positives / n_false_nulls
    return power


def compute_fdr(rejections, true_nulls):
    """
    Compute realized FDR for this replication.
    
    Parameters:
    -----------
    rejections : np.ndarray
        Boolean array of rejections
    true_nulls : np.ndarray
        Boolean array of true nulls
    
    Returns:
    --------
    fdr : float
        Realized FDR
    """
    R = rejections.sum()
    V = (rejections & true_nulls).sum()
    
    if R == 0:
        return 0.0
    
    return V / R


def compute_fwer(rejections, true_nulls):
    """
    Compute FWER indicator.
    
    Parameters:
    -----------
    rejections : np.ndarray
        Boolean array of rejections
    true_nulls : np.ndarray
        Boolean array of true nulls
    
    Returns:
    --------
    fwer : float
        1.0 if any Type I error, else 0.0
    """
    V = (rejections & true_nulls).sum()
    return 1.0 if V >= 1 else 0.0