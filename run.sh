#!/bin/bash

echo "Running pfSenseManger..."

echo "Verifying pfSense API key existence."
bash Codebase/verify_api.sh

# Run full deploy (live)
echo "\nRunning full pfSenseManager deploy"
python3 ./Codebase/deploy.py