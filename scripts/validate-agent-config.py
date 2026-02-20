#!/usr/bin/env python3
"""
Comprehensive agent configuration validation script.
Validates agent configurations across all agent directories.
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any

class AgentConfigValidator:
    def __init__(self):
        self.results = []
        self.errors = []
        
    def validate_all(self):
        """Run all validation checks."""
        print("🔍 Running comprehensive agent configuration validation...")
        
        # Check directory structure
        self.validate_directory_structure()
        
        # Validate agent configurations
        self.validate_agent_configs()
        
        # Validate rule structure
        self.validate_rule_structure()
        
        # Validate naming conventions
        self.validate_naming_conventions()
        
        # Validate dependencies
        self.validate_dependencies()
        
        # Print results
        self.print_results()
        
        return len(self.errors) == 0
    
    def validate_directory_structure(self):
        """Validate that all required directories exist."""
        required_dirs = [
            '.kilocode/agents',
            '.agents',
            '.kilocode/rules',
            '.clinerules/skills',
            '.gemini/rules'
        ]
        
        for dir_path in required_dirs:
            if not Path(dir_path).exists():
                self.errors.append(f"Missing required directory: {dir_path}")
                print(f"❌ {dir_path}")
            else:
                print(f"✅ {dir_path}")
    
    def validate_agent_configs(self):
        """Validate all agent configuration files."""
        agent_dirs = ['.kilocode/agents']
        
        for agent_dir in agent_dirs:
            if not Path(agent_dir).exists():
                continue
                
            for agent_file in Path(agent_dir).glob('*.json'):
                self.validate_agent_config(agent_file)
    
    def validate_agent_config(self, agent_file: Path):
        """Validate a single agent configuration file."""
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Check required fields
            required_fields = ['name', 'description', 'prompt']
            for field in required_fields:
                if field not in config:
                    self.errors.append(f"Missing required field '{field}' in {agent_file}")
                    return
            
            # Check prompt path
            prompt_path = config.get('prompt', '')
            if prompt_path and not Path(prompt_path).exists():
                self.errors.append(f"Prompt file not found: {prompt_path} in {agent_file}")
            
            print(f"✅ {agent_file.name}")
            
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in {agent_file}: {e}")
        except Exception as e:
            self.errors.append(f"Error validating {agent_file}: {e}")
    
    def validate_rule_structure(self):
        """Validate rule structure across all agent directories."""
        rule_dirs = ['.kilocode/rules', '.agents/rules', '.clinerules/skills', '.gemini/rules']
        
        critical_rules = [
            'server-preservation',
            'python-preferred',
            'cost-optimization',
            'bmad-integration'
        ]
        
        for rule_dir in rule_dirs:
            if not Path(rule_dir).exists():
                continue
                
            for rule in critical_rules:
                rule_file = Path(rule_dir) / f"{rule}.md"
                if not rule_file.exists():
                    self.errors.append(f"Missing critical rule: {rule_file}")
                else:
                    print(f"✅ {rule_dir}/{rule}.md")
    
    def validate_naming_conventions(self):
        """Validate agent naming conventions."""
        # Check for consistent naming patterns
        agent_files = list(Path('.kilocode/agents').glob('*.json'))
        
        for agent_file in agent_files:
            name = agent_file.stem
            if not name.startswith('bmad-') and name not in ['orchestrator', 'server-monitor', 'sysadmin']:
                self.errors.append(f"Agent name doesn't follow convention: {name}")
            else:
                print(f"✅ {name}")
    
    def validate_dependencies(self):
        """Validate dependency configurations."""
        deps_file = Path('.kilocode/config/dependencies.json')
        if deps_file.exists():
            try:
                with open(deps_file, 'r') as f:
                    deps = json.load(f)
                print("✅ Dependencies configuration")
            except json.JSONDecodeError:
                self.errors.append("Invalid dependencies.json")
        else:
            print("⚠️  No dependencies configuration found")
    
    def print_results(self):
        """Print validation results."""
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        
        if self.errors:
            print(f"❌ Validation completed with {len(self.errors)} errors:")
            for error in self.errors:
                print(f"  • {error}")
        else:
            print("✅ All validations passed!")

def main():
    """Main entry point."""
    validator = AgentConfigValidator()
    success = validator.validate_all()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()