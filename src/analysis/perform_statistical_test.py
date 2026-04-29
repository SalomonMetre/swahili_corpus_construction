import json
import os
import numpy as np
from scipy import stats

def load_cleaned_data(base_path, position):
    path = os.path.join(base_path, position, "vowel_formants_cleaned_analysis.json")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_paired_data(data1, data2, vowel_char, formant_key):
    """Aligns tokens from two positions using their IDs to ensure a paired test."""
    v1_entry = next((v for v in data1 if v['vowel'] == vowel_char), None)
    v2_entry = next((v for v in data2 if v['vowel'] == vowel_char), None)
    
    if not v1_entry or not v2_entry:
        return [], []
    
    # Map occurrences by ID: { "01": [val1, val2], "02": [val1] }
    def map_by_id(entries):
        mapping = {}
        for entry in entries:
            fid = entry['id']
            if fid not in mapping:
                mapping[fid] = []
            mapping[fid].append(entry[formant_key])
        return mapping

    map1 = map_by_id(v1_entry['cleaned_data'])
    map2 = map_by_id(v2_entry['cleaned_data'])
    
    paired_v1 = []
    paired_v2 = []
    
    # Only use IDs present in both datasets
    common_ids = sorted(set(map1.keys()) & set(map2.keys()))
    for fid in common_ids:
        # Pair occurrences within the same file by index
        list1, list2 = map1[fid], map2[fid]
        n_pairs = min(len(list1), len(list2))
        for i in range(n_pairs):
            paired_v1.append(list1[i])
            paired_v2.append(list2[i])
            
    return paired_v1, paired_v2

def run_paired_test(v1, v2):
    """Executes the rel (related/paired) t-test."""
    if len(v1) < 2:
        return "N/A", "N/A", "Insufficient Pairs"
    
    t_stat, p_val = stats.ttest_rel(v1, v2)
    conclusion = "SIGNIFICANT" if p_val < 0.05 else "not significant"
    return round(t_stat, 3), round(p_val, 4), conclusion

def main():
    # Assumes script is run from src/analysis/
    base_dir = os.path.dirname(__file__)
    
    positions = ["standing", "sitting", "supine"]
    vowels = ["a", "e", "i", "o", "u"]
    formants = ["f1", "f2", "f3"]
    # Comparison pairs
    comparisons = [
        ("standing", "sitting"), 
        ("standing", "supine"), 
        ("sitting", "supine")
    ]
    
    # Load all cleaned data
    data = {pos: load_cleaned_data(base_dir, pos) for pos in positions}
    
    output_lines = [
        "SWAHILI VOWEL POSTURAL ANALYSIS - PAIRED T-TEST RESULTS",
        "=" * 115,
        f"{'Vowel':<8} | {'Comparison':<25} | {'t-statistic':<12} | {'p-value':<10} | {'Conclusion'}",
        "-" * 115
    ]

    for f_key in formants:
        output_lines.append(f"\n--- ANALYSIS FOR {f_key.upper()} ---")
        
        for v in vowels:
            for p1, p2 in comparisons:
                v1_vals, v2_vals = get_paired_data(data[p1], data[p2], v, f_key)
                t, p, conclusion = run_paired_test(v1_vals, v2_vals)
                
                comp_label = f"{p1.capitalize()} vs {p2.capitalize()}"
                row = f"{v.upper():<8} | {comp_label:<25} | {str(t):<12} | {str(p):<10} | {conclusion}"
                output_lines.append(row)
            output_lines.append("-" * 115) # Separator between vowels

    # Save results to txt file
    output_path = os.path.join(base_dir, "statistical_test_results.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    
    print(f"Success! Detailed report saved to: {output_path}")

if __name__ == "__main__":
    main()