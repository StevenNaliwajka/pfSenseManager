#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
vlans:
  - id: 20
    name: IoT
    parent: igb1
  - id: 30
    name: Media
    parent: igb1

EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/create_vlans.yaml"

echo "Created $TARGET_DIR/create_vlans.yaml"
