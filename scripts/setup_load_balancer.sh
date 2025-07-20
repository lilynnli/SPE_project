#!/bin/bash
source ./common.env

ssh ${USER}@${LOAD_BALANCER_IP} <<'EOF'
sudo apt update
sudo apt install -y haproxy
sudo systemctl enable haproxy
sudo systemctl start haproxy
EOF

echo "HAProxy installation completed." 