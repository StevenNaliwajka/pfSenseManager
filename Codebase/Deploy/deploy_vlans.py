import os
import requests
import yaml
import sys

CONFIG_PATH = "./Config/pfbox_api.env"
VLAN_FILE = "./Config/vlans.yaml"

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

# Load VLANs config
def load_vlans():
    with open(VLAN_FILE, "r") as f:
        return yaml.safe_load(f).get("vlans", [])

# API helper
def call_api(method, endpoint, data=None):
    if dry_run and method in ["POST", "PUT", "DELETE"]:
        print(f"[Dry Run] {method} {endpoint} => {data}")
        return type("DummyResponse", (), {"ok": True, "json": lambda: {}})()
    url = f"{PFSENSE_API_HOST}/api/v1/{endpoint}"
    resp = requests.request(method, url, headers=headers, auth=auth, json=data, verify=False)
    if not resp.ok:
        print(f"Error [{resp.status_code}] {endpoint}: {resp.text}")
    else:
        print(f"{endpoint} success")
    return resp

# Deploy VLANs, Interfaces, DHCP
def deploy_vlan_stack():
    vlans = load_vlans()
    for vlan in vlans:
        vlan_tag = vlan["tag"]
        vlan_if = vlan["if"]
        vlan_name = f"vlan{vlan_tag}"
        opt_iface = f"OPT{vlan_tag}"  # crude assumption, customize if needed

        # --- Step 1: Create VLAN ---
        vlan_payload = {
            "if": vlan_if,
            "tag": vlan_tag,
            "descr": vlan.get("description", f"VLAN {vlan_tag}"),
            "pcp": vlan.get("pcp", 0)
        }
        call_api("POST", "interfaces/vlan", vlan_payload)

        # --- Step 2: Assign VLAN to OPT interface ---
        iface_payload = {
            "interface": vlan_name,
            "descr": vlan.get("description", f"VLAN {vlan_tag}")
        }
        call_api("POST", "interfaces/assignments", iface_payload)

        # --- Step 3: Configure Interface ---
        interface_config = {
            "enable": True,
            "descr": vlan.get("description", f"VLAN {vlan_tag}"),
            "ipaddr": vlan.get("ipv4_address"),
            "subnet": vlan.get("subnet"),
            "type": "staticv4"
        }
        call_api("PUT", f"interfaces/{opt_iface}", interface_config)

        # --- Step 4: Configure DHCP ---
        dhcp_config = {
            "enable": True,
            "range": {
                "from": vlan.get("dhcp_pool_min_ip"),
                "to": vlan.get("dhcp_pool_max_ip")
            },
            "defaultleasetime": vlan.get("dhcp_default_lease_time", 7200),
            "maxleasetime": vlan.get("dhcp_max_lease_time", 86400),
            "dnsserver": [vlan.get("dhcp_dns_server")],
            "gateway": vlan.get("dhcp_gateway")
        }

        # Optional static mappings
        static_mappings = vlan.get("dhcp_static_mappings", [])
        if static_mappings:
            dhcp_config["staticmap"] = [
                {
                    "mac": m["mac_address"],
                    "ipaddr": m["ip_address"],
                    "descr": m.get("description", "")
                }
                for m in static_mappings
            ]

        call_api("PUT", f"services/dhcp/server/{opt_iface}", dhcp_config)

if __name__ == "__main__":
    deploy_vlan_stack()
