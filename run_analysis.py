import numpy as np
from config import create_config
from simulation import run_simulation, get_summary_statistics

if __name__ == "__main__":
    
    # # Run quick example
    # results = run_quick_example()

    # Store all results for later comparison
    all_results = {}

    # Run simulations with different parameters
    for m in [4, 8]:
        for m0_proportion in [0.75, 0.50, 0.25]:
            m0 = int(m * m0_proportion)
            
            # Create configuration
            config = create_config(m=m, m0=m0, distribution='E', L=5.0, n_reps=1000)
            
            # Run simulation
            results = run_simulation(config, show_progress=True)
            
            # Store with descriptive key
            key = (m, m0, 'E')  # (total, nulls, distribution)
            all_results[key] = results
            
            print(f"m={m}, m0={m0}: Power = {np.mean(results['power_bh']):.3f}")

    # Later, access specific results
    results_32_16 = all_results[(8, 4, 'E')]
    print(f"\nResults for m=32, m0=16:")
    print(get_summary_statistics(results_32_16))
    
    print("\n✓ Simulation complete!")