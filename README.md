# Swahili Postural Phonetics Corpus 🌍🗣️

An experimental study exploring the impact of body posture on vowel formant production in Swahili. This project analyzes how physical orientation (Standing, Sitting, and Supine) affects the geometry of the vocal tract and the resulting acoustic output.

## 📌 Project Overview
The study investigates whether the human speech motor system compensates for postural changes to maintain acoustic constancy. By comparing recordings in three positions, we track shifts in $F_1$, $F_2$, and $F_3$ formants caused by the passive repositioning of the tongue and jaw.

## 🛠️ Technology Stack
* **Language:** Python 3.14+
* **Acoustic Analysis:** [Praat-Parselmouth](https://github.com/YannickJadoul/Parselmouth) (LPC Burg Method)
* **Annotation Parsing:** [TextGrid](https://github.com/kylebgorman/textgrid)
* **Statistics:** NumPy, SciPy (Welch's & Paired Student's t-tests)
* **Environment Management:** [uv](https://github.com/astral-sh/uv)

## 🧪 Methodology

### 1. Data Collection & Preprocessing
* **Corpus:** 10 Swahili sentences selected for balanced vowel distribution.
* **Conditions:** High-fidelity audio captured in **Standing**, **Sitting**, and **Supine** (lying down) positions.
* **Control:** Durations strictly monitored (3.60s to 5.92s) to ensure consistent speech rate across all trials.

### 2. Formant Extraction & Data Cleaning
* **Physiological Bounds:** Filtering for plausible human ranges ($300 < F_1 < 800$, etc.).
* **Statistical $2\sigma$ Filter:** Tokens beyond two standard deviations from the vowel mean are discarded to remove tracking errors.
* **Token Alignment:** Unique `file_id` tracking allows for high-precision paired t-tests between specific vowel occurrences.

### 3. Statistical Analysis
* **Paired Student’s t-test:** Used to compare identical tokens across postures, isolating the effect of orientation on the individual speaker.
* **Welch’s t-test:** Global aggregate analysis to detect systematic shifts in the overall acoustic space.

## 📊 Results & Conclusions
The analysis focuses on two primary articulatory shifts:
* **Vertical Aperture ($F_1$):** Examining if lying down leads to a more open/closed vocal tract due to jaw repositioning.
* **Tongue Retraction ($F_2$):** Measuring horizontal shifts as the tongue mass moves toward the pharynx in the supine position.
* **Motor Control:** Evaluating the speaker's ability to maintain acoustic targets despite physical changes in orientation.

---
**Researcher:** Salomon Metre  
**Affiliation:** IDMC, Université de Lorraine (Nancy, France)