#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
nat:
  - interface: WAN
    protocol: tcp
    destination_port: 80
    redirect_to_ip: 192.168.20.10
    redirect_port: 80
    description: Forward HTTP to internal web server

EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/nat_rules.yaml"

echo "Created $TARGET_DIR/nat_rules.yaml"
