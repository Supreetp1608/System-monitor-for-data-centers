import psutil
import requests
import json
import time
import socket
import platform
from datetime import datetime
import sys

class SystemMonitor:
    def __init__(self, server_url="http://localhost:5000"):
        self.server_url = server_url
        self.pc_name = socket.gethostname()
        self.api_endpoint = f"{server_url}/api/metrics"
        
    def get_system_metrics(self):
        """Collect current system metrics"""
        try:
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
                "pc_name": self.pc_name,
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
    
    def send_metrics(self, metrics):
        """Send metrics to the server"""
        try:
            response = requests.post(
                self.api_endpoint,
                json=metrics,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✓ Metrics sent successfully - CPU: {metrics['cpu_percent']}%, RAM: {metrics['memory_percent']}%")
            else:
                print(f"✗ Failed to send metrics. Status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("✗ Cannot connect to server. Make sure the server is running.")
        except requests.exceptions.Timeout:
            print("✗ Request timeout. Server might be overloaded.")
        except Exception as e:
            print(f"✗ Error sending metrics: {e}")
    
    def run(self, interval=5):
        """Run the monitoring loop"""
        print(f"🚀 System Monitor Started")
        print(f"📊 PC Name: {self.pc_name}")
        print(f"🌐 Server URL: {self.server_url}")
        print(f"⏱️  Update Interval: {interval} seconds")
        print(f"📈 Press Ctrl+C to stop monitoring\n")
        
        try:
            while True:
                metrics = self.get_system_metrics()
                if metrics:
                    self.send_metrics(metrics)
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='System Monitor Client')
    parser.add_argument('--server', default='http://localhost:5000', 
                       help='Server URL (default: http://localhost:5000)')
    parser.add_argument('--interval', type=int, default=5,
                       help='Update interval in seconds (default: 5)')
    
    args = parser.parse_args()
    
    monitor = SystemMonitor(args.server)
    monitor.run(args.interval)

if __name__ == "__main__":
    main() 