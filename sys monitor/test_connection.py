#!/usr/bin/env python3
"""
Test connection to the System Monitor server
"""

import requests
import sys

def test_server_connection(server_url):
    """Test if we can connect to the server"""
    try:
        print(f"Testing connection to: {server_url}")
        
        # Test basic connectivity
        response = requests.get(f"{server_url}/test", timeout=5)
        
        if response.status_code == 200:
            print("✅ Connection successful!")
            print(f"Server response: {response.json()}")
            return True
        else:
            print(f"❌ Server returned status: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server.")
        print("Possible issues:")
        print("1. Server is not running")
        print("2. Firewall is blocking the connection")
        print("3. Wrong IP address")
        print("4. Network connectivity issues")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    server_url = "http://192.168.209.126:5000"
    
    if len(sys.argv) > 1:
        server_url = sys.argv[1]
    
    print("🔍 System Monitor Connection Test")
    print("=" * 40)
    print(f"Testing server: {server_url}")
    print()
    
    if test_server_connection(server_url):
        print("\n🎉 Connection test passed!")
        print("You can now run the client script:")
        print(f"python monitor_client.py --server {server_url}")
    else:
        print("\n❌ Connection test failed!")
        print("Please check:")
        print("1. Server is running on the central PC")
        print("2. Firewall is configured")
        print("3. Both PCs are on the same network")
        print("4. IP address is correct")

if __name__ == "__main__":
    main() 