
"""
Richard Stoiberer - CMS 380 - Dr. Myers

FastPass+ System Simulation
This simulation models a two-class priority queueing system representing Disney's FastPass+

The system models:
- Two customer classes: FastPass holders (high priority) and regular customers (low priority)
- An M/M/1 queue with exponential service and arrival times
- FastPass holders always enter service before regular customers
- The impact of different FastPass allocation percentages on customer wait times
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import heapq

# Constants and configuration
SIMULATION_TIME = 50000  # Total simulation time (minutes)
WARM_UP_TIME = 5000      # Warm-up period before collecting statistics (minutes)
SERVICE_RATE = 1.0       # Service rate (μ = 1 customer per minute)

# Event types
ARRIVAL = 'arrival'
DEPARTURE = 'departure'

# Customer types
FASTPASS = 'fastpass'
REGULAR = 'regular'

class Event:
    """Event in the discrete-event simulation"""
    def __init__(self, time, event_type, customer=None):
        self.time = time
        self.type = event_type
        self.customer = customer
    
    def __lt__(self, other):
        """Comparison operator for priority queue based on event time"""
        return self.time < other.time

class Customer:
    """Customer in the queueing system"""
    def __init__(self, customer_type, arrival_time):
        self.type = customer_type
        self.arrival_time = arrival_time
        self.departure_time = None
        
    @property
    def residence_time(self):
        """Calculate total time spent in the system (waiting + service)"""
        if self.departure_time is None:
            return None
        return self.departure_time - self.arrival_time

def generate_exponential(rate):
    """Generate exponentially distributed random number with given rate"""
    return np.random.exponential(1.0 / rate)

def simulate_fastpass_system(arrival_rate, fastpass_fraction):
    """
    Simulates a FastPass+ priority queue system with the given parameters
    
    Args:
        arrival_rate: Total arrival rate (λ)
        fastpass_fraction: Fraction of customers with FastPass (f)
        
    Returns:
        Dictionary with statistics about the simulation run
    """
    # Initialize state
    current_time = 0.0
    server_busy = False
    server_end_time = 0.0
    
    # Queues for waiting customers
    fastpass_queue = deque()
    regular_queue = deque()
    
    # Event queue (priority queue)
    event_queue = []
    
    # Statistics
    stats = {
        FASTPASS: {
            'total_customers': 0,
            'completed_customers': 0,
            'total_residence_time': 0.0,
            'avg_residence_time': 0.0,
            'max_residence_time': 0.0
        },
        REGULAR: {
            'total_customers': 0,
            'completed_customers': 0,
            'total_residence_time': 0.0,
            'avg_residence_time': 0.0,
            'max_residence_time': 0.0
        }
    }
    
    # Define start_service function inside the simulate_fastpass_system scope
    def start_service(time):
        """Start serving the next customer (with priority to FastPass holders)"""
        nonlocal server_busy, server_end_time
        
        # FastPass customers have priority
        if fastpass_queue:
            customer = fastpass_queue.popleft()
        elif regular_queue:
            customer = regular_queue.popleft()
        else:
            return  # No customers to serve
        
        # Mark server as busy
        server_busy = True
        
        # Generate service time (exponentially distributed)
        service_time = generate_exponential(SERVICE_RATE)
        server_end_time = time + service_time
        
        # Schedule departure
        heapq.heappush(event_queue, Event(server_end_time, DEPARTURE, customer))
    
    # Schedule the first arrival
    first_arrival_time = generate_exponential(arrival_rate)
    heapq.heappush(event_queue, Event(first_arrival_time, ARRIVAL))
    
    # Main simulation loop
    while event_queue and current_time < SIMULATION_TIME:
        # Get the next event
        event = heapq.heappop(event_queue)
        current_time = event.time
        
        if event.type == ARRIVAL:
            # Handle arrival event
            customer_type = FASTPASS if np.random.random() < fastpass_fraction else REGULAR
            
            # Create new customer
            customer = Customer(customer_type, current_time)
            
            # Track total customers
            stats[customer_type]['total_customers'] += 1
            
            # Add customer to appropriate queue
            if customer_type == FASTPASS:
                fastpass_queue.append(customer)
            else:
                regular_queue.append(customer)
            
            # Schedule next arrival
            next_arrival_time = current_time + generate_exponential(arrival_rate)
            heapq.heappush(event_queue, Event(next_arrival_time, ARRIVAL))
            
            # If server is idle, start service immediately
            if not server_busy:
                start_service(current_time)
                
        elif event.type == DEPARTURE:
            # Handle departure event
            server_busy = False
            
            # Record departure time for the customer
            event.customer.departure_time = current_time
            
            # Only collect statistics after warm-up period
            if current_time > WARM_UP_TIME:
                customer_type = event.customer.type
                residence_time = event.customer.residence_time
                
                stats[customer_type]['completed_customers'] += 1
                stats[customer_type]['total_residence_time'] += residence_time
                stats[customer_type]['max_residence_time'] = max(
                    stats[customer_type]['max_residence_time'], residence_time
                )
            
            # If there are customers waiting, start serving the next one
            if fastpass_queue or regular_queue:
                start_service(current_time)
    
    # Calculate final statistics
    for customer_type in [FASTPASS, REGULAR]:
        if stats[customer_type]['completed_customers'] > 0:
            stats[customer_type]['avg_residence_time'] = (
                stats[customer_type]['total_residence_time'] / 
                stats[customer_type]['completed_customers']
            )
    
    return stats


def run_experiments(arrival_rates, fastpass_fractions):
    """
    Run simulation experiments for different arrival rates and FastPass fractions
    
    Args:
        arrival_rates: List of arrival rates to test
        fastpass_fractions: List of FastPass fractions to test
        
    Returns:
        Dictionary with results for each experiment
    """
    results = {}
    
    for arrival_rate in arrival_rates:
        results[arrival_rate] = {
            'fastpass_times': [],
            'regular_times': [],
            'fractions': fastpass_fractions
        }
        
        for fraction in fastpass_fractions:
            print(f"Running simulation with λ={arrival_rate}, f={fraction}")
            stats = simulate_fastpass_system(arrival_rate, fraction)
            
            # Store average residence times
            results[arrival_rate]['fastpass_times'].append(stats[FASTPASS]['avg_residence_time'])
            results[arrival_rate]['regular_times'].append(stats[REGULAR]['avg_residence_time'])
    
    return results

def plot_results(results, arrival_rates):
    """Plot residence times as a function of FastPass fraction"""
    fig, axes = plt.subplots(len(arrival_rates), 1, figsize=(10, 5 * len(arrival_rates)))
    
    if len(arrival_rates) == 1:
        axes = [axes]
    
    for i, arrival_rate in enumerate(arrival_rates):
        ax = axes[i]
        result = results[arrival_rate]
        
        # Plot residence times
        ax.plot(result['fractions'], result['fastpass_times'], 'b-o', label='FastPass Customers')
        ax.plot(result['fractions'], result['regular_times'], 'r-o', label='Regular Customers')
        
        # Add labels and title
        ax.set_xlabel('FastPass Fraction (f)')
        ax.set_ylabel('Average Residence Time (minutes)')
        ax.set_title(f'Residence Times vs. FastPass Fraction (λ={arrival_rate})')
        ax.grid(True)
        ax.legend()
        
        # Add baseline M/M/1 waiting time
        theoretical_mm1_time = 1 / (1 - arrival_rate)
        ax.axhline(y=theoretical_mm1_time, color='g', linestyle='--', 
                   label=f'M/M/1 Time: {theoretical_mm1_time:.2f}')
        
        # Set y-axis limits
        if arrival_rate == 0.95:
            ax.set_ylim(0, 100)
    
    plt.tight_layout()
    return fig

def main():
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Define experiment parameters
    arrival_rates = [0.5, 0.95]  # Low and high utilization
    fastpass_fractions = np.linspace(0, 0.95, 20)  # Range of FastPass fractions to test
    
    # Run experiments
    results = run_experiments(arrival_rates, fastpass_fractions)
    
    # Plot results
    fig = plot_results(results, arrival_rates)
    plt.savefig('fastpass_results.png')
    plt.show()
    
    # Print recommendations
    for arrival_rate in arrival_rates:
        print(f"\nResults for λ={arrival_rate}:")
        result = results[arrival_rate]
        
        # Find good operating point based on results
        # (This is a simple approach - the actual recommendation would depend on business criteria)
        # We'll look for the highest fraction where regular customers' time is less than twice the M/M/1 time
        theoretical_mm1_time = 1 / (1 - arrival_rate)
        threshold = 2.5 * theoretical_mm1_time
        
        good_fractions = []
        for i, fraction in enumerate(result['fractions']):
            regular_time = result['regular_times'][i]
            fastpass_time = result['fastpass_times'][i]
            
            if regular_time < threshold and not np.isnan(fastpass_time) and not np.isnan(regular_time):
                good_fractions.append((fraction, fastpass_time, regular_time))
        
        if good_fractions:
            best_fraction = max(good_fractions, key=lambda x: x[0])
            print(f"Recommended FastPass fraction: {best_fraction[0]:.2f}")
            print(f"  - FastPass residence time: {best_fraction[1]:.2f} minutes")
            print(f"  - Regular residence time: {best_fraction[2]:.2f} minutes")
            print(f"  - Regular/FastPass time ratio: {best_fraction[2]/best_fraction[1]:.2f}")
        else:
            print("No good operating point found under the criteria.")

if __name__ == "__main__":
    main()