#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
port_forward:
  - description: example_1
    protocol: tcp
    # destination_type:
    # destination_type, destination
    # ------------------------
    # address, 192.168.20.1
    # network, 192.168.20.0/24
    # self_gateway, n/a
    # self_subnets, n/a
    destination_type: self_gateway
    destination: n/a
    destination_port_min: 443
    destination_port_max: 443
    redirect_target_ip: 192.168.32.103
    redirect_target_port: 443
    # Nat reflection options:
    # Enable (NAT + Proxy)
    # Enable (Pure NAT)
    # Disable
    nat_reflection: Enable (Pure Nat)


# links into pfSenseAPI w/



EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/port_forward.yaml"

echo "Created $TARGET_DIR/port_forward.yaml"
