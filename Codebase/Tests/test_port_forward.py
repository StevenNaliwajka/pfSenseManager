import pytest
from Codebase.Deploy import deploy_port_forward as dpf

def test_forward_with_bad_port(monkeypatch):
    monkeypatch.setattr(dpf, "load_forwarding", lambda: [{
        "description": "BadPort",
        "protocol": "tcp",
        "destination_type": "self_gateway",
        "destination": "n/a",
        "destination_port_min": 99999,  # invalid port
        "destination_port_max": 99999,
        "redirect_target_ip": "192.168.1.10",
        "redirect_target_port": 443,
        "nat_reflection": "Enable (Pure NAT)"
    }])
    dpf.deploy_port_forwards()  # Should handle gracefully

def test_mismatched_port_range(monkeypatch):
    monkeypatch.setattr(dpf, "load_forwarding", lambda: [{
        "description": "bad_range",
        "protocol": "tcp",
        "destination_type": "self_gateway", "destination": "n/a",
        "destination_port_min": 8081,
        "destination_port_max": 8080,  # Invalid order
        "redirect_target_ip": "192.168.1.100",
        "redirect_target_port": 80,
        "nat_reflection": "Enable (Pure NAT)"
    }])
    dpf.deploy_port_forwards()  # Should detect or reorder automatically

def test_port_forward_to_invalid_internal_ip(monkeypatch):
    monkeypatch.setattr(dpf, "load_forwarding", lambda: [{
        "description": "bad_ip_forward",
        "protocol": "tcp",
        "destination_type": "address",
        "destination": "192.168.1.1",
        "destination_port_min": 80,
        "destination_port_max": 80,
        "redirect_target_ip": "192.999.999.999",  # invalid
        "redirect_target_port": 80,
        "nat_reflection": "Enable (Pure NAT)"
    }])
    dpf.deploy_port_forwards()
