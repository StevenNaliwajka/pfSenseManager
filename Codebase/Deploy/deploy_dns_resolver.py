import os
import requests
import yaml
import sys

CONFIG_PATH = "./Config/pfbox_api.env"
DNS_FILE = "./Config/dns_resolver.yaml"

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

# Load DNS resolver config
def load_dns_config():
    with open(DNS_FILE, "r") as f:
        return yaml.safe_load(f).get("dns_resolver", {})

# API helper
def call_api(method, endpoint, data=None):
    if dry_run and method in ["POST", "PUT", "DELETE"]:
        print(f"[Dry Run] {method} {endpoint} => {data}")
        return type("DummyResponse", (), {"ok": True, "json": lambda: {}})()
    url = f"{PFSENSE_API_HOST}/api/v1/{endpoint}"
    resp = requests.request(method, url, headers=headers, auth=auth, json=data, verify=False)
    return resp

# Sync host overrides
def sync_host_overrides(desired_hosts):
    existing = call_api("GET", "services/unbound/host_override").json().get("data", [])
    existing_by_key = {(h["host"], h["domain"]): h for h in existing}
    desired_keys = set()

    for entry in desired_hosts:
        key = (entry["host"], entry["parent_domain"])
        desired_keys.add(key)
        payload = {
            "host": entry["host"],
            "domain": entry["parent_domain"],
            "ip": entry["ip_to_return"],
            "descr": entry["desc"]
        }

        current = existing_by_key.get(key)
        if current:
            if current.get("ip") != payload["ip"] or current.get("descr") != payload["descr"]:
                print(f"Updating host override: {key}")
                call_api("PUT", f"services/unbound/host_override/{current['id']}", payload)
            else:
                print(f"Host override up to date: {key}")
        else:
            print(f"Creating host override: {key}")
            call_api("POST", "services/unbound/host_override", payload)

    for key, entry in existing_by_key.items():
        if key not in desired_keys:
            print(f"Deleting host override: {key}")
            call_api("DELETE", f"services/unbound/host_override/{entry['id']}")

# Sync domain overrides
def sync_domain_overrides(desired_domains):
    existing = call_api("GET", "services/unbound/domain_override").json().get("data", [])
    existing_by_key = {(d["domain"], d["ip"]): d for d in existing}
    desired_keys = set()

    for entry in desired_domains:
        key = (entry["domain"], entry["lookup_ip_addr"])
        desired_keys.add(key)
        payload = {
            "domain": entry["domain"],
            "ip": entry["lookup_ip_addr"],
            "descr": entry["desc"]
        }

        current = existing_by_key.get(key)
        if current:
            if current.get("descr") != payload["descr"]:
                print(f"Updating domain override: {key}")
                call_api("PUT", f"services/unbound/domain_override/{current['id']}", payload)
            else:
                print(f"Domain override up to date: {key}")
        else:
            print(f"Creating domain override: {key}")
            call_api("POST", "services/unbound/domain_override", payload)

    for key, entry in existing_by_key.items():
        if key not in desired_keys:
            print(f"Deleting domain override: {key}")
            call_api("DELETE", f"services/unbound/domain_override/{entry['id']}")

if __name__ == "__main__":
    config = load_dns_config()
    sync_host_overrides(config.get("host_overrides", []))
    sync_domain_overrides(config.get("domain_overrides", []))
    print("DNS resolver sync complete." + (" (dry run)" if dry_run else ""))