#!/usr/bin/env python3
"""
Simple dashboard startup script
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

def start_dashboard():
    """Start the dashboard application"""
    try:
        from dashboard.app import main
        print("🚀 Starting Mining Reliability Dashboard...")
        print("Dashboard will be available at: http://localhost:8050")
        print("Press Ctrl+C to stop the server")
        main()
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    start_dashboard()
