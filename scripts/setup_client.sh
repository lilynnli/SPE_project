#!/bin/bash
source ./common.env

ssh ${USER}@${CLIENT_IP} <<'EOF'
sudo apt update
sudo apt install -y git build-essential libssl-dev
if [ ! -d wrk ]; then
  git clone https://github.com/wg/wrk.git
fi
cd wrk && make
sudo cp wrk /usr/local/bin/
EOF

echo "wrk installation completed." 