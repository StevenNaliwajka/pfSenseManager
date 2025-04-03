import pytest
from Codebase.Deploy import deploy_dns_resolver as ddr

def test_duplicate_host_override(monkeypatch):
    monkeypatch.setattr(ddr, "load_dns_config", lambda: {
        "host_overrides": [
            {"host": "test", "parent_domain": "local", "ip_to_return": "1.1.1.1", "desc": "A"},
            {"host": "test", "parent_domain": "local", "ip_to_return": "1.1.1.2", "desc": "B"}
        ],
        "domain_overrides": []
    })
    ddr.sync_host_overrides(ddr.load_dns_config()["host_overrides"])  # Should detect or override

def test_empty_dns_entries(monkeypatch):
    monkeypatch.setattr(ddr, "load_dns_config", lambda: {
        "host_overrides": [],
        "domain_overrides": []
    })
    ddr.sync_host_overrides([])  # Should be a no-op
    ddr.sync_domain_overrides([])

def test_invalid_ip_override(monkeypatch):
    monkeypatch.setattr(ddr, "load_dns_config", lambda: {
        "host_overrides": [{
            "host": "broken", "parent_domain": "example.com",
            "ip_to_return": "not_an_ip", "desc": "oops"
        }],
        "domain_overrides": []
    })
    ddr.sync_host_overrides(ddr.load_dns_config()["host_overrides"])  # Should print an error

def test_domain_override_with_non_dns_ip(monkeypatch):
    monkeypatch.setattr(ddr, "load_dns_config", lambda: {
        "domain_overrides": [{
            "domain": "broken.domain",
            "lookup_ip_addr": "999.999.999.999",
            "desc": "Bad IP"
        }],
        "host_overrides": []
    })
    ddr.sync_domain_overrides(ddr.load_dns_config()["domain_overrides"])
