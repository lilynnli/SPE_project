# Monitoring and Visualization Guide

This document describes how to set up system monitoring and visualization for your load balancing testbed using Prometheus, Node Exporter, and Grafana.

## 1. Overview
- **Node Exporter**: Collects system metrics (CPU, memory, disk, network) from all VMs.
- **Prometheus**: Centralized metrics collection and storage.
- **Grafana**: Visualization and dashboarding for Prometheus data.

## 2. Setup Steps

### 2.1. Prerequisites
- All VMs must have static IPs and SSH access.
- `scripts/common.env` must be configured with all VM IPs and usernames.
- Choose one VM (e.g., the load balancer) as the Prometheus & Grafana host. Set `PROMETHEUS_HOST` in `common.env`.

### 2.2. Install Node Exporter on All VMs
```bash
cd scripts
./setup_node_exporter.sh
```

### 2.3. Install Prometheus on the Monitoring VM
```bash
./setup_prometheus.sh
```

### 2.4. Generate and Deploy Prometheus Config
```bash
./generate_prometheus_config.sh
```

### 2.5. Install Grafana on the Monitoring VM
```bash
./setup_grafana.sh
```

### 2.6. Access Grafana
- Open your browser and go to: `http://<PROMETHEUS_HOST>:3000`
- Default login: `admin` / `admin`
- Add Prometheus as a data source (URL: `http://localhost:9090`)
- Import or create dashboards for system metrics.

## 3. Customization
- You can add more VMs by editing `common.env` and regenerating the Prometheus config.
- For advanced dashboards, use Grafana's import feature and the official Node Exporter dashboard JSON.

## 4. References
- [Prometheus Node Exporter](https://github.com/prometheus/node_exporter)
- [Prometheus](https://prometheus.io/)
- [Grafana](https://grafana.com/) 