import json
import os
import numpy as np
from collections import defaultdict

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_stats(formants_list):
    """Helper to compute mean and std for f1, f2, f3."""
    if not formants_list:
        return None
    
    metrics = {}
    for key in ['f1', 'f2', 'f3']:
        vals = [f[key] for f in formants_list]
        metrics[key] = {
            "mean": round(float(np.mean(vals)), 2),
            "standard deviation": round(float(np.std(vals)), 2)
        }
    return metrics

def clean_and_summarize_position(data):
    results = []
    
    for entry in data:
        vowel = entry['vowel']
        raw_formants = entry['formants']
        initial_count = len(raw_formants)
        
        # 1. Hard Frequency Bound Filtering
        bounded = [
            f for f in raw_formants 
            if 300 < f['f1'] < 800 and 700 < f['f2'] < 2500 and 800 < f['f3'] < 3400
        ]
        
        # 2. Statistical Outlier Filtering (2nd pass)
        if len(bounded) > 2:
            f1_vals = np.array([f['f1'] for f in bounded])
            f2_vals = np.array([f['f2'] for f in bounded])
            
            f1_mu, f1_std = np.mean(f1_vals), np.std(f1_vals)
            f2_mu, f2_std = np.mean(f2_vals), np.std(f2_vals)
            
            final_formants = []
            for f in bounded:
                f1_ok = (f1_mu - 2*f1_std) <= f['f1'] <= (f1_mu + 2*f1_std)
                f2_ok = (f2_mu - 2*f2_std) <= f['f2'] <= (f2_mu + 2*f2_std)
                
                if f1_ok and f2_ok:
                    final_formants.append(f)
        else:
            final_formants = bounded

        final_count = len(final_formants)
        filtered_out = initial_count - final_count
        
        # 3. Final Summary Calculation
        summary = calculate_stats(final_formants)

        results.append({
            "vowel": vowel,
            "initial_nb_occurrences": initial_count,
            "nb_occurrences_filtered_out": filtered_out,
            "final_nb_occurrences": final_count,
            "summary": summary if summary else "Insufficient data after filtering",
            "cleaned_data": final_formants # This preserves the 'id', 'f1', 'f2', 'f3' for each token
        })

    return results

def main():
    base_dir = os.path.dirname(__file__)
    positions = ["standing", "sitting", "supine"]
    
    for pos in positions:
        input_path = os.path.join(base_dir, pos, "vowel_formants.json")
        output_path = os.path.join(base_dir, pos, "vowel_formants_cleaned_analysis.json")
        
        if os.path.exists(input_path):
            print(f"Cleaning data for: {pos}...")
            raw_data = load_json(input_path)
            summarized_data = clean_and_summarize_position(raw_data)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(summarized_data, f, indent=4)
            print(f"Saved cleaned analysis with IDs to: {output_path}")
        else:
            print(f"Warning: Raw data for {pos} not found.")

if __name__ == "__main__":
    main()