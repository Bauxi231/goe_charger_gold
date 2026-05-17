"""Tests for the goe_charger_gold manifest."""

import json
from pathlib import Path

import pytest


def test_manifest_exists():
    """Test that the manifest.json file exists."""
    manifest_path = Path(__file__).parent.parent / "manifest.json"
    assert manifest_path.exists(), "manifest.json not found"


def test_manifest_valid_json():
    """Test that the manifest.json is valid JSON."""
    manifest_path = Path(__file__).parent.parent / "manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)
    assert isinstance(manifest, dict), "manifest.json is not a valid JSON object"


def test_manifest_has_required_fields():
    """Test that the manifest.json has required fields."""
    manifest_path = Path(__file__).parent.parent / "manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)

    required_fields = ["domain", "name", "version", "config_flow"]
    for field in required_fields:
        assert field in manifest, f"Missing required field: {field}"


def test_manifest_quality_scale_gold():
    """Test that the manifest.json declares Gold quality scale."""
    manifest_path = Path(__file__).parent.parent / "manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)

    assert manifest.get("quality_scale") == "gold", "quality_scale is not set to 'gold'"
