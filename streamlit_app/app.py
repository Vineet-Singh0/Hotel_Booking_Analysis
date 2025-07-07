#!/usr/bin/env python3
"""
Hotel Analytics Dashboard - Main Entry Point
"""

import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the dashboard
from hotel_dashboard import main

if __name__ == "__main__":
    main() 