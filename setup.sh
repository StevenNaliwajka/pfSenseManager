#!/bin/bash

echo "Welcome to pfSenseManager setup."

# Setup
bash Codebase/Setup/create_aliases.sh
bash Codebase/Setup/create_dns_resolver.sh
bash Codebase/Setup/create_global.sh
bash Codebase/Setup/create_port_forward.sh
bash Codebase/Setup/create_rules.sh
bash Codebase/Setup/create_vlans.sh

# verify python install
bash Codebase/Setup/install_python.sh

# create venv
bash Codebase/Setup/setup_venv.sh


echo "Update all config files in ./Config/*"
echo "One updated, run 'sudo bash run.sh'"
echo "This will deploy all settings to pfSense."