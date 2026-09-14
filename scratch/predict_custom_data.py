import sys
import os
import csv
import json
from datetime import datetime

# Adjust Python path to allow importing app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.ml.predictor import failure_predictor

def predict_csv(file_path):
    results = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            router_id = row.get("router_id", f"Custom-R{idx+1}")
            try:
                router_dict = {
                    "router_id": router_id,
                    "cpu": float(row["cpu"]),
                    "memory": float(row["memory"]),
                    "latency": float(row["latency"]),
                    "packet_loss": float(row["packet_loss"]),
                    "bandwidth": float(row["bandwidth"])
                }
            except KeyError as e:
                print(f"Error: Missing required column {e} in CSV.")
                return
            except ValueError as e:
                print(f"Error parsing row values: {e}")
                continue
            
            pred = failure_predictor.predict(router_dict)
            results.append({
                "Router ID": router_id,
                "CPU (%)": router_dict["cpu"],
                "Memory (%)": router_dict["memory"],
                "Latency (ms)": router_dict["latency"],
                "Packet Loss (%)": router_dict["packet_loss"],
                "Bandwidth (%)": router_dict["bandwidth"],
                "Predicted State": pred["predicted_state"],
                "Failure Probability": f"{pred['failure_probability'] * 100:.1f}%",
                "Risk Score": pred["risk_score"]
            })
    return results

def predict_json(file_path):
    results = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        data = json.load(f)
        # Ensure it is a list of objects
        if not isinstance(data, list):
            data = [data]
            
        for idx, row in enumerate(data):
            router_id = row.get("router_id", f"Custom-R{idx+1}")
            try:
                router_dict = {
                    "router_id": router_id,
                    "cpu": float(row["cpu"]),
                    "memory": float(row["memory"]),
                    "latency": float(row["latency"]),
                    "packet_loss": float(row["packet_loss"]),
                    "bandwidth": float(row["bandwidth"])
                }
            except KeyError as e:
                print(f"Error: Missing required field {e} in JSON object.")
                return
            except ValueError as e:
                print(f"Error parsing values: {e}")
                continue
            
            pred = failure_predictor.predict(router_dict)
            results.append({
                "Router ID": router_id,
                "CPU (%)": router_dict["cpu"],
                "Memory (%)": router_dict["memory"],
                "Latency (ms)": router_dict["latency"],
                "Packet Loss (%)": router_dict["packet_loss"],
                "Bandwidth (%)": router_dict["bandwidth"],
                "Predicted State": pred["predicted_state"],
                "Failure Probability": f"{pred['failure_probability'] * 100:.1f}%",
                "Risk Score": pred["risk_score"]
            })
    return results

def print_table(results):
    if not results:
        return
    headers = ["Router ID", "CPU (%)", "Memory (%)", "Latency (ms)", "Packet Loss (%)", "Bandwidth (%)", "State", "Fail Prob", "Risk Score"]
    
    # Calculate column widths
    widths = {h: len(h) for h in headers}
    for r in results:
        widths["Router ID"] = max(widths["Router ID"], len(str(r["Router ID"])))
        widths["CPU (%)"] = max(widths["CPU (%)"], len(str(r["CPU (%)"])))
        widths["Memory (%)"] = max(widths["Memory (%)"], len(str(r["Memory (%)"])))
        widths["Latency (ms)"] = max(widths["Latency (ms)"], len(str(r["Latency (ms)"])))
        widths["Packet Loss (%)"] = max(widths["Packet Loss (%)"], len(str(r["Packet Loss (%)"])))
        widths["Bandwidth (%)"] = max(widths["Bandwidth (%)"], len(str(r["Bandwidth (%)"])))
        widths["State"] = max(widths["State"], len(str(r["Predicted State"])))
        widths["Fail Prob"] = max(widths["Fail Prob"], len(str(r["Failure Probability"])))
        widths["Risk Score"] = max(widths["Risk Score"], len(str(r["Risk Score"])))
        
    # Print Headers
    header_str = " | ".join(f"{h:<{widths[h]}}" for h in headers)
    print(header_str)
    print("-+-".join("-" * widths[h] for h in headers))
    
    # Print Rows
    for r in results:
        row_str = " | ".join([
            f"{str(r['Router ID']):<{widths['Router ID']}}",
            f"{str(r['CPU (%)']):<{widths['CPU (%)']}}",
            f"{str(r['Memory (%)']):<{widths['Memory (%)']}}",
            f"{str(r['Latency (ms']):<{widths['Latency (ms)']}}" if 'Latency (ms' in r else f"{str(r['Latency (ms)']):<{widths['Latency (ms)']}}",
            f"{str(r['Packet Loss (%)']):<{widths['Packet Loss (%)']}}",
            f"{str(r['Bandwidth (%)']):<{widths['Bandwidth (%)']}}",
            f"{str(r['Predicted State']):<{widths['State']}}",
            f"{str(r['Failure Probability']):<{widths['Fail Prob']}}",
            f"{str(r['Risk Score']):<{widths['Risk Score']}}"
        ])
        print(row_str)

def main(file_path):
    print(f"=== Processing Custom Dataset: {file_path} ===")
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return
        
    if file_path.endswith('.csv'):
        results = predict_csv(file_path)
    elif file_path.endswith('.json'):
        results = predict_json(file_path)
    else:
        print("Error: Unsupported file format. Please use a .csv or .json file.")
        return
        
    if results:
        print("\n=== ML Classification & Outage Risk Analysis ===")
        print_table(results)
        
        # Save output to CSV using csv module
        output_path = f"predictions_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        with open(output_path, mode='w', newline='', encoding='utf-8') as f:
            if results:
                writer = csv.DictWriter(f, fieldnames=results[0].keys())
                writer.writeheader()
                writer.writerows(results)
        print(f"\n[Success] Results saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python predict_custom_data.py <path_to_csv_or_json>")
        print("Example: python predict_custom_data.py sample_router_data.csv")
    else:
        main(sys.argv[1])
