#!/bin/bash
source ./common.env

# $1: total_requests  $2: concurrency  $3: url
if [ $# -ne 3 ]; then
  echo "Usage: $0 <total_requests> <concurrency> <url>"
  exit 1
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="../results"
mkdir -p $RESULTS_DIR
OUTFILE="$RESULTS_DIR/ab_${1}n_${2}c_${TIMESTAMP}.txt"

ssh ${USER}@${CLIENT_IP} "ab -n $1 -c $2 $3" | tee $OUTFILE

echo "ab output saved to $OUTFILE" 