# Nexora — Anomaly Detection Subsystem

> **AI-Driven Network Traffic Evaluation & Anomaly Detection**  
> Official machine learning module designed to analyze network traffic stealth, detect anomalies, and benchmark against Tor traffic for the [Nexora Overlay Network](https://github.com/Youssef-Abo-Al-Ella/Nexora).

---

## 📌 Overview

**Nexora-Anomaly-Detection** serves as the machine learning intelligence layer for the Nexora project—a Post-Quantum, Invitation-Gated Anonymous Peer-to-Peer Overlay Network. 

This repository contains the model architectures, PCAP feature extraction pipelines, and traffic evaluation protocols engineered to analyze packet structures, score anomalies, and compare custom research protocol behavior against encrypted Tor stream footprints.

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
