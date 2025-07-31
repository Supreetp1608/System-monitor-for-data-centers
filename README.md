# 🖥️ System Monitor Pro - Real-Time Multi-PC Monitoring Dashboard

A powerful, enterprise-grade system monitoring solution that collects real-time metrics from multiple Windows PCs and displays them in a beautiful, interactive web dashboard. Perfect for IT administrators, system managers, and anyone who needs to monitor multiple computers simultaneously.

## 🌟 Features

### 📊 **Real-Time Monitoring**
- **CPU Usage** - Live CPU percentage with historical trends
- **Memory (RAM) Usage** - Current and historical memory consumption
- **Disk Usage** - Storage utilization with available space tracking
- **Network I/O** - Bytes sent/received monitoring
- **System Information** - OS version, uptime, and hostname

### 🎯 **Multi-PC Support**
- **Unlimited Clients** - Monitor as many PCs as you need
- **Auto-Discovery** - New PCs appear automatically when connected
- **Individual Tracking** - Each PC has its own metrics and charts
- **Status Indicators** - Visual online/offline status for each PC

### 📈 **Beautiful Dashboard**
- **Interactive Charts** - Real-time line graphs with Chart.js
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Auto-Refresh** - Updates every 10 seconds automatically
- **Professional UI** - Modern glass-morphism design with gradients

### ⚡ **Zero-Configuration Setup**
- **One-Click Client** - Single file handles everything automatically
- **Auto-Installation** - Required packages installed automatically
- **Connection Testing** - Verifies connectivity before starting
- **Error Handling** - Clear feedback and troubleshooting guidance

## 🏗️ Architecture

```
┌─────────────────┐    HTTP/WebSocket    ┌─────────────────┐
│   Client PCs    │ ────────────────────► │  Central Server │
│  (auto_client)  │                      │   (Flask App)   │
└─────────────────┘                      └─────────────────┘
                                                │
                                                ▼
                                       ┌─────────────────┐
                                       │   Dashboard     │
                                       │  (React/HTML)   │
                                       └─────────────────┘
```

## 🚀 Quick Start

### **For System Administrators**

#### **Step 1: Server Setup (Central PC)**

1. **Clone or download** this repository to your central monitoring PC
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure firewall** (run as Administrator):
   ```bash
   setup_firewall.bat
   ```
4. **Start the server:**
   ```bash
   python server/app.py
   ```
5. **Access dashboard:** Open browser and go to `http://localhost:5000`

#### **Step 2: Client Deployment (Monitored PCs)**

**Option A: One-Click Deployment (Recommended)**
1. **Copy these 2 files** to each PC you want to monitor:
   - `auto_client.py`
   - `start_monitoring.bat`
2. **Double-click** `start_monitoring.bat` on each PC
3. **Done!** PCs automatically appear on dashboard

**Option B: Command Line Deployment**
1. **Copy** `auto_client.py` to each PC
2. **Open Command Prompt** on each PC
3. **Run:** `python auto_client.py`
4. **Done!** PCs automatically appear on dashboard

## 📋 Detailed Setup Instructions

### **Prerequisites**

#### **Server PC Requirements:**
- ✅ **Windows 10/11** (tested on Windows 10)
- ✅ **Python 3.7+** installed
- ✅ **Administrator access** (for firewall configuration)
- ✅ **Network connectivity** (to accept client connections)

#### **Client PC Requirements:**
- ✅ **Windows 10/11** (tested on Windows 10)
- ✅ **Python 3.7+** installed
- ✅ **Network connectivity** (to reach server)
- ✅ **Internet access** (for package installation)

### **Server Installation**

#### **1. Download and Extract**
```bash
# Download the repository
git clone https://github.com/yourusername/system-monitor-pro.git
cd system-monitor-pro
```

#### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

#### **3. Configure Firewall**
**Important:** Run as Administrator
```bash
# Right-click setup_firewall.bat and "Run as administrator"
setup_firewall.bat
```

#### **4. Start Server**
```bash
cd server
python app.py
```

#### **5. Verify Installation**
- Open browser and go to: `http://localhost:5000`
- You should see the dashboard interface
- Test API endpoint: `http://localhost:5000/test`

### **Client Deployment**

#### **Method 1: Automated Deployment (Recommended)**

1. **Copy deployment files** to each client PC:
   ```
   auto_client.py
   start_monitoring.bat
   ```

2. **Run on each PC:**
   - **Double-click** `start_monitoring.bat`
   - **Wait** for automatic setup to complete
   - **Verify** success messages appear

3. **Expected output:**
   ```
   ==================================================
   🤖 Auto System Monitor Client
   ==================================================
   Server: http://192.168.209.126:5000
   PC Name: CLIENT-PC-NAME

   📦 Step 1: Installing required packages...
   ✅ psutil already installed
   ✅ requests already installed

   ✅ All packages installed successfully!

   🔍 Step 2: Testing connection to server...
   ✅ Connection successful!

   🎯 Step 3: Starting monitoring...
   ✅ Everything is ready! Starting to monitor...

   ✓ Sent: CPU 25.5%, RAM 60.2%
   ✓ Sent: CPU 28.1%, RAM 61.5%
   ```

#### **Method 2: Manual Deployment**

1. **Copy** `auto_client.py` to each client PC
2. **Open Command Prompt** on each PC
3. **Navigate** to the file location
4. **Run:** `python auto_client.py`
5. **Follow** the on-screen instructions

### **Network Configuration**

#### **Finding Your Server IP**
```bash
# On server PC, run:
ipconfig

# Look for your main network adapter (usually Wi-Fi or Ethernet)
# Note the IPv4 Address (e.g., 192.168.1.100)
```

#### **Updating Client Configuration**
If your server IP changes, update the client configuration:

1. **Edit** `auto_client.py` on each client PC
2. **Change** the `SERVER_IP` variable:
   ```python
   SERVER_IP = "192.168.1.100"  # Your actual server IP
   ```

#### **Network Troubleshooting**
- **Same Network:** All PCs must be on the same network
- **Firewall:** Ensure Windows Firewall allows the connection
- **Test Connection:** Try accessing `http://SERVER_IP:5000` from client PC browser

## 📊 Dashboard Features

### **Real-Time Metrics Display**
- **Current Values:** Live CPU, RAM, and Disk usage
- **Historical Charts:** Interactive line graphs showing trends
- **Status Indicators:** Green (online) / Red (offline) dots
- **Auto-Refresh:** Updates every 10 seconds

### **Multi-PC Management**
- **Individual Cards:** Each PC has its own monitoring card
- **Hostname Display:** Shows actual PC names
- **Connection Status:** Real-time online/offline detection
- **Data Retention:** Keeps last 1000 data points per PC

### **Mobile Access**
- **Responsive Design:** Works on phones and tablets
- **Touch-Friendly:** Optimized for mobile interaction
- **Same Features:** Full functionality on mobile devices

## 🔧 Troubleshooting Guide

### **Common Issues and Solutions**

#### **Server Issues**

**Problem:** "Port 5000 is already in use"
```
Solution: Change port in server/app.py
socketio.run(app, host='0.0.0.0', port=8080, debug=True)
```

**Problem:** "Firewall blocking connections"
```
Solution: Run setup_firewall.bat as Administrator
```

**Problem:** "Cannot access dashboard"
```
Solution: Check if server is running and try http://localhost:5000
```

#### **Client Issues**

**Problem:** "Cannot connect to server"
```
Solutions:
1. Verify server is running
2. Check network connectivity
3. Test with browser: http://SERVER_IP:5000
4. Verify firewall settings
```

**Problem:** "Failed to install packages"
```
Solutions:
1. Check internet connection
2. Run manually: pip install psutil requests
3. Try with administrator privileges
```

**Problem:** "Python not found"
```
Solutions:
1. Install Python from python.org
2. Add Python to PATH during installation
3. Verify with: python --version
```

### **Network Diagnostics**

#### **Test Server Connectivity**
```bash
# On client PC, test if server is reachable
ping 192.168.209.126

# Test web access
curl http://192.168.209.126:5000/test
```

#### **Check Firewall Settings**
```bash
# On server PC, verify firewall rule
netsh advfirewall firewall show rule name="System Monitor Server"
```

## 📈 Performance and Scalability

### **Resource Usage**
- **Server:** ~50MB RAM, minimal CPU usage
- **Client:** ~20MB RAM, <1% CPU overhead
- **Network:** ~1KB per update (every 5 seconds)
- **Storage:** In-memory only (no database required)

### **Scalability**
- **Tested:** Up to 50 concurrent clients
- **Recommended:** Up to 100 clients for optimal performance
- **Limitation:** In-memory storage (consider database for larger deployments)

### **Data Retention**
- **Default:** Last 1000 data points per PC
- **Configurable:** Modify `maxlen=1000` in server/app.py
- **Cleanup:** Inactive clients removed after 5 minutes

## 🔒 Security Considerations

### **Current Security Model**
- **Local Network Only:** Designed for internal network use
- **No Authentication:** Simple deployment model
- **No Encryption:** HTTP communication (not HTTPS)

### **Production Recommendations**
- **Add Authentication:** Implement user login system
- **Use HTTPS:** Configure SSL certificates
- **Database Storage:** Replace in-memory storage with database
- **Network Isolation:** Use dedicated monitoring network

## 🛠️ Customization and Extension

### **Adding New Metrics**
1. **Modify client collection** in `auto_client.py`:
   ```python
   # Add new metric
   new_metric = psutil.some_function()
   metrics["new_metric"] = new_metric
   ```

2. **Update dashboard display** in `server/templates/dashboard.html`:
   ```html
   <div class="metric-card">
       <div class="metric-value">{latestMetrics.new_metric}</div>
       <div class="metric-label">New Metric</div>
   </div>
   ```

### **Changing Update Intervals**
- **Client Side:** Modify `time.sleep(5)` in `auto_client.py`
- **Server Side:** Modify refresh interval in dashboard JavaScript

### **Database Integration**
Replace in-memory storage with database:
```python
# Example with SQLite
import sqlite3
# Store metrics in database instead of memory
```

## 📞 Support and Maintenance

### **Log Files**
- **Server Logs:** Displayed in console when running server
- **Client Logs:** Displayed in console when running client
- **Error Tracking:** All errors logged with timestamps

### **Monitoring the Monitor**
- **Server Health:** Check server console for errors
- **Client Status:** Dashboard shows online/offline status
- **Network Issues:** Connection errors logged automatically

### **Backup and Recovery**
- **Configuration:** Backup `auto_client.py` and server files
- **Data:** Currently in-memory (implement database for persistence)
- **Deployment:** Keep copies of deployment files

## 🎯 Best Practices

### **Deployment Best Practices**
1. **Test First:** Always test on a single PC before mass deployment
2. **Document IPs:** Keep a list of server IP addresses
3. **Version Control:** Use consistent versions across all clients
4. **Backup Configs:** Save configuration files

### **Network Best Practices**
1. **Dedicated Network:** Use separate VLAN for monitoring if possible
2. **Firewall Rules:** Configure specific rules for monitoring traffic
3. **Bandwidth Monitoring:** Monitor network usage impact
4. **Redundancy:** Consider backup server for critical deployments

### **Security Best Practices**
1. **Network Isolation:** Use dedicated monitoring network
2. **Access Control:** Implement authentication for production use
3. **Encryption:** Use HTTPS for sensitive environments
4. **Audit Logs:** Implement comprehensive logging

## 📄 License

This project is open source and available under the MIT License. Feel free to modify and distribute according to the license terms.

## 🤝 Contributing

We welcome contributions! Please feel free to submit issues, feature requests, or pull requests to improve this monitoring solution.

---

**System Monitor Pro** - Making multi-PC monitoring simple, powerful, and beautiful! 🚀

*Built with ❤️ for system administrators who need reliable, real-time monitoring without the complexity.* 
