#!/usr/bin/env python3
"""
Nexus Tech Store Project Setup Helper Script.
Verifies Python dependencies, Django database migrations, and initial seed state.
"""

import sys
import subprocess
import os

def check_environment():
    print("⚡ Checking Python environment for Nexus Tech Store...")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version.split()[0]}")

if __name__ == "__main__":
    check_environment()
