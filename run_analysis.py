import numpy as np
from config import create_config
from simulation import run_simulation, get_summary_statistics
from visualization import plot_figure1_reproduction, plot_power_heatmap, plot_fdr_control_diagnostic

if __name__ == "__main__":
    

    # Store all results for later comparison
    all_results = {}

    # parameters for the simulations
    m_values = [4, 8, 16, 32, 64]
    null_proportions = [0.75, 0.50, 0.25, 0]
    distributions = ['D', 'E', 'I']

    # Run simulations with different parameters
    for m in m_values:
        for m0_proportion in null_proportions:
            for distribution in distributions:
                m0 = int(m * m0_proportion)
                
                # Create configuration
                config = create_config(m=m, m0=m0, distribution=distribution, L=5.0, n_reps=1000, seed=12345)
                
                # Run simulation
                results = run_simulation(config, show_progress=True)
                
                # Store with descriptive key
                key = (m, m0, distribution)  # (total, nulls, distribution)
                all_results[key] = results
                
                print(f"m={m}, m0={m0}, dist={distribution}: Power = {np.mean(results['power_bh']):.3f}, FDR = {np.mean(results['fdr_bh']):.3f}")

    # plot_figure1_reproduction(all_results,distributions, null_proportions, m_values)
    # plot_power_heatmap(all_results,distributions, null_proportions, m_values)
    plot_fdr_control_diagnostic(all_results)

    # access specific results
    results_32_16 = all_results[(32, 16, 'E')]
    print(f"\nResults for m=32, m0=16:")
    print(get_summary_statistics(results_32_16))
    
    print("\n✓ Simulation complete!")