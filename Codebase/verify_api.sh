#!/bin/bash

CONFIG_PATH="./Config/pfbox_api.env"
PREP_SCRIPT="./Codebase/Setup/pfbox_prep.sh"

# Check if pfbox_api.env exists
if [[ ! -f "$CONFIG_PATH" ]]; then
  echo "API config not found. Running pfbox_prep.sh..."
  bash "$PREP_SCRIPT"
  exit 0
fi

# Load and check required variables
source "$CONFIG_PATH"

if [[ -z "$PFSENSE_API_HOST" || -z "$PFSENSE_API_USER" || -z "$PFSENSE_API_PASS" ]]; then
  echo "API config is incomplete. Running pfbox_prep.sh..."
  bash "$PREP_SCRIPT"
  exit 0
fi

# All good
echo "API config found and complete."
exit 0
