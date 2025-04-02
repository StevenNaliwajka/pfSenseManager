#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
firewall_rules:
  - interface: OPT2
    action: pass
    protocol: tcp
    source: 192.168.20.0/24
    destination: any
    port: 80
    description: Allow HTTP from IoT

EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/firewall_rules.yaml"

echo "Created $TARGET_DIR/firewall_rules.yaml"
