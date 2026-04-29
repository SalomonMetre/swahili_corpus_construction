import textgrid
import os

def count_phonemes_in_dir(directory_path):
    total_phonemes = 0
    file_count = 0
    
    # Iterate through all TextGrid files in the provided directory
    for filename in sorted(os.listdir(directory_path)):
        if filename.endswith(".TextGrid"):
            path = os.path.join(directory_path, filename)
            try:
                tg = textgrid.TextGrid.fromFile(path)
                # Tier 0 is your phoneme tier
                phoneme_tier = tg[0]
                
                # Count intervals that are NOT empty strings (silences/pauses)
                # mark.strip() handles potential whitespace-only annotations
                count = sum(1 for interval in phoneme_tier if interval.mark.strip())
                
                total_phonemes += count
                file_count += 1
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                
    return total_phonemes, file_count

def main():
    # Path logic relative to your src directory
    base_annotations_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "annotations"))
    positions = ["standing", "sitting", "supine"]
    
    grand_total = 0
    print(f"{'Position':<12} | {'Files':<6} | {'Phonemes':<10}")
    print("-" * 35)
    
    for pos in positions:
        pos_path = os.path.join(base_annotations_path, pos)
        if os.path.exists(pos_path):
            count, files = count_phonemes_in_dir(pos_path)
            print(f"{pos.capitalize():<12} | {files:<6} | {count:<10}")
            grand_total += count
        else:
            print(f"Warning: Directory {pos_path} not found.")

    print("-" * 35)
    print(f"{'GRAND TOTAL':<21} | {grand_total:<10}")

if __name__ == "__main__":
    main()