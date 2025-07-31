#!/usr/bin/env python3
"""
Test script for System Monitor
This script tests the basic functionality of the monitoring system.
"""

import requests
import json
import time
import sys
import os

def test_server_connection(server_url="http://localhost:5000"):
    """Test if the server is running and accessible"""
    try:
        response = requests.get(f"{server_url}/api/clients", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and accessible")
            return True
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the server is running.")
        return False
    except Exception as e:
        print(f"❌ Error connecting to server: {e}")
        return False

def test_metrics_endpoint(server_url="http://localhost:5000"):
    """Test the metrics endpoint"""
    try:
        # Create sample metrics
        sample_metrics = {
            "pc_name": "TEST_PC",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "cpu_percent": 25.5,
            "memory_percent": 60.2,
            "memory_used_gb": 8.5,
            "memory_total_gb": 16.0,
            "disk_percent": 45.8,
            "disk_used_gb": 500.0,
            "disk_total_gb": 1000.0,
            "network_sent_mb": 150.0,
            "network_recv_mb": 200.0,
            "uptime_seconds": 3600,
            "os_info": "Windows 10"
        }
        
        # Send test metrics
        response = requests.post(
            f"{server_url}/api/metrics",
            json=sample_metrics,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            print("✅ Metrics endpoint is working")
            return True
        else:
            print(f"❌ Metrics endpoint returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing metrics endpoint: {e}")
        return False

def test_dashboard_access(server_url="http://localhost:5000"):
    """Test if the dashboard is accessible"""
    try:
        response = requests.get(f"{server_url}/", timeout=5)
        if response.status_code == 200:
            print("✅ Dashboard is accessible")
            return True
        else:
            print(f"❌ Dashboard returned status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing dashboard: {e}")
        return False

def main():
    print("🔍 System Monitor Test Suite")
    print("=" * 40)
    
    # Get server URL from command line or use default
    server_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    
    print(f"Testing server at: {server_url}")
    print()
    
    # Run tests
    tests = [
        ("Server Connection", lambda: test_server_connection(server_url)),
        ("Metrics Endpoint", lambda: test_metrics_endpoint(server_url)),
        ("Dashboard Access", lambda: test_dashboard_access(server_url))
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing: {test_name}")
        if test_func():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is working correctly.")
        print("\nNext steps:")
        print("1. Open your browser and go to:", server_url)
        print("2. Run the client script on other PCs:")
        print("   python client/monitor_client.py --server", server_url)
    else:
        print("❌ Some tests failed. Please check the server setup.")
        print("\nTroubleshooting:")
        print("1. Make sure the server is running: python server/app.py")
        print("2. Check if port 5000 is available")
        print("3. Verify all dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main() 