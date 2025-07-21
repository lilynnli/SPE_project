#!/bin/bash
source ./common.env

cat > prometheus.yml <<EOL
global:
  scrape_interval: 5s

scrape_configs:
  - job_name: 'node_exporters'
    static_configs:
      - targets: 
        - '${LOAD_BALANCER_IP}:9100'
        - '${BACKEND1_IP}:9100'
        - '${BACKEND2_IP}:9100'
        - '${BACKEND3_IP}:9100'
        - '${CLIENT_IP}:9100'
EOL

scp prometheus.yml ${USER}@${PROMETHEUS_HOST}:/opt/prometheus/prometheus.yml
ssh ${USER}@${PROMETHEUS_HOST} 'sudo systemctl restart prometheus'
echo "Prometheus config deployed and service restarted." 