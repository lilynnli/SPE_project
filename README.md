# Load Balancing Simulation and Real Environment Testing

This project evaluates and compares three classic load balancing algorithms (Round Robin, Least Connection, Weighted Round Robin) through both simulation and real-world virtualized deployment.

## Project Structure

```
load_balancing_simulation/
├── simulation.py                # Main simulation script
├── load_balancer.py             # Core algorithm implementations
├── requirements.txt             # Python dependencies
├── scripts/                     # Automation scripts for VM setup and testing
│   ├── common.env
│   ├── setup_load_balancer.sh
│   ├── setup_backend.sh
│   ├── setup_client.sh
│   ├── deploy_configs.sh
│   ├── run_wrk.sh
│   ├── setup_node_exporter.sh
│   ├── setup_prometheus.sh
│   ├── generate_prometheus_config.sh
│   └── setup_grafana.sh
├── configs/                     # HAProxy config templates
│   ├── haproxy_rr.cfg
│   ├── haproxy_lc.cfg
│   └── haproxy_wrr.cfg
├── results/                     # Simulation and test results
├── MONITORING.md                # Monitoring and visualization guide
└── README.md
```

## 1. Simulation (Python)

- Run the simulation and generate performance metrics and plots:

```bash
pip install -r requirements.txt
python simulation.py
```

- Algorithms: Round Robin, Least Connection, Weighted Round Robin
- Request patterns: normal, exponential, uniform distributions
- Outputs: server load distribution, balance score, CSV and PNG results

## 2. Real Environment (UTM VMs)

### VM Preparation
- Use UTM to create 4 VMs:
  - 1 Load Balancer (Ubuntu, HAProxy)
  - 2 Backend Servers (Ubuntu, Nginx)
  - 1 Client (Ubuntu, wrk)
- Assign static IPs and set up SSH access for automation.

### Automation Scripts

- Edit `scripts/common.env` to match your VM IPs and username.
- Make all scripts executable:

```bash
chmod +x scripts/*.sh
```

- Install and configure HAProxy on the load balancer:

```bash
cd scripts
./setup_load_balancer.sh
```

- Install and configure Nginx on backend servers:

```bash
./setup_backend.sh
```

- Install wrk on the client:

```bash
./setup_client.sh
```

- Deploy a HAProxy config (e.g. round robin):

```bash
./deploy_configs.sh haproxy_rr.cfg
```

- Run a wrk test from the client:

```bash
./run_wrk.sh 100 30s http://<LOAD_BALANCER_IP>/
```

## 3. HAProxy Config Templates
- `configs/haproxy_rr.cfg`: Round Robin
- `configs/haproxy_lc.cfg`: Least Connection
- `configs/haproxy_wrr.cfg`: Weighted Round Robin

## 4. Results and Analysis
- Simulation results are saved in `results/` as CSV and PNG files.
- Real environment test results can be collected from wrk output and system monitoring tools.

## 5. Monitoring and Visualization (Optional)
- See [MONITORING.md](MONITORING.md) for a complete guide to setting up Prometheus, Node Exporter, and Grafana for system metrics collection and visualization.
- Scripts for monitoring setup are in the `scripts/` directory.

## 6. Extensions
- Add more backend servers for scalability tests.
- Integrate Prometheus + Grafana for monitoring (see above).
- Test with bursty traffic or network faults.

---

**For any step, adjust IPs, usernames, and file paths as needed for your environment.** 