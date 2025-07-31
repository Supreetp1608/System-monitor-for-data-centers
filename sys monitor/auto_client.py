#!/usr/bin/env python3
"""
Auto System Monitor Client
This single file handles everything automatically:
1. Installs required packages
2. Tests connection to server
3. Starts monitoring
"""

import subprocess
import sys
import os
import time
import socket
import platform
from datetime import datetime

# Server configuration
SERVER_IP = "192.168.209.126"  # Your server IP
SERVER_PORT = "5000"
SERVER_URL = f"http://{SERVER_IP}:{SERVER_PORT}"

def install_package(package):
    """Install a Python package"""
    try:
        print(f"📦 Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"✅ {package} installed successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to install {package}")
        return False

def test_connection():
    """Test connection to server"""
    try:
        print(f"🔍 Testing connection to {SERVER_URL}...")
        
        # Try to import requests (install if needed)
        try:
            import requests
        except ImportError:
            if not install_package("requests"):
                return False
        
        # Test connection
        response = requests.get(f"{SERVER_URL}/test", timeout=5)
        
        if response.status_code == 200:
            print("✅ Connection successful!")
            return True
        else:
            print(f"❌ Server returned status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure the server is running on the central PC")
        print("2. Check if both PCs are on the same network")
        print("3. Verify the server IP address is correct")
        print(f"4. Try accessing {SERVER_URL} in a web browser")
        return False

def get_system_metrics():
    """Collect system metrics"""
    try:
        import psutil
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used_gb = memory.used / (1024**3)
        memory_total_gb = memory.total / (1024**3)
        
        # Disk usage
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used_gb = disk.used / (1024**3)
        disk_total_gb = disk.total / (1024**3)
        
        # Network I/O
        network = psutil.net_io_counters()
        network_sent_mb = network.bytes_sent / (1024**2)
        network_recv_mb = network.bytes_recv / (1024**2)
        
        # System info
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        
        metrics = {
            "pc_name": socket.gethostname(),
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": round(cpu_percent, 2),
            "memory_percent": round(memory_percent, 2),
            "memory_used_gb": round(memory_used_gb, 2),
            "memory_total_gb": round(memory_total_gb, 2),
            "disk_percent": round(disk_percent, 2),
            "disk_used_gb": round(disk_used_gb, 2),
            "disk_total_gb": round(disk_total_gb, 2),
            "network_sent_mb": round(network_sent_mb, 2),
            "network_recv_mb": round(network_recv_mb, 2),
            "uptime_seconds": int(uptime_seconds),
            "os_info": platform.system() + " " + platform.release()
        }
        
        return metrics
        
    except Exception as e:
        print(f"Error collecting metrics: {e}")
        return None

def send_metrics(metrics):
    """Send metrics to server"""
    try:
        import requests
        
        response = requests.post(
            f"{SERVER_URL}/api/metrics",
            json=metrics,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✓ Sent: CPU {metrics['cpu_percent']}%, RAM {metrics['memory_percent']}%")
        else:
            print(f"✗ Failed to send. Status: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error sending metrics: {e}")

def run_monitoring():
    """Run the monitoring loop"""
    print(f"\n🚀 Starting System Monitor Client")
    print(f"📊 PC Name: {socket.gethostname()}")
    print(f"🌐 Server: {SERVER_URL}")
    print(f"⏱️  Update Interval: 5 seconds")
    print(f"📈 Press Ctrl+C to stop monitoring\n")
    
    try:
        while True:
            metrics = get_system_metrics()
            if metrics:
                send_metrics(metrics)
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

def main():
    """Main function - handles everything automatically"""
    print("=" * 50)
    print("🤖 Auto System Monitor Client")
    print("=" * 50)
    print(f"Server: {SERVER_URL}")
    print(f"PC Name: {socket.gethostname()}")
    print()
    
    # Step 1: Install required packages
    print("📦 Step 1: Installing required packages...")
    packages_to_install = ["psutil", "requests"]
    
    for package in packages_to_install:
        try:
            __import__(package)
            print(f"✅ {package} already installed")
        except ImportError:
            if not install_package(package):
                print(f"❌ Failed to install {package}. Please install manually:")
                print(f"   pip install {package}")
                input("Press Enter to exit...")
                return
    
    print("\n✅ All packages installed successfully!")
    
    # Step 2: Test connection
    print("\n🔍 Step 2: Testing connection to server...")
    if not test_connection():
        print("\n❌ Cannot connect to server.")
        print("Please check:")
        print("1. Server is running on the central PC")
        print("2. Both PCs are on the same network")
        print("3. Firewall is configured")
        print(f"4. Try accessing {SERVER_URL} in a web browser")
        input("\nPress Enter to exit...")
        return
    
    # Step 3: Start monitoring
    print("\n🎯 Step 3: Starting monitoring...")
    print("✅ Everything is ready! Starting to monitor...")
    print()
    
    run_monitoring()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        input("Press Enter to exit...") 