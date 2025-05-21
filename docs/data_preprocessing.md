# Data Collection & Preprocessing

## Data Sources

### 1. Public Dataset: UNSW-NB15
- Downloaded from the official [UNSW Canberra Cyber](https://www.unsw.adfa.edu.au/unsw-canberra-cyber/cybersecurity/ADFA-NB15-Datasets/) website.
- Contains labeled network traffic with normal and attack types.

### 2. Simulated/Real-Time Data
- Collected using tcpdump and processed with Python scripts.
- Includes both normal and attack traffic generated in a controlled environment.

## Data Collection Methods

### UNSW-NB15
- Downloaded and extracted using `scripts/data_collection/download_unsw_nb15.py`.
- Raw CSV files stored in `data/raw/public/unsw-nb15/`.

### Simulated/Real-Time Data
- Capture traffic using:
  - `scripts/data_collection/capture_realtime_tcpdump.py` (automates tcpdump)
    - Example: `sudo python capture_realtime_tcpdump.py -i eth0 -d 60 -o test_capture.pcap`
  - Output pcap files stored in `data/raw/simulated/`.

## Preprocessing Steps

### UNSW-NB15
- Preprocessing script: `scripts/preprocessing/preprocess_unsw_nb15.py`
- Steps:
  1. Load and merge CSV files
  2. Anonymize IP addresses (SHA-256 hash)
  3. Select relevant features
  4. Clean missing values
  5. Save processed data to `data/processed/unsw-nb15.csv`

### Simulated/Real-Time Data
- Preprocessing script: `scripts/preprocessing/preprocess_simulated_pcap.py`
- Steps:
  1. Iterate over all `.pcap` files in `data/raw/simulated/`
  2. Extract features (timestamp, src/dst IP, ports, protocol, packet length)
  3. Anonymize IP addresses
  4. Save processed data to `data/processed/simulated.csv`

## Labeling
- UNSW-NB15: Uses provided labels (normal, attack types)
- Simulated: Manual labeling based on generated/captured traffic (to be documented as needed) 