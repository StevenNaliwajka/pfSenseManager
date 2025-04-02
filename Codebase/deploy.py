import os
import requests
import yaml

# Load API credentials
CONFIG_PATH = "./Config/pfbox_api.env"
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

# Basic auth for all API calls
auth = (PFSENSE_API_USER, PFSENSE_API_PASS)
headers = {"Content-Type": "application/json"}

# Function to load YAML config
def load_yaml(file_name):
    with open(os.path.join("./Config", file_name)) as f:
        return yaml.safe_load(f)

# Function to call pfSense API
def call_api(method, endpoint, data=None):
    url = f"{PFSENSE_API_HOST}/api/v1/{endpoint}"
    resp = requests.request(method, url, headers=headers, auth=auth, json=data, verify=False)
    if not resp.ok:
        print(f"API call to {endpoint} failed: {resp.status_code} {resp.text}")
    else:
        print(f"{endpoint} updated.")
    return resp


def deploy_vlans():
    vlans = load_yaml("vlans.yaml")
    for vlan in vlans.get("vlans", []):
        call_api("POST", "interfaces/vlan", vlan)

def deploy_interfaces():
    interfaces = load_yaml("interfaces.yaml")
    for iface in interfaces.get("interfaces", []):
        call_api("POST", "interfaces/assignments", iface)

def deploy_dhcp():
    dhcp = load_yaml("dhcp_servers.yaml")
    for entry in dhcp.get("dhcp", []):
        interface = entry.pop("interface")
        call_api("PUT", f"services/dhcp/server/{interface}", entry)

def deploy_dns():
    dns_entries = load_yaml("dns_overrides.yaml")
    for entry in dns_entries.get("dns", []):
        call_api("POST", "services/unbound/host_override", entry)

def deploy_firewall():
    rules = load_yaml("firewall_rules.yaml")
    for rule in rules.get("firewall_rules", []):
        call_api("POST", "firewall/rule", rule)

def deploy_nat():
    nat_rules = load_yaml("nat_rules.yaml")
    for rule in nat_rules.get("nat", []):
        call_api("POST", "firewall/nat/port_forward", rule)

def deploy_wan():
    wan = load_yaml("wan.yaml")
    wan_config = wan.get("wan", {})
    if wan_config:
        call_api("PUT", "interfaces/WAN", wan_config)

if __name__ == "__main__":
    deploy_vlans()
    deploy_interfaces()
    deploy_dhcp()
    deploy_dns()
    deploy_firewall()
    deploy_nat()
    deploy_wan()
    print("\npfSenseManager deployment complete.")
