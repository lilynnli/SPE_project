#!/bin/bash
source ./common.env

ssh ${USER}@${CLIENT_IP} <<'EOF'
sudo apt update
sudo apt install -y apache2-utils
EOF

echo "ab (ApacheBench) installation completed." 