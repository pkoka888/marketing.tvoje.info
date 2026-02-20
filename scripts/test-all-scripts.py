#!/usr/bin/env python3
"""
Comprehensive script testing and validation.
"""

import os
import subprocess
import sys
import time
from pathlib import Path

class ScriptTester:
    def __init__(self):
        self.scripts_dir = Path("scripts")
        self.results = []
    
    def test_validation_scripts(self):
        """Test all validation scripts."""
        validation_scripts = [
            "validate-agent-config.py",
            "validate-dependencies.py",
            "verify_agentic_platform.py",
            "agent-resolver.py"
        ]
        
        for script in validation_scripts:
            script_path = self.scripts_dir / script
            if script_path.exists():
                self.run_script_test(script_path)
    
    def test_utility_scripts(self):
        """Test utility scripts."""
        utility_scripts = [
            "generate_images_advanced.py",
            "orchestrate.py",
            "setup_mcp_servers.py"
        ]
        
        for script in utility_scripts:
            script_path = self.scripts_dir / script
            if script_path.exists():
                self.run_script_test(script_path)
    
    def run_script_test(self, script_path):
        """Run individual script test."""
        print(f"Testing {script_path.name}...")
        
        start_time = time.time()
        try:
            result = subprocess.run(
                ["python", str(script_path)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            self.results.append({
                'script': script_path.name,
                'status': 'PASS' if result.returncode == 0 else 'FAIL',
                'duration': duration,
                'return_code': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            })
            
            print(f"  Status: {self.results[-1]['status']}")
            print(f"  Duration: {duration:.2f}s")
            
        except subprocess.TimeoutExpired:
            self.results.append({
                'script': script_path.name,
                'status': 'TIMEOUT',
                'duration': 300,
                'return_code': -1,
                'stdout': '',
                'stderr': 'Script timed out after 5 minutes'
            })
            print(f"  Status: TIMEOUT")
        
        except Exception as e:
            self.results.append({
                'script': script_path.name,
                'status': 'ERROR',
                'duration': 0,
                'return_code': -1,
                'stdout': '',
                'stderr': str(e)
            })
            print(f"  Status: ERROR - {e}")
    
    def generate_report(self):
        """Generate test report."""
        print("\n" + "="*60)
        print("SCRIPT TESTING REPORT")
        print("="*60)
        
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        timeout = sum(1 for r in self.results if r['status'] == 'TIMEOUT')
        error = sum(1 for r in self.results if r['status'] == 'ERROR')
        
        print(f"Total Scripts: {len(self.results)}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Timeout: {timeout}")
        print(f"Error: {error}")
        
        print("\nDetailed Results:")
        for result in self.results:
            print(f"  {result['script']}: {result['status']} ({result['duration']:.2f}s)")
        
        return passed == len(self.results)
    
    def run_all_tests(self):
        """Run all script tests."""
        print("Starting comprehensive script testing...")
        
        self.test_validation_scripts()
        self.test_utility_scripts()
        
        success = self.generate_report()
        return success

if __name__ == "__main__":
    tester = ScriptTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)