import json
import os
import numpy as np
from scipy import stats

def load_aggregate(base_path, position):
    path = os.path.join(base_path, position, "vowel_formants_aggregates.json")
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_welch_t(mean1, std1, n1, mean2, std2, n2):
    """Computes t-stat and p-value from summary statistics using Welch's t-test."""
    # Handle edge cases with no data
    if n1 < 2 or n2 < 2:
        return 0.0, 1.0
        
    t_stat, p_val = stats.ttest_ind_from_stats(
        mean1=mean1, std1=std1, nobs1=n1,
        mean2=mean2, std2=std2, nobs2=n2,
        equal_var=False 
    )
    return round(t_stat, 3), round(p_val, 4)

def main():
    # Use absolute path based on script location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    positions = ["standing", "sitting", "supine"]
    comparisons = [("standing", "sitting"), ("standing", "supine"), ("sitting", "supine")]
    formants = ["f1", "f2", "f3"]

    # Load data
    try:
        data = {pos: load_aggregate(base_dir, pos) for pos in positions}
    except FileNotFoundError as e:
        print(f"Error: Could not find aggregate JSON files. Make sure they exist in the position subfolders.\n{e}")
        return

    output_lines = []
    header_main = "GLOBAL POSTURAL SIGNIFICANCE (ALL VOWELS COMBINED)"
    divider = "=" * 95
    table_header = f"{'Formant':<8} | {'Comparison':<25} | {'t-stat':<10} | {'p-value':<10} | {'Conclusion'}"
    sub_divider = "-" * 95

    output_lines.extend([header_main, divider, table_header, sub_divider])

    for f in formants:
        for p1, p2 in comparisons:
            s1 = data[p1][f]
            s2 = data[p2][f]
            
            t, p = calculate_welch_t(
                s1['mean'], s1['std'], s1['nb'],
                s2['mean'], s2['std'], s2['nb']
            )
            
            conclusion = "SIGNIFICANT" if p < 0.05 else "not significant"
            comp_label = f"{p1.capitalize()} vs {p2.capitalize()}"
            
            row = f"{f.upper():<8} | {comp_label:<25} | {t:<10} | {p:<10} | {conclusion}"
            output_lines.append(row)
        output_lines.append(sub_divider)

    # Print to console
    final_output = "\n".join(output_lines)
    print(final_output)

    # Save to file
    output_path = os.path.join(base_dir, "global_significance_results.txt")
    with open(output_path, "w", encoding="utf-8") as f_out:
        f_out.write(final_output)
    
    print(f"\nGlobal analysis saved to: {output_path}")

if __name__ == "__main__":
    main()