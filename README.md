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

## 📌 AI Subsystem Overview

This repository contains the dedicated **Artificial Intelligence and Machine Learning layer** designed to evaluate network traffic stealth and detect protocol anomalies. 

The core role of this AI component is to analyze network telemetry, classify traffic patterns, and detect anomalous peer behavior[cite: 6]. It determines whether custom overlay traffic can be mathematically distinguished from standard encrypted Tor streams. The AI pipeline executes this through three distinct phases:

1. **Feature Engineering:** Parses raw network packet captures (`.pcap`) to extract critical behavioral flow metrics, including Inter-Arrival Time (IAT), packet length distributions, and overall flow durations.
2. **Predictive Modeling:** Evaluates the network traffic using a dual-model architecture[cite: 2]:
   - **Random Forest:** Provides rapid, high-efficiency tabular classification of the extracted packet features[cite: 2].
   - **LSTM (Long Short-Term Memory):** Models sequential time-series dynamics to identify temporal anomalies and hidden patterns in the traffic flows[cite: 2].
3. **Stealth Benchmarking:** Scores the extracted features to evaluate the underlying protocol's ability to resist machine learning-based traffic classification, comparing its footprint directly against Tor baseline data.

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

---

## Quick Start

> Target platform is Windows with Python 3.10+ and a virtual environment.

From `Nexora-Anomaly-Detection/` :

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python src/feature_extraction/parse_pcap.py --input data/sample.pcap --output data/processed.csv