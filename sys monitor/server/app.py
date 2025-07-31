from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
from datetime import datetime, timedelta
import threading
import time
from collections import defaultdict, deque
import traceback

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['DEBUG'] = True  # Enable debug mode
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory storage for metrics (in production, use a database)
metrics_store = defaultdict(lambda: deque(maxlen=1000))  # Keep last 1000 data points per PC
active_clients = set()
last_seen = {}

@app.route('/test')
def test():
    """Simple test route"""
    return jsonify({'status': 'Server is working!', 'timestamp': datetime.now().isoformat()})

@app.route('/simple')
def simple():
    """Simple HTML test"""
    return render_template('simple.html')

@app.route('/test-dashboard')
def test_dashboard():
    """Test dashboard for debugging"""
    return render_template('test_dashboard.html')

@app.route('/')
def dashboard():
    try:
        return render_template('dashboard.html')
    except Exception as e:
        print(f"Error rendering dashboard: {e}")
        print(traceback.format_exc())
        return f"Error: {str(e)}", 500

@app.route('/api/metrics', methods=['POST'])
def receive_metrics():
    """Receive metrics from client PCs"""
    try:
        data = request.get_json()
        
        if not data or 'pc_name' not in data:
            return jsonify({'error': 'Invalid data format'}), 400
        
        pc_name = data['pc_name']
        timestamp = datetime.fromisoformat(data['timestamp'])
        
        # Store metrics
        metrics_store[pc_name].append({
            'timestamp': timestamp,
            'data': data
        })
        
        # Update active clients
        active_clients.add(pc_name)
        last_seen[pc_name] = datetime.now()
        
        # Emit to connected dashboard clients
        socketio.emit('new_metrics', {
            'pc_name': pc_name,
            'metrics': data
        })
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        print(f"Error receiving metrics: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/api/clients')
def get_clients():
    """Get list of active clients"""
    try:
        # Remove clients that haven't sent data in the last 30 seconds
        current_time = datetime.now()
        inactive_clients = [
            pc for pc, last_time in last_seen.items()
            if (current_time - last_time) > timedelta(seconds=30)
        ]
        
        for pc in inactive_clients:
            active_clients.discard(pc)
            if pc in last_seen:
                del last_seen[pc]
        
        result = {
            'active_clients': list(active_clients),
            'last_seen': {pc: time.isoformat() for pc, time in last_seen.items()}
        }
        
        print(f"API /api/clients called - returning: {result}")
        return jsonify(result)
        
    except Exception as e:
        print(f"Error getting clients: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e), 'active_clients': [], 'last_seen': {}}), 500

@app.route('/api/metrics/<pc_name>')
def get_metrics(pc_name):
    """Get metrics for a specific PC"""
    try:
        if pc_name not in metrics_store:
            print(f"PC {pc_name} not found in metrics_store")
            return jsonify({'error': 'PC not found', 'pc_name': pc_name, 'metrics': []}), 404
        
        # Convert deque to list for JSON serialization
        metrics_list = list(metrics_store[pc_name])
        
        # Convert datetime objects to ISO strings (only if they're datetime objects)
        for metric in metrics_list:
            if hasattr(metric['timestamp'], 'isoformat'):
                # It's a datetime object
                metric['timestamp'] = metric['timestamp'].isoformat()
            # If it's already a string, leave it as is
        
        result = {
            'pc_name': pc_name,
            'metrics': metrics_list
        }
        
        print(f"API /api/metrics/{pc_name} called - returning {len(metrics_list)} metrics")
        return jsonify(result)
        
    except Exception as e:
        print(f"Error getting metrics for {pc_name}: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e), 'pc_name': pc_name, 'metrics': []}), 500

@app.route('/api/metrics')
def get_all_metrics():
    """Get metrics for all PCs"""
    try:
        all_metrics = {}
        
        for pc_name, metrics_deque in metrics_store.items():
            metrics_list = list(metrics_deque)
            for metric in metrics_list:
                if hasattr(metric['timestamp'], 'isoformat'):
                    # It's a datetime object
                    metric['timestamp'] = metric['timestamp'].isoformat()
                # If it's already a string, leave it as is
            all_metrics[pc_name] = metrics_list
        
        return jsonify(all_metrics)
    except Exception as e:
        print(f"Error getting all metrics: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.errorhandler(500)
def internal_error(error):
    print(f"Internal Server Error: {error}")
    print(traceback.format_exc())
    return jsonify({'error': 'Internal Server Error', 'details': str(error)}), 500

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404

def cleanup_inactive_clients():
    """Periodically cleanup inactive clients"""
    while True:
        try:
            current_time = datetime.now()
            inactive_clients = [
                pc for pc, last_time in last_seen.items()
                if (current_time - last_time) > timedelta(minutes=5)
            ]
            
            for pc in inactive_clients:
                active_clients.discard(pc)
                if pc in last_seen:
                    del last_seen[pc]
                if pc in metrics_store:
                    del metrics_store[pc]
            
            time.sleep(60)  # Check every minute
        except Exception as e:
            print(f"Error in cleanup: {e}")
            time.sleep(60)

if __name__ == '__main__':
    # Start cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_inactive_clients, daemon=True)
    cleanup_thread.start()
    
    print("🚀 System Monitor Server Starting...")
    print("📊 Dashboard available at: http://localhost:5000")
    print("🌐 API endpoints:")
    print("   - POST /api/metrics (receive client data)")
    print("   - GET  /api/clients (list active clients)")
    print("   - GET  /api/metrics/<pc_name> (get PC metrics)")
    print("   - GET  /api/metrics (get all metrics)")
    print("\n⏳ Waiting for client connections...\n")
    
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"Error starting server: {e}")
        print(traceback.format_exc()) 