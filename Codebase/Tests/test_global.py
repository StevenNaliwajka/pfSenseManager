import pytest
from Codebase.Deploy import deploy_global as dg

def test_missing_dns_resolver_config(monkeypatch):
    monkeypatch.setattr(dg, "load_global_config", lambda: {})
    dg.sync_global()  # Should not raise an error

def test_invalid_server_backend(monkeypatch):
    monkeypatch.setattr(dg, "load_global_config", lambda: {"server_backend": "nonsense"})
    dg.sync_global()  # Should warn or skip without crashing

def test_uppercase_keys(monkeypatch):
    monkeypatch.setattr(dg, "load_global_config", lambda: {"DNS_RESOLVER": "enable"})
    dg.sync_global()  # Should ignore unrecognized keys

def test_boolean_values_as_strings(monkeypatch):
    monkeypatch.setattr(dg, "load_global_config", lambda: {
        "dns_resolver": "True",  # Should interpret as enabled
        "dns_query_forwarding": "false"  # Should interpret as disabled
    })
    dg.sync_global()

def test_invalid_yaml(monkeypatch):
    monkeypatch.setattr(dg, "load_global_config", lambda: {"dns_resolver": None})
    dg.sync_global()  # Should handle gracefully
