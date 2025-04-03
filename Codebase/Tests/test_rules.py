import pytest
from Codebase.Deploy import deploy_rules as dr

def test_rule_with_invalid_destination_type(monkeypatch):
    monkeypatch.setattr(dr, "load_rules", lambda: [{
        "rule_description": "Bad Rule",
        "action": "pass",
        "address_family": "ipv4",
        "protocol": "tcp",
        "source_type": "address",
        "source": "192.168.0.1",
        "destination_type": "not_real_type",
        "destination": "n/a",
        "where_to_apply": ["lan"]
    }])
    dr.deploy_rules()  # Should skip or warn

def test_invalid_interface_ref(monkeypatch):
    monkeypatch.setattr(dr, "load_rules", lambda: [{
        "rule_description": "bad-iface",
        "action": "pass", "address_family": "ipv4", "protocol": "tcp",
        "source_type": "address", "source": "192.168.0.1",
        "destination_type": "address", "destination": "192.168.0.1",
        "where_to_apply": ["xyz"]  # Invalid interface reference
    }])
    dr.deploy_rules()  # Should skip or print a warning

def test_missing_required_fields(monkeypatch):
    monkeypatch.setattr(dr, "load_rules", lambda: [{}])
    dr.deploy_rules()  # Should handle missing keys gracefully

def test_firewall_rule_with_icmp(monkeypatch):
    monkeypatch.setattr(dr, "load_rules", lambda: [{
        "rule_description": "Allow ICMP",
        "action": "pass",
        "address_family": "ipv4",
        "protocol": "icmp",
        "source_type": "self_gateway",
        "source": "n/a",
        "destination_type": "network",
        "destination": "192.168.100.0/24",
        "where_to_apply": ["lan"]
    }])
    dr.deploy_rules()  # Should handle ICMP
