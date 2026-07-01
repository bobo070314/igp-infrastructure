#!/usr/bin/env bash
# IGP Infrastructure — Branch Office Starter Script
# Usage: bash scripts/start-branches.sh

set -e

echo "=== IGP Branch Offices ==="

# Check if openclaw is installed
if ! command -v openclaw &> /dev/null; then
    echo "[WARN] openclaw CLI not found. Use Docker Compose instead."
    echo "       docker compose --profile full up -d"
    exit 0
fi

# Start branch gateways
echo "Starting main gateway (port 18791)..."
nohup openclaw --profile main --port 18791 gateway > /tmp/igp-main.log 2>&1 &

echo "Starting ops gateway (port 19789)..."
nohup openclaw --profile ops --port 19789 gateway > /tmp/igp-ops.log 2>&1 &

echo "Starting rescue gateway (port 20789)..."
nohup openclaw --profile rescue --port 20789 gateway > /tmp/igp-rescue.log 2>&1 &

echo "All branch gateways started."
echo "  main:    http://localhost:18791"
echo "  ops:     http://localhost:19789"
echo "  rescue:  http://localhost:20789"
echo ""
echo "Logs: tail -f /tmp/igp-{main,ops,rescue}.log"
