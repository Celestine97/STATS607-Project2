# Makefile for the simulation project

.PHONY: all simulate analyze figures clean test help install

# Default
all: 
	@echo "Results will be saved to:"
	@echo "  - results/all_results_*.pkl"
	@echo "  - figures/*.png"
	@echo ""

# Install required packages
install:
	@echo "Installing required packages..."
	pip install -r requirements.txt
	@echo "✓ Installation complete"

# Run tests
test:
	@echo ""
	@echo "Running test suite..."
	pytest test.py

# Run simulations and save raw results
simulate_and_visualize:
	@echo ""
	@echo "Running simulations..."
	@echo ""
	python run_analysis.py
	@echo "Simulations complete"

# Quick test run (fewer replications)
quick_test:
	@echo ""
	@echo "Running quick test (n_reps=100)..."
	python run_toy_analysis.py
	echo ""
	@echo "Quick test complete"

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	rm -rf results/*.pkl
	rm -rf results/*.csv
	rm -rf results/raw/*.pkl
	rm -rf results/numpy/*.npz
	rm -rf figures/*.png
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	@echo "✓ Cleanup complete"

# Deep clean (including cache and dependencies)
distclean: clean
	@echo "Deep cleaning..."
	rm -rf venv
	rm -rf .venv
	rm -rf *.egg-info
	@echo "✓ Deep cleanup complete"

# Show help
help:
	@echo ""
	@echo "Benjamini-Hochberg Simulation Study - Makefile"
	@echo "=============================================="
	@echo ""
	@echo "Available targets:"
	@echo ""
	@echo "  make all        - Run complete pipeline (install, test, simulate, analyze, figures)"
	@echo "  make install    - Install required Python packages"
	@echo "  make test       - Run test suite with pytest"
	@echo "  make simulate   - Run simulations and save raw results"
	@echo "  make analyze    - Process results and generate summary statistics"
	@echo "  make figures    - Create all visualizations"
	@echo "  make quick      - Quick test run with fewer replications"
	@echo "  make clean      - Remove generated files (results, figures, cache)"
	@echo "  make distclean  - Remove everything including virtual environment"
	@echo "  make help       - Show this help message"
	@echo ""
	@echo "Typical workflow:"
	@echo "  1. make install     # First time setup"
	@echo "  2. make test        # Verify implementation"
	@echo "  3. make simulate    # Run full simulations (slow!)"
	@echo "  4. make figures     # Generate plots"
	@echo ""
	@echo "Or simply:"
	@echo "  make all           # Does everything"
	@echo ""