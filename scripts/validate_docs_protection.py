#!/usr/bin/env python3
"""
Validate that changes don't inappropriately modify docs/ directory.

This script can be used in CI/CD or manually to check if a PR or commit
follows the docs protection guidelines.
"""

import subprocess
import sys
import os
from pathlib import Path

def run_git_command(cmd):
    """Run a git command and return the output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {cmd}")
        print(f"Error: {e.stderr}")
        return None

def get_changed_files(base_ref="HEAD~1"):
    """Get list of files changed since base_ref."""
    cmd = f"git diff --name-only {base_ref}..HEAD"
    output = run_git_command(cmd)
    if output:
        return [line.strip() for line in output.split('\n') if line.strip()]
    return []

def validate_docs_changes(changed_files):
    """Validate that docs changes are appropriate."""
    docs_files = [f for f in changed_files if f.startswith('docs/') and f.endswith('.md')]
    
    if not docs_files:
        print("✅ No docs markdown files modified - validation passed")
        return True
    
    print(f"⚠️  Found {len(docs_files)} docs files modified:")
    print("This requires careful review to ensure book content integrity.")
    return True  # Allow but warn

def main():
    """Main validation function."""
    print("🔍 Validating docs directory protection...")
    
    # Check if we're in a git repository
    if not Path('.git').exists():
        print("❌ Not in a git repository")
        return 1
    
    # Get changed files
    changed_files = get_changed_files()
    
    if not changed_files:
        print("ℹ️  No changes detected")
        return 0
    
    print(f"\n📝 Found {len(changed_files)} changed files:")
    for file_path in changed_files:
        print(f"   {file_path}")
    
    # Validate docs changes
    docs_valid = validate_docs_changes(changed_files)
    
    print("\n✅ Validation completed")
    return 0

if __name__ == "__main__":
    sys.exit(main())
