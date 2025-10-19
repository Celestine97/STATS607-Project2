"""
Enhanced Visualization Functions for BH Simulation Study
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality style
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9



def plot_figure1_reproduction(all_results, 
                             distributions,
                             null_proportions,
                             m_values,
                             save_path='figures/figure1_reproduction.png'):
    """
    Reproduce Figure 1 from the paper with customizable parameters.
    
    Creates a grid: len(null_proportions) rows × len(distributions) columns
    Each panel shows power vs. m for the three methods.
    
    Parameters:
    -----------
    all_results : dict
        Dictionary of all simulation results
    distributions : list of str
        Which distributions to plot (subset of ['D', 'E', 'I'])
    null_proportions : list of float
        Which null proportions to plot (subset of [0.0, 0.25, 0.50, 0.75])
    m_values : list of int
        Which m values to include (subset of [4, 8, 16, 32, 64])
    save_path : str
        Path to save the figure
    
    Examples:
    ---------
    # Full figure (like the paper)
    plot_figure1_reproduction(all_results)
    
    # Only Equal distribution, 50% and 25% null
    plot_figure1_reproduction(all_results, 
                             distributions=['E'],
                             null_proportions=[0.50, 0.25])
    
    # All distributions but only m=16,32,64
    plot_figure1_reproduction(all_results,
                             m_values=[16, 32, 64])
    """
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Distribution names for titles
    dist_names = {'D': 'Decreasing', 'E': 'Equal', 'I': 'Increasing'}
    
    # Calculate figure size based on number of panels
    n_rows = len(null_proportions)
    n_cols = len(distributions)
    fig = plt.figure(figsize=(4 * n_cols, 3.5 * n_rows))
    
    # Create equal-spaced positions for m values
    positions = np.arange(len(m_values))
    
    # Loop through conditions
    for row_idx, null_prop in enumerate(null_proportions):
        for col_idx, dist in enumerate(distributions):
            # Create subplot
            ax = plt.subplot(n_rows, n_cols, row_idx * n_cols + col_idx + 1)
            
            # Collect power values for each m
            powers_bonf = []
            powers_hoch = []
            powers_bh = []
            ses_bonf = []
            ses_hoch = []
            ses_bh = []
            
            for m in m_values:
                m0 = int(m * null_prop)
                key = (m, m0, dist)
                
                if key in all_results:
                    result = all_results[key]
                    
                    # Mean power
                    powers_bonf.append(np.nanmean(result['power_bonf']))
                    powers_hoch.append(np.nanmean(result['power_hoch']))
                    powers_bh.append(np.nanmean(result['power_bh']))
                    
                    # Standard errors
                    n = len(result['power_bonf'])
                    ses_bonf.append(np.nanstd(result['power_bonf']) / np.sqrt(n))
                    ses_hoch.append(np.nanstd(result['power_hoch']) / np.sqrt(n))
                    ses_bh.append(np.nanstd(result['power_bh']) / np.sqrt(n))
                else:
                    # Missing data - use NaN
                    powers_bonf.append(np.nan)
                    powers_hoch.append(np.nan)
                    powers_bh.append(np.nan)
                    ses_bonf.append(0)
                    ses_hoch.append(0)
                    ses_bh.append(0)
            
            # Convert to arrays
            powers_bonf = np.array(powers_bonf)
            powers_hoch = np.array(powers_hoch)
            powers_bh = np.array(powers_bh)
            ses_bonf = np.array(ses_bonf)
            ses_hoch = np.array(ses_hoch)
            ses_bh = np.array(ses_bh)
            
            # Plot with equal spacing on x-axis
            ax.plot(positions, powers_bonf, 'o:', label='Bonferroni', 
                   color='#1f77b4', linewidth=2, markersize=5, alpha=0.8)
            ax.fill_between(positions, powers_bonf - 1.96*ses_bonf, 
                          powers_bonf + 1.96*ses_bonf, alpha=0.15, color='#1f77b4')
            
            ax.plot(positions, powers_hoch, 's--', label='Hochberg', 
                   color='#ff7f0e', linewidth=2, markersize=5, alpha=0.8)
            ax.fill_between(positions, powers_hoch - 1.96*ses_hoch, 
                          powers_hoch + 1.96*ses_hoch, alpha=0.15, color='#ff7f0e')
            
            ax.plot(positions, powers_bh, '^-', label='BH', 
                   color='#2ca02c', linewidth=2.5, markersize=6, alpha=0.9)
            ax.fill_between(positions, powers_bh - 1.96*ses_bh, 
                          powers_bh + 1.96*ses_bh, alpha=0.2, color='#2ca02c')
            
            # Set x-ticks with equal spacing
            ax.set_xticks(positions)
            ax.set_xticklabels(m_values)
            ax.set_xlim([-0.3, len(positions) - 0.7])
            
            # Formatting
            ax.set_ylim([0, 1.05])
            ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
            ax.set_axisbelow(True)
            
            # Labels (only on edges)
            if row_idx == n_rows - 1:  # Bottom row
                ax.set_xlabel('Number of Hypotheses (m)', fontweight='bold', fontsize=11)
            if col_idx == 0:  # Left column
                ax.set_ylabel('Average Power', fontweight='bold', fontsize=11)
            
            # Title (top row only)
            if row_idx == 0:
                ax.set_title(f'{dist_names[dist]}', fontweight='bold', fontsize=12)
            
            # Left annotation (proportion of nulls)
            if col_idx == 0:
                null_pct = int(null_prop * 100)
                ax.text(-0.20, 0.5, f'{null_pct}% Null', 
                       transform=ax.transAxes, fontsize=11,
                       rotation=90, va='center', ha='center',
                       fontweight='bold')
            
            # Legend (only on top right panel)
            if row_idx == 0 and col_idx == n_cols - 1:
                ax.legend(loc='lower left', framealpha=0.95, 
                         edgecolor='gray', fancybox=True, fontsize=9)
    
    plt.tight_layout()
    
    # Adjust spacing
    if n_cols > 1 and n_rows > 1:
        plt.subplots_adjust(left=0.08, right=0.98, top=0.96, bottom=0.05)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Figure saved to {save_path}")
    
    plt.show()


def plot_power_heatmap(all_results, 
                             distributions,
                             null_proportions,
                             m_values,
                             save_path='figures/power_heatmap.png'):
    """
    PUBLICATION FIGURE: Heatmap showing BH power advantage over Bonferroni.
    
    Shows the absolute gain in power (BH - Bonferroni) across all conditions.
    """
    fig, axes = plt.subplots(1, 3, figsize=(15, 6))
    
    dist_names = {'D': 'Decreasing', 'E': 'Equal', 'I': 'Increasing'}
    
    for col_idx, dist in enumerate(distributions):
        ax = axes[col_idx]
        
        # Build matrix: rows=null_prop, cols=m
        power_gain = np.zeros((len(null_proportions), len(m_values)))
        
        for i, null_prop in enumerate(null_proportions):
            for j, m in enumerate(m_values):
                m0 = int(m * null_prop)
                key = (m, m0, dist)
                
                if key in all_results:
                    result = all_results[key]
                    power_bh = np.nanmean(result['power_bh'])
                    power_bonf = np.nanmean(result['power_bonf'])
                    power_gain[i, j] = power_bh - power_bonf
                else:
                    power_gain[i, j] = np.nan
        
        # Create heatmap
        im = ax.imshow(power_gain, cmap='RdYlGn', aspect='auto', 
              vmin=0, vmax=0.4, interpolation='nearest')
        
        # Add text annotations
        for i in range(len(null_proportions)):
            for j in range(len(m_values)):
                if not np.isnan(power_gain[i, j]):
                    text = ax.text(j, i, f'{power_gain[i, j]:.2f}',
                                 ha="center", va="center", 
                                 color="black" if power_gain[i, j] < 0.25 else "white",
                                 fontsize=9, fontweight='bold')
        
        # Set ticks and labels
        ax.set_xticks(np.arange(len(m_values)))
        ax.set_yticks(np.arange(len(null_proportions)))
        ax.set_xticklabels(m_values)
        ax.set_yticklabels([f'{int(p*100)}%' for p in null_proportions])
        
        ax.set_xlabel('Number of Hypotheses (m)', fontweight='bold')
        if col_idx == 0:
            ax.set_ylabel('Proportion of True Nulls', fontweight='bold')
        
        ax.set_title(f'{dist_names[dist]} Distribution', fontweight='bold', fontsize=12)
        
        # Grid
        ax.set_xticks(np.arange(len(m_values))-0.5, minor=True)
        ax.set_yticks(np.arange(len(null_proportions))-0.5, minor=True)
        ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)
    
    # Add colorbar
    fig.subplots_adjust(right=0.9)
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    cbar = fig.colorbar(im, cax=cbar_ax)
    cbar.set_label('Power Gain (BH - Bonferroni)', rotation=270, 
                   labelpad=20, fontweight='bold')
    
    plt.suptitle('BH Power Advantage Over Bonferroni Across All Conditions', 
                fontsize=14, fontweight='bold', y=0.98)
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Figure saved to {save_path}")
    
    plt.show()



def plot_fdr_control_diagnostic(all_results, save_path='fdr_diagnostic.png'):
    """
    DIAGNOSTIC FIGURE: Verify that BH controls FDR at the nominal level.
    
    Shows empirical FDR for all methods across conditions.
    """
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(3, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    distributions = ['D', 'E', 'I']
    dist_names = {'D': 'Decreasing', 'E': 'Equal', 'I': 'Increasing'}
    m_values = [4, 8, 16, 32, 64]
    null_proportions = [0.75, 0.50, 0.25]
    
    for col_idx, dist in enumerate(distributions):
        for row_idx, null_prop in enumerate(null_proportions):
            ax = fig.add_subplot(gs[row_idx, col_idx])
            
            # Collect FDR values
            fdrs_bonf = []
            fdrs_hoch = []
            fdrs_bh = []
            
            for m in m_values:
                m0 = int(m * null_prop)
                key = (m, m0, dist)
                
                if key in all_results:
                    result = all_results[key]
                    fdrs_bonf.append(np.mean(result['fdr_bonf']))
                    fdrs_hoch.append(np.mean(result['fdr_hoch']))
                    fdrs_bh.append(np.mean(result['fdr_bh']))
                else:
                    fdrs_bonf.append(np.nan)
                    fdrs_hoch.append(np.nan)
                    fdrs_bh.append(np.nan)
            
            # Plot
            ax.plot(m_values, fdrs_bonf, 'o:', label='Bonferroni', 
                   color='#1f77b4', linewidth=2, markersize=6)
            ax.plot(m_values, fdrs_hoch, 's--', label='Hochberg', 
                   color='#ff7f0e', linewidth=2, markersize=6)
            ax.plot(m_values, fdrs_bh, '^-', label='BH', 
                   color='#2ca02c', linewidth=2, markersize=7)
            
            # Nominal level line
            ax.axhline(y=0.05, color='red', linestyle='--', 
                      linewidth=2, alpha=0.7, label='Nominal (α=0.05)')
            
            # Formatting
            ax.set_xlabel('Number of Hypotheses (m)')
            ax.set_ylabel('Empirical FDR')
            ax.set_xticks(m_values)
            ax.set_ylim([0, 0.08])
            ax.grid(True, alpha=0.3)
            
            # Title
            if row_idx == 0:
                ax.set_title(f'{dist_names[dist]}', fontweight='bold')
            
            # Left label
            if col_idx == 0:
                ax.text(-0.35, 0.5, f'{int(null_prop*100)}% Null', 
                       transform=ax.transAxes, rotation=90, 
                       va='center', ha='center', fontweight='bold')
            
            # Legend
            if row_idx == 0 and col_idx == 2:
                ax.legend(loc='upper left', fontsize=8, framealpha=0.95)
    
    plt.suptitle('FDR Control Verification: All Methods Stay Below Nominal Level', 
                fontsize=14, fontweight='bold')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✓ Figure saved to {save_path}")
    
    plt.show()
