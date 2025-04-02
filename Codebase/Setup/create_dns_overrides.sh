#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
dns:
  - host: git
    domain: home.local
    ip: 192.168.20.2
  - host: dashboard
    domain: home.local
    ip: 192.168.30.5

EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/dns_overrides.yaml"

echo "Created $TARGET_DIR/dns_overrides.yaml"
