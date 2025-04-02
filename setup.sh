#!/bin/bash

echo "Welcome to pfSenseManager setup."

# Setup
bash Codebase/Setup/create_dhcp_servers.sh
bash Codebase/Setup/create_dns_overrides.sh
bash Codebase/Setup/create_firewall_rules.sh
bash Codebase/Setup/create_global.sh
bash Codebase/Setup/create_interfaces.sh
bash Codebase/Setup/create_nat_rules.sh
bash Codebase/Setup/create_vlans.sh

echo "Update all config files in ./Config/*"
echo "One updated, run 'sudo bash run.sh'"
echo "This will deploy all settings to pfSense."