import argparse
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import os

def train_rf(data_path, model_out):
    print(f"Loading training data from {data_path}...")
    df = pd.read_csv(data_path)
    
    if 'label' not in df.columns:
        print("Warning: 'label' column missing. Generating dummy labels (0=Nexora, 1=Tor/Anomaly).")
        df['label'] = np.random.randint(0, 2, df.shape[0])
        
    features = ['packet_count', 'total_bytes', 'mean_iat', 'mean_pkt_len', 'flow_duration']
    X = df[features].fillna(0)
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Anomaly Detector...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=15, random_state=42)
    clf.fit(X_train, y_train)
    
    print("Evaluating Model on Test Split:")
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=["Normal Nexora", "Anomaly / Tor"]))
    
    os.makedirs(os.path.dirname(model_out), exist_ok=True)
    joblib.dump(clf, model_out)
    print(f"Model successfully saved to {model_out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Nexora AI Anomaly Detection Models.")
    parser.add_argument("--data", default="data/processed.csv", help="Processed CSV feature file")
    parser.add_argument("--model", default="src/models/rf_anomaly_model.pkl", help="Model output path")
    args = parser.parse_args()
    
    train_rf(args.data, args.model)