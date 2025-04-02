#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
wan:
  enable: true
  ipaddr: dhcp
  ipaddrv6: dhcp6
  descr: WAN Interface
  blockbogons: true

EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/wan.yaml"

echo "Created $TARGET_DIR/wan.yaml"
