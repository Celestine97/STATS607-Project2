
# visualizations based on simulation results

from save_files import load_all_simulation_results
from visualization import (
    plot_figure1_reproduction, 
    plot_power_heatmap, 
    plot_fdr_control_diagnostic,
)

if __name__ == "__main__":
    
    m_values = [4, 8, 16, 32, 64]
    null_proportions = [0.75, 0.50, 0.25, 0.0]
    distributions = ['D', 'E', 'I']

    all_results = load_all_simulation_results('generated_data/')
    
    # Generate visualizations
    plot_figure1_reproduction(all_results,distributions, null_proportions, m_values)
    plot_power_heatmap(all_results,distributions, null_proportions, m_values)
    plot_fdr_control_diagnostic(all_results,distributions, null_proportions, m_values)
    
    print("All complete.")