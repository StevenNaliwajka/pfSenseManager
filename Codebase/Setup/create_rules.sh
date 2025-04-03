#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
rules:
  - rule_description: demo_rule_1
    action: pass
    address_family: ipv4
    protocol: tcp
    # few options for source_type:
    # source_type, source
    # ------------------------
    # address, 192.168.20.1
    # network, 192.168.20.0/24
    # self_gateway, n/a
    # self_subnets, n/a
    source_type: self_gateway
    source: n/a
    # same goes for destination_type:
    # destination_type, destination
    # ------------------------
    # address, 192.168.20.1
    # network, 192.168.20.0/24
    # self_gateway, n/a
    # self_subnets, n/a
    destination_type: network
    destination: 192.168.20.0/24
    destination_port: 53
    where_to_apply: [lan,wan,20,21,22,30,101]


EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/rules.yaml"

echo "Created $TARGET_DIR/rules.yaml"
