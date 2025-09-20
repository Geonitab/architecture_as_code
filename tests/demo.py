#!/usr/bin/env python3
"""
Demo script showcasing the content validation test suite.

This script demonstrates all the test suite capabilities.
"""
import subprocess
import sys
from pathlib import Path

def run_demo():
    """Run a comprehensive demo of the test suite."""
    
    print("🚀 Content Validation Test Suite Demo")
    print("=" * 60)
    
    # Change to project directory
    project_root = Path(__file__).parent.parent
    print(f"Project root: {project_root}")
    
    demos = [
        {
            "name": "📋 Completeness Tests",
            "description": "Validates all required chapters and sections exist",
            "command": ["python3", "tests/run_tests.py", "--type", "completeness", "--quiet"]
        },
        {
            "name": "🎯 Consistency Tests", 
            "description": "Ensures uniform formatting and style",
            "command": ["python3", "tests/run_tests.py", "--type", "consistency", "--quiet"]
        },
        {
            "name": "📖 Clarity Tests",
            "description": "Checks content quality and readability", 
            "command": ["python3", "tests/run_tests.py", "--type", "clarity", "--quiet"]
        },
        {
            "name": "⚙️ Technical Accuracy Tests",
            "description": "Validates code examples and technical content",
            "command": ["python3", "tests/run_tests.py", "--type", "technical", "--quiet"]
        }
    ]
    
    results = []
    
    for demo in demos:
        print(f"\n{demo['name']}")
        print(f"Description: {demo['description']}")
        print("-" * 40)
        
        try:
            result = subprocess.run(
                demo["command"],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            success = result.returncode == 0
            results.append({
                "name": demo["name"],
                "success": success,
                "returncode": result.returncode
            })
            
            if success:
                print("✅ All tests passed!")
            else:
                print("⚠️ Tests completed with warnings or issues")
            
            # Show brief output
            if result.stdout:
                lines = result.stdout.split('\n')
                summary_lines = [line for line in lines if 'passed' in line or 'failed' in line or 'warnings' in line]
                if summary_lines:
                    print(f"Summary: {summary_lines[-1]}")
                    
        except subprocess.TimeoutExpired:
            print("❌ Test timed out")
            results.append({"name": demo["name"], "success": False, "returncode": -1})
        except Exception as e:
            print(f"❌ Error running test: {e}")
            results.append({"name": demo["name"], "success": False, "returncode": -1})
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 DEMO SUMMARY")
    print("=" * 60)
    
    for result in results:
        status = "✅ PASSED" if result["success"] else "⚠️ WARNINGS" if result["returncode"] == 1 else "❌ FAILED"
        print(f"{result['name']:<30} {status}")
    
    passed_count = sum(1 for r in results if r["success"])
    total_count = len(results)
    
    print(f"\nOverall: {passed_count}/{total_count} test suites passed")
    
    print("\n📋 Available Reports:")
    report_dir = project_root / "test-reports"
    if report_dir.exists():
        for report in report_dir.glob("*.html"):
            print(f"  • {report.name}")
    
    print("\n🔧 Quick Start Commands:")
    print("  npm run test:content              # Run all tests")  
    print("  npm run test:content:report       # Generate HTML reports")
    print("  python3 tests/run_tests.py --help # See all options")
    
    print("\n💡 Integration:")
    print("  • Tests run automatically on PR/push via GitHub Actions")
    print("  • Reports uploaded as artifacts") 
    print("  • Warnings help improve content quality")
    print("  • Modular design allows easy expansion")

if __name__ == "__main__":
    run_demo()