import numpy as np
from scipy import stats

def compute_pvalues(data):
    """
    Compute two-sided p-values for z-tests.
    
    Parameters:
    -----------
    data : np.ndarray
        Observed data
    
    Returns:
    --------
    pvalues : np.ndarray
        Two-sided p-values
    """
    pvalues = 2 * (1 - stats.norm.cdf(np.abs(data)))
    return pvalues


def bonferroni_method(pvalues, alpha=0.05):
    """
    Bonferroni multiple testing procedure.
    
    Parameters:
    -----------
    pvalues : np.ndarray
        P-values for all hypotheses
    alpha : float
        Significance level
    
    Returns:
    --------
    rejections : np.ndarray
        Boolean array indicating rejections
    """
    m = len(pvalues)
    threshold = alpha / m
    rejections = pvalues <= threshold
    return rejections


def hochberg_method(pvalues, alpha=0.05):
    """
    Hochberg (1988) step-up multiple testing procedure.
    
    Parameters:
    -----------
    pvalues : np.ndarray
        P-values for all hypotheses
    alpha : float
        Significance level
    
    Returns:
    --------
    rejections : np.ndarray
        Boolean array indicating rejections
    """
    m = len(pvalues)
    
    # Sort p-values
    sorted_indices = np.argsort(pvalues)
    sorted_pvalues = pvalues[sorted_indices]
    
    # Find largest i where P_(i) <= alpha/(m+1-i)
    k = 0
    for i in range(m-1, -1, -1):
        if sorted_pvalues[i] <= alpha / (m + 1 - (i+1)):
            k = i + 1
            break
    
    # Reject all hypotheses up to k
    rejections = np.zeros(m, dtype=bool)
    if k > 0:
        rejections[sorted_indices[:k]] = True
    
    return rejections


def benjamini_hochberg_method(pvalues, q=0.05):
    """
    Benjamini-Hochberg (1995) FDR controlling procedure.
    
    Parameters:
    -----------
    pvalues : np.ndarray
        P-values for all hypotheses
    q : float
        FDR level to control
    
    Returns:
    --------
    rejections : np.ndarray
        Boolean array indicating rejections
    """
    m = len(pvalues)
    
    # Sort p-values
    sorted_indices = np.argsort(pvalues)
    sorted_pvalues = pvalues[sorted_indices]
    
    # Find largest i where P_(i) <= (i/m)*q
    k = 0
    for i in range(m-1, -1, -1):
        if sorted_pvalues[i] <= ((i+1) / m) * q:
            k = i + 1
            break
    
    # Reject all hypotheses up to k
    rejections = np.zeros(m, dtype=bool)
    if k > 0:
        rejections[sorted_indices[:k]] = True
    
    return rejections