import pytest
from Codebase.Deploy import deploy_vlans as dv

def test_vlan_with_missing_fields(monkeypatch):
    monkeypatch.setattr(dv, "load_vlans", lambda: [{
        "tag": 30,
        "if": "igb1"  # Missing IP info
    }])
    dv.deploy_vlan_stack()  # Should not crash

def test_vlan_conflicting_tags(monkeypatch):
    monkeypatch.setattr(dv, "load_vlans", lambda: [
        {"tag": 10, "if": "igb1", "ipv4_address": "192.168.10.1", "subnet": 24},
        {"tag": 10, "if": "igb2", "ipv4_address": "192.168.20.1", "subnet": 24}
    ])
    dv.deploy_vlan_stack()  # Should raise warning about conflicts

def test_dhcp_missing_range(monkeypatch):
    monkeypatch.setattr(dv, "load_vlans", lambda: [{
        "tag": 99, "if": "igb1", "ipv4_address": "192.168.99.1", "subnet": 24,
        "dhcp_dns_server": "192.168.99.1", "dhcp_gateway": "192.168.99.1"
    }])
    dv.deploy_vlan_stack()  # Should not crash without a range

def test_vlan_with_reserved_tag(monkeypatch):
    monkeypatch.setattr(dv, "load_vlans", lambda: [{
        "tag": 1,  # Often reserved
        "if": "igb1",
        "ipv4_address": "192.168.50.1",
        "subnet": 24
    }])
    dv.deploy_vlan_stack()  # Should allow or warn
