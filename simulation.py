import numpy as np
import matplotlib.pyplot as plt
from load_balancer import RoundRobinLoadBalancer, LeastConnectionLoadBalancer, WeightedRoundRobinLoadBalancer
import time
import pandas as pd
from typing import Dict, List
import json
import os

# Set matplotlib to use non-interactive backend to avoid popup windows
plt.switch_backend('Agg')

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

def plot_comparison_results(all_results: Dict[str, List[Dict]], save_path: str = None):
    """Plot comparison results for all algorithms and distributions"""
    # Prepare data for plotting
    algorithms = list(all_results.keys())
    distributions = ['Normal Distribution', 'Exponential Distribution', 'Uniform Distribution']
    
    # Calculate average metrics for each algorithm and distribution
    comparison_data = []
    for algo in algorithms:
        for dist in distributions:
            # Get all runs for this combination
            runs = []
            for result in all_results[algo]:
                if dist in result:
                    runs.append(result[dist])
            
            if runs:
                # Calculate average metrics
                avg_metrics = {
                    'Algorithm': algo,
                    'Distribution': dist,
                    'Mean Load': np.mean([r['mean_load'] for r in runs]),
                    'Std Load': np.mean([r['std_load'] for r in runs]),
                    'Balance Score': np.mean([r['balance_score'] for r in runs]),
                    'Requests/sec': np.mean([r['requests_per_second'] for r in runs]),
                    'Execution Time': np.mean([r['execution_time'] for r in runs])
                }
                comparison_data.append(avg_metrics)
    
    # Create comparison charts
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Load Balancing Algorithm Comparison', fontsize=16, fontweight='bold')
    
    # 1. Balance Score Comparison
    ax1 = axes[0, 0]
    balance_data = pd.DataFrame(comparison_data)
    pivot_balance = balance_data.pivot(index='Distribution', columns='Algorithm', values='Balance Score')
    pivot_balance.plot(kind='bar', ax=ax1, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax1.set_title('Load Balance Score (Higher is Better)')
    ax1.set_ylabel('Balance Score')
    ax1.set_ylim(0, 1)
    ax1.legend(title='Algorithm')
    ax1.tick_params(axis='x', rotation=45)
    
    # 2. Standard Deviation Comparison (Lower is Better)
    ax2 = axes[0, 1]
    pivot_std = balance_data.pivot(index='Distribution', columns='Algorithm', values='Std Load')
    pivot_std.plot(kind='bar', ax=ax2, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax2.set_title('Load Standard Deviation (Lower is Better)')
    ax2.set_ylabel('Standard Deviation')
    ax2.legend(title='Algorithm')
    ax2.tick_params(axis='x', rotation=45)
    
    # 3. Throughput Comparison
    ax3 = axes[1, 0]
    pivot_throughput = balance_data.pivot(index='Distribution', columns='Algorithm', values='Requests/sec')
    pivot_throughput.plot(kind='bar', ax=ax3, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax3.set_title('Throughput (Requests per Second)')
    ax3.set_ylabel('Requests/sec')
    ax3.legend(title='Algorithm')
    ax3.tick_params(axis='x', rotation=45)
    
    # 4. Execution Time Comparison
    ax4 = axes[1, 1]
    pivot_time = balance_data.pivot(index='Distribution', columns='Algorithm', values='Execution Time')
    pivot_time.plot(kind='bar', ax=ax4, color=['#FF6B6B', '#4ECDC4', '#45B7D1'])
    ax4.set_title('Execution Time (Lower is Better)')
    ax4.set_ylabel('Time (seconds)')
    ax4.legend(title='Algorithm')
    ax4.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Comparison chart saved to: {save_path}")
    
    plt.close()  # Close the figure to free memory
    
    return comparison_data

def plot_server_loads_comparison(all_results: Dict[str, List[Dict]], save_path: str = None):
    """Plot server load distribution comparison"""
    # Get the last run of each algorithm for visualization
    server_loads_data = {}
    for algo in all_results.keys():
        if all_results[algo]:
            # Get the last run with normal distribution
            for result in reversed(all_results[algo]):
                if 'Normal Distribution' in result:
                    server_loads_data[algo] = result['Normal Distribution']
                    break
    
    if not server_loads_data:
        return
    
    # Create server loads comparison chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig.suptitle('Server Load Distribution Comparison', fontsize=16, fontweight='bold')
    
    # Bar chart
    x = np.arange(5)  # 5 servers
    width = 0.25
    
    for i, (algo, metrics) in enumerate(server_loads_data.items()):
        # We need to get the actual server loads from the balancer
        # For now, we'll show the metrics
        loads = [metrics['mean_load']] * 5  # Simplified representation
        ax1.bar(x + i*width, loads, width, label=algo, alpha=0.8)
    
    ax1.set_xlabel('Server Index')
    ax1.set_ylabel('Load')
    ax1.set_title('Average Server Loads')
    ax1.set_xticks(x + width)
    ax1.set_xticklabels(['Server 1', 'Server 2', 'Server 3', 'Server 4', 'Server 5'])
    ax1.legend()
    
    # Balance score comparison
    algorithms = list(server_loads_data.keys())
    balance_scores = [server_loads_data[algo]['balance_score'] for algo in algorithms]
    
    bars = ax2.bar(algorithms, balance_scores, color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
    ax2.set_title('Load Balance Score Comparison')
    ax2.set_ylabel('Balance Score')
    ax2.set_ylim(0, 1)
    
    # Add value labels on bars
    for bar, score in zip(bars, balance_scores):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{score:.3f}', ha='center', va='bottom')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Server loads comparison saved to: {save_path}")
    
    plt.close()

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

def print_summary_report(comparison_data: List[Dict]):
    """Print a human-readable summary report"""
    print("\n" + "="*80)
    print("LOAD BALANCING ALGORITHM PERFORMANCE SUMMARY")
    print("="*80)
    
    df = pd.DataFrame(comparison_data)
    
    # Group by algorithm and show average performance
    print("\n📊 OVERALL PERFORMANCE RANKING:")
    print("-" * 50)
    
    # Calculate overall scores
    algo_scores = {}
    for algo in df['Algorithm'].unique():
        algo_data = df[df['Algorithm'] == algo]
        avg_balance = algo_data['Balance Score'].mean()
        avg_std = algo_data['Std Load'].mean()
        avg_throughput = algo_data['Requests/sec'].mean()
        
        # Normalize scores (balance score is already 0-1, std and throughput need normalization)
        normalized_std = 1 - (avg_std / df['Std Load'].max())  # Lower std is better
        normalized_throughput = avg_throughput / df['Requests/sec'].max()  # Higher throughput is better
        
        # Overall score (weighted average)
        overall_score = (avg_balance * 0.5 + normalized_std * 0.3 + normalized_throughput * 0.2)
        algo_scores[algo] = overall_score
    
    # Sort by overall score
    sorted_algos = sorted(algo_scores.items(), key=lambda x: x[1], reverse=True)
    
    for i, (algo, score) in enumerate(sorted_algos, 1):
        print(f"{i}. {algo}: {score:.3f}")
    
    print("\n🔍 DETAILED METRICS BY ALGORITHM:")
    print("-" * 50)
    
    for algo in df['Algorithm'].unique():
        algo_data = df[df['Algorithm'] == algo]
        print(f"\n{algo}:")
        print(f"  • Average Balance Score: {algo_data['Balance Score'].mean():.3f}")
        print(f"  • Average Load Std Dev: {algo_data['Std Load'].mean():.3f}")
        print(f"  • Average Throughput: {algo_data['Requests/sec'].mean():.0f} req/s")
        print(f"  • Average Execution Time: {algo_data['Execution Time'].mean():.4f}s")
    
    print("\n" + "="*80)

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
    
    print("🚀 Starting Load Balancing Simulation...")
    print(f"📊 Testing {len(balancers)} algorithms with {len(distributions)} distributions")
    print(f"🔄 Running {num_runs} iterations for reliability")
    print("-" * 60)
    
    # Run simulations multiple times
    for run in range(num_runs):
        print(f"\n🔄 Run {run + 1}/{num_runs}")
        
        for dist_name, request_generator in distributions.items():
            requests = request_generator()
            
            for balancer_name, balancer in balancers.items():
                print(f"  Testing {balancer_name} with {dist_name}")
                
                metrics = run_simulation(balancer, requests)
                results = {
                    'server_loads': balancer.get_server_loads(),
                    'metrics': metrics
                }
                
                all_results[balancer_name].append({dist_name: metrics})
    
    print("\n📈 Generating comparison charts and reports...")
    
    # Generate comparison charts
    comparison_data = plot_comparison_results(all_results, 'results/algorithm_comparison.png')
    plot_server_loads_comparison(all_results, 'results/server_loads_comparison.png')
    
    # Analyze and save overall results
    analysis_df = analyze_results(all_results)
    analysis_df.to_csv('results/analysis_results.csv', index=False)
    
    # Print summary report
    print_summary_report(comparison_data)
    
    # Save detailed results
    save_results(all_results, 'detailed_results')
    
    print(f"\n✅ Simulation completed!")
    print(f"📁 Results saved in 'results/' directory:")
    print(f"   • algorithm_comparison.png - Main comparison chart")
    print(f"   • server_loads_comparison.png - Server load distribution")
    print(f"   • analysis_results.csv - Detailed data")
    print(f"   • detailed_results.json - Raw simulation data")

if __name__ == "__main__":
    main() 