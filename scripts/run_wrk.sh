#!/bin/bash
source ./common.env

# $1: connections  $2: duration  $3: url
if [ $# -ne 3 ]; then
  echo "Usage: $0 <connections> <duration> <url>"
  exit 1
fi

ssh ${USER}@${CLIENT_IP} "wrk -t4 -c$1 -d$2 $3" 