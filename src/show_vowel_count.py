import matplotlib.pyplot as plt
from collections import Counter
import os

def count_vowels(file_path):
    """
    Reads the corpus file and counts the frequency of each Swahili vowel.
    """
    vowels = "aeiou"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().lower()
        
        counts = Counter(char for char in text if char in vowels)
        # Ensure all vowels are represented even if count is 0
        return {v: counts.get(v, 0) for v in vowels}
    except FileNotFoundError:
        return None

def print_terminal_table(data):
    """
    Prints a clean ASCII table of the vowel distribution for terminal use.
    """
    print("\n" + "="*25)
    print(f"{'Vowel':<10} | {'Frequency':<10}")
    print("-" * 25)
    for vowel, count in data.items():
        print(f"{vowel.upper():<10} | {count:<10}")
    print("="*25 + "\n")

def generate_visualization(data, output_path):
    """
    Generates a simple colored pie chart showing the proportional share of vowels.
    """
    vowels = [v.upper() for v in data.keys()]
    counts = list(data.values())
    
    # Professional academic palette
    colors = ['#4A90E2', '#7ED321', '#F5A623', '#D0021B', '#4A4A4A']
    
    plt.figure(figsize=(10, 7))
    plt.pie(
        counts, 
        labels=vowels, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    
    plt.title('Corpus Vowel Distribution')
    plt.savefig(output_path)
    print(f"Pie chart saved to: {output_path}")

if __name__ == "__main__":
    # Standardizing paths relative to the project structure
    data_path = os.path.join("..", "data", "sentences_to_record.txt")
    output_viz = os.path.join("..", "vowel_distribution.png")
    
    vowel_data = count_vowels(data_path)
    
    if vowel_data:
        # 1. Output to terminal
        print_terminal_table(vowel_data)
        
        # 2. Generate PNG pie chart
        generate_visualization(vowel_data, output_viz)
    else:
        print(f"Error: Could not find dataset at {data_path}")
