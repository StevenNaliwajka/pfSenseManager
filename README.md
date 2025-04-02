# pfSenseManager
**Config-based pfSense configuration and management tool.**  
Define your network once in YAML — pfSenseManager handles the rest.

--------
## Features:
- VLAN creation and interface mapping
- DHCP server setup per VLAN
- NAT and port forwarding rules
- Firewall rule configuration
- DNS resolver/host overrides
- All config defined via simple YAML files

-------

## Setup:
### On your pfSense box
1) Install and go through base setup for pfSense.
2) Ensure SSH is enabled on your pfSense Box.

> You do **not** need to install anything manually on pfSense — pfSenseManager will handle the rest.

### On machine B:
1) Clone this repo:
```bash
sudo git clone https://github.com/StevenNaliwajka/pfSenseManager /opt/pfSenseManager
cd /opt/pfSenseManager
```
2) Run Setup:
```bash
sudo bash setup.sh
```
3) Edit your configuration files:
```bash
cd /Config/
```

## Run:
1) Run pfSenseManager to deploy configs
```bash
sudo bash run.sh
```
2) If first time setup, input ssh info as prompted to allow getting API token.
