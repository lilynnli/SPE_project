#!/bin/bash
source ./common.env

# $1: connections  $2: duration  $3: url
if [ $# -ne 3 ]; then
  echo "Usage: $0 <connections> <duration> <url>"
  exit 1
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="../results"
mkdir -p $RESULTS_DIR
OUTFILE="$RESULTS_DIR/wrk_${1}c_${2}_${TIMESTAMP}.txt"

ssh ${USER}@${CLIENT_IP} "wrk -t4 -c$1 -d$2 $3" | tee $OUTFILE

echo "wrk output saved to $OUTFILE" 