#!/bin/bash
set -x
echo "START: $0"
cd /app && ./daily.py yesterday
echo "END: $0"
