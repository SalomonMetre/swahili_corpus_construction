import os
import wave
import numpy as np

def get_duration(file_path):
    """Returns the duration of a WAV file in seconds."""
    with wave.open(file_path, 'rb') as wf:
        frames = wf.getnframes()
        rate = wf.getframerate()
        return frames / float(rate)

def main():
    # Path logic: from src/ to project_root/data/audio/
    base_audio_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "audio"))
    positions = ["standing", "sitting", "supine"]
    
    all_durations = []
    position_stats = {}

    for pos in positions:
        pos_dir = os.path.join(base_audio_path, pos)
        durations = []
        
        if not os.path.exists(pos_dir):
            continue

        for filename in os.listdir(pos_dir):
            if filename.endswith(".wav"):
                file_path = os.path.join(pos_dir, filename)
                dur = get_duration(file_path)
                durations.append(dur)
                all_durations.append(dur)
        
        if durations:
            position_stats[pos] = {
                "min": min(durations),
                "max": max(durations),
                "mean": np.mean(durations)
            }

    # Global Summary
    if all_durations:
        print("\n" + "="*45)
        print(f"{'Position':<12} | {'Min (s)':<8} | {'Max (s)':<8} | {'Mean (s)':<8}")
        print("-" * 45)
        for pos, stats in position_stats.items():
            print(f"{pos.capitalize():<12} | {stats['min']:<8.2f} | {stats['max']:<8.2f} | {stats['mean']:<8.2f}")
        
        print("-" * 45)
        print(f"{'GLOBAL':<12} | {min(all_durations):<8.2f} | {max(all_durations):<8.2f} | {np.mean(all_durations):<8.2f}")
        print("="*45 + "\n")
    else:
        print("No audio files found. Check your paths!")

if __name__ == "__main__":
    main()