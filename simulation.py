import numpy as np
import matplotlib.pyplot as plt
from load_balancer import RoundRobinLoadBalancer, LeastConnectionLoadBalancer, WeightedRoundRobinLoadBalancer
import time
import pandas as pd
from typing import Dict, List
import json
import os

def set_random_seed(seed: int = 42):
    """Set random seed for reproducibility"""
    np.random.seed(seed)

def generate_requests(num_requests: int, distribution: str = 'normal', **kwargs) -> np.ndarray:
    """Generate request loads with different distributions"""
    if distribution == 'normal':
        return np.random.normal(kwargs.get('mean', 1.0), kwargs.get('std', 0.5), num_requests)
    elif distribution == 'exponential':
        return np.random.exponential(kwargs.get('scale', 1.0), num_requests)
    elif distribution == 'uniform':
        return np.random.uniform(kwargs.get('low', 0.5), kwargs.get('high', 1.5), num_requests)
    else:
        raise ValueError(f"Unknown distribution: {distribution}")

def run_simulation(balancer, requests: np.ndarray) -> dict:
    """Run simulation with given load balancer and requests"""
    balancer.reset()  # Reset the load balancer state
    start_time = time.time()
    
    for request in requests:
        balancer.assign_request(request)
    
    end_time = time.time()
    metrics = balancer.get_load_metrics()
    metrics['execution_time'] = end_time - start_time
    
    return metrics

def plot_results(results: dict, title: str, save_path: str = None):
    """Plot simulation results with enhanced visualization"""
    plt.figure(figsize=(15, 10))
    
    # Plot server loads
    plt.subplot(2, 2, 1)
    server_loads = results['server_loads']
    plt.bar(range(len(server_loads)), server_loads)
    plt.title('Server Loads Distribution')
    plt.xlabel('Server Index')
    plt.ylabel('Load')
    
    # Plot load distribution
    plt.subplot(2, 2, 2)
    plt.hist(server_loads, bins=20, alpha=0.7)
    plt.title('Load Distribution Histogram')
    plt.xlabel('Load')
    plt.ylabel('Frequency')
    
    # Plot metrics
    plt.subplot(2, 2, 3)
    metrics = results['metrics']
    plt.bar(metrics.keys(), metrics.values())
    plt.title('Load Balancing Metrics')
    plt.xticks(rotation=45)
    
    # Plot balance score
    plt.subplot(2, 2, 4)
    plt.bar(['Balance Score'], [metrics['balance_score']])
    plt.title('Load Balance Score')
    plt.ylim(0, 1)
    
    plt.tight_layout()
    plt.suptitle(title)
    
    if save_path:
        plt.savefig(save_path)
    plt.show()

def analyze_results(all_results: Dict[str, List[Dict]]) -> pd.DataFrame:
    """Analyze and compare results from different algorithms"""
    analysis_data = []
    
    for balancer_name, results in all_results.items():
        for result in results:
            for dist_name, metrics in result.items():
                analysis_data.append({
                    'Algorithm': balancer_name,
                    'Distribution': dist_name,
                    'Mean Load': metrics['mean_load'],
                    'Std Load': metrics['std_load'],
                    'Balance Score': metrics['balance_score'],
                    'Requests/sec': metrics['requests_per_second'],
                    'Execution Time': metrics['execution_time']
                })
    
    df = pd.DataFrame(analysis_data)
    return df

def save_results(results: Dict, filename: str):
    """Save simulation results to file"""
    os.makedirs('results', exist_ok=True)
    with open(f'results/{filename}.json', 'w') as f:
        json.dump(results, f, indent=4)

def main():
    # Set random seed for reproducibility
    set_random_seed(42)
    
    # Simulation parameters
    num_servers = 5
    num_requests = 1000
    num_runs = 5  # Run multiple times to ensure reliability
    
    # Create results directory
    os.makedirs('results', exist_ok=True)
    
    # Generate requests with different distributions
    distributions = {
        'Normal Distribution': lambda: generate_requests(num_requests, 'normal', mean=1.0, std=0.5),
        'Exponential Distribution': lambda: generate_requests(num_requests, 'exponential', scale=1.0),
        'Uniform Distribution': lambda: generate_requests(num_requests, 'uniform', low=0.5, high=1.5)
    }
    
    # Initialize load balancers
    balancers = {
        'Round Robin': RoundRobinLoadBalancer(num_servers),
        'Least Connection': LeastConnectionLoadBalancer(num_servers),
        'Weighted Round Robin': WeightedRoundRobinLoadBalancer(num_servers, weights=[1, 2, 3, 2, 1])
    }
    
    # Store all results
    all_results = {name: [] for name in balancers.keys()}
    
    # Run simulations multiple times
    for run in range(num_runs):
        print(f"\nRun {run + 1}/{num_runs}")
        
        for dist_name, request_generator in distributions.items():
            requests = request_generator()
            
            for balancer_name, balancer in balancers.items():
                print(f"Testing {balancer_name} with {dist_name}")
                
                metrics = run_simulation(balancer, requests)
                results = {
                    'server_loads': balancer.get_server_loads(),
                    'metrics': metrics
                }
                
                # Save individual run results
                plot_results(results, 
                           f'{balancer_name} - {dist_name} (Run {run + 1})',
                           f'results/{balancer_name}_{dist_name}_run{run + 1}.png')
                
                all_results[balancer_name].append({dist_name: metrics})
    
    # Analyze and save overall results
    analysis_df = analyze_results(all_results)
    analysis_df.to_csv('results/analysis_results.csv', index=False)
    
    # Print summary statistics
    print("\nSummary Statistics:")
    print(analysis_df.groupby(['Algorithm', 'Distribution']).mean())
    
    # Save detailed results
    save_results(all_results, 'detailed_results')

if __name__ == "__main__":
    main() 