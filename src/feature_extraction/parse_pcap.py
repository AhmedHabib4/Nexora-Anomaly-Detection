import argparse
import pandas as pd
from scapy.all import rdpcap, IP, TCP, UDP
from tqdm import tqdm

def extract_features(pcap_file):
    print(f"Parsing {pcap_file}...")
    packets = rdpcap(pcap_file)
    
    flows = {}
    for pkt in tqdm(packets, desc="Extracting features"):
        if IP in pkt and (TCP in pkt or UDP in pkt):
            src = pkt[IP].src
            dst = pkt[IP].dst
            proto = pkt[IP].proto
            length = len(pkt)
            time = float(pkt.time)
            
            flow_id = (src, dst, proto)
            
            if flow_id not in flows:
                flows[flow_id] = {'packet_count': 0, 'total_bytes': 0, 'start_time': time, 'last_time': time, 'iat_total': 0}
            
            flow = flows[flow_id]
            flow['packet_count'] += 1
            flow['total_bytes'] += length
            
            if flow['packet_count'] > 1:
                iat = time - flow['last_time']
                flow['iat_total'] += iat
                
            flow['last_time'] = time

    data = []
    for flow_id, metrics in flows.items():
        avg_iat = metrics['iat_total'] / (metrics['packet_count'] - 1) if metrics['packet_count'] > 1 else 0
        avg_pkt_len = metrics['total_bytes'] / metrics['packet_count']
        duration = metrics['last_time'] - metrics['start_time']
        data.append([
            flow_id[0], flow_id[1], flow_id[2], 
            metrics['packet_count'], metrics['total_bytes'], 
            avg_iat, avg_pkt_len, duration
        ])
        
    df = pd.DataFrame(data, columns=[
        'src_ip', 'dst_ip', 'protocol', 
        'packet_count', 'total_bytes', 
        'mean_iat', 'mean_pkt_len', 'flow_duration'
    ])
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract ML features from Nexora PCAPs.")
    parser.add_argument("--input", required=True, help="Input .pcap file")
    parser.add_argument("--output", required=True, help="Output .csv dataset file")
    args = parser.parse_args()
    
    df = extract_features(args.input)
    df.to_csv(args.output, index=False)
    print(f"Feature extraction complete. Saved to {args.output}")