#!/bin/bash

echo "Running pfSenseManger..."

echo "Verifying pfSense API key existence."
bash Codebase/verify_api.sh


# Deploying Configs
bash Codebase/deploy.sh