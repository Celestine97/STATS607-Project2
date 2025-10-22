# Benjamini-Hochberg Simulation Study

Reproduction and extension of Benjamini & Hochberg (1995) "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing"

## Project Overview

This project implements a simulation study comparing three multiple testing procedures:
- **Bonferroni correction** (controls FWER)
- **Hochberg's procedure** (controls FWER)
- **Benjamini-Hochberg procedure** (controls FDR)

The simulation uses advanced variance reduction techniques to estimate power and false discovery rates across configurations.

## Project Structure
```
project2/
├── README.md
├── requirements.txt
├── Makefile
├── ADEMP.md
├── ANALYSIS.md
│
├── config.py                    # Configuration management
├── data_generation.py           # Data generating functions
├── simulation.py                # Simulation functions
├── visualization.py             # Plotting functions
├── save_files.py                # Result saving and loading utilities
├── run_simulations.py           # Simulation script
├── run_analysis.py              # Analysis script
├── run_visualization.py         # Visualization script
│
├── test.py                      # Test functions
│
├── generated_data/              # Saved simulation raw results
│   └── sim_*.pkl
├── results/                     # Summary statistics
│   ├── power_comparison_*.csv
│   ├── fdr_control_*.csv
│   └── complete_summary_*.csv
└── figures/                     # Visualizations
    ├── figure1_reproduction.png
    └── power_heatmap.png
    └── fdr_diagnostic.png
```

## To run the simulation

### Setup Environment
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Test
```bash
make test
```

### Execution
```bash
make all

# or
python run_simulations.py    # Run simulations
python run_analysis.py        # Analyze
python run_visualization.py   # Visualize
```


## Makefile Commands

| Command | Description |
|---------|-------------|
| `make all` | Run complete pipeline (install, test, simulate, analyze, figures) |
| `make install` | Install Python dependencies |
| `make test` | Run pytest test suite |
| `make simulate` | Run full simulations (20,000 replications) |
| `make analyze` | Generate summary statistics and tables |
| `make figures` | Create all visualizations |
| `make clean` | Remove generated files |


## Key Findings
- **Power Advantage**: The Benjamini-Hochberg procedure gains more power gains over Bonferroni and Hoshberg's methods.
- **FDR Control**: BH successfully controls the False Discovery Rate at target level across all simulation conditions, with empirical FDR consistently below the threshold.