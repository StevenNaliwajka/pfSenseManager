#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
global:
  - dns_resolver: enable
    server_backend: kea dhcp  # /system/advanced/networking
    dns_query_forwarding: enable # /services/dns resolver/general settings

EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/global.yaml"

echo "Created $TARGET_DIR/global.yaml"
