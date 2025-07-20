#!/bin/bash
source ./common.env

ssh ${USER}@${CLIENT_IP} <<'EOF'
sudo apt update
sudo apt install -y git build-essential libssl-dev unzip
if [ -d wrk ]; then
  cd wrk && git pull && make clean
else
  git clone https://github.com/wg/wrk.git
  cd wrk
fi
make
sudo cp wrk /usr/local/bin/
EOF

echo "wrk installation completed." 