import json
import os
import numpy as np

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_aggregate(raw_data):
    # Flatten all formants into separate lists for global analysis
    all_f1 = []
    all_f2 = []
    all_f3 = []
    
    for entry in raw_data:
        for f in entry['formants']:
            all_f1.append(f['f1'])
            all_f2.append(f['f2'])
            all_f3.append(f['f3'])
            
    # Process each formant independently
    results = {}
    for label, data in [("f1", all_f1), ("f2", all_f2), ("f3", all_f3)]:
        if not data:
            results[label] = {"nb": 0, "mean": 0, "std": 0}
            continue
            
        arr = np.array(data)
        mu, sigma = np.mean(arr), np.std(arr)
        
        # Filter: Keep values within 2 standard deviations
        filtered = arr[(arr >= mu - 2*sigma) & (arr <= mu + 2*sigma)]
        
        # Recompute stats on the filtered subset
        results[label] = {
            "nb": len(filtered),
            "mean": round(float(np.mean(filtered)), 2),
            "std": round(float(np.std(filtered)), 2)
        }
        
    return results

def main():
    # Path logic relative to script location
    base_dir = os.path.dirname(__file__)
    positions = ["standing", "sitting", "supine"]
    
    for pos in positions:
        input_path = os.path.join(base_dir, pos, "vowel_formants.json")
        output_path = os.path.join(base_dir, pos, "vowel_formants_aggregates.json")
        
        if os.path.exists(input_path):
            print(f"Aggregating data for: {pos}...")
            raw_data = load_json(input_path)
            aggregated_results = process_aggregate(raw_data)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(aggregated_results, f, indent=4)
            print(f"Saved aggregates to: {output_path}")
        else:
            print(f"Warning: {input_path} not found.")

if __name__ == "__main__":
    main()