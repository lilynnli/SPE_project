import numpy as np
from typing import List, Dict
import time
from abc import ABC, abstractmethod

class LoadBalancer(ABC):
    def __init__(self, num_servers: int):
        self.num_servers = num_servers
        self.server_loads = np.zeros(num_servers)
        self.request_history = []
        self.total_requests = 0
        self.start_time = time.time()
        
    @abstractmethod
    def assign_request(self, request_load: float) -> int:
        """Assign a request to a server and return the server index"""
        pass
    
    def get_server_loads(self) -> np.ndarray:
        """Get current load of all servers"""
        return self.server_loads
    
    def get_load_metrics(self) -> Dict:
        """Calculate load balancing metrics"""
        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        # Calculate dynamic load metrics
        loads = self.server_loads
        mean_load = np.mean(loads)
        std_load = np.std(loads)
        
        # Calculate load balance score (between 0 and 1, closer to 1 means more balanced)
        if mean_load == 0:
            balance_score = 1.0
        else:
            balance_score = 1 - (std_load / mean_load)
        
        return {
            'mean_load': mean_load,
            'std_load': std_load,
            'max_load': np.max(loads),
            'min_load': np.min(loads),
            'balance_score': balance_score,
            'requests_per_second': self.total_requests / elapsed_time if elapsed_time > 0 else 0,
            'total_requests': self.total_requests
        }
    
    def reset(self):
        """Reset the load balancer state"""
        self.server_loads = np.zeros(self.num_servers)
        self.request_history = []
        self.total_requests = 0
        self.start_time = time.time()

class RoundRobinLoadBalancer(LoadBalancer):
    def __init__(self, num_servers: int):
        super().__init__(num_servers)
        self.current_server = 0
    
    def assign_request(self, request_load: float) -> int:
        server_idx = self.current_server
        self.server_loads[server_idx] += request_load
        self.current_server = (self.current_server + 1) % self.num_servers
        self.total_requests += 1
        self.request_history.append((server_idx, request_load))
        return server_idx

class LeastConnectionLoadBalancer(LoadBalancer):
    def assign_request(self, request_load: float) -> int:
        server_idx = np.argmin(self.server_loads)
        self.server_loads[server_idx] += request_load
        self.total_requests += 1
        self.request_history.append((server_idx, request_load))
        return server_idx

class WeightedRoundRobinLoadBalancer(LoadBalancer):
    def __init__(self, num_servers: int, weights: List[float]):
        super().__init__(num_servers)
        if len(weights) != num_servers:
            raise ValueError("Number of weights must match number of servers")
        if not all(w > 0 for w in weights):
            raise ValueError("All weights must be positive")
            
        self.weights = np.array(weights)
        self.current_server = 0
        self.weight_counter = 0
        self.max_weight = max(weights)
        
        # Calculate weight ratios
        self.weight_ratios = self.weights / self.max_weight
        
    def assign_request(self, request_load: float) -> int:
        server_idx = self.current_server
        self.server_loads[server_idx] += request_load
        self.weight_counter += 1
        
        # Decide whether to switch to the next server based on the weight ratio
        if self.weight_counter >= self.weight_ratios[server_idx] * self.max_weight:
            self.current_server = (self.current_server + 1) % self.num_servers
            self.weight_counter = 0
            
        self.total_requests += 1
        self.request_history.append((server_idx, request_load))
        return server_idx 