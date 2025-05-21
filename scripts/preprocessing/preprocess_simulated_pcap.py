import os
import pandas as pd
import pyshark
import hashlib
from glob import glob

RAW_DIR = "data/raw/simulated/"
OUTPUT_PATH = "data/processed/simulated.csv"

# Helper to anonymize IP addresses
def anonymize_ip(ip):
    if pd.isna(ip) or ip is None:
        return ip
    return hashlib.sha256(ip.encode()).hexdigest()

def extract_features_from_pcap(pcap_path):
    print(f"Processing {pcap_path}...")
    cap = pyshark.FileCapture(pcap_path, only_summaries=False)
    rows = []
    for pkt in cap:
        try:
            # Only process packets with an IP layer
            if not hasattr(pkt, 'ip'):
                continue
            # Only process packets with a transport layer (TCP/UDP)
            if not hasattr(pkt, 'transport_layer') or pkt.transport_layer is None:
                continue
            proto = pkt.transport_layer
            # Check if the protocol layer exists in the packet
            if not hasattr(pkt, proto):
                continue
            srcip = anonymize_ip(getattr(pkt.ip, 'src', None))
            dstip = anonymize_ip(getattr(pkt.ip, 'dst', None))
            sport = getattr(pkt[proto], 'srcport', None)
            dsport = getattr(pkt[proto], 'dstport', None)
            row = {
                'timestamp': float(pkt.sniff_timestamp),
                'srcip': srcip,
                'dstip': dstip,
                'sport': sport,
                'dsport': dsport,
                'proto': proto,
                'length': int(pkt.length) if hasattr(pkt, 'length') else None
            }
            rows.append(row)
        except Exception as e:
            print(f"Error processing packet: {e}")
    cap.close()
    return rows

def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    all_rows = []
    pcap_files = glob(os.path.join(RAW_DIR, '*.pcap'))
    for pcap in pcap_files:
        rows = extract_features_from_pcap(pcap)
        all_rows.extend(rows)
    df = pd.DataFrame(all_rows)
    df = df.dropna()
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved processed simulated data to {OUTPUT_PATH}")

if __name__ == "__main__":
    main() 