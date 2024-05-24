import socket
import threading
import argparse

# Function to scan a single port
def scan_port(target, port):
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        # Attempt to connect to the port
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"Port {port} is open")
        sock.close()
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

# Main function to initiate the scan
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Simple Port Scanner")
    parser.add_argument("target", help="Target IP address or hostname")
    parser.add_argument("ports", help="Comma-separated list of ports or port ranges (e.g., 80,443,1000-2000)")

    args = parser.parse_args()

    target = args.target
    ports = parse_ports(args.ports)

    print(f"Scanning {target} for open ports...")

    threads = []

    # Create a thread for each port scan
    for port in ports:
        thread = threading.Thread(target=scan_port, args=(target, port))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("Scanning complete.")

# Function to parse the ports argument
def parse_ports(ports_str):
    ports = set()
    port_ranges = ports_str.split(',')

    for port_range in port_ranges:
        if '-' in port_range:
            start, end = port_range.split('-')
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(port_range))

    return sorted(ports)

if __name__ == "__main__":
    main()
