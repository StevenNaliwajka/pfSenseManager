#!/bin/bash

# Exit on any failure
set -e

# Print steps
set -x

CONFIG_PATH="./Config/pfbox_api.env"

# Prompt user for SSH info
read -p "Enter pfSense IP/hostname: " PFSENSE_HOST
read -p "Enter pfSense SSH username: " PFSENSE_USER
read -s -p "Enter pfSense SSH password: " PFSENSE_PASS

echo

# Function to run commands over SSH
run_ssh() {
  sshpass -p "$PFSENSE_PASS" ssh -o StrictHostKeyChecking=no "$PFSENSE_USER@$PFSENSE_HOST" "$1"
}

# Step 1: Install pfSense-pkg-API
run_ssh "pkg add https://github.com/jaredhendrickson13/pfsense-api/releases/latest/download/pfSense-pkg-API.txz"

# Step 2: Create API user and generate token
API_USER="pfmgr_user"
API_PASS="pfmgr_password123"

# Create user with full API access
run_ssh "echo '<?xml version=\"1.0\"?><user><name>$API_USER</name><password>$API_PASS</password><priv>user-shell-access</priv><priv>page-all</priv><scope>user</scope></user>' > /tmp/add_user.xml && pfSsh.php playback configxml /tmp/add_user.xml"

# Restart web GUI to apply user changes
run_ssh "pfSsh.php playback svc restart webgui"

# Wait for pfSense to come back up
sleep 10

# Step 3: Try authenticating with API
API_URL="https://$PFSENSE_HOST/api/v1/system/version"
RESPONSE=$(curl -sk -u "$API_USER:$API_PASS" "$API_URL")

if echo "$RESPONSE" | grep -q 'version'; then
  echo "\npfSense API is reachable and authentication succeeded."
else
  echo "\nFailed to contact pfSense API or authenticate. Response:"
  echo "$RESPONSE"
  exit 1
fi

# Save API details
mkdir -p ./Config
cat > "$CONFIG_PATH" <<EOF
PFSENSE_API_HOST=https://$PFSENSE_HOST
PFSENSE_API_USER=$API_USER
PFSENSE_API_PASS=$API_PASS
EOF

echo "\nAPI credentials saved to $CONFIG_PATH"
