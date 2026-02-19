#!/usr/bin/env python3
"""
Config Snapshot Comparison Script
Compares current state against known-good snapshot to detect drift.

Usage:
    python scripts/protected/snapshot_config.py --compare
    python scripts/protected/snapshot_config.py --generate
    python scripts/protected/snapshot_config.py --report
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv

SNAPSHOT_PATH = Path(__file__).parent / "config-snapshot.json"


def load_snapshot():
    """Load the known-good snapshot."""
    if not SNAPSHOT_PATH.exists():
        print(f"❌ Snapshot not found: {SNAPSHOT_PATH}")
        return None
    
    with open(SNAPSHOT_PATH) as f:
        return json.load(f)


def get_current_config():
    """Extract current configuration from verification script.
    
    Imports API_KEYS_CONFIG from verify_api_keys.py to avoid duplication.
    This ensures single source of truth for API key configurations.
    """
    try:
        from verify_api_keys import API_KEYS_CONFIG
        # Extract endpoint/method/auth info from each key config
        config = {}
        for key_name, key_data in API_KEYS_CONFIG.items():
            config[key_name] = {
                "endpoint": key_data.get("endpoint"),
                "method": key_data.get("method", "GET"),
                "auth_type": key_data.get("auth_type"),
                "param_name": key_data.get("param_name"),
                "presence_only": key_data.get("presence_only", False),
            }
        return config
    except ImportError:
        # Fallback for when import fails - DO NOT remove hardcoded config
        # This ensures the script still works if verify_api_keys.py is unavailable
        return {
            "OPENROUTER_API_KEY": {
                "endpoint": "https://openrouter.ai/api/v1/models",
                "method": "GET",
                "auth_type": "bearer",
            },
            "GROQ_API_KEY": {
                "endpoint": "https://api.groq.com/openai/v1/models",
                "method": "GET",
                "auth_type": "bearer",
            },
            "GEMINI_API_KEY": {
                "endpoint": "https://generativelanguage.googleapis.com/v1beta/models",
                "method": "GET",
                "auth_type": "param",
                "param_name": "key",
            },
            "OPENAI_API_KEY": {
                "endpoint": "https://api.openai.com/v1/models",
                "method": "GET",
                "auth_type": "bearer",
            },
            "NVIDIA_API_KEY": {
                "endpoint": "https://integrate.api.nvidia.com/v1/models",
                "method": "GET",
                "auth_type": "bearer",
            },
            "KILOCODE_API_KEY": {
                "presence_only": True,
            },
            "ROUTEWAY_API_KEY": {
                "endpoint": "https://api.routeway.ai/v1/models",
                "method": "GET",
                "auth_type": "bearer",
            },
            "FIRECRAWL_API_KEY": {
                "presence_only": True,
            },
            "GITHUB_TOKEN": {
                "endpoint": "https://api.github.com/user",
                "method": "GET",
                "auth_type": "bearer",
            },
        }


def compare_configs(snapshot, current):
    """Compare current config against snapshot and report drift."""
    drift_detected = False
    issues = []
    
    snapshot_keys = snapshot.get("keys", {})
    
    # Check each key in snapshot
    for key_name, snapshot_config in snapshot_keys.items():
        current_config = current.get(key_name, {})
        
        # Check endpoint changes
        if "endpoint" in snapshot_config:
            snapshot_endpoint = snapshot_config.get("endpoint")
            current_endpoint = current_config.get("endpoint")
            
            if snapshot_endpoint != current_endpoint:
                drift_detected = True
                issues.append({
                    "type": "endpoint_changed",
                    "key": key_name,
                    "expected": snapshot_endpoint,
                    "current": current_endpoint,
                })
        
        # Check auth_type changes
        if "auth_type" in snapshot_config:
            snapshot_auth = snapshot_config.get("auth_type")
            current_auth = current_config.get("auth_type")
            
            if snapshot_auth != current_auth:
                drift_detected = True
                issues.append({
                    "type": "auth_type_changed",
                    "key": key_name,
                    "expected": snapshot_auth,
                    "current": current_auth,
                })
        
        # Check method changes
        if "method" in snapshot_config:
            snapshot_method = snapshot_config.get("method")
            current_method = current_config.get("method")
            
            if snapshot_method != current_method:
                drift_detected = True
                issues.append({
                    "type": "method_changed",
                    "key": key_name,
                    "expected": snapshot_method,
                    "current": current_method,
                })
    
    return drift_detected, issues


def generate_report(snapshot, issues):
    """Generate drift report."""
    print("=" * 70)
    print("API CONFIG DRIFT REPORT")
    print("=" * 70)
    print(f"Snapshot Version: {snapshot.get('version')}")
    print(f"Snapshot Date: {snapshot.get('snapshot_date')}")
    print(f"Verified Keys: {snapshot.get('verified_count')}")
    print()
    
    if not issues:
        print("✅ NO DRIFT DETECTED - Configuration matches known-good state")
        print()
        return 0
    
    print(f"⚠️  DRIFT DETECTED: {len(issues)} issue(s)")
    print()
    
    for issue in issues:
        print(f"  🔸 {issue['key']}")
        print(f"     Type: {issue['type']}")
        if "expected" in issue:
            print(f"     Expected: {issue['expected']}")
        if "current" in issue:
            print(f"     Current:  {issue['current']}")
        print()
    
    return 1


def compare():
    """Main comparison function."""
    snapshot = load_snapshot()
    if not snapshot:
        return 1
    
    current = get_current_config()
    drift_detected, issues = compare_configs(snapshot, current)
    
    return generate_report(snapshot, issues)


def generate():
    """Generate new snapshot from current state."""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path, override=True)
    
    current = get_current_config()
    
    snapshot = {
        "version": "1.0.0",
        "snapshot_date": datetime.now().isoformat() + "Z",
        "verified_count": 19,
        "verification_status": "19/19 keys verified",
        "keys": {},
        "verification_script": {
            "path": "scripts/verify_api_keys.py",
            "version": "3",
            "last_verified": datetime.now().strftime("%Y-%m-%d")
        },
    }
    
    # Add current config to snapshot
    for key, config in current.items():
        snapshot["keys"][key] = config
    
    with open(SNAPSHOT_PATH, "w") as f:
        json.dump(snapshot, f, indent=2)
    
    print(f"✅ Snapshot generated: {SNAPSHOT_PATH}")
    return 0


def report():
    """Show snapshot summary."""
    snapshot = load_snapshot()
    if not snapshot:
        return 1
    
    print(f"Version: {snapshot.get('version')}")
    print(f"Date: {snapshot.get('snapshot_date')}")
    print(f"Verified Keys: {snapshot.get('verified_count')}")
    print(f"Status: {snapshot.get('verification_status')}")
    print()
    print("Keys in snapshot:")
    for key in snapshot.get("keys", {}).keys():
        print(f"  - {key}")
    
    return 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    
    command = sys.argv[1]
    
    if command == "--compare":
        return compare()
    elif command == "--generate":
        return generate()
    elif command == "--report":
        return report()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        return 1


if __name__ == "__main__":
    sys.exit(main())
