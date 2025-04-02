#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
interfaces:
  - interface: OPT2
    enable: true
    descr: IoT Network
    ipaddr: 192.168.20.1
    subnet: 24
    type: staticv4
    blockbogons: true

EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/interfaces.yaml"

echo "Created $TARGET_DIR/interfaces.yaml"
