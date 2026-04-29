import parselmouth
import textgrid
import json
import os
from collections import defaultdict

def extract_formants(audio_path, tg_path):
    """Processes a single file pair and extracts formants for all vowels."""
    snd = parselmouth.Sound(audio_path)
    tg = textgrid.TextGrid.fromFile(tg_path)
    
    # Settings for a male speaker
    formant_obj = snd.to_formant_burg(
        time_step=0.005, 
        max_number_of_formants=5, 
        maximum_formant=5000, 
        window_length=0.025
    )
    
    target_vowels = ['a', 'e', 'i', 'o', 'u']
    file_data = defaultdict(list)

    # Vowels are in the first tier
    for interval in tg[0]:
        vowel_label = interval.mark.lower().strip()
        if vowel_label in target_vowels:
            duration = interval.maxTime - interval.minTime
            mid_point = interval.minTime + (duration / 2)
            
            f1 = formant_obj.get_value_at_time(1, mid_point)
            f2 = formant_obj.get_value_at_time(2, mid_point)
            f3 = formant_obj.get_value_at_time(3, mid_point)
            
            if all(v is not None for v in [f1, f2, f3]):
                file_data[vowel_label].append({
                    "f1": round(f1, 2),
                    "f2": round(f2, 2),
                    "f3": round(f3, 2)
                })
    return file_data

def process_corpus():
    # Adjusted path: src/analysis -> src -> project_root
    base_path = "../../" 
    positions = ["standing", "sitting", "supine"]
    
    for pos in positions:
        print(f"Processing position: {pos}...")
        pos_results = defaultdict(list)
        
        audio_dir = os.path.join(base_path, "data", "audio", pos)
        tg_dir = os.path.join(base_path, "data", "annotations", pos)
        
        # Saves analysis output to project_root/analysis/
        output_dir = os.path.join(base_path, "analysis", pos)
        os.makedirs(output_dir, exist_ok=True)

        if not os.path.isdir(audio_dir):
            print(f"Error: Directory not found -> {audio_dir}")
            continue

        for filename in sorted(os.listdir(audio_dir)):
            if filename.endswith(".wav"):
                prefix = os.path.splitext(filename)[0]
                audio_path = os.path.join(audio_dir, filename)
                tg_path = os.path.join(tg_dir, f"{prefix}.TextGrid")
                
                if os.path.exists(tg_path):
                    vowel_occurrences = extract_formants(audio_path, tg_path)
                    for vowel, formants in vowel_occurrences.items():
                        pos_results[vowel].extend(formants)

        final_json = []
        for vowel in ['a', 'e', 'i', 'o', 'u']:
            final_json.append({
                "vowel": vowel,
                "formants": pos_results.get(vowel, [])
            })

        output_file = os.path.join(output_dir, "vowel_formants.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(final_json, f, indent=4)
        print(f"Success! Results saved to: {output_file}")

if __name__ == "__main__":
    process_corpus()