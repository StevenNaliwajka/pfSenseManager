import os
import requests
import yaml
import sys

CONFIG_PATH = "./Config/pfbox_api.env"
FORWARD_FILE = "./Config/port_forward.yaml"

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

# Load forwarding rules
def load_forwarding():
    with open(FORWARD_FILE, "r") as f:
        return yaml.safe_load(f).get("port_forward", [])

# API helper
def call_api(method, endpoint, data=None):
    if dry_run and method in ["POST", "PUT", "DELETE"]:
        print(f"[Dry Run] {method} {endpoint} => {data}")
        return type("DummyResponse", (), {"ok": True, "json": lambda: {}})()
    url = f"{PFSENSE_API_HOST}/api/v1/{endpoint}"
    resp = requests.request(method, url, headers=headers, auth=auth, json=data, verify=False)
    return resp

# Address type mapping
def translate_address(type_, iface="wan"):
    if type_ == "address":
        return "wanip"
    elif type_ == "network":
        return f"{iface}_subnets"
    elif type_ == "self_gateway":
        return f"{iface}_address"
    elif type_ == "self_subnets":
        return f"{iface}_subnets"
    return ""

# Normalize nat reflection
reflection_map = {
    "Enable (NAT + Proxy)": "enable_proxy",
    "Enable (Pure NAT)": "enable_nat",
    "Disable": "disable"
}

# Deploy logic
def deploy_port_forwards():
    desired = load_forwarding()
    existing = call_api("GET", "firewall/nat/port_forward").json().get("data", [])
    existing_by_descr = {r.get("descr"): r for r in existing}
    desired_names = set()

    for rule in desired:
        descr = rule["description"]
        desired_names.add(descr)

        payload = {
            "interface": "wan",
            "protocol": rule["protocol"],
            "descr": descr,
            "destination": translate_address(rule["destination_type"]),
            "dstport": f"{rule['destination_port_min']}-{rule['destination_port_max']}",
            "target": rule["redirect_target_ip"],
            "local-port": str(rule["redirect_target_port"]),
            "natreflection": reflection_map.get(rule["nat_reflection"], "disable")
        }

        current = existing_by_descr.get(descr)
        if current:
            update_needed = any([
                current.get("protocol") != payload["protocol"],
                current.get("destination") != payload["destination"],
                current.get("dstport") != payload["dstport"],
                current.get("target") != payload["target"],
                current.get("local-port") != payload["local-port"],
                current.get("natreflection") != payload["natreflection"]
            ])
            if update_needed:
                print(f"Updating port forward: {descr}")
                call_api("PUT", f"firewall/nat/port_forward/{current['id']}", payload)
            else:
                print(f"Port forward already up-to-date: {descr}")
        else:
            print(f"Creating port forward: {descr}")
            call_api("POST", "firewall/nat/port_forward", payload)

    # Delete obsolete rules
    for descr, rule in existing_by_descr.items():
        if descr not in desired_names:
            print(f"Deleting port forward: {descr}")
            call_api("DELETE", f"firewall/nat/port_forward/{rule['id']}")

    print("Port forwarding sync complete." + (" (dry run)" if dry_run else ""))

if __name__ == "__main__":
    deploy_port_forwards()