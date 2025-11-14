#!/usr/bin/env python3
"""
Test runner script for LinkedIn MCP Server.

Usage:
    python tests/run_tests.py [options]

Examples:
    python tests/run_tests.py --all                # Run all tests
    python tests/run_tests.py --scraping           # Scraping tests only
    python tests/run_tests.py --api                # API tests only
    python tests/run_tests.py --integration        # Integration tests only
    python tests/run_tests.py --coverage           # Generate coverage report
    python tests/run_tests.py --quick              # Quick tests (no integration)
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd):
    """Run a shell command and return the exit code."""
    print(f"\n{'='*60}")
    print(f"Running: {' '.join(cmd)}")
    print(f"{'='*60}\n")
    
    result = subprocess.run(cmd)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description="Run LinkedIn MCP Server tests")
    
    # Test selection
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--scraping", action="store_true", help="Run scraping tool tests")
    parser.add_argument("--api", action="store_true", help="Run API tool tests")
    parser.add_argument("--integration", action="store_true", help="Run integration tests")
    parser.add_argument("--error-handling", action="store_true", help="Run error handling tests")
    parser.add_argument("--quick", action="store_true", help="Run quick tests (no integration)")
    
    # Options
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--failed", action="store_true", help="Rerun only failed tests")
    parser.add_argument("--marks", type=str, help="Run tests with specific markers")
    
    args = parser.parse_args()
    
    # Build pytest command
    cmd = ["pytest"]
    
    # Determine which tests to run
    if args.scraping:
        cmd.append("tests/test_scraping_tools.py")
    elif args.api:
        cmd.append("tests/test_api_tools.py")
    elif args.integration:
        cmd.append("tests/test_integration.py")
    elif args.error_handling:
        cmd.append("tests/test_error_handling.py")
    elif args.quick:
        cmd.extend(["tests/", "-m", "not integration and not slow"])
    elif args.all:
        cmd.append("tests/")
    else:
        # Default: run non-integration tests
        cmd.extend(["tests/", "-m", "not integration"])
    
    # Add options
    if args.verbose:
        cmd.append("-v")
    
    if args.coverage:
        cmd.extend([
            "--cov=linkedin_mcp_server",
            "--cov-report=html",
            "--cov-report=term"
        ])
    
    if args.failed:
        cmd.append("--lf")
    
    if args.marks:
        cmd.extend(["-m", args.marks])
    
    # Run the tests
    exit_code = run_command(cmd)
    
    # Print summary
    print(f"\n{'='*60}")
    if exit_code == 0:
        print("✅ All tests passed!")
    else:
        print("❌ Some tests failed!")
    print(f"{'='*60}\n")
    
    # Open coverage report if generated
    if args.coverage and exit_code == 0:
        print("\n📊 Coverage report generated at: htmlcov/index.html")
        print("To view: open htmlcov/index.html (macOS) or start htmlcov/index.html (Windows)\n")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
