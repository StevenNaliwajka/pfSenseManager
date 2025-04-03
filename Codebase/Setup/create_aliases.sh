#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
aliases:
  - name: 20
    type:
    descr: IoT
    address: [10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16]
    detail: [EnterpriseLan, Mid-SizeLan, HomeNetwork]


# links into pfSenseAPI w/

# get all existing in pfsense
# GET /api/v2/firewall/aliases
# For all existing
# DELETE /api/v2/firewall/aliases

# For all files in this .yaml
# POST /api/v2/firewall/alias


# Apply Pending Firewall changes
# POST /api/v2/firewall/apply

EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/aliases.yaml"

echo "Created $TARGET_DIR/aliases.yaml"
