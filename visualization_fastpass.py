"""
Richard Stoiberer - CMS 380 - Dr. Myers

FastPass+ Results Visualization

This script visualizes the results of the FastPass+ system simulation.
It plots residence times for both FastPass and regular customers as a
function of the FastPass allocation fraction.
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_fastpass_results(results_file=None):
    """
    Plot FastPass+ simulation results
    
    If results_file is provided, loads results from the file.
    Otherwise, uses pre-defined results for demonstration.
    """
    # Use pre-defined results if no file is provided
    # These are results from a previous run of the simulation
    fractions = np.array([0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45,
                         0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95])
    
    # Low utilization results (λ = 0.5)
    low_fp_times = np.array([0, 1.493, 1.512, 1.591, 1.558, 1.542, 1.635, 1.587, 
                             1.596, 1.690, 1.635, 1.663, 1.693, 1.763, 1.764, 
                             1.834, 1.801, 1.822, 1.955, 1.911])
    low_reg_times = np.array([1.944, 2.031, 2.034, 2.127, 2.129, 2.042, 2.252, 
                              2.169, 2.166, 2.377, 2.268, 2.320, 2.370, 2.396, 
                              2.606, 2.642, 2.523, 2.642, 2.738, 2.630])

    # High utilization results (λ = 0.95)
    high_fp_times = np.array([0, 1.974, 2.096, 2.129, 2.209, 2.288, 2.358, 2.469, 
                              2.520, 2.675, 2.852, 2.984, 3.248, 3.425, 4.022, 
                              4.230, 4.810, 5.560, 7.752, 9.236])
    high_reg_times = np.array([27.804, 14.780, 30.476, 30.850, 26.111, 39.608, 
                               32.452, 32.148, 29.321, 25.677, 58.659, 28.527, 
                               49.362, 46.552, 65.308, 64.304, 79.345, 83.357, 
                               211.362, 121.572])

    # Create figure with two subplots
    fig, axes = plt.subplots(2, 1, figsize=(10, 12))
    
    # Plot for low utilization (λ = 0.5)
    ax = axes[0]
    ax.plot(fractions, low_fp_times, 'b-o', label='FastPass Customers')
    ax.plot(fractions, low_reg_times, 'r-o', label='Regular Customers')
    
    # Add theoretical M/M/1 time
    theoretical_mm1_time_low = 1 / (1 - 0.5)
    ax.axhline(y=theoretical_mm1_time_low, color='g', linestyle='--', 
              label=f'M/M/1 Time: {theoretical_mm1_time_low:.2f}')
    
    # Add labels and title
    ax.set_xlabel('FastPass Fraction (f)')
    ax.set_ylabel('Average Residence Time (minutes)')
    ax.set_title('Residence Times vs. FastPass Fraction (λ=0.5)')
    ax.grid(True)
    ax.legend()
    ax.set_ylim(0, 5)  # Set y-axis limits for better visualization
    
    # Plot for high utilization (λ = 0.95)
    ax = axes[1]
    ax.plot(fractions, high_fp_times, 'b-o', label='FastPass Customers')
    ax.plot(fractions, high_reg_times, 'r-o', label='Regular Customers')
    
    # Add theoretical M/M/1 time
    theoretical_mm1_time_high = 1 / (1 - 0.95)
    ax.axhline(y=theoretical_mm1_time_high, color='g', linestyle='--', 
               label=f'M/M/1 Time: {theoretical_mm1_time_high:.2f}')
    
    # Add labels and title
    ax.set_xlabel('FastPass Fraction (f)')
    ax.set_ylabel('Average Residence Time (minutes)')
    ax.set_title('Residence Times vs. FastPass Fraction (λ=0.95)')
    ax.grid(True)
    ax.legend()
    ax.set_ylim(0, 100)  # Set y-axis limits
    
    plt.tight_layout()
    plt.savefig('fastpass_results.png')
    plt.show()
    
    # Return the figure for further modification if needed
    return fig

if __name__ == "__main__":
    plot_fastpass_results()