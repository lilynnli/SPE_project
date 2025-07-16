#!/bin/bash
source ./common.env

for ip in ${BACKEND1_IP} ${BACKEND2_IP}; do
  ssh ${USER}@${ip} <<'EOF'
  sudo apt update
  sudo apt install -y nginx
  sudo systemctl enable nginx
  sudo systemctl start nginx
EOF
done

echo "All backend Nginx installation completed." 