import os
import requests
import yaml
import sys

CONFIG_PATH = "./Config/pfbox_api.env"
GLOBAL_FILE = "./Config/global.yaml"

# Dry run toggle
dry_run = "--dry-run" in sys.argv

# Load API credentials
creds = {}
with open(CONFIG_PATH) as f:
    for line in f:
        if line.strip():
            key, val = line.strip().split("=", 1)
            creds[key] = val

PFSENSE_API_HOST = creds.get("PFSENSE_API_HOST")
PFSENSE_API_USER = creds.get("PFSENSE_API_USER")
PFSENSE_API_PASS = creds.get("PFSENSE_API_PASS")

if not all([PFSENSE_API_HOST, PFSENSE_API_USER, PFSENSE_API_PASS]):
    print("Missing API credentials in pfbox_api.env")
    exit(1)

auth = (PFSENSE_API_USER, PFSENSE_API_PASS)
headers = {"Content-Type": "application/json"}

# Load desired global settings
def load_global_config():
    with open(GLOBAL_FILE, "r") as f:
        return yaml.safe_load(f).get("global", [])[0]  # Assuming only one dict inside the list

# Update global pfSense settings
def sync_global():
    desired = load_global_config()

    # --- DNS Resolver ---
    if "dns_resolver" in desired:
        endpoint = "services/unbound/settings"
        current = requests.get(f"{PFSENSE_API_HOST}/api/v1/{endpoint}", auth=auth, headers=headers, verify=False).json()

        should_enable = desired["dns_resolver"].lower() == "enable"
        if current.get("enable") != should_enable:
            print("Updating DNS Resolver enable setting")
            if not dry_run:
                requests.put(f"{PFSENSE_API_HOST}/api/v1/{endpoint}", json={"enable": should_enable}, auth=auth, headers=headers, verify=False)
            else:
                print(f"[Dry Run] PUT {endpoint} => {{'enable': {should_enable}}}")

    # --- DNS Query Forwarding ---
    if "dns_query_forwarding" in desired:
        endpoint = "services/unbound/settings"
        current = requests.get(f"{PFSENSE_API_HOST}/api/v1/{endpoint}", auth=auth, headers=headers, verify=False).json()

        should_forward = desired["dns_query_forwarding"].lower() == "enable"
        if current.get("dnsqueryforwarding") != should_forward:
            print("Updating DNS query forwarding setting")
            if not dry_run:
                requests.put(f"{PFSENSE_API_HOST}/api/v1/{endpoint}", json={"dnsqueryforwarding": should_forward}, auth=auth, headers=headers, verify=False)
            else:
                print(f"[Dry Run] PUT {endpoint} => {{'dnsqueryforwarding': {should_forward}}}")

    # --- Server Backend ---
    if "server_backend" in desired:
        endpoint = "system/advanced/networking"
        current = requests.get(f"{PFSENSE_API_HOST}/api/v1/{endpoint}", auth=auth, headers=headers, verify=False).json()

        backend_value = desired["server_backend"]
        if current.get("dhcpregistration_backend") != backend_value:
            print("Updating server backend setting")
            if not dry_run:
                requests.put(f"{PFSENSE_API_HOST}/api/v1/{endpoint}", json={"dhcpregistration_backend": backend_value}, auth=auth, headers=headers, verify=False)
            else:
                print(f"[Dry Run] PUT {endpoint} => {{'dhcpregistration_backend': '{backend_value}'}}")

    print("Global settings sync complete." + (" (dry run)" if dry_run else ""))

if __name__ == "__main__":
    sync_global()