import yaml
import json
import sys
import os

def validate_yaml(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        print(f"✅ {file_path} is valid YAML")
        return True
    except Exception as e:
        print(f"❌ {file_path} invalid YAML: {e}")
        return False

def validate_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            json.load(f)
        print(f"✅ {file_path} is valid JSON")
        return True
    except Exception as e:
        print(f"❌ {file_path} invalid JSON: {e}")
        return False

if __name__ == "__main__":
    success = True
    project_root = "."
    
    # Check .kilocodemodes
    if not validate_yaml(".kilocodemodes"):
        success = False
        
    # Check agents
    agent_dir = ".kilocode/agents"
    if os.path.exists(agent_dir):
        for file in os.listdir(agent_dir):
            if file.endswith(".json"):
                if not validate_json(os.path.join(agent_dir, file)):
                    success = False

    if not success:
        sys.exit(1)
