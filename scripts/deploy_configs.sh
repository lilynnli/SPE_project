#!/bin/bash
source ./common.env

# $1: config file name (e.g. haproxy_rr.cfg)
if [ -z "$1" ]; then
  echo "Usage: $0 <haproxy_cfg_file>"
  exit 1
fi

scp ./configs/$1 ${USER}@${LOAD_BALANCER_IP}:/tmp/haproxy.cfg
ssh ${USER}@${LOAD_BALANCER_IP} 'sudo mv /tmp/haproxy.cfg /etc/haproxy/haproxy.cfg && sudo systemctl restart haproxy'

echo "HAProxy config $1 deployed and restarted." 