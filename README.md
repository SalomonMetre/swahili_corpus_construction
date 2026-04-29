# Postural Effects on Swahili Vowel Articulation 🌍🗣️
### *An Acoustic Analysis of Formant Variability Across Body Positions*

## 📌 Project Overview
This study investigates how body posture (Standing, Sitting, and Supine) influences the acoustic properties of the Swahili five-vowel system (/a/, /e/, /i/, /o/, /u/). By analyzing $F_1$, $F_2$, and $F_3$ formants, we examine how changes in physical orientation lead to the passive displacement of articulators (tongue and jaw) and whether the speech motor system successfully compensates for these shifts to maintain phonetic targets.

## 🛠️ Technology Stack
* **Language:** Python 3.14+
* **Acoustic Analysis:** [Praat-Parselmouth](https://github.com/YannickJadoul/Parselmouth) (LPC Burg Method)
* **Annotation Parsing:** [TextGrid](https://github.com/kylebgorman/textgrid)
* **Statistics:** NumPy, SciPy (Welch's & Paired Student's t-tests)
* **Workflow Management:** [uv](https://github.com/astral-sh/uv)

## 📂 Directory Structure
```text
.
├── data/
│   ├── audio/        # 30 WAV samples (10 per posture)
│   ├── annotations/  # Manual TextGrid alignments (Tier 1: Vowels)
│   └── text/         # Recording script (10 Swahili sentences)
├── src/
│   ├── analysis/     # Extraction, Cleaning, and Statistics scripts
│   └── util/         # Audio duration and metadata utilities
├── analysis/         # Processed JSON data and .txt statistical reports
└── README.md
```

## 🧪 Methodology

### 1. Corpus & Data Collection
* **Material:** 10 phonetically balanced Swahili sentences.
* **Conditions:** Audio captured in three controlled postures: **Standing**, **Sitting**, and **Supine**.
* **Consistency:** Total durations are verified (range: 3.60s – 5.92s) to ensure a stable speech rate across all conditions.

### 2. Formant Extraction & Data Integrity
* **Automated Tracking:** Mid-point formant extraction using the Burg algorithm.
* **Physiological Filtering:** Removal of tracking artifacts through frequency boundary constraints.
* **Statistical Cleaning ($2\sigma$):** Tokens falling outside two standard deviations from the mean are excluded to ensure a robust representative sample.
* **Token ID Persistence:** Unique `file_id` tagging is maintained through the pipeline to allow for high-precision paired comparisons.

### 3. Statistical Framework
* **Paired Student’s t-test:** Direct comparison of identical vowel tokens across postures to isolate the effect of orientation.
* **Welch’s t-test:** Analysis of aggregated formant populations to identify global shifts in the vocal tract's acoustic space.

## 📊 Results & Analysis
The final reports evaluate:
* **Vertical Aperture ($F_1$):** Variations in jaw opening and tongue height.
* **Vowel Backness ($F_2$):** Shifts in tongue mass toward the pharyngeal wall (retraction).
* **Resonator Length ($F_3$):** Global vocal tract stability across postures.

---
**Researcher:** Salomon Metre  
**Affiliation:** IDMC, Université de Lorraine (Nancy, France)

---