import os
import numpy as np
import pandas as pd

np.random.seed(42)

BASE_DIR = os.path.join("generated_datasets", "tor_like_baseline")

# Exact composition from Table 5 & Section 13.4:
# Total flows = 10,121 (7,200 hidden_service, 2,921 non-hidden-service)
# browsing_heavy has 15% hidden-service flows (~354 HS, 2,006 non-HS)
SCENARIOS = {
    "browsing_heavy": {"total_flows": 2360, "hs_flows": 354, "minutes": 60},
    "hidden_service_heavy": {"total_flows": 4605, "hs_flows": 4145, "minutes": 60},
    "mixed": {"total_flows": 3156, "hs_flows": 2701, "minutes": 60},
}

ROLES = ["client", "guard", "middle", "exit", "directory", "hidden_service", "web_server"]


def generate_scenario(name: str, cfg: dict):
    scenario_dir = os.path.join(BASE_DIR, name)
    os.makedirs(scenario_dir, exist_ok=True)

    n_total = cfg["total_flows"]
    n_hs = cfg["hs_flows"]
    n_non_hs = n_total - n_hs
    n_minutes = cfg["minutes"]

    labels = np.array(["hidden_service"] * n_hs + ["browsing"] * n_non_hs)
    np.random.shuffle(labels)

    rows = []
    for i, label in enumerate(labels):
        minute_idx = i % n_minutes
        is_hs = label == "hidden_service"

        if is_hs:
            # Hidden-service flows route via introduction/rendezvous circuits (non-exit termination)
            init_role = np.random.choice(["client", "guard", "middle"], p=[0.4, 0.3, 0.3])
            resp_role = np.random.choice(["middle", "hidden_service", "directory"], p=[0.45, 0.45, 0.10])
            dst_port = np.random.choice([9001, 9030, 8080, 443], p=[0.45, 0.25, 0.20, 0.10])
            packet_count = int(np.random.randint(18, 220))
            bytes_per_pkt = float(np.random.uniform(480, 620))
            duration_ms = float(np.random.uniform(120, 4500))
            phase = np.random.choice(["hs_intro", "hs_rendezvous", "hs_data"])
        else:
            # Ordinary browsing/maintenance flows typically traverse exit -> web_server
            init_role = np.random.choice(["client", "guard", "exit"], p=[0.35, 0.25, 0.40])
            resp_role = np.random.choice(["exit", "web_server", "directory"], p=[0.45, 0.45, 0.10])
            dst_port = np.random.choice([443, 80, 9001, 53], p=[0.50, 0.30, 0.10, 0.10])
            packet_count = int(np.random.randint(8, 180))
            bytes_per_pkt = float(np.random.uniform(420, 950))
            duration_ms = float(np.random.uniform(50, 3800))
            phase = np.random.choice(["circuit_build", "web_fetch", "dir_sync"])

        byte_count = int(packet_count * bytes_per_pkt)
        src_port = int(np.random.randint(1024, 65535))

        rows.append({
            "minute": minute_idx,
            # Leaky fields stored in dataset schema (to be excluded in train.py)
            "phase": phase,
            "circuit_id": f"circ_{minute_idx}_{np.random.randint(1, 25)}",
            "client_id": f"client_{np.random.randint(1, 15)}",
            "service_id": f"onion_{np.random.randint(1, 6)}" if is_hs else "none",
            "src_ip": f"10.0.{np.random.randint(1, 5)}.{np.random.randint(2, 254)}",
            "dst_ip": f"10.0.{np.random.randint(6, 10)}.{np.random.randint(2, 254)}",
            # Non-leaky observer features
            "packet_count": packet_count,
            "byte_count": byte_count,
            "duration_ms": round(duration_ms, 2),
            "bytes_per_packet": round(byte_count / packet_count, 2),
            "duration_per_packet": round(duration_ms / packet_count, 2),
            "src_port": src_port,
            "dst_port": dst_port,
            "initiator_role": init_role,
            "responder_role": resp_role,
            # Target label
            "session_type": label,
        })

    flows_df = pd.DataFrame(rows).sort_values("minute").reset_index(drop=True)
    flows_path = os.path.join(scenario_dir, "flows.csv")
    flows_df.to_csv(flows_path, index=False)

    # Aggregate flows.csv by minute to create minute_features.csv (60 rows per scenario)
    minute_df = (
        flows_df.groupby("minute")
        .agg(
            packets=("packet_count", "sum"),
            bytes=("byte_count", "sum"),
            active_circuits=("circuit_id", "nunique"),
            active_clients=("client_id", "nunique"),
            mean_packet_size=("bytes_per_packet", "mean"),
            p95_inter_arrival_ms=("duration_per_packet", lambda s: np.percentile(s, 95)),
        )
        .reset_index()
    )
    minute_df["mean_packet_size"] = minute_df["mean_packet_size"].round(2)
    minute_df["p95_inter_arrival_ms"] = minute_df["p95_inter_arrival_ms"].round(2)
    minute_df["scenario"] = name

    minute_path = os.path.join(scenario_dir, "minute_features.csv")
    minute_df.to_csv(minute_path, index=False)

    print(f"[{name}] Saved {len(flows_df)} flows -> {flows_path}")
    print(f"[{name}] Saved {len(minute_df)} minutes -> {minute_path}")


if __name__ == "__main__":
    # Create AI pipeline directories matching Chapter 13
    os.makedirs(os.path.join("ai", "hidden_service_flow_classifier"), exist_ok=True)
    os.makedirs(os.path.join("ai", "scenario_minute_profiler"), exist_ok=True)
    os.makedirs(os.path.join("ai", "results"), exist_ok=True)

    for scenario_name, config in SCENARIOS.items():
        generate_scenario(scenario_name, config)

    print("\nDataset pack generation complete (10,121 total flows, 180 total minutes).")