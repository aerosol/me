#!/bin/bash
set -x
echo "START: $0"
cd /app && ./daily.py
echo "END: $0"
