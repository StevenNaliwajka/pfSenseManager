#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
vlans:
  - if: igb2
    tag: 20
    description: Server_LoadBalancing
    pcp: 7 # priority order.
    ipv4_address: 192.168.28.1
    subnet: 24
    dhcp_pool_min_ip: 192.168.28.2
    dhcp_pool_max_ip: 192.168.28.254
    dhcp_dns_server: 192.168.28.1
    dhcp_gateway: 192.168.28.1
    dhcp_default_lease_time: 7200
    dhcp_max_lease_time: 86400
    dhcp_static_mappings:
      - mac_address: 00:23:25:g9:9d:64
        ip_address: 192.168.28.101
        description: nginx
         # uses vlan deault dns server and gateway



# links into pfSenseAPI w/

# ensure to call enable for everything

# Vlan creation done through
# DELETE /api/v2/interface/vlan

# Interface mgmt is done through
# POST /api/v2/interface

# to mangage DHCP server
# PUT /api/v2/services/dhcp_server/{interface}

# to manage static mapping
# POST /api/v2/services/dhcp_server/{interface}/static_mapping

# to retrieve the current config
# GET /api/v2/services/dhcp_server/{interface}

EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/vlans.yaml"

echo "Created $TARGET_DIR/vlans.yaml"
