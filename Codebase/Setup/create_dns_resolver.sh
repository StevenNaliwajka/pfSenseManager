#!/bin/bash

# Get absolute path two levels up
TARGET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/Config"

# Ensure the target config directory exists
mkdir -p "$TARGET_DIR"

# Define the JSON content
read -r -d '' JSON_CONTENT << 'EOF'
dns_resolver:
  host_overrides:
    - host: www
      parent_domain: example.com
      ip_to_return: 192.168.32.103
      desc: example_web


  domain_overrides:
    - domain: www.example.com
      lookup_ip_addr: 192.168.32.103
      desc: example_web

EOF

# Write the JSON to the target path
echo "$JSON_CONTENT" > "$TARGET_DIR/dns_resolver.yaml"

echo "Created $TARGET_DIR/dns_resolver.yaml"
