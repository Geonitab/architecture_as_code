#!/usr/bin/env python3
"""
Content validation test runner for "Arkitektur som Kod" book.

This script runs the complete test suite and generates reports.
"""
import sys
import subprocess
import argparse
from pathlib import Path
import os

def install_requirements():
    """Install required Python packages."""
    requirements = [
        "pytest>=7.0.0",
        "pytest-html>=3.1.0",
        "pyyaml>=6.0.0"
    ]
    
    print("Installing Python test dependencies...")
    for req in requirements:
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", req
            ], check=True, capture_output=True)
            print(f"✓ Installed {req}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {req}: {e}")
            return False
    return True

def ensure_dependencies_installed():
    """Ensure runtime Python dependencies required by the test suite are available."""

    try:
        import yaml  # noqa: F401 - we only need to ensure the package can be imported
    except ModuleNotFoundError:
        print("Required dependency 'pyyaml' is missing. Attempting automatic installation...")
        if not install_requirements():
            print("Failed to install required test dependencies. Aborting.")
            return False
    return True


def run_tests(test_type="all", verbose=True, generate_report=True):
    """Run content validation tests."""

    if not ensure_dependencies_installed():
        return 1
    
    # Ensure we're in the right directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    # Create report directory
    report_dir = project_root / "test-reports"
    report_dir.mkdir(exist_ok=True)
    
    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]
    
    # Select test files based on type
    if test_type == "completeness":
        cmd.append("tests/test_completeness.py")
    elif test_type == "consistency":
        cmd.append("tests/test_consistency.py")
    elif test_type == "clarity":
        cmd.append("tests/test_clarity.py")
    elif test_type == "technical":
        cmd.append("tests/test_technical_accuracy.py")
    else:
        cmd.append("tests/")
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    
    # Add HTML report generation
    if generate_report:
        report_file = report_dir / f"content-validation-{test_type}.html"
        cmd.extend([
            "--html", str(report_file),
            "--self-contained-html"
        ])
    
    # Add warnings summary
    cmd.append("-W ignore::pytest.PytestUnraisableExceptionWarning")
    
    print(f"Running content validation tests ({test_type})...")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, check=False)
        
        if result.returncode == 0:
            print("\n✓ All tests passed!")
        elif result.returncode == 1:
            print("\n⚠ Some tests failed or had warnings")
        else:
            print(f"\n✗ Test execution failed with code {result.returncode}")
        
        if generate_report:
            print(f"\nTest report generated: {report_file}")
            
            # Apply mobile responsiveness to the generated report
            try:
                mobile_script = script_dir / "make_mobile_responsive.py"
                subprocess.run([sys.executable, str(mobile_script), str(report_file)], 
                              check=True, capture_output=True)
                print(f"✓ Mobile responsiveness applied to {report_file.name}")
            except subprocess.CalledProcessError as e:
                print(f"⚠ Warning: Could not apply mobile responsiveness: {e}")
            except Exception as e:
                print(f"⚠ Warning: Mobile responsiveness error: {e}")
        
        return result.returncode
        
    except FileNotFoundError:
        print("Error: pytest not found. Please install pytest first.")
        return 1
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Content validation test runner for Arkitektur som Kod book"
    )
    parser.add_argument(
        "--type", 
        choices=["all", "completeness", "consistency", "clarity", "technical"],
        default="all",
        help="Type of tests to run (default: all)"
    )
    parser.add_argument(
        "--install-deps", 
        action="store_true",
        help="Install required Python dependencies"
    )
    parser.add_argument(
        "--no-report", 
        action="store_true",
        help="Skip HTML report generation"
    )
    parser.add_argument(
        "--quiet", 
        action="store_true",
        help="Reduce output verbosity"
    )
    
    args = parser.parse_args()
    
    # Install dependencies if requested
    if args.install_deps:
        if not install_requirements():
            print("Failed to install dependencies")
            return 1
        print("-" * 60)
    
    # Run tests
    return run_tests(
        test_type=args.type,
        verbose=not args.quiet,
        generate_report=not args.no_report
    )

if __name__ == "__main__":
    sys.exit(main())