import os
import pandas as pd
import numpy as np
import hashlib
from glob import glob

RAW_DIR = "data/raw/public/unsw-nb15/"
OUTPUT_PATH = "data/processed/unsw-nb15.csv"

# Helper to anonymize IP addresses
def anonymize_ip(ip):
    if pd.isna(ip):
        return ip
    return hashlib.sha256(ip.encode()).hexdigest()

def load_and_merge_csvs(raw_dir):
    csv_files = glob(os.path.join(raw_dir, '*.csv'))
    dfs = []
    for f in csv_files:
        print(f"Loading {f}...")
        dfs.append(pd.read_csv(f))
    df = pd.concat(dfs, ignore_index=True)
    return df

def preprocess(df):
    # Select only relevant features for ML and traffic analysis
    features = [
        'dur', 'proto', 'service', 'state', 'spkts', 'dpkts', 'sbytes', 'dbytes', 'rate',
        'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt', 'sjit', 'djit',
        'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean', 'dmean',
        'trans_depth', 'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm',
        'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 'is_ftp_login', 'ct_ftp_cmd',
        'ct_flw_http_mthd', 'ct_src_ltm', 'ct_srv_dst', 'is_sm_ips_ports', 'attack_cat', 'label'
    ]
    # Only keep features that exist in the DataFrame
    features = [f for f in features if f in df.columns]
    df = df[features]
    # Clean missing values
    df = df.dropna()
    return df

def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df = load_and_merge_csvs(RAW_DIR)
    print(f"Loaded {len(df)} rows.")
    df = preprocess(df)
    print(f"Processed {len(df)} rows.")
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved processed data to {OUTPUT_PATH}")

if __name__ == "__main__":
    main() 