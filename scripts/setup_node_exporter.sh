#!/bin/bash
source ./common.env

for ip in ${LOAD_BALANCER_IP} ${BACKEND1_IP} ${BACKEND2_IP} ${CLIENT_IP}; do
  ssh ${USER}@${ip} <<'EOF'
  wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
  tar -xzf node_exporter-1.7.0.linux-amd64.tar.gz
  sudo mv node_exporter-1.7.0.linux-amd64/node_exporter /usr/local/bin/
  sudo useradd -rs /bin/false node_exporter || true
  sudo tee /etc/systemd/system/node_exporter.service > /dev/null <<EOL
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=default.target
EOL
  sudo systemctl daemon-reload
  sudo systemctl enable node_exporter
  sudo systemctl start node_exporter
EOF
done

echo "Node Exporter installed and started on all VMs." 