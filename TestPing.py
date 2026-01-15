import http.server
import socketserver
import sys
import socket
import os
import time
import subprocess
import logging
from datetime import datetime
from threading import Thread

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('server.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Define port and public IP
PORT = 20000
PUBLIC_IP = "218.55.238.15"

# Global variables for status tracking
server_status = {
    'running': False,
    'start_time': None,
    'total_requests': 0,
    'total_errors': 0,
    'last_client_ip': None,
    'last_request_time': None
}

class StatusHandler(http.server.SimpleHTTPRequestHandler):
    """HTTP Request Handler with comprehensive error handling and status tracking"""
    
    def do_GET(self):
        """Handle GET requests with comprehensive error handling"""
        try:
            # Update status
            server_status['total_requests'] += 1
            server_status['last_client_ip'] = self.client_address[0]
            server_status['last_request_time'] = datetime.now().isoformat()
            
            # Log request
            logger.info(f"Incoming connection from {self.client_address[0]}:{self.client_address[1]}")
            
            # Validate request path
            if not self.path or self.path == '/':
                self.send_success_response()
            elif self.path == '/status':
                self.send_status_response()
            elif self.path == '/health':
                self.send_health_check_response()
            else:
                self.send_not_found_response()
                
        except BrokenPipeError as e:
            server_status['total_errors'] += 1
            logger.warning(f"Connection broken by client {self.client_address[0]}: {e}")
            
        except ConnectionResetError as e:
            server_status['total_errors'] += 1
            logger.warning(f"Connection reset by client {self.client_address[0]}: {e}")
            
        except UnicodeEncodeError as e:
            server_status['total_errors'] += 1
            logger.error(f"Unicode encoding error: {e}")
            self.send_error_response("Encoding Error", 500)
            
        except Exception as e:
            server_status['total_errors'] += 1
            logger.error(f"Unexpected error handling request from {self.client_address[0]}: {type(e).__name__}: {e}")
            self.send_error_response("Internal Server Error", 500)
    
    def send_success_response(self):
        """Send successful connection test response"""
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            self.end_headers()
            
            uptime = self.calculate_uptime()
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Connection Test Success</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f0f0; }}
        .container {{ background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .success {{ color: #27ae60; font-size: 24px; font-weight: bold; }}
        .info {{ color: #333; font-size: 16px; margin: 10px 0; }}
        .status {{ background-color: #ecf0f1; padding: 15px; border-radius: 4px; margin-top: 20px; }}
        .timestamp {{ color: #7f8c8d; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="success">✓ Congratulations! Your Public Network Connection is Successful!</div>
        <hr>
        <div class="info"><strong>Connection Status:</strong> CONNECTED</div>
        <div class="info"><strong>Client IP Address:</strong> {self.client_address[0]}</div>
        <div class="info"><strong>Client Port:</strong> {self.client_address[1]}</div>
        <div class="info"><strong>Server Port:</strong> {PORT}</div>
        <div class="info"><strong>Connection Time:</strong> {self.date_time_string()}</div>
        <div class="status">
            <strong>Server Status:</strong><br>
            Uptime: {uptime}<br>
            Total Requests: {server_status['total_requests']}<br>
            Total Errors: {server_status['total_errors']}<br>
            Last Update: {datetime.now().isoformat()}
        </div>
        <div class="timestamp">If you can see this page, it means your port forwarding is correctly configured.</div>
    </div>
</body>
</html>
            """
            self.wfile.write(html.encode("utf-8"))
            logger.info(f"✓ Successfully responded to {self.client_address[0]}")
            
        except Exception as e:
            logger.error(f"Error sending success response: {type(e).__name__}: {e}")
            raise
    
    def send_status_response(self):
        """Send current server status"""
        try:
            self.send_response(200)
            self.send_header("Content-type", "application/json; charset=utf-8")
            self.end_headers()
            
            uptime = self.calculate_uptime()
            
            json_response = f"""{{
    "status": "running",
    "port": {PORT},
    "uptime": "{uptime}",
    "total_requests": {server_status['total_requests']},
    "total_errors": {server_status['total_errors']},
    "last_client_ip": "{server_status['last_client_ip']}",
    "last_request_time": "{server_status['last_request_time']}",
    "server_time": "{datetime.now().isoformat()}"
}}"""
            self.wfile.write(json_response.encode("utf-8"))
            logger.info(f"Status request from {self.client_address[0]}")
            
        except Exception as e:
            logger.error(f"Error sending status response: {type(e).__name__}: {e}")
            raise
    
    def send_health_check_response(self):
        """Send health check response"""
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
            logger.debug(f"Health check from {self.client_address[0]}")
            
        except Exception as e:
            logger.error(f"Error sending health check: {type(e).__name__}: {e}")
            raise
    
    def send_not_found_response(self):
        """Send 404 not found response"""
        try:
            self.send_response(404)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>404 - Not Found</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f0f0; }}
        .container {{ background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .error {{ color: #e74c3c; font-size: 24px; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="error">✗ Error 404 - Page Not Found</div>
        <p>The requested path "{self.path}" does not exist.</p>
        <p>Available endpoints:</p>
        <ul>
            <li><strong>/</strong> - Connection test page</li>
            <li><strong>/status</strong> - Server status (JSON)</li>
            <li><strong>/health</strong> - Health check</li>
        </ul>
    </div>
</body>
</html>
            """
            self.wfile.write(html.encode("utf-8"))
            logger.warning(f"404 request from {self.client_address[0]} for path: {self.path}")
            
        except Exception as e:
            logger.error(f"Error sending 404 response: {type(e).__name__}: {e}")
            raise
    
    def send_error_response(self, error_msg, status_code):
        """Send generic error response"""
        try:
            self.send_response(status_code)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Error {status_code}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f0f0f0; }}
        .container {{ background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .error {{ color: #e74c3c; font-size: 24px; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="error">✗ Error {status_code}</div>
        <p>{error_msg}</p>
    </div>
</body>
</html>
            """
            self.wfile.write(html.encode("utf-8"))
            
        except Exception as e:
            logger.error(f"Error sending error response: {type(e).__name__}: {e}")
    
    def log_message(self, format, *args):
        """Override to suppress default logging"""
        pass
    
    @staticmethod
    def calculate_uptime():
        """Calculate server uptime"""
        if not server_status['start_time']:
            return "0s"
        
        elapsed = time.time() - server_status['start_time']
        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"


class MyTCPServer(socketserver.TCPServer):
    """Custom TCP Server with address reuse"""
    allow_reuse_address = True
    daemon_threads = True
    
    def server_bind(self):
        """Override to provide better error handling"""
        try:
            super().server_bind()
            logger.info(f"Server successfully bound to port {PORT}")
        except OSError as e:
            logger.error(f"Failed to bind to port {PORT}: {e}")
            raise


def get_local_ip():
    """Get local network IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        logger.info(f"Local IP detected: {local_ip}")
        return local_ip
    except socket.timeout:
        logger.warning("Timeout connecting to 8.8.8.8 for IP detection")
        return "127.0.0.1"
    except OSError as e:
        logger.warning(f"Failed to detect local IP: {e}")
        return "127.0.0.1"
    except Exception as e:
        logger.error(f"Unexpected error detecting local IP: {type(e).__name__}: {e}")
        return "127.0.0.1"


def check_port_availability(port):
    """Check if port is available"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex(("127.0.0.1", port))
        s.close()
        
        if result == 0:
            logger.warning(f"Port {port} is already in use")
            return False
        return True
    except Exception as e:
        logger.error(f"Error checking port availability: {type(e).__name__}: {e}")
        return False


def print_status_line(message, status="INFO"):
    """Print status line with timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{status:8s}] {message}")


def monitor_status():
    """Background thread to monitor and display status"""
    while server_status['running']:
        try:
            time.sleep(30)  # Display status every 30 seconds
            if server_status['running']:
                uptime = StatusHandler.calculate_uptime()
                print_status_line(f"Status | Requests: {server_status['total_requests']} | Errors: {server_status['total_errors']} | Uptime: {uptime}", "STATUS")
        except Exception as e:
            logger.error(f"Error in status monitor: {type(e).__name__}: {e}")


def main():
    """Main server function with comprehensive error handling"""
    
    print("=" * 70)
    print(" " * 15 + "NETWORK CONNECTION TEST SERVER")
    print("=" * 70)
    print()
    
    print_status_line("Initializing server...", "INIT")
    
    try:
        # Check Python version
        if sys.version_info < (3, 6):
            print_status_line("Python 3.6+ required", "ERROR")
            logger.error("Python 3.6+ required")
            sys.exit(1)
        
        print_status_line(f"Python version: {sys.version.split()[0]}", "INFO")
        
        # Check port availability
        print_status_line(f"Checking port {PORT} availability...", "INFO")
        if not check_port_availability(PORT):
            print_status_line(f"Port {PORT} is already in use!", "ERROR")
            print_status_line("Solutions:", "INFO")
            print_status_line("  1. Close other programs using port {PORT}", "INFO")
            print_status_line(f"  2. Use 'netstat -ano | findstr {PORT}' to find process ID", "INFO")
            print_status_line(f"  3. Modify PORT variable in script (currently {PORT})", "INFO")
            logger.error(f"Port {PORT} already in use")
            sys.exit(1)
        
        print_status_line(f"Port {PORT} is available ✓", "SUCCESS")
        
        # Get local IP
        print_status_line("Detecting local IP address...", "INFO")
        local_ip = get_local_ip()
        print_status_line(f"Local IP: {local_ip}", "INFO")
        
        # Validate socket creation
        print_status_line(f"Creating TCP server socket...", "INFO")
        
        # Create and start server
        with MyTCPServer(("", PORT), StatusHandler) as httpd:
            server_status['running'] = True
            server_status['start_time'] = time.time()
            
            print_status_line(f"Server started successfully! ✓", "SUCCESS")
            print()
            print("=" * 70)
            print(f"Server Configuration:")
            print(f"  Port (Local):       {PORT}")
            print(f"  Local IP:           {local_ip}")
            print(f"  Listen Address:     0.0.0.0:{PORT}")
            print("=" * 70)
            print()
            print("Access Instructions:")
            print(f"  1. Public Network:  http://{PUBLIC_IP}:{PORT}")
            print(f"  2. Local Network:   http://{local_ip}:{PORT}")
            print(f"  3. Status Endpoint: http://{local_ip}:{PORT}/status")
            print(f"  4. Health Check:    http://{local_ip}:{PORT}/health")
            print()
            print("=" * 70)
            print()
            
            # Start status monitoring thread
            monitor_thread = Thread(target=monitor_status, daemon=True)
            monitor_thread.start()
            
            print_status_line("Server listening for connections (Press Ctrl+C to stop)...", "RUNNING")
            print()
            
            # Serve requests
            httpd.serve_forever()
    
    except OSError as e:
        print_status_line(f"OS Error: {e}", "ERROR")
        
        if e.errno == 10048:
            print_status_line(f"Port {PORT} already in use", "ERROR")
            print_status_line("Solutions:", "INFO")
            print_status_line(f"  1. Close application using port {PORT}", "INFO")
            print_status_line(f"  2. Command: netstat -ano | findstr {PORT}", "INFO")
        elif e.errno == 10013:
            print_status_line(f"Permission denied - try running as administrator", "ERROR")
        else:
            print_status_line(f"Error code: {e.errno}", "ERROR")
        
        logger.error(f"OSError: {e} (errno: {e.errno})")
        sys.exit(1)
    
    except PermissionError as e:
        print_status_line(f"Permission Error: Cannot bind to port {PORT}", "ERROR")
        print_status_line("Solutions:", "INFO")
        print_status_line("  1. Run as administrator", "INFO")
        print_status_line(f"  2. Use port > 1024 (current: {PORT})", "INFO")
        logger.error(f"PermissionError: {e}")
        sys.exit(1)
    
    except socket.error as e:
        print_status_line(f"Socket Error: {e}", "ERROR")
        logger.error(f"Socket error: {e}")
        sys.exit(1)
    
    except KeyboardInterrupt:
        server_status['running'] = False
        print()
        print()
        print("=" * 70)
        print_status_line("Shutdown signal received", "INFO")
        print_status_line("Server stopping...", "INFO")
        
        # Display final statistics
        uptime = StatusHandler.calculate_uptime() if server_status['start_time'] else "0s"
        print()
        print("Final Statistics:")
        print(f"  Total Requests:  {server_status['total_requests']}")
        print(f"  Total Errors:    {server_status['total_errors']}")
        print(f"  Uptime:          {uptime}")
        print("=" * 70)
        print_status_line("Server stopped successfully", "SUCCESS")
        logger.info("Server stopped by user")
        sys.exit(0)
    
    except Exception as e:
        server_status['running'] = False
        print_status_line(f"Unexpected Error: {type(e).__name__}: {e}", "ERROR")
        logger.error(f"Unexpected error: {type(e).__name__}: {e}", exc_info=True)
        
        print()
        print("Error Details:")
        import traceback
        traceback.print_exc()
        
        print()
        print("=" * 70)
        logger.error("Server crashed due to unexpected error")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_status_line(f"Fatal Error: {type(e).__name__}: {e}", "FATAL")
        logger.critical(f"Fatal error: {type(e).__name__}: {e}", exc_info=True)
        sys.exit(1)