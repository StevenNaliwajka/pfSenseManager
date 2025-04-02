#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
dhcp:
  - interface: OPT2
    range_start: 192.168.20.10
    range_end: 192.168.20.100
    lease_time: 7200
    dns_servers:
      - 192.168.1.1
    enabled: true

EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/dhcp_servers.yaml"

echo "Created $TARGET_DIR/dhcp_servers.yaml"
