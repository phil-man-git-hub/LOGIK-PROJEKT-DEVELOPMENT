#!/usr/bin/env python3
import socket
import json
import argparse
import signal
import sys

def main():
    parser = argparse.ArgumentParser(description="Listen to LOGIK-PROJEKT live diagnostic stream.")
    parser.add_argument("--port", type=int, default=54322, help="UDP port to listen on (default: 54322)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON (for machine parsing)")
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.bind(('127.0.0.1', args.port))
    except OSError as e:
        print(f"Error: Could not bind to port {args.port}. Is another listener running?")
        sys.exit(1)

    print(f"📡 LOGIK-PROJEKT Debug Listener active on port {args.port}...")
    print("Press Ctrl+C to stop.")

    def signal_handler(sig, frame):
        print("\nExiting listener...")
        sock.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            data, addr = sock.recvfrom(4096) # Buffer size
            line = data.decode('utf-8')
            
            try:
                record = json.loads(line)
                if args.json:
                    print(line)
                else:
                    # Pretty print for humans
                    timestamp = record.get("timestamp", "").split("T")[-1][:12] # Clean time
                    level = record.get("level", "INFO")
                    msg = record.get("message", "")
                    module = record.get("module", "")
                    
                    # Color coding (if terminal supports it)
                    color = "\033[0m"
                    if level == "ERROR": color = "\033[91m" # Red
                    elif level == "WARNING": color = "\033[93m" # Yellow
                    elif level == "DEBUG": color = "\033[90m" # Grey
                    
                    print(f"{color}[{timestamp}] [{level:<7}] {module}: {msg}\033[0m")
                    
            except json.JSONDecodeError:
                print(f"Raw Data: {line}")
                
        except Exception as e:
            print(f"Error receiving data: {e}")

if __name__ == "__main__":
    main()
