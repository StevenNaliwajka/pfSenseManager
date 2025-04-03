#!/bin/bash

echo "Running pfSenseManger..."

echo "Verifying pfSense API key existence."
bash Codebase/verify_api.sh

# Run test
echo "\nRunning pfSenseManager in dry-run mode"
python3 ./Codebase/deploy.py --dry-run