import os
import argparse
import subprocess
from datetime import datetime

SIMULATED_DIR = "data/raw/simulated/"
os.makedirs(SIMULATED_DIR, exist_ok=True)

def capture_packets(interface, duration, output):
    output_path = os.path.join(SIMULATED_DIR, output)
    cmd = [
        "tcpdump",
        "-i", interface,
        "-w", output_path,
        "-G", str(duration),
        "-W", "1",
        "-nn"
    ]
    print(f"Starting capture on {interface} for {duration} seconds...")
    try:
        subprocess.run(cmd, check=True)
        print(f"Capture complete. Saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during capture: {e}")
        print("Make sure you have tcpdump installed and run as root or with sudo.")

def main():
    parser = argparse.ArgumentParser(description="Capture real-time network traffic using tcpdump.")
    parser.add_argument("-i", "--interface", required=True, help="Network interface to capture on (e.g., eth0, wlan0)")
    parser.add_argument("-d", "--duration", type=int, default=60, help="Capture duration in seconds (default: 60)")
    parser.add_argument("-o", "--output", default=None, help="Output pcap filename (default: capture_<timestamp>.pcap)")
    args = parser.parse_args()

    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"capture_{timestamp}.pcap"

    capture_packets(args.interface, args.duration, args.output)

if __name__ == "__main__":
    main() 