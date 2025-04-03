import os
import requests
import yaml
import sys

CONFIG_PATH = "./Config/pfbox_api.env"
RULES_FILE = "./Config/rules.yaml"

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

# Load rules config
def load_rules():
    with open(RULES_FILE, "r") as f:
        return yaml.safe_load(f).get("rules", [])

# API helper
def call_api(method, endpoint, data=None):
    if dry_run and method in ["POST", "PUT", "DELETE"]:
        print(f"[Dry Run] {method} {endpoint} => {data}")
        return type("DummyResponse", (), {"ok": True, "json": lambda: {}})()
    url = f"{PFSENSE_API_HOST}/api/v1/{endpoint}"
    resp = requests.request(method, url, headers=headers, auth=auth, json=data, verify=False)
    return resp

# Build address fields based on type
def build_address_block(type_, value, iface):
    if type_ == "address" or type_ == "network":
        return {"address": value}
    elif type_ == "self_gateway":
        return {"address": f"{iface}_address"}
    elif type_ == "self_subnets":
        return {"address": f"{iface}_subnets"}
    return {}

# Translate interface target
def translate_interface(ref):
    if ref == "lan":
        return "lan"
    elif ref == "wan":
        return "wan"
    else:
        return f"OPT{ref}"

# Fetch existing rules by interface
def get_existing_rules():
    existing_rules = {}
    resp = call_api("GET", "firewall/rule")
    if resp.ok:
        rules = resp.json().get("data", [])
        for rule in rules:
            iface = rule.get("interface")
            descr = rule.get("descr")
            if iface not in existing_rules:
                existing_rules[iface] = {}
            existing_rules[iface][descr] = rule
    return existing_rules

# Deploy all rules
def deploy_rules():
    rules = load_rules()
    existing = get_existing_rules()
    desired_descriptions = set()

    for rule in rules:
        for net in rule.get("where_to_apply", []):
            iface = translate_interface(net)
            descr = rule["rule_description"]
            desired_descriptions.add((iface, descr))

            payload = {
                "interface": iface,
                "action": rule["action"],
                "ipprotocol": rule["address_family"],
                "protocol": rule["protocol"],
                "descr": descr,
                "source": build_address_block(rule["source_type"], rule["source"], iface),
                "destination": build_address_block(rule["destination_type"], rule["destination"], iface),
            }
            if "destination_port" in rule:
                payload["destination"]["port"] = str(rule["destination_port"])

            current_rule = existing.get(iface, {}).get(descr)
            if current_rule:
                # Check if update is needed
                if (current_rule.get("protocol") != payload["protocol"] or
                    current_rule.get("action") != payload["action"] or
                    current_rule.get("ipprotocol") != payload["ipprotocol"] or
                    current_rule.get("source", {}).get("address") != payload["source"]["address"] or
                    current_rule.get("destination", {}).get("address") != payload["destination"]["address"] or
                    current_rule.get("destination", {}).get("port") != payload["destination"].get("port")):
                    print(f"Updating rule: {iface} - {descr}")
                    call_api("PUT", f"firewall/rule/{current_rule['id']}", payload)
                else:
                    print(f"Rule already up-to-date: {iface} - {descr}")
            else:
                print(f"Creating rule: {iface} - {descr}")
                call_api("POST", "firewall/rule", payload)

    # Remove rules not in config
    for iface, rules_by_descr in existing.items():
        for descr, rule in rules_by_descr.items():
            if (iface, descr) not in desired_descriptions:
                print(f"Deleting rule: {iface} - {descr}")
                call_api("DELETE", f"firewall/rule/{rule['id']}")

    print("Firewall rule sync complete." + (" (dry run)" if dry_run else ""))

if __name__ == "__main__":
    deploy_rules()