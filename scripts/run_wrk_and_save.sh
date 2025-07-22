#!/bin/bash
source ./common.env

# $1: concurrency  $2: duration  $3: url
if [ $# -ne 3 ]; then
  echo "Usage: $0 <concurrency> <duration> <url>"
  exit 1
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
RESULTS_DIR="../results"
mkdir -p $RESULTS_DIR
OUTFILE="$RESULTS_DIR/wrk_${1}c_${2}_${TIMESTAMP}.txt"

url=$3
[[ "${url}" != */ ]] && url="${url}/"

ssh ${USER}@${CLIENT_IP} "wrk -t4 -c$1 -d$2 $url" | tee $OUTFILE

echo "wrk (long connection) output saved to $OUTFILE" 
