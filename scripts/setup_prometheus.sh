#!/bin/bash
source ./common.env

echo "PROMETHEUS_HOST is: $PROMETHEUS_HOST"

ssh ${USER}@${PROMETHEUS_HOST} <<'EOF'
sudo apt update
sudo apt install -y wget tar
wget https://github.com/prometheus/prometheus/releases/download/v2.52.0/prometheus-2.52.0.linux-amd64.tar.gz
tar -xzf prometheus-2.52.0.linux-amd64.tar.gz
sudo mv prometheus-2.52.0.linux-amd64 /opt/prometheus
sudo useradd -rs /bin/false prometheus || true
sudo tee /etc/systemd/system/prometheus.service > /dev/null <<EOL
[Unit]
Description=Prometheus
After=network.target

[Service]
User=prometheus
ExecStart=/opt/prometheus/prometheus --config.file=/opt/prometheus/prometheus.yml

[Install]
WantedBy=default.target
EOL
sudo systemctl daemon-reload
sudo systemctl enable prometheus
sudo systemctl start prometheus
EOF

echo "Prometheus installed and started." 