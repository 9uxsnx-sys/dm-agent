#!/usr/bin/env python3
"""Run all tests."""
import subprocess
import sys

def main():
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], cwd="c:\dm-agent")
    return result.returncode

if __name__ == "__main__":
    sys.exit(main())
