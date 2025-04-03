import pytest
from Codebase.Deploy import deploy_aliases as da

def test_alias_with_invalid_type(monkeypatch):
    monkeypatch.setattr(da, "load_aliases", lambda: [{
        "name": "bad_alias",
        "type": "INVALID_TYPE",
        "desc": "Should Fail",
        "address": ["192.168.1.1"]
    }])
    da.sync_aliases()  # Should handle gracefully

def test_alias_empty_address(monkeypatch):
    monkeypatch.setattr(da, "load_aliases", lambda: [{
        "name": "empty_test",
        "type": "network",
        "desc": "No addresses",
        "address": []
    }])
    da.sync_aliases()  # Should warn or skip

def test_duplicate_alias_names(monkeypatch):
    monkeypatch.setattr(da, "load_aliases", lambda: [
        {"name": "dup", "type": "host", "desc": "1", "address": ["1.1.1.1"]},
        {"name": "dup", "type": "host", "desc": "2", "address": ["2.2.2.2"]}
    ])
    da.sync_aliases()  # Should only apply the last or warn

def test_alias_with_mixed_address_types(monkeypatch):
    monkeypatch.setattr(da, "load_aliases", lambda: [{
        "name": "mixed_alias",
        "type": "network",
        "desc": "Mixed",
        "address": ["192.168.1.1", "10.0.0.0/8", "abc.def.ghi.jkl"]
    }])
    da.sync_aliases()  # Should validate entries

def test_alias_with_special_characters(monkeypatch):
    monkeypatch.setattr(da, "load_aliases", lambda: [{
        "name": "danger$alias",
        "type": "host",
        "desc": "Special chars",
        "address": ["8.8.8.8"]
    }])
    da.sync_aliases()  # Should reject or sanitize
