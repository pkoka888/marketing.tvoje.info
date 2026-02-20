#!/usr/bin/env python3
"""
Archival Dependency Verification Script

This script scans the project for dependencies on directories before archival.
It helps identify potential risks before removing any repository or directory.

Usage:
    python scripts/verify-archival-dependencies.py <directory_to_archive>
    
Example:
    python scripts/verify-archival-dependencies.py tmp-agentic/old-repo
"""

import os
import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import argparse


class DependencyVerifier:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.findings: Dict[str, List[str]] = {
            "file_references": [],
            "config_references": [],
            "imports": [],
            "submodules": [],
            "git_references": []
        }
        self.risk_level = "LOW"
        
    def scan_for_references(self, directory_name: str) -> Dict[str, List[str]]:
        """Scan entire project for references to the directory."""
        print(f"🔍 Scanning for references to '{directory_name}'...")
        
        # Normalize directory name for comparison
        dir_name = directory_name.strip("/\\").lower()
        
        # File extensions to scan
        extensions = [".py", ".js", ".ts", ".mjs", ".cjs", ".json", ".yml", 
                     ".yaml", ".md", ".txt", ".sh", ".bat", ".toml", ".ini",
                     ".lock", ".env", ".config", ".html", ".css"]
        
        scanned_files = 0
        for root, dirs, files in os.walk(self.project_root):
            # Skip .git and node_modules
            if ".git" in root or "node_modules" in root:
                continue
                
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    scanned_files += 1
                    self._scan_file(file_path, dir_name)
        
        print(f"✅ Scanned {scanned_files} files")
        return self.findings
    
    def _scan_file(self, file_path: str, dir_name: str):
        """Scan a single file for references."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Check for directory reference
            if dir_name in content.lower():
                relative_path = os.path.relpath(file_path, self.project_root)
                self.findings["file_references"].append(relative_path)
                
                # Check if it's a config reference
                if any(ext in file_path for ext in [".json", ".yml", ".yaml", ".toml"]):
                    self.findings["config_references"].append(relative_path)
                
                # Check for import statements
                if "import" in content or "require(" in content or "from" in content:
                    self.findings["imports"].append(relative_path)
                    
        except Exception as e:
            pass  # Skip files that can't be read
    
    def check_git_submodules(self, directory_name: str) -> List[str]:
        """Check if directory is a git submodule."""
        gitmodules_path = self.project_root / ".gitmodules"
        if gitmodules_path.exists():
            with open(gitmodules_path, 'r') as f:
                content = f.read()
                if directory_name in content:
                    self.findings["submodules"].append(".gitmodules")
        return self.findings["submodules"]
    
    def calculate_risk_level(self) -> str:
        """Calculate risk level based on findings."""
        total_references = (
            len(self.findings["file_references"]) +
            len(self.findings["config_references"]) * 2 +  # Weight configs more
            len(self.findings["submodules"]) * 3  # Weight submodules most
        )
        
        if total_references == 0:
            self.risk_level = "LOW"
        elif total_references < 5:
            self.risk_level = "MEDIUM"
        else:
            self.risk_level = "HIGH"
            
        return self.risk_level
    
    def generate_report(self, directory_name: str) -> str:
        """Generate a detailed risk assessment report."""
        risk = self.calculate_risk_level()
        
        report = f"""
================================================================================
                    ARCHIVAL DEPENDENCY VERIFICATION REPORT
================================================================================

Directory: {directory_name}
Risk Level: {risk}

--------------------------------------------------------------------------------
FINDINGS SUMMARY
--------------------------------------------------------------------------------

Total File References: {len(self.findings['file_references'])}
Configuration References: {len(self.findings['config_references'])}
Import Statements: {len(self.findings['imports'])}
Git Submodules: {len(self.findings['submodules'])}

"""
        
        if self.findings["file_references"]:
            report += "File References:\n"
            for ref in self.findings["file_references"]:
                report += f"  - {ref}\n"
            report += "\n"
            
        if self.findings["config_references"]:
            report += "Configuration References (HIGH PRIORITY):\n"
            for ref in self.findings["config_references"]:
                report += f"  - {ref}\n"
            report += "\n"
            
        if self.findings["submodules"]:
            report += "Git Submodule References (CRITICAL):\n"
            for ref in self.findings["submodules"]:
                report += f"  - {ref}\n"
            report += "\n"
        
        # Add recommendations
        report += f"""
--------------------------------------------------------------------------------
RECOMMENDATIONS
--------------------------------------------------------------------------------
"""
        
        if risk == "LOW":
            report += """
✅ SAFE TO ARCHIVE: No significant dependencies found.
   - Directory can be safely moved to archive.
   - No configuration or submodule dependencies detected.
   - No critical imports or references found.
"""
        elif risk == "MEDIUM":
            report += """
⚠️  CAUTION ADVISED: Some dependencies found.
   - Review file references before archival.
   - Check configuration files for hardcoded paths.
   - Consider updating references if necessary.
"""
        else:
            report += """
❌ HIGH RISK: Significant dependencies found.
   - DO NOT ARCHIVE without further analysis.
   - Review all configuration references.
   - Check for git submodule dependencies.
   - Update all references before archival.
"""
        
        report += """
--------------------------------------------------------------------------------
NEXT STEPS
--------------------------------------------------------------------------------

1. Review the findings above
2. If risk is MEDIUM or HIGH, investigate each reference
3. Update or remove references as needed
4. Re-run verification after making changes
5. Only proceed with archival after risk is LOW

================================================================================
"""
        
        return report


def main():
    parser = argparse.ArgumentParser(
        description="Verify dependencies before archiving a directory"
    )
    parser.add_argument(
        "directory",
        help="Directory to verify for archival"
    )
    parser.add_argument(
        "--project-root",
        default=".",
        help="Project root directory (default: current directory)"
    )
    
    args = parser.parse_args()
    
    verifier = DependencyVerifier(args.project_root)
    
    # Scan for references
    verifier.scan_for_references(args.directory)
    
    # Check git submodules
    verifier.check_git_submodules(args.directory)
    
    # Generate and print report
    report = verifier.generate_report(args.directory)
    print(report)
    
    # Exit with appropriate code
    if verifier.risk_level == "HIGH":
        sys.exit(2)
    elif verifier.risk_level == "MEDIUM":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()