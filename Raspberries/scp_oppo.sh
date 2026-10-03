#!/bin/bash

PREFIX="192.168.1"
USER="u0_a277"

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <file> <host_number>"
    exit 1
fi

FILE="$1"
HOST="$2"
URL="${USER}"@"${PREFIX}.${HOST}"

scp -P 8022 "$1" "${URL}:~/storage/music"