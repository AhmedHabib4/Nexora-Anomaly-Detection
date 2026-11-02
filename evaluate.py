import argparse
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, confusion_matrix

def evaluate_model(data_path, model_path):
    print(f"Loading anomaly detection model from {model_path}...")
    clf = joblib.load(model_path)
    
    print(f"Loading benchmark data from {data_path}...")
    df = pd.read_csv(data_path)
    
    features = ['packet_count', 'total_bytes', 'mean_iat', 'mean_pkt_len', 'flow_duration']
    X = df[features].fillna(0)
    
    if 'label' in df.columns:
        y_true = df['label']
        y_pred = clf.predict(X)
        acc = accuracy_score(y_true, y_pred)
        cm = confusion_matrix(y_true, y_pred)
        print(f"Benchmark Accuracy: {acc*100:.2f}%")
        print("Confusion Matrix (Normal vs Tor/Anomaly):")
        print(cm)
    else:
        print("No ground-truth labels found. Scoring traffic blindly...")
        preds = clf.predict(X)
        anomalies = sum(preds)
        print(f"Results: {anomalies} anomalies detected out of {len(preds)} total flows.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Nexora Traffic footprint against Tor.")
    parser.add_argument("--data", required=True, help="Test data CSV (e.g., tor_baseline.csv)")
    parser.add_argument("--model", default="src/models/rf_anomaly_model.pkl", help="Trained model path")
    args = parser.parse_args()
    
    evaluate_model(args.data, args.model)