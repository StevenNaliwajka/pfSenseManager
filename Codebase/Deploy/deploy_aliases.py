import requests
import yaml
import sys

CONFIG_PATH = "./Config/pfbox_api.env"
ALIASES_FILE = "./Codebase/aliases.yaml"

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

# Load YAML aliases
def load_aliases():
    with open(ALIASES_FILE, "r") as f:
        return yaml.safe_load(f).get("aliases", [])

# Get all aliases currently on pfSense
def get_existing_aliases():
    resp = requests.get(f"{PFSENSE_API_HOST}/api/v1/firewall/alias", auth=auth, headers=headers, verify=False)
    if not resp.ok:
        print("Failed to fetch existing aliases")
        exit(1)
    return {alias['name']: alias for alias in resp.json().get('data', [])}

# Update aliases on pfSense
def sync_aliases():
    desired_aliases = load_aliases()
    current_aliases = get_existing_aliases()
    desired_names = set()

    for alias in desired_aliases:
        name = alias['name']
        desired_names.add(name)
        payload = {
            "name": name,
            "type": alias["type"],
            "descr": alias["desc"],
            "address": ",".join(alias["address"]),
            "detail": ",".join(alias.get("detail", []))
        }

        if name in current_aliases:
            current = current_aliases[name]
            needs_update = any([
                current.get("type") != payload["type"],
                current.get("descr") != payload["descr"],
                current.get("address") != payload["address"],
                current.get("detail") != payload["detail"]
            ])
            if needs_update:
                print(f"Updating alias: {name}")
                if not dry_run:
                    requests.put(f"{PFSENSE_API_HOST}/api/v1/firewall/alias/{name}", json=payload, auth=auth, headers=headers, verify=False)
            else:
                print(f"Alias '{name}' is up to date")
        else:
            print(f"Adding new alias: {name}")
            if not dry_run:
                requests.post(f"{PFSENSE_API_HOST}/api/v1/firewall/alias", json=payload, auth=auth, headers=headers, verify=False)

    # Delete aliases not in config
    for name in current_aliases:
        if name not in desired_names:
            print(f"Deleting alias: {name}")
            if not dry_run:
                requests.delete(f"{PFSENSE_API_HOST}/api/v1/firewall/alias/{name}", auth=auth, headers=headers, verify=False)

    print("Alias sync complete." + (" (dry run)" if dry_run else ""))

if __name__ == "__main__":
    sync_aliases()
