<div align="center">

# Nexora — Anomaly Detection

**A Machine Learning Subsystem for the Post-Quantum, Invitation-Gated Anonymous Peer-to-Peer Overlay Network**

*AI-driven network traffic evaluation, feature extraction, and anomaly detection benchmarked against Tor traffic.*

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange?style=flat-square&logo=scikit-learn)
![PyTorch](https://img.shields.io/badge/framework-PyTorch-ee4c2c?style=flat-square&logo=pytorch)
![Scapy](https://img.shields.io/badge/packet--parsing-Scapy-yellow?style=flat-square)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/status-research_prototype-db5139?style=flat-square)

</div>

---

## 📌 Overview

**Nexora-Anomaly-Detection** is the dedicated machine learning intelligence layer for [Nexora](https://github.com/Youssef-Abo-Al-Ella/Nexora), a Post-Quantum, Invitation-Gated Anonymous Peer-to-Peer Overlay Network[cite: 18]. 

While the core Nexora repository acts as the secure networking substrate—handling post-quantum cryptography, UDP socket routing, and distributed hash tables[cite: 6, 7]—this repository functions as its analytical engine. It was engineered specifically to analyze network telemetry, evaluate protocol stealth, and detect anomalous peer behavior[cite: 6].

By parsing raw `.pcap` network captures, this subsystem extracts critical flow metrics (such as Inter-Arrival Time, flow duration, and packet length distributions) and processes them through predictive machine learning models. Using both Random Forest and LSTM architectures, it provides a standardized evaluation framework to compare Nexora's custom hidden-service traffic footprint directly against standard encrypted Tor streams.

---

## ✨ Key Features

- **PCAP & Traffic Parsing:** Utilizes **Scapy** and **Wireshark / TShark** pipelines to convert raw network packet captures into structured ML-ready datasets.
- **Dual ML Architecture:**
  - **Random Forest:** High-efficiency tabular classification for rapid packet feature scoring and anomaly detection.
  - **LSTM (Long Short-Term Memory):** Sequential time-series analysis to model flow dynamics and temporal traffic patterns.
- **Tor Traffic Benchmarking:** Standardized evaluation framework comparing protocol stealth and node behavior against standard encrypted Tor traffic.
- **Feature Engineering:** Extracts flow metrics including inter-arrival time (IAT), packet length distribution, payload entropy, and directional ratios.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Machine Learning & Analytics:** PyTorch / TensorFlow, Scikit-learn, XGBoost, Pandas, NumPy
- **Packet Processing:** Scapy, PyShark / Wireshark

---

## 📁 Repository Structure

```text
├── data/                  # Sample PCAPs & processed feature CSVs (git-ignored)
├── notebooks/             # Data exploration, flow analysis, & model prototyping
├── src/
│   ├── feature_extraction/# Scapy & Wireshark PCAP parsing routines
│   ├── models/            # Random Forest & LSTM model definitions
│   └── utils/             # Data cleaning, scaling, and evaluation helpers
├── train.py               # Model training entrypoint
├── evaluate.py            # Anomaly scoring & benchmark script
├── requirements.txt       # Python dependencies
└── README.md              # Documentation
